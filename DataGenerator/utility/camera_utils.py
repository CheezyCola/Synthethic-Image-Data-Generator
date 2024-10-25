"""Functions to check conditions in the camera's viewport."""
import numbers
import sys
from typing import Union, List, Set
from collections import defaultdict

import bpy
import numpy as np
from mathutils import Matrix, Vector

from blenderproc.python.types.MeshObjectUtility import MeshObject

class BlenderCamera:
    def __init__(self) -> None:
        self.cam_ob = bpy.context.scene.camera

    #  Build intrinsic camera parameters from Blender camera data
    #
    # See notes on this in 
    # blender.stackexchange.com/questions/15102/what-is-blenders-camera-projection-matrix-model
    # as well as
    # https://blender.stackexchange.com/a/120063/3581
    def get_calibration_matrix_K_from_blender(self):
        # BKE_camera_sensor_size
        def get_sensor_size(sensor_fit, sensor_x, sensor_y):
            if sensor_fit == 'VERTICAL':
                return sensor_y
            return sensor_x

        # BKE_camera_sensor_fit
        def get_sensor_fit(sensor_fit, size_x, size_y):
            if sensor_fit == 'AUTO':
                if size_x >= size_y:
                    return 'HORIZONTAL'
                else:
                    return 'VERTICAL'
            return sensor_fit
        
        if self.cam_ob.data.type != 'PERSP':
            raise ValueError('Non-perspective cameras not supported')
        scene = bpy.context.scene
        f_in_mm = self.cam_ob.data.lens
        scale = scene.render.resolution_percentage / 100
        resolution_x_in_px = scale * scene.render.resolution_x
        resolution_y_in_px = scale * scene.render.resolution_y
        sensor_size_in_mm = get_sensor_size(self.cam_ob.data.sensor_fit, self.cam_ob.data.sensor_width, self.cam_ob.data.sensor_height)
        sensor_fit = get_sensor_fit(
            self.cam_ob.data.sensor_fit,
            scene.render.pixel_aspect_x * resolution_x_in_px,
            scene.render.pixel_aspect_y * resolution_y_in_px
        )
        pixel_aspect_ratio = scene.render.pixel_aspect_y / scene.render.pixel_aspect_x
        if sensor_fit == 'HORIZONTAL':
            view_fac_in_px = resolution_x_in_px
        else:
            view_fac_in_px = pixel_aspect_ratio * resolution_y_in_px
        pixel_size_mm_per_px = sensor_size_in_mm / f_in_mm / view_fac_in_px
        s_u = 1 / pixel_size_mm_per_px
        s_v = 1 / pixel_size_mm_per_px / pixel_aspect_ratio

        # Parameters of intrinsic calibration matrix K
        u_0 = resolution_x_in_px / 2 - self.cam_ob.data.shift_x * view_fac_in_px
        v_0 = resolution_y_in_px / 2 + self.cam_ob.data.shift_y * view_fac_in_px / pixel_aspect_ratio
        skew = 0 # only use rectangular pixels

        K = Matrix(
            ((s_u, skew, u_0),
            (   0,  s_v, v_0),
            (   0,    0,   1)))
        return K

    # Returns camera rotation and translation matrices from Blender.
    # 
    # There are 3 coordinate systems involved:
    #    1. The World coordinates: "world"
    #       - right-handed
    #    2. The Blender camera coordinates: "bcam"
    #       - x is horizontal
    #       - y is up
    #       - right-handed: negative z look-at direction
    #    3. The desired computer vision camera coordinates: "cv"
    #       - x is horizontal
    #       - y is down (to align to the actual pixel coordinates 
    #         used in digital images)
    #       - right-handed: positive z look-at direction
    def get_3x4_RT_matrix_from_blender(self):
        # bcam stands for blender camera
        R_bcam2cv = Matrix(
            ((1, 0,  0),
            (0, -1, 0),
            (0, 0, -1)))

        # Transpose since the rotation is object rotation, 
        # and we want coordinate rotation
        # R_world2bcam = cam.rotation_euler.to_matrix().transposed()
        # T_world2bcam = -1*R_world2bcam @ location
        #
        # Use matrix_world instead to account for all constraints
        location, rotation = self.cam_ob.matrix_world.decompose()[0:2]
        R_world2bcam = rotation.to_matrix().transposed()

        # Convert camera location to translation vector used in coordinate changes
        # T_world2bcam = -1*R_world2bcam @ cam.location
        # Use location from matrix_world to account for constraints:     
        T_world2bcam = -1*R_world2bcam @ location

        # Build the coordinate transform matrix from world to computer vision camera
        R_world2cv = R_bcam2cv@R_world2bcam
        T_world2cv = R_bcam2cv@T_world2bcam

        # put into 3x4 matrix
        RT = Matrix((
            R_world2cv[0][:] + (T_world2cv[0],),
            R_world2cv[1][:] + (T_world2cv[1],),
            R_world2cv[2][:] + (T_world2cv[2],)
            ))
        return RT

    def get_3x4_P_matrix_from_blender(self):
        K = self.get_calibration_matrix_K_from_blender()
        RT = self.get_3x4_RT_matrix_from_blender()
        return K@RT, K, RT

