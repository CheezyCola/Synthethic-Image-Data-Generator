"""
A script to handle failed image in generation loop
"""
import os
from PIL import Image
from pycocotools.coco import COCO
import json

def create_empty_coco(file_path):
    coco = {
        "info": {
            "description": "coco_annotations",
            "url": "https://github.com/waspinator/pycococreator",
            "version": "0.1.0",
            "year": 2020,
            "contributor": "Unknown",
            "date_created": "2024-02-19 15:17:41.735338"
        },
        "licenses": [
            {
            "id": 1,
            "name": "Attribution-NonCommercial-ShareAlike License",
            "url": "http://creativecommons.org/licenses/by-nc-sa/2.0/"
            }
        ],
        "categories": [],
        "images": [],
        "annotations": []
    }
    with open(file_path, 'w', encoding="utf-8") as json_file:
        json.dump(coco, json_file)
            
def dummy_img_anno(new_img_id: int, new_file_name: str, width: int, heigth: int):
    return {"id": new_img_id,
            "file_name": new_file_name,
            "width": width,
            "height": heigth,
            "date_captured": "",
            "license": 1,
            "coco_url": "",
            "flickr_url": ""}

def create_dummy_img(dataset_dir:str, annotate_image:bool):
    """Create a dummy image to replace the failed image in generation. The annotation
    of this image will be written as empty.

    :param dataset_dir: a directory which holds 'coco_data'
    :param annotate_image: if True, annotates the augmentated image and saves it
    """
    coco_data_dir = os.path.join(dataset_dir, "coco_data")
    images_dir = os.path.join(coco_data_dir, "images")
    anno_images_dir = os.path.join(coco_data_dir, "annotated_images")
    coco_anno = os.path.join(coco_data_dir, "coco_annotations.json")
    os.makedirs(images_dir, exist_ok=True)

    if not os.path.exists(coco_anno):
        create_empty_coco(coco_anno)

    coco = COCO(coco_anno)
    images = coco.dataset["images"]
    new_img_id = len(images)
    new_file_name = "images/" + str(new_img_id).zfill(6)+".jpg"
    img = Image.new("RGB", (1920, 1920), (255, 255, 255))
    img.save(os.path.join(coco_data_dir, new_file_name), "jpeg")
    width = 0
    height = 0

    new_img_anno = dummy_img_anno(new_img_id, new_file_name, width, height)
    images.append(new_img_anno)
    new_coco_annotations = {
        "info": coco.dataset["info"],
        "licenses": coco.dataset["licenses"],
        "categories": coco.dataset["categories"],
        "images": images,
        "annotations": coco.dataset["annotations"]
    }        
    with open(coco_anno, 'w', encoding="utf-8") as json_file:
        json.dump(new_coco_annotations, json_file)

    if annotate_image:
        os.makedirs(anno_images_dir, exist_ok=True)
        img.save(os.path.join(anno_images_dir, "coco_annotated_"+str(new_img_id)+".png"), "png")

def replace_dummy_img_with_latest(dataset_dir:str, annotate_image:bool, index: int):
    """Replace the dummy image of a index with the latest created image. This is to
    replace the dummy image created during failure with the re-generated image.

    :param dataset_dir: a directory which holds 'coco_data'
    :param annotate_image: if True, annotates the augmentated image and saves it
    """
    coco_data_dir = os.path.join(dataset_dir, "coco_data")
    images_dir = os.path.join(coco_data_dir, "images")
    anno_images_dir = os.path.join(coco_data_dir, "annotated_images")
    coco_anno = os.path.join(coco_data_dir, "coco_annotations.json")
    os.makedirs(images_dir, exist_ok=True)

    coco = COCO(coco_anno)
    annotations =  coco.dataset["annotations"]
    images = coco.dataset["images"]
    latest_img_id = len(images)-1
    latest_img_file = "images/" + str(latest_img_id).zfill(6)+".jpg"

    # delete dummy img (occupant at index)
    dummy_img_file = "images/" + str(index).zfill(6)+".jpg"

    if dummy_img_file == latest_img_file:
        print("new image:", latest_img_file)
        return # not dummy to be replaced
    
    os.remove(os.path.join(coco_data_dir, dummy_img_file))
    # rename latest jpg to index
    os.rename(os.path.join(coco_data_dir, latest_img_file), os.path.join(coco_data_dir, dummy_img_file))

    if annotate_image:
        anno_dummy_img_file = str(index)+".png"
        latest_img_file = str(latest_img_id)+".png"
        os.makedirs(anno_images_dir, exist_ok=True)
        if os.path.exists(os.path.join(anno_images_dir, "coco_annotated_"+anno_dummy_img_file)):
            os.remove(os.path.join(anno_images_dir, "coco_annotated_"+anno_dummy_img_file))
        if os.path.exists(os.path.join(anno_images_dir, "coco_annotated_"+latest_img_file)): 
            os.rename(os.path.join(anno_images_dir, "coco_annotated_"+latest_img_file),
                      os.path.join(anno_images_dir, "coco_annotated_"+anno_dummy_img_file))

    # arrange coco annotations
    latest_id_images = [x for x in images if x["id"]==latest_img_id]
    latest_id_annotations = [x for x in annotations if x["image_id"]==latest_img_id]
        
    new_id_image = latest_id_images[0].copy()
    new_id_image.update({"id": index})
    new_id_image.update({"file_name": dummy_img_file})
    images = [d for d in images if d['id'] not in [index, latest_img_id]]
    images.append(new_id_image)
    images.sort(key=lambda x: x.get('id'))

    annotations = [d for d in annotations if not d.get("image_id")==latest_img_id]
    for _latest_id_annotation in latest_id_annotations:
        latest_id_annotation = _latest_id_annotation.copy()
        latest_id_annotation.update({"image_id": index})
        annotations.append(latest_id_annotation)

    new_coco_annotations = {
        "info": coco.dataset["info"],
        "licenses": coco.dataset["licenses"],
        "categories": coco.dataset["categories"],
        "images": images,
        "annotations": annotations
    }        
    with open(coco_anno, 'w', encoding="utf-8") as json_file:
        json.dump(new_coco_annotations, json_file)
