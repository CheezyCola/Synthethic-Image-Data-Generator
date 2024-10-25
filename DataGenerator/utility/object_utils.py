"""
A script to create, adjust and measure Blender object
"""
from typing import List, Optional, Union
import numpy as np
import random
import math
from collections import namedtuple

import bpy
from mathutils import Vector, Matrix, Euler
from mathutils.geometry import normal

from blenderproc.python.types.MeshObjectUtility import MeshObject
from .camera_utils import BlenderCamera

# unit RGB
color_dict = {'Red': (1,0,0,0.8), 'DarkRed': (0.6,0,0,0.8),
			  'Green': (0,1,0,0.8), 'DarkGreen': (0.4,0.5,0.2,0.8), 'LightGreen': (0.6,1,0.4,0.8),
			  'Blue': (0,0,1,0.8), 'DarkBlue': (0,0,0.4,0.8), 'LightBlue': (0.6,1,1,0.8),
			  'Orange': (1,0.569,0,0.8), 'Yellow': (1,0.984,0,0.8),
			  'Purple': (0.8,0,1,0.8), 'Tiffany': (0,1,0.761,0.8),
			  'Pink': (1,0,0.569,0.8),
			  'Dark': (0,0,0,0.8), 'White': (1,1,1,0.8), 'Grey': (0.7,0.7,0.7,0.8)}

def merge_objects(objects: List[MeshObject]):
	""" Merge the objects....

	:param objects:

	"""
	ctx = bpy.context.copy()
	ctx['active_object'] = objects[0].blender_obj
	ctx['selected_objects'] = [obj.blender_obj for obj in objects]
	bpy.ops.object.join(ctx)

	return objects[0]

def set_center_of_mass(object: Union[List[MeshObject], MeshObject]):
	""" Sets the center of the mass....

	:param object:

	"""
	if not isinstance(object, List):
		object = [object]
	
	for obj in object:
		for ob in bpy.context.selected_objects:
			ob.select_set(False)
		obj.blender_obj.select_set(True)
		bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_VOLUME', center='MEDIAN')
		bpy.ops.object.transform_apply(location=False, rotation=False, scale=False)

def adjust_mass(object: Union[List[MeshObject], MeshObject], correction_factor: float=0.000003):
	""" Adjust the mass.....

	:param object:
	:param correction_factor:

	"""
	if not isinstance(object, List):
		object = [object]

	for obj in object:	
		if bpy.context.scene.unit_settings.length_unit == 'MILLIMETERS':
			obj.blender_obj.rigid_body.mass *= 10**9 * correction_factor
		elif bpy.context.scene.unit_settings.length_unit == 'CENTIMETERS':
			obj.blender_obj.rigid_body.mass *= 10**6 * correction_factor
		elif bpy.context.scene.unit_settings.length_unit == 'METERS':
			obj.blender_obj.rigid_body.mass *= correction_factor

def center_object_at_origin_below_z(object: Union[List[MeshObject], MeshObject]):
	""" Center the object at origin below z axis.....

	:param object:
	
	"""
	if not isinstance(object, List):
		object = [object]

	for obj in object:	
		offset = Vector((0,0,0)) - boundbox_center(obj)
		offset[-1] = offset[-1] - calculate_world_bound_box_geometry(obj)[-1]/2
		obj.blender_obj.location += offset

def set_object_euler_rotation(object: Union[List[MeshObject], MeshObject],
							  X_degree: float, 
							  Y_degree:float, 
							  Z_degree:float):
	""" Sets the object euler rotation

	:param object:
	:param X_degree:
	:param Y_degree:
	:param Z_degree:


	"""
	if not isinstance(object, List):
		object = [object]

	for obj in object:	
		previous_mode = obj.blender_obj.rotation_mode 
		obj.blender_obj.rotation_mode = "XYZ"
		obj.blender_obj.rotation_euler = (math.radians(X_degree), math.radians(Y_degree), math.radians(Z_degree))
		obj.blender_obj.rotation_mode  = previous_mode

