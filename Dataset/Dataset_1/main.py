import blenderproc as bproc
import glob
import numpy as np
import random
import os
import sys
from typing import List, Union, Optional
file_dir = os.path.dirname(__file__)
print(file_dir)
sys.path.append(file_dir)
sys.path.append(os.path.abspath(os.path.join(file_dir, os.pardir)))
sys.path.append("/BlenderProc2/DataGenerator/renderer")
sys.path.append("/BlenderProc2/DataGenerator")

from signal import signal, SIGPIPE, SIG_DFL   
signal(SIGPIPE,SIG_DFL)

import setting
import camera 
import cc_texture_loader
import object_utils 

from utility import coco_utils 
from config.Config import Config 

# #For debug purpose
# import debugpy
# debugpy.listen(5678)
# debugpy.wait_for_client()

class ObjectSampler:
    def __init__(self, objects, ground,
                 adjust_to_objects: bool=True,
                 min_height=0.01, max_height=10,
                 sampling_region_percentage: float=5,
                 Config=None):
        self.objects = objects
        self.ground = ground
        self.Config = Config
        
        if self.Config:
            self.adjust_to_objects = self.Config.objects.sampler.adjust_to_objects
            self.min_height= self.Config.objects.sampler.min_height
            self.max_height = self.Config.objects.sampler.max_height
            self.sampling_region_percentage = self.Config.objects.sampler.sampling_region_percentage    
        else:
            self.adjust_to_objects = adjust_to_objects
            self.min_height= min_height
            self.max_height = max_height
            self.sampling_region_percentage = sampling_region_percentage

        self.sampling_height_factor = 0
        _, self.obj_max_length = object_utils.get_max_min_length_of_all_objects(objects)
        
    def sample_function(self):
        def sample_pose(objs: bproc.types.MeshObject):
            # Sample the objs location above the surface
            if self.adjust_to_objects:
                min_height = 0.01
                max_height = self.obj_max_length
                if len(self.objects) >= 10:
                    self.sampling_height_factor += int(str(len(self.objects))[:-1])
                else:
                    self.sampling_height_factor += 1
            else:
                min_height = self.min_height
                max_height = self.max_height
                self.sampling_height_factor += 1

            objs.set_location(bproc.sampler.upper_region(
                objects_to_sample_on=self.ground,
                min_height=min_height,
                max_height=max_height*self.sampling_height_factor,
                use_ray_trace_check=False,
                use_upper_dir=False,
                upper_dir=[0.0, 0.0, 1.0],
                face_sample_range=[0.5-(self.sampling_region_percentage*0.5/100),
                                   0.5+(self.sampling_region_percentage*0.5/100)]
            ))
            objs.set_rotation_euler(np.random.uniform([0, 0, 0], [np.pi*2, np.pi*2, np.pi*2]))
        return sample_pose

class Simulator:
    def __init__(self, objects,
                 adjust_time_to_objects: bool=True,
                 check_object_interval: float=0.5,
                 substeps_per_frame: int=25,
                 solver_iters: int=25,
                 min_time_s: float=0.5,
                 max_time_s: float=2,
                 Config=None):
        self.objects = objects
        self.Config = Config

        if self.Config:
            self.adjust_time_to_objects = Config.simulation.time.adjust_to_objects
            self.check_object_interval = Config.simulation.check_object_interval
            self.substeps_per_frame = Config.simulation.substeps_per_frame
            self.solver_iters = Config.simulation.solver_iters
            self.min_time_s = Config.simulation.time.min
            self.max_time_s = Config.simulation.time.max
        else:
            self.adjust_time_to_objects = adjust_time_to_objects
            self.check_object_interval = check_object_interval
            self.substeps_per_frame = substeps_per_frame
            self.solver_iters = solver_iters
            self.min_time_s = min_time_s
            self.max_time_s = max_time_s

        self.simu_time_increment = 0

    def simulate(self):
        if self.adjust_time_to_objects:
            min_simu_time = 0.5
            max_simu_time = 1 + self.simu_time_increment*0.6
        else:
            min_simu_time = self.min_time_s
            max_simu_time = self.max_time_s
        # run the simulation and fix the poses of the objects
        bproc.object.simulate_physics_and_fix_final_poses(min_simulation_time=min_simu_time,
                                                          max_simulation_time= max_simu_time,
                                                          check_object_interval=self.check_object_interval,
                                                          substeps_per_frame=self.substeps_per_frame,
                                                          solver_iters=self.solver_iters)

