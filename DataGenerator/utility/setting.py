"""
Functions to set the world scene and renderer
"""
import bpy

def set_scene_to_MM():
    """Sets the scene lenght unit to mm.
    
    """
    bpy.context.scene.unit_settings.scale_length = 0.001
    bpy.context.scene.unit_settings.length_unit = 'MILLIMETERS'

def set_scene_to_CM():
    """Sets the scene lenght unit to cm.
    
    """
    bpy.context.scene.unit_settings.scale_length = 0.01
    bpy.context.scene.unit_settings.length_unit = 'CENTIMETERS'

def set_scene_to_M():
    """Sets the scene lenght unit to m.
    
    """
    bpy.context.scene.unit_settings.scale_length = 1
    bpy.context.scene.unit_settings.length_unit = 'METERS'

def set_gravity_SI_unit(gravitational_acceleration=-9.8):
    """Sets the gravity of the scene

    :param gravitational_acceleration: gravitational acceleration in m/s2
    """
    if bpy.context.scene.unit_settings.length_unit == 'MILLIMETERS':
        bpy.context.scene.gravity[2]=gravitational_acceleration*1000
    elif bpy.context.scene.unit_settings.length_unit == 'CENTIMETERS':
        bpy.context.scene.gravity[2]=gravitational_acceleration*100
    elif bpy.context.scene.unit_settings.length_unit == 'METERS':
        bpy.context.scene.gravity[2]=gravitational_acceleration

def set_world_background_black(bool):
    """Sets the background of world scene to pitch black.
    
    """
    if bool:
        bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[0].default_value = (0,0,0,1)

def set_3Dview_clip_start(clip_start_dist: float=0.1):
    """Sets 3D view clip start.

    :param clip_start_dist: start distant in unit length of scene
    
    """
    for a in bpy.context.screen.areas:
        for s in a.spaces:
            if s.type == "VIEW_3D":
                s.clip_start = clip_start_dist

def set_3Dview_clip_end(clip_end_dist: float=1000):
    """Sets 3D view clip end

    :param clip_start_dist: end distant in unit length of scene
    
    """   

    for a in bpy.context.screen.areas:
        for s in a.spaces:
            if s.type == "VIEW_3D":
                s.clip_end = clip_end_dist

def enable_ambient_occlusion(bool):
    """Enables ambient occlusion. Only taks effect, if ambient light presents.
    
    """
    if bool:
        bpy.context.scene.cycles.use_fast_gi = True

def set_render_engine(engine: str):
    """Sets render engine. 

    :param engine: Option : CYCLES, EVEVEE
    
    """
    bpy.context.scene.render.engine = engine

def set_render_image_compression(percentage: int):
    """Sets render image compression percentage. The compression percentage does not affect the image quality.
    The CPU takes longer time to perform higher percentage compression, results in smaller size.
    
    :param percentage: percentage of compression.
    
    """
    bpy.context.scene.render.image_settings.compression = percentage
    