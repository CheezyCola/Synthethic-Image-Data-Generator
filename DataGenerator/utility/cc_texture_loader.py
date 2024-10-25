"""
A script to load the cc_textures
Reference: https://github.com/DLR-RM/BlenderProc/blob/main/blenderproc/python/loader/CCMaterialLoader.py
"""
import bpy
import os
from typing import List

from blenderproc.python.material import MaterialLoaderUtility
from blenderproc.python.types.MaterialUtility import Material
from blenderproc.python.utility.Utility import Utility, resolve_path
from blenderproc.python.loader.CCMaterialLoader import _CCMaterialLoader

def usable_cctextures(cctexture_dir: str = "/BlenderProc2/cc_textures") -> List[str]:
    """ Returns list of cc_textures that are usable 

    Checks if the images needed to construct a material from cc_texture exists and returns a list of cc_textures that passed the check

    :param cctexture_dir: The directory of cc_textures. For example, parent directory of 'Metal001'.
    :return: A list of prefix of cc_textures 
    """
    cctexture_dir = resolve_path(cctexture_dir)
    usable_cctextures = []
    if os.path.exists(cctexture_dir) and os.path.isdir(cctexture_dir):
        for asset in os.listdir(cctexture_dir):
            current_path = os.path.join(cctexture_dir, asset)
            if os.path.isdir(current_path):
                base_image_path = os.path.join(current_path, f"{asset}_2K_Color.jpg")
                if not os.path.exists(base_image_path):
                    continue

                # check other important image paths
                roughness_image_path = base_image_path.replace("Color", "Roughness")
                if not os.path.exists(roughness_image_path):
                    continue

                displacement_image_path = base_image_path.replace("Color", "Displacement")
                if not os.path.exists(displacement_image_path):
                    continue

                usable_cctextures.append(asset)
        return usable_cctextures
    raise FileNotFoundError(f"The folder path does not exist: {cctexture_dir}")

def material(cctexture_dir: str = "/BlenderProc2/cc_textures", prefix: str = "") -> Material:
    """ This method loads textures obtained from https://ambientCG.com, use the script
    (scripts/download_cc_textures.py) to download all the textures to your pc.

    All textures here support Physically based rendering (PBR), which makes the textures more realistic.

    :param cctexture_dir: The directory of cc_textures. For example, parent directory of 'Metal001'.
    :param prefix: The short name of the cc_texture.

    :return a loaded material with textures specified by the prefix 
    """
    cctexture_dir = resolve_path(cctexture_dir)
    if os.path.exists(cctexture_dir) and os.path.isdir(cctexture_dir):
        current_path = os.path.join(cctexture_dir, prefix)
        if os.path.isdir(current_path):
            base_image_path = os.path.join(current_path, f"{prefix}_2K_Color.jpg")
            if os.path.exists(base_image_path):
                # construct all image paths
                ambient_occlusion_image_path = base_image_path.replace("Color", "AmbientOcclusion")
                metallic_image_path = base_image_path.replace("Color", "Metalness")
                roughness_image_path = base_image_path.replace("Color", "Roughness")
                alpha_image_path = base_image_path.replace("Color", "Opacity")
                normal_image_path = base_image_path.replace("Color", "Normal")
                displacement_image_path = base_image_path.replace("Color", "Displacement")

                
                # search for existing material
                new_mat = MaterialLoaderUtility.find_cc_material_by_name(prefix, {})

                if new_mat is None:
                    new_mat = MaterialLoaderUtility.create_new_cc_material(prefix, {})
                    # create material based on these image paths
                    _CCMaterialLoader.create_material(new_mat, base_image_path, ambient_occlusion_image_path,
                                                        metallic_image_path, roughness_image_path, alpha_image_path,
                                                        normal_image_path, displacement_image_path)
                return Material(new_mat)
            
            raise FileNotFoundError(f"The resources does not satisfy for creation of material: {prefix}")
        
        raise FileNotFoundError(f"The prefix does not match: {prefix}")
    
    raise FileNotFoundError(f"The folder path does not exist: {cctexture_dir}")