def load_objects(object_dir: str, class_instance_num: dict, 
                 file_type: str=".obj", is_from_ShapeNet: bool=False,
                 linear_damping:float=0.6, friction: float=1.0,
                 random_color: bool=False,
                 keep_loaded_material: bool=True,
                 define_cc_material: str="Metal000",
                 random_material: bool=False,
                 cc_textures_dir: str="/BlenderProc2/cc_textures",
                 Config=None):
    if Config:
        file_type = Config.Object3D_loader.file_type
        is_from_ShapeNet = Config.Object3D_loader.is_from_ShapeNet
        linear_damping = Config.objects.config.linear_damping
        friction = Config.objects.config.friction
        random_color = Config.objects.config.color.random
        keep_loaded_material = Config.objects.config.material.keep_loaded
        define_cc_material = Config.objects.config.material.defined 
        random_material = Config.objects.config.material.random
        cc_textures_dir = Config.cc_textures_dir

    object_dir = object_dir.replace(os.sep, '/')
    obj_paths = glob.glob(object_dir + "/**/*" + file_type, recursive=True)
    objects_to_position = []
    unneeded = [x for x in class_instance_num if class_instance_num[x]==0]  
    _obj_paths = [x for x in obj_paths if all(y not in x for y in unneeded)]

    print("####################################################################")
    for obj_path in _obj_paths:
        obj = bproc.loader.load_obj(obj_path, use_legacy_obj_import=is_from_ShapeNet)
        if len(obj)>0:
            obj[0].enable_rigidbody(active=True, collision_shape="CONVEX_HULL",
                                    linear_damping=linear_damping,
                                    friction=friction)
            object_utils.set_center_of_mass(obj[0])
            object_utils.adjust_mass(obj[0])
            objects_to_position.append(obj[0])
            obj[0].set_name(obj[0].get_name().split('_')[0])
            num = class_instance_num[obj[0].get_name()]
            for i in range(num-1):
                dup = obj[0].duplicate()
                objects_to_position.append(dup)

    if not keep_loaded_material:
        if random_material:
            for obj in objects_to_position:
                mats = cc_texture_loader.usable_cctextures(cc_textures_dir)
                mat = cc_texture_loader.material(cc_textures_dir, prefix=mats[np.random.randint(len(mats))])
                obj.replace_materials(mat)
        else:
            mat = cc_texture_loader.material(cc_textures_dir, prefix=define_cc_material)
            for obj in objects_to_position:
                obj.replace_materials(mat)

    if random_color:
        object_utils.random_color(objects_to_position)

    for obj in objects_to_position:
        obj.add_uv_mapping(projection="smart")
        obj.set_shading_mode("AUTO")

    print("loaded: " + str(len(objects_to_position)) + " object(s)")
    print("####################################################################\n")
    return objects_to_position

