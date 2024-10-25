"""
A script to handle COCO annotations and contains some modified functions from: 
https://github.com/DLR-RM/BlenderProc/blob/main/blenderproc/python/writer/CocoWriterUtility.py
for flexibility.
"""
import os
from typing import Dict, List
from itertools import groupby
import json
import numpy as np
from PIL import Image, ImageFont, ImageDraw

from blenderproc.python.utility import LabelIdMapping

def read_coco_annotations(coco_dir: str="Dataset/coco_data", json_file: str="coco_annotations.json"):
    """Reads json file of coco annotations and returns the annotations, categories and images.
    
    :param coco_dir: a directory which holds images and 'coco_annotations.json'.
    :param json_file: json file name
    :return: annotations, categories and images written in json file
    """
    if os.path.exists(coco_dir) and os.path.isdir(coco_dir):
        file = os.path.join(coco_dir, json_file)
        if os.path.exists(file):
            with open(file, "r", encoding="utf-8") as f:
                annotations = json.load(f)
                categories = annotations['categories']
                images = annotations['images']
                annotations = annotations['annotations']
            return annotations, categories, images
        raise FileNotFoundError(f"The folder path does not exist: {file}")
    raise FileNotFoundError(f"The folder path does not exist: {coco_dir}")

def binary_mask_to_rle(binary_mask: np.ndarray) -> Dict[str, List[int]]:
    """Converts a binary mask to COCOs run-length encoding (RLE) format. Instead of outputting
    a mask image, you give a list of start pixels and how many pixels after each of those
    starts are included in the mask.

    :param binary_mask: a 2D binary numpy array where '1's represent the object
    :return: Mask in RLE format
    """
    rle: Dict[str, List[int]] = {'counts': [], 'size': list(binary_mask.shape)}
    counts = rle.get('counts')
    for i, (value, elements) in enumerate(groupby(binary_mask.ravel(order='F'))):
        if i == 0 and value == 1:
            counts.append(0)
        counts.append(len(list(elements)))
    return rle

def rle_to_binary_mask(rle):
    """Converts a COCOs run-length encoding (RLE) to binary mask.

    :param rle: Mask in RLE format
    :return: a 2D binary numpy array where '1's represent the object
    """
    binary_array = np.zeros(np.prod(rle.get('size')), dtype=bool)
    counts = rle.get('counts')

    start = 0
    for i in range(len(counts) - 1):
        start += counts[i]
        end = start + counts[i + 1]
        binary_array[start:end] = (i + 1) % 2

    binary_mask = binary_array.reshape(*rle.get('size'), order='F')
    return binary_mask

def bbox_from_binary_mask(binary_mask: np.ndarray) -> List[int]:
    """ Returns the smallest bounding box containing all pixels marked "1" in the given image mask.

    :param binary_mask: A binary image mask with the shape [H, W].
    :return: The bounding box represented as [x, y, width, height]
    """
    # Find all columns and rows that contain 1s
    rows = np.any(binary_mask, axis=1)
    cols = np.any(binary_mask, axis=0)
    # Find the min and max col/row index that contain 1s
    rmin, rmax = np.where(rows)[0][[0, -1]]
    cmin, cmax = np.where(cols)[0][[0, -1]]
    # Calc height and width
    h = rmax - rmin + 1
    w = cmax - cmin + 1
    return [int(cmin), int(rmin), int(w), int(h)]

def calc_binary_mask_area(binary_mask: np.ndarray) -> int:
    """ Returns the area of the given binary mask which is defined as the number of 1s in the mask.

    :param binary_mask: A binary image mask with the shape [H, W].
    :return: The computed area
    """
    return binary_mask.sum().tolist()