def delete_obj(object: Union[List[MeshObject], MeshObject]):
	""" deletes the object...

	:param object:


	"""
	if not isinstance(object, List):
		object = [object]
	
	for obj in object:
		for ob in bpy.context.selected_objects:
			ob.select_set(False)
		obj.blender_obj.select_set(True)
		bpy.ops.object.delete()

def boundbox_center(object: MeshObject):
	""" Bound the box in the center....

	:param object:

	"""
	local_bbox_center = 0.5*(Vector(object.blender_obj.bound_box[0]) + Vector(object.blender_obj.bound_box[6]))
	world_bbox_center = object.blender_obj.matrix_world @ local_bbox_center
	return world_bbox_center

def calculate_world_bound_box_geometry(obj: MeshObject):
	""" Calculates the worls bound box geometry

	:param obj:

	"""
#     # bound_box = obj.get_bound_box()
#     # x_length = abs(bound_box[1][0]-bound_box[5][0])
#     # y_length = abs(bound_box[1][1]-bound_box[3][1])
#     # z_length = abs(bound_box[1][2]-bound_box[2][2])
#     # geometry = [x_length, y_length, z_length]
#     # return geometry
	bbox_min = Vector(obj.get_bound_box()[0])
	bbox_max = Vector(obj.get_bound_box()[6])
	z = bbox_max.z - bbox_min.z
	x = bbox_max.x - bbox_min.x
	y = bbox_max.y - bbox_min.y
	geometry = [x, y, z]
	return geometry

def calculate_object_volume(object: MeshObject):
	""" Calculates the objects volume....

	:param object:

	"""
	xyz = get_object_dimensions(object)[:]
	return xyz[0]*xyz[1]*xyz[2]

def get_largest_obj_geometery(list_of_objs: List[MeshObject]):
	""" Gets the largest the object geometry.....

	:param list_of_objs:


	"""
	objs_volume = [calculate_object_volume(x) for x in list_of_objs]
	index_max_volume = objs_volume.index(max(objs_volume))
	obj = list_of_objs[index_max_volume]
	xyz = get_object_dimensions(obj)[:]
	sorted_xyz = sorted(xyz)
	max_length = sorted_xyz[2]
	second_max_length = sorted_xyz[1]
	min_length = sorted_xyz[0]
	return xyz, max_length, second_max_length, min_length

def get_smallest_obj_geometry(list_of_objs: List[MeshObject]):
	""" Gets the smallest object geometry...

	:param list_of_objs:

	"""
	objs_volume = [calculate_object_volume(x) for x in list_of_objs]
	index_min_volume = objs_volume.index(min(objs_volume))
	obj = list_of_objs[index_min_volume]
	xyz = get_object_dimensions(obj)[:]
	sorted_xyz = sorted(xyz)
	max_length = sorted_xyz[2]
	second_max_length = sorted_xyz[1]
	min_length = sorted_xyz[0]
	return xyz, max_length, second_max_length, min_length

def get_max_min_length_of_all_objects(list_of_objs: List[MeshObject]):
	""" Get the maximum and minimum length of all objects in........

	:param list_of_objs:

	"""
	lengths=[]
	for obj in list_of_objs:
		xyz = get_object_dimensions(obj)[:]
		lengths.extend(xyz)
	return min(lengths), max(lengths)

def get_object_dimensions(object: MeshObject):
	""" Gets the object dimensions....

	:param object:

	"""
	return object.blender_obj.dimensions

def random_color(object: Union[List[MeshObject], MeshObject]):
	""" Randoms the color...

	:param object:

	"""
	if not isinstance(object, List):
		object = [object]
	
	for obj in object:
		color = color_dict.keys()
		_color = random.choice(list(color))

		mat_slots = obj.blender_obj.material_slots
		if mat_slots:
			for slot in mat_slots.values():
				mat = slot.material
				mat.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = color_dict[_color]
		else:
			# Create a material
			mat = bpy.data.materials.new("Mat")
			# Activate its nodes
			mat.use_nodes = True
			# Assign color
			mat.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = color_dict[_color]
			# Assign the material to the object
			obj.blender_obj.data.materials.append(mat)

def create_spotlight_object(energy: float, location: List,
							spread_angle: float, blend: float,
							distance: float=None,
							rotation_euler=None):
	""" Creates spotlight object.

	:param energy: the 
	:param location:
	:param spread_angle:
	:param blend:
	:param distance:
	:param rotation_euler:
	
	"""

	# Create a new spot light and set its properties
	light = bpy.data.lights.new(name="Spot light", type='SPOT')
	light.energy = energy * 10**6
	light.spot_size = math.radians(spread_angle)
	light.spot_blend = blend
	if distance:
		light.use_custom_distance=True
		light.distance = distance
	light.show_cone = True
	# Create a new lamp object and link it to the light
	lamp = bpy.data.objects.new(name="Spot lamp", object_data=light)
	bpy.context.scene.collection.objects.link(lamp)
	# Set the lamp's location
	lamp.location = location

	if rotation_euler:
		lamp.rotation_euler = rotation_euler
	return lamp

def rotation_from_forward_vec(forward_vec: Union[np.ndarray, Vector], up_axis: str = 'Y',
                              inplane_rot: Optional[float] = None) -> np.ndarray:
    """ Returns a camera rotation matrix for the given forward vector and up axis

    :param forward_vec: The forward vector which specifies the direction the camera should look
    :param up_axis: The up axis, usually Y
    :param inplane_rot: The inplane rotation in radians. If None is given, the inplane rotation is determined only
                        based on the up vector
    :return: The corresponding rotation matrix
    """
    rotation_matrix = Vector(forward_vec).to_track_quat('-Z', up_axis).to_matrix()
    if inplane_rot is not None:
        rotation_matrix @= Euler((0.0, 0.0, inplane_rot)).to_matrix()
    return rotation_matrix

def calculate_distance(location1, location2):
	"""Calculate the distance between two world location.

	:param location1: initial location
	:param location2: final location
	:return: distance
	"""
	loc1 = Vector(location1)
	loc2 = Vector(location2)
	distance = (loc2 - loc1).length
	return distance

def update_scene():
	bpy.context.view_layer.update()
	bpy.ops.render.render(write_still=True)

def check_occlusion(objects: List[MeshObject], cam2world_matrix: Union[Matrix, np.ndarray], others: List[MeshObject]=None)->dict:
	""" Check occlusion of objects with each other and also with others(ground/distractor).

	Send rays from an object's vertices to camera direction and check whether the rays hit an object or ground. 
	If the ray hits any object or ground, the vertex is occluded from camera view. 
	The objects and its percentage of occluded vertices is returned.
	
	:param objects: The objects to check.
	:param ground: The ground where the objects are sampled on.
	:param cam2world_matrix: Camera position in world matrix to specify the direction of rays. 
							 If None, the ray is parallel to z-axis. 

	:return: A dict of objects and its percentage of occluded vertices.
	"""
	cam2world_matrix = Matrix(cam2world_matrix)
	cam_position = cam2world_matrix.to_translation()

	cam = BlenderCamera()
	P, K, RT = cam.get_3x4_P_matrix_from_blender()
	render = bpy.context.scene.render
	render_scale = render.resolution_percentage / 100
	res_x = render.resolution_x *render_scale
	res_y = render.resolution_y *render_scale

	occlusion = {}
	objects2 = objects + others
	for obj1 in objects:
		verts = [obj1.blender_obj.matrix_world @ vert.co for vert in obj1.blender_obj.data.vertices]
		hit_count = 0
		for vert in verts:
			down_direction = cam_position - Vector(vert)
			for obj2 in objects2:
				if not obj1 == obj2:
					p = P @ vert
					p /= p[2]
					if not (0 <= p[0] <= res_x and 0 <= p[1] <= res_y):
						hit_count += 1
						break
					world2local = Matrix(np.linalg.inv(obj2.get_local2world_mat()))
					# Send raycast on object (this will ignore all other objects, so we only need to check whether the ray hit)
					hit_res, hit_loc, face_normal, face_index = obj2.blender_obj.ray_cast(world2local @ Vector(vert),
																						world2local.to_3x3() @ Vector(down_direction))
					if hit_res:
						hit_count += 1
						break

		occlusion[obj1.get_name()] = round(hit_count/len(verts)*100, 2)		
	return occlusion