def add_flying_disctractor(ground: bproc.types.MeshObject,
                           objects: Optional[List[bproc.types.MeshObject]]=None,
                           number: int=5,
                           defined_size: List=[10,10,10],
                           adjust_size_to_objects: bool=True,
                           min_height: float=500.0, 
                           max_height: float=300.0,
                           sampling_region_percentage: float=15.0,
                           Config=None):
    if Config:
        number = Config.flying_distractor.number
        defined_size = Config.flying_distractor.size.defined
        adjust_size_to_objects = Config.flying_distractor.size.adjust_to_objects
        min_height = Config.flying_distractor.sampler.min_height
        max_height =  Config.flying_distractor.sampler.max_height
        sampling_region_percentage = Config.flying_distractor.sampler.sampling_region_percentage

    shapes = ["CUBE", "CONE", "SPHERE", "MONKEY"]

    if not objects:
        objects = []

    if adjust_size_to_objects and objects:
        _, _, mid_L, _ = object_utils.get_smallest_obj_geometry(objects)
        print("MAXXXXXXX", mid_L)
        _scale = [mid_L/2, mid_L/2, mid_L/2]
    else:
        _scale = defined_size

    distractors = []
    for i in range(number):
        _shape = random.choice(shapes)
        distractors.append(bproc.object.create_primitive(shape=_shape, scale=_scale))

    if distractors:
        object_utils.random_color(distractors)
        object_utils.center_object_at_origin_below_z(distractors)

        def sample_pose(objs: bproc.types.MeshObject):
            objs.set_location(bproc.sampler.upper_region(
                objects_to_sample_on=ground,
                min_height=min_height,
                max_height=max_height,
                use_ray_trace_check=False,
                use_upper_dir=False,
                upper_dir=[0.0, 0.0, 1.0],
                face_sample_range=[0.5-(sampling_region_percentage*0.5/100),
                                   0.5+(sampling_region_percentage*0.5/100)]
            ))
            objs.set_rotation_euler(np.random.uniform([0, 0, 0], [np.pi*2, np.pi*2, np.pi*2]))
            
        bproc.object.sample_poses(distractors,
                                objects_to_check_collisions=distractors + [ground] + objects,
                                sample_pose_func=sample_pose)
    
    for distractor in distractors:    
        distractor.set_cp("category_id", 0)
    return distractors
    
def load_grounds(ground_dir:str, file_type: str=".obj",
                 is_from_ShapeNet: bool=False):
    ground_dir = ground_dir.replace(os.sep, '/')
    ground_paths = glob.glob(ground_dir + "/**/*" + file_type, recursive=True)
    
    print("####################################################################")
    grounds = []
    for ground_path in ground_paths:
        gnd = bproc.loader.load_obj(ground_path, use_legacy_obj_import=is_from_ShapeNet)
        if len(gnd)>0:
            grounds.append(gnd[0])
    print("loaded: " + str(len(grounds)) + " ground(s)")
    print("####################################################################\n")
    return grounds