def save_annotated_image(coco_dir: str="Dataset/coco_data", json_file: str="coco_annotations.json"):
    """Annotates the latest image in directory 'coco_data/images' and saves the 
    annotated image into directory 'coco_data/annotated_images'.

    :param coco_dir: a directory which holds images and 'coco_annotations.json'
    :param json_file: json file name
    """
    annotations, categories, images = read_coco_annotations(coco_dir, json_file)
    output_dir = os.path.join(coco_dir, "annotated_images")
    os.makedirs(output_dir,exist_ok=True)

    # open the last saved image
    i = len(images)-1
    if i<0:
        raise RuntimeError(f"No coco annotation is saved in {os.path.join(coco_dir, json_file)}")
    im = Image.open(os.path.join(coco_dir, images[i]['file_name']))

    font = ImageFont.load_default()
    # Add bounding boxes and masks
    for annotation in annotations:
        if annotation["image_id"] == i:
            draw = ImageDraw.Draw(im)
            bb = annotation['bbox']
            _id = annotation["category_id"]
            category = [category["name"] for category in categories if category["id"] == _id]
            if category:
                _category = category[0]
            else:
                raise RuntimeError(f"Category {_id} is not defined in {json_file}")

            draw.rectangle(((bb[0], bb[1]), (bb[0] + bb[2], bb[1] + bb[3])), fill=None, outline="red")
            draw.text((bb[0] + 2, bb[1] + 2), _category, font=font)
            if isinstance(annotation["segmentation"], dict):
                im.putalpha(255)
                rle_seg = annotation["segmentation"]
                item = rle_to_binary_mask(rle_seg).astype(np.uint8) * 255
                item = Image.fromarray(item, mode='L')
                overlay = Image.new('RGBA', im.size)
                draw_ov = ImageDraw.Draw(overlay)
                rand_color = np.random.randint(0, 256, 3)
                draw_ov.bitmap((0, 0), item, fill=(rand_color[0], rand_color[1], rand_color[2], 128))
                im = Image.alpha_composite(im, overlay)
            else:
                # go through all polygons and plot them
                for item in annotation['segmentation']:
                    poly = Image.new('RGBA', im.size)
                    pdraw = ImageDraw.Draw(poly)
                    rand_color = np.random.randint(0, 256, 3)
                    pdraw.polygon(item, fill=(rand_color[0], rand_color[1], rand_color[2], 127),
                                  outline=(255, 255, 255, 255))
                    im.paste(poly, mask=poly)

            im.save(os.path.join(output_dir, f'coco_annotated_{i}.png'), "PNG")

def save_annotated_images(coco_dir: str="Dataset/coco_data", json_file: str="coco_annotations.json"):
    """Annotates the images in directory 'coco_data/images' and saves the 
    annotated images into directory 'coco_data/annotated_images'.

    :param coco_dir: a directory which holds images and 'coco_annotations.json'
    :param json_file: json file name
    """
    annotations, categories, images = read_coco_annotations(coco_dir, json_file)
    output_dir = os.path.join(coco_dir, "annotated_images")
    os.makedirs(output_dir,exist_ok=True)

    for i, image in enumerate(images):
        im = Image.open(os.path.join(coco_dir, image['file_name']))

        font = ImageFont.load_default()
        # Add bounding boxes and masks
        for annotation in annotations:
            if annotation["image_id"] == i:
                draw = ImageDraw.Draw(im)
                bb = annotation['bbox']
                _id = annotation["category_id"]
                category = [category["name"] for category in categories if category["id"] == _id]
                if category:
                    _category = category[0]
                else:
                    raise RuntimeError(f"Category {_id} is not defined in {json_file}")

                draw.rectangle(((bb[0], bb[1]), (bb[0] + bb[2], bb[1] + bb[3])), fill=None, outline="red")
                draw.text((bb[0] + 2, bb[1] + 2), _category, font=font)
                if isinstance(annotation["segmentation"], dict):
                    im.putalpha(255)
                    rle_seg = annotation["segmentation"]
                    item = rle_to_binary_mask(rle_seg).astype(np.uint8) * 255
                    item = Image.fromarray(item, mode='L')
                    overlay = Image.new('RGBA', im.size)
                    draw_ov = ImageDraw.Draw(overlay)
                    rand_color = np.random.randint(0, 256, 3)
                    draw_ov.bitmap((0, 0), item, fill=(rand_color[0], rand_color[1], rand_color[2], 128))
                    im = Image.alpha_composite(im, overlay)
                else:
                    # go through all polygons and plot them
                    for item in annotation['segmentation']:
                        poly = Image.new('RGBA', im.size)
                        pdraw = ImageDraw.Draw(poly)
                        rand_color = np.random.randint(0, 256, 3)
                        pdraw.polygon(item, fill=(rand_color[0], rand_color[1], rand_color[2], 127),
                                    outline=(255, 255, 255, 255))
                        im.paste(poly, mask=poly)

                im.save(os.path.join(output_dir, f'coco_annotated_{i}.png'), "PNG")