def fully_visible_objects(objects: List[MeshObject]) -> List[MeshObject]:
    """Performs check on whether the objects are fully visible in camera view and
    returns a list of fully visible objects.

    :param objects: a list of objects of interest
    :return: a list of fully visible objects in camera view
    """
    cam = BlenderCamera()
    P, K, RT = cam.get_3x4_P_matrix_from_blender()

    render = bpy.context.scene.render
    render_scale = render.resolution_percentage / 100
    res_x = render.resolution_x *render_scale
    res_y = render.resolution_y *render_scale

    fully_visible = []
    for obj in objects:
        in_frame = True
        for vertex in [obj.blender_obj.matrix_world @ v.co for v in obj.blender_obj.data.vertices]:
            p = P @ vertex
            p /= p[2]
            
            if not (0 <= p[0] <= res_x and 0 <= p[1] <= res_y):
                in_frame = False
                break

        if in_frame:
            fully_visible.append(obj)

    return fully_visible

def visible_objects(objects: List[MeshObject]) -> List[MeshObject]:
    """Performs check on whether the objects are visible in camera view and returns 
    a list of visible objects. Objects can be partially visible in camera view.

    :param objects: a list of objects of interest
    :return: a list of fully visible objects in camera view
    """
    cam = BlenderCamera()
    P, K, RT = cam.get_3x4_P_matrix_from_blender()

    render = bpy.context.scene.render
    render_scale = render.resolution_percentage / 100
    res_x = render.resolution_x *render_scale
    res_y = render.resolution_y *render_scale

    visible = []
    for obj in objects:
        in_frame = False
        for vertex in [obj.blender_obj.matrix_world @ v.co for v in obj.blender_obj.data.vertices]:
            p = P @ vertex
            p /= p[2]
            
            if (0 <= p[0] <= res_x and 0 <= p[1] <= res_y):
                in_frame = True
                break

        if in_frame:
            visible.append(obj)

    return visible

def is_background_seen(cam2world_matrix: Union[Matrix, np.ndarray]) -> bool:
    """Check whether world background is in camera view.

    :param cam2world_matrix: The world matrix which describes the camera orientation to check
    :return: True if background is seen in camera view
    """
    cam2world_matrix = Matrix(cam2world_matrix)

    cam_ob = bpy.context.scene.camera
    cam = cam_ob.data

    # Get position of the corners of the near plane
    frame = cam.view_frame(scene=bpy.context.scene)
    # Bring to world space
    frame = [cam2world_matrix @ v for v in frame]

    # Compute vectors along both sides of the plane
    vec_x = frame[1] - frame[0]
    vec_y = frame[3] - frame[0]

    sqrt_number_of_rays = 150

    # Go in discrete grid-like steps over plane
    position = cam2world_matrix.to_translation()
    for x in range(0, sqrt_number_of_rays):
        for y in range(0, sqrt_number_of_rays):
            # Compute current point on plane
            end = frame[0] + vec_x * x / float(sqrt_number_of_rays - 1) + vec_y * y / float(sqrt_number_of_rays - 1)
            # Send ray from the camera position through the current point on the plane
            hit, _, _, _, _, _ = bpy.context.scene.ray_cast(bpy.context.evaluated_depsgraph_get(),
                                                                   position, end - position)
            if not hit:
                return True
            
    return False