def create_ground(ground_dir: str=None, objects: Optional[List[bproc.types.MeshObject]]=None, 
                  file_type:str=".obj", is_from_ShapeNet: bool=False,
                  random_pick: bool=True,
                  euler_rotX: float=0,
                  euler_rotY: float=0,
                  euler_rotZ: float=0,
                  plane_xy = [500,500],
                  adjust_plane_size_to_objects: bool=True, 
                  linear_damping :float=0.99, friction: float=100.00,
                  keep_loaded_material: bool=True,
                  define_cc_material: str="Metal000",
                  random_material: bool=False,
                  cc_textures_dir: str="/BlenderProc2/cc_textures",
                  Config=None):
    if Config:
        file_type = Config.Object3D_loader.file_type
        is_from_ShapeNet = Config.Object3D_loader.is_from_ShapeNet
        random_pick = Config.ground.random_pick
        euler_rotX = Config.ground.euler_rotation.X
        euler_rotY = Config.ground.euler_rotation.Y
        euler_rotZ = Config.ground.euler_rotation.Z
        plane_xy = Config.ground.plane_size.defined
        adjust_plane_size_to_objects = Config.ground.plane_size.adjust_to_objects
        linear_damping = Config.ground.linear_damping
        friction = Config.ground.friction
        keep_loaded_material = Config.ground.material.keep_loaded
        define_cc_material = Config.ground.material.defined 
        random_material = Config.ground.material.random
        cc_textures_dir = Config.cc_textures_dir

    grounds = None
    if ground_dir:
        grounds = load_grounds(ground_dir, file_type, is_from_ShapeNet)

    if not grounds:
        print("No ground loaded, creating a ground plane normal to z-axis...")
        if objects and adjust_plane_size_to_objects:
            _, max_length = object_utils.get_max_min_length_of_all_objects(objects)
            ground = bproc.object.create_primitive('PLANE', scale=[max_length*len(objects)*2, max_length*len(objects)*2, 1])
        else:
            ground = bproc.object.create_primitive('PLANE', scale=plane_xy+[1])
        ground.set_name('ground_plane')
    elif len(grounds)>1:
        if random_pick:
            ground = grounds[np.random.randint(len(grounds))]
        else:
            ground = grounds[-1]
        for gnd in grounds:
            if gnd != ground:
                object_utils.delete_obj(gnd)
    else:
        ground = grounds[0]
        object_utils.set_object_euler_rotation(ground, euler_rotX, euler_rotY, euler_rotZ)
    
    if not keep_loaded_material:
        if random_material:
            mats = cc_texture_loader.usable_cctextures(cc_textures_dir)
            mat = cc_texture_loader.material(cc_textures_dir, prefix=mats[np.random.randint(len(mats))])
        else:
            mat = cc_texture_loader.material(cc_textures_dir, prefix=define_cc_material)

    ground.replace_materials(mat)
    ground.add_uv_mapping(projection="smart")
    ground.set_shading_mode("AUTO")
    ground.enable_rigidbody(active=False, collision_shape="MESH", collision_margin=0.0,
                            friction=friction, linear_damping=linear_damping, angular_damping=0.99)
    ground.set_cp("category_id", 0)
    ground.set_cp("xyz_dimensions", object_utils.calculate_world_bound_box_geometry(ground))
    object_utils.set_center_of_mass(ground)
    object_utils.adjust_mass(ground)
    object_utils.center_object_at_origin_below_z(ground)
    return ground

def set_ceiling_light(ground: bproc.types.MeshObject,
                      enabled: bool=True,
                      plane_xy: List=[500, 500], fit_to_ground: bool=True,
                      define_position: List=[0, 0, 1000],
                      random_position: bool=False,
                      min_height: float=1000, max_height: float=1250,
                      define_intensity: float=3.5,
                      random_intensity: bool=True, 
                      min_intensity: float=1.0, max_intensity: float=7.0,
                      Config=None):
    if Config:
        enabled = Config.ceiling_light.enabled
        plane_xy = Config.ceiling_light.plane_xy.defined
        fit_to_ground = Config.ceiling_light.plane_xy.fit_to_ground
        define_position = Config.ceiling_light.position.defined
        random_position = Config.ceiling_light.position.random.enabled
        min_height = Config.ceiling_light.position.random.min_height
        max_height = Config.ceiling_light.position.random.max_height
        define_intensity = Config.ceiling_light.intensity.defined
        random_intensity = Config.ceiling_light.intensity.random.enabled
        min_intensity = Config.ceiling_light.intensity.random.min
        max_intensity = Config.ceiling_light.intensity.random.max

    if enabled:
        if fit_to_ground:
            ground_xyz= ground.get_cp("xyz_dimensions")
            plane_xy = ground_xyz[:-1]

        if random_position:
            location = [0, 0, np.random.uniform(min_height, max_height)]
        else:
            location = define_position

        if random_intensity:
            emission_strength=np.random.uniform(min_intensity, max_intensity)
        else:
            emission_strength = define_intensity

        # make light plane
        light_plane = bproc.object.create_primitive('PLANE', scale=[plane_xy[0]/2, plane_xy[1]/2, 0])
        light_plane.set_name("ceiling_light")      
        light_plane.set_location(location)
        light_plane.set_cp("category_id", 0)
        light_plane_material = bproc.material.create("light_material")
        light_plane_material.make_emissive(emission_strength)    
        light_plane.replace_materials(light_plane_material)
        return light_plane
    return None

def sample_spot_light(objects = None, 
                      number: int=1,
                      spread_angle: float=60.0,
                      blend: float=0.2,
                      define_position: List=[0, 0, 500],
                      random_position: bool=True,
                      center: List=[0,0,0],
                      min_radius: float=250, max_radius: float=450,
                      min_elevation: float=0, max_elevation: float=90,
                      rotation_to_objects: bool=True,
                      define_intensity_watt: float=50,
                      random_intensity: bool=True, 
                      min_intensity_watt: float=10, max_intensity_watt: float=100,
                      Config=None):
    if Config:
        number =  Config.spot_light.number
        spread_angle: Config.spot_light.spread_angle
        blend: Config.spot_light.blend
        define_position = Config.spot_light.position.defined
        random_position = Config.spot_light.position.random.enabled
        center = Config.spot_light.position.random.center
        min_radius = Config.spot_light.position.random.min_radius
        max_radius = Config.spot_light.position.random.max_radius
        min_elevation = Config.spot_light.position.random.min_elevation
        max_elevation = Config.spot_light.position.random.max_elevation
        rotation_to_objects = Config.spot_light.rotation.to_objects
        define_intensity_watt = Config.spot_light.intensity_watt.defined
        random_intensity = Config.spot_light.intensity_watt.random.enabled
        min_intensity_watt = Config.spot_light.intensity_watt.random.min
        max_intensity_watt = Config.spot_light.intensity_watt.random.max

    spotlights = []
    if number>0:
        if objects:
            poi = bproc.object.compute_poi(objects)
        else:
            poi = [0,0,0]
        for i in range(number):
            if random_position:
                location = bproc.sampler.shell(center = center,
                                            radius_min = min_radius,
                                            radius_max = max_radius,
                                            elevation_min = min_elevation,
                                            elevation_max = max_elevation,
                                            uniform_volume = True)
            else:
                location = define_position

            if random_intensity:
                emission_strength=np.random.uniform(min_intensity_watt, max_intensity_watt)
            else:
                emission_strength = define_intensity_watt

            if rotation_to_objects:
                rotation_mat = object_utils.rotation_from_forward_vec(poi - location)
                dist = object_utils.calculate_distance(poi, location)
                light = object_utils.create_spotlight_object(energy=emission_strength, location=location,
                                                            spread_angle=spread_angle, blend=blend, distance=dist,
                                                            rotation_euler=rotation_mat.to_euler('XYZ'))
            else:
                dist = object_utils.calculate_distance([0,0,0], location)
                light = object_utils.create_spotlight_object(energy=emission_strength, location=location,
                                                            spread_angle=spread_angle, blend=blend, distance=dist)
            spotlights.append(light)
    return spotlights

def set_up_camera(image_width: int=1920, image_height: int=1920,
                  clip_start: float=0.1, clip_end: float=1500,
                  Config=None):
    if Config:
        image_width = Config.camera.config.image_width
        image_height = Config.camera.config.image_height
        clip_start = Config.camera.config.clip_start
        clip_end = Config.camera.config.clip_end
    bproc.camera.set_resolution(image_width, image_height)
    bproc.camera.set_intrinsics_from_blender_params(clip_start=clip_start, clip_end=clip_end)
    
def sample_camera(objects: Optional[List[bproc.types.MeshObject]]=None,
                  define_position: List=[0, 0, 350],
                  random_position: bool=True,
                  center=[0,0,0],
                  min_radius: float=150, max_radius: float=500,
                  min_elevation: float=30.0, max_elevation: float=90.0,
                  prefer_small_radius: bool=True,
                  random_rotation: bool=True,
                  check_no_world_background: bool=True,
                  check_all_objects_visible: bool=True,
                  Config=None):

    if Config:
        define_position = Config.camera.sampler.position.defined
        random_position = Config.camera.sampler.position.random.enabled
        center = Config.camera.sampler.position.random.center
        min_radius = Config.camera.sampler.position.random.min_radius
        max_radius = Config.camera.sampler.position.random.max_radius
        prefer_small_radius = Config.camera.sampler.position.random.prefer_small_radius
        min_elevation = Config.camera.sampler.position.random.min_elevation
        max_elevation =  Config.camera.sampler.position.random.max_elevation
        random_rotation = Config.camera.sampler.rotation.random.enabled
        check_no_world_background = Config.camera.sampler.check.no_world_background
        check_all_objects_visible = Config.camera.sampler.check.all_objects_fully_visible

    if objects:
        poi = bproc.object.compute_poi(objects)
    else:
        poi = [0,0,0]

    while min_radius < max_radius:    
        for i in range(10):
            for j in range(30):
                if random_position:
                    position = bproc.sampler.shell(
                        center=center,
                        radius_min=min_radius,
                        radius_max=max_radius,
                        elevation_min=min_elevation,
                        elevation_max=max_elevation,
                        uniform_volume=not prefer_small_radius
                    )
                else:
                    position = define_position
                
                if random_rotation:
                    rotation_matrix = bproc.camera.rotation_from_forward_vec(poi - position,
                                                                             inplane_rot=np.random.uniform(-0.7854,0.7854))
                else:
                    rotation_matrix = bproc.camera.rotation_from_forward_vec(poi - position)

                cam2world_matrix = bproc.math.build_transformation_mat(position, rotation_matrix)
                
                if not (check_no_world_background and random_position):
                    break

                if camera.is_background_seen(cam2world_matrix):
                    print("Bad Camera Postion: world background in camera view")
                    print("Resample camera")
                else:
                    break
                
                if j == 29:
                    return False
                
            bproc.camera.add_camera_pose(cam2world_matrix,0)

            if not random_position:
                return True
            
            if check_all_objects_visible:
                fully_visible_objs = camera.fully_visible_objects(objects)
                if all([x in fully_visible_objs for x in objects]):
                    print("all objects fully visible")
                    # Persist camera pose
                    return True
                else:
                    print("Bad Camera Postion: objects outside camera view")
                    print("resample camera")
            else:
                visible_objs = bproc.camera.visible_objects(cam2world_matrix,300)
                if all([x in visible_objs for x in objects]):
                    print("all objects visible")
                    # Persist camera pose
                    return True
                else:
                    print("Bad Camera Postion: objects outside camera view")
                    print("resample camera")
            
        print("§§§§ Camera sampling parameter adjusted §§§§")
        min_radius += 10
    return False

def COCO_annotater(rendered_data, label_map, output_dir, object_occlusion,
                   save_annotated_image: bool=True, Config=None):
    if Config:
        save_annotated_image = Config.save_coco_annotated_image
    bproc.writer.write_coco_annotations(os.path.join(output_dir, 'coco_data'),
                                        instance_segmaps=rendered_data["instance_segmaps"],
                                        instance_attribute_maps=rendered_data["instance_attribute_maps"],
                                        colors=rendered_data["colors"],
                                        color_file_format="JPEG",
                                        append_to_existing_output=True,
                                        label_mapping=label_map,
                                        jpg_quality=95)
    coco_utils.store_image_occlusion_data(object_occlusion, coco_dir=os.path.join(output_dir, "coco_data"))
    if save_annotated_image:
        coco_utils.save_annotated_image(os.path.join(output_dir,"coco_data"))

def render_with_config(obj_dir, gnd_dir, class_instance_num, output_dir, config_file):
    CONF = Config.load_json(config_file)

    bproc.init(clean_up_scene=True)
    bproc.utility.reset_keyframes()
    ############################## world setting ##############################
    if CONF.world.unit == "mm":
        setting.set_scene_to_MM()
    elif CONF.world.unit == "cm":
        setting.set_scene_to_CM()
    elif CONF.world.unit == "m":
        setting.set_scene_to_M()
    else:
        setting.set_scene_to_MM()

    setting.set_gravity_SI_unit(CONF.world.gravitaty_ms2)
    setting.set_world_background_black(CONF.world.background_black)
    setting.set_3Dview_clip_start(CONF.world._3Dview_clip_start)
    setting.set_3Dview_clip_end(CONF.world._3Dview_clip_end)
    ###########################################################################


    ############################## renderer setting ##############################
    setting.enable_ambient_occlusion(CONF.renderer.ambient_occlusion)
    setting.set_render_image_compression(CONF.renderer.image_compression_perc)
    setting.set_render_engine(CONF.renderer.engine)            
    bproc.renderer.set_cpu_threads(CONF.renderer.cpu_cores_number)
    bproc.renderer.set_simplify_subdivision_render(CONF.renderer.number_of_subdivision)
    bproc.renderer.set_denoiser(CONF.renderer.denoiser)
    bproc.renderer.set_noise_threshold(CONF.renderer.noise_treshold)
    bproc.renderer.set_render_devices(use_only_cpu=CONF.renderer.use_only_cpu,
                                      desired_gpu_device_type=CONF.renderer.desired_gpu_device_type)
    ##############################################################################


    ###################################### load objects ##################################
    objs_to_position = load_objects(obj_dir, class_instance_num, Config=CONF)
    label_map = coco_utils.map_coco_label(objects=objs_to_position, coco_dir= os.path.join(output_dir,"coco_data"))
    ######################################################################################
    

    ####################################### load ground ###################################
    ground = create_ground(gnd_dir, objects= objs_to_position, Config=CONF)
    #######################################################################################


    ####################################### light ###################################
    ceilingLight = set_ceiling_light(ground, Config=CONF)
    spotLight = sample_spot_light(Config=CONF)
    #################################################################################


    set_up_camera(Config=CONF)

    for i in range(3):
        obj_sammpler = ObjectSampler(objs_to_position, ground, Config=CONF)
        simulator = Simulator(objs_to_position, Config=CONF)
        if len(objs_to_position) >= 10:
            simulator.simu_time_increment += int(str(len(objs_to_position))[:-1])

        if objs_to_position:
            object_sampling_success = False
            while True:
                for j in range(3):
                    object_utils.center_object_at_origin_below_z(objs_to_position)

                    placed_objs = bproc.object.sample_poses(
                        objs_to_position,
                        objects_to_check_collisions=objs_to_position + [ground],
                        sample_pose_func=obj_sammpler.sample_function()
                    )
                    if all(x[-1] for x in placed_objs.values()):
                        print("all object(s) placed")
                        object_sampling_success = True
                        break
                    else:
                        print("resample objects...")
                if object_sampling_success:
                    break
                else:
                    obj_sammpler.sampling_height_factor += 0.5
                    obj_sammpler.sampling_region_percentage += 0.5
            
        simulator.simulate()

        if sample_camera(objects=objs_to_position, Config=CONF):
            distractors = add_flying_disctractor(ground, objs_to_position, Config=CONF)
            object_utils.update_scene()
            object_occlusion = object_utils.check_occlusion(objs_to_position, [ground]+distractors, bproc.camera.get_camera_pose())
            data = bproc.renderer.render()
            data.update(bproc.renderer.render_segmap(map_by=["class", "instance", "class_name"], default_values={"class_name": None}))
            COCO_annotater(data, label_map, output_dir, object_occlusion, Config=CONF)
            print("Successfull")
            return True
    
    print("Failed")
    return False

obj_dir = "/BlenderProc2/object/Ball Socket Head Screw"
gnd_dir = "/BlenderProc2/ground/tisch"
output_dir = "/BlenderProc2/Dataset/Dataset_50"
config_file = "/BlenderProc2/Config/BallSocketheadScrew_Tisch.json"
class_instance_num = {'bcr-12x50': 2, 'bcr-10x40': 2, 'bcr-10x25': 2, 'bcr-16x40': 3, 'bcr-16x60': 3, 'bcr-12x30': 3, 'bcr-8x35': 2, 'bcr-8x20': 1, 'bcf-10x25': 3, 'bcf-12x30': 3, 'bcf-8x20': 3, 'bcf-6x16': 3}

if __name__ == '__main__':
    render_with_config(obj_dir,gnd_dir,
                       class_instance_num,
                       output_dir, config_file)