def prettyprint_coco_annotations(coco_dir: str="Dataset/coco_data", json_file: str="coco_annotations.json") -> None:
    """Prints the content in json file with indentation.

    :param coco_dir: a directory which holds images and 'coco_annotations.json'
    :param json_file: json file name
    """
    if os.path.exists(coco_dir) and os.path.isdir(coco_dir):
        file = os.path.join(coco_dir, json_file)
        if os.path.exists(file):
            with open(file, "r", encoding="utf-8") as f:
                annotations = json.load(f)
                print(json.dumps(annotations, indent=6))
                return None
        raise FileNotFoundError(f"The folder path does not exist: {file}")
    raise FileNotFoundError(f"The folder path does not exist: {coco_dir}")

def map_coco_label(objects: List, coco_dir: str="Dataset/coco_data", json_file: str="coco_annotations.json") -> LabelIdMapping.LabelIdMapping:
    """Maps coco labels. When category id already exists, maps segmentation's id to existing category id.
    When not category id does not exist, create a new category id.

    :param coco_dir: a directory which holds images and 'coco_annotations.json'
    :param json_file: json file name
    :return: A LabelIdMapping object of blenderproc.python.utility
    """
    label_mapping = LabelIdMapping.LabelIdMapping()
    _id = 1
    try:
        _, categories, _ = read_coco_annotations(coco_dir, json_file)
        id_list = []
        for category in categories:
            id_list.append(category["id"])
            label_mapping.add(category["name"], category["id"])
        if id_list:
            _id = max(id_list)+1
    except FileNotFoundError:
        print("coco_annotations.json does'nt exist")

    for _object in objects:
        obj_name = _object.get_name()
        obj_name = obj_name.split(".")[0]
        print(obj_name)
        if not label_mapping.has_label(obj_name):
            label_mapping.add(obj_name, _id)
            _id += 1
        _object.set_cp("category_id", label_mapping.id_from_label(obj_name))
        _object.set_cp("class_name", obj_name)

    return label_mapping

def store_image_occlusion_data(object_occlusion: dict, coco_dir: str="Dataset/coco_data", json_file: str="coco_annotations.json"):
    """Stores the percentage of objects' occlusion of latest image in the image's info in 'coco_annotations.json'. 

    :param object_occlusion: A dict of objects and their percentage of occlusion to camera view
    :param coco_dir: a directory which holds images and 'coco_annotations.json'
    :param json_file: json file name
    """
    _, _, images = read_coco_annotations(coco_dir, json_file)
    img_id = len(images)-1

    for image in images:
        if image["id"] == img_id:
            image.update({"object_occlusion": object_occlusion})

    file = os.path.join(coco_dir, json_file)
    with open(file, "r", encoding="utf-8") as f:
        json_annotations = json.load(f)

    json_annotations.update({"images": images})
    with open(file, "w", encoding="utf-8") as f:
        json.dump(json_annotations, f)
    