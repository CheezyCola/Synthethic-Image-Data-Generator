'''
A script that contains functions to perform augmentation of image data.
Augmentation library: https://albumentations.ai/
'''
import os
import shutil
import glob
import random
import json
from typing import List

import cv2
import albumentations as albu
from pycocotools import mask as coco_mask
from pycocotools.coco import COCO

from DataGenerator.utility import coco_utils

class Augmentator:
    def __init__(self, dataset_dir: str, annotate_image:bool) -> None:
        """Performs augmentation(s) to images in dataset.

        :param dataset_dir: a directory which holds 'coco_data'
        :param annotate_image: if True, annotates the augmentated image and saves it
        """
        self.pixel_transforms = [
            albu.GaussNoise((15,50)),
            albu.GaussianBlur(),
            albu.RandomBrightnessContrast(),
            albu.HueSaturationValue(25,35,25),
            albu.RandomGamma(),
            albu.MotionBlur(),
            albu.CLAHE()
        ]
        self.spatial_transforms = [
            albu.VerticalFlip(),
            albu.HorizontalFlip(),
            albu.Rotate(limit=(-90, 90),border_mode=cv2.BORDER_CONSTANT, value=(0,0,0))
        ]
        self.cropping_transforms = [
            albu.BBoxSafeRandomCrop(),
            albu.RandomCropNearBBox(max_part_shift=0, cropping_box_key='cropping_box', p=1),
        ]

        self.coco_data_dir = os.path.join(dataset_dir, "coco_data")
        self.images_dir = os.path.join(self.coco_data_dir, "images")
        self.anno_images_dir = os.path.join(self.coco_data_dir, "annotated_images")
        self.annotate_image = annotate_image
        self.img_paths =  glob.glob(self.images_dir + "/*.jpg")
        self.img_paths.sort()
        shutil.copy(os.path.join(self.coco_data_dir, "coco_annotations.json"), os.path.join(self.coco_data_dir, "old_coco_annotations.json"))
    
    # private method for check continuation of task
    def __to_continue(self, check_CANCEL):
        if check_CANCEL:
            ret = check_CANCEL()
            return ret
        else:
            return "continue"

    def universal_bbox_from_bboxes(self, bboxes: List[List[int]]) -> List:
        """Returns a bounding box that includes all input boxes

        :param bboxes: a directory which holds images and 'coco_annotations.json'
        """
        min_x, min_y = float('inf'), float('inf')
        max_x, max_y = float('-inf'), float('-inf')

        for bbox in bboxes:
            x, y, width, height = bbox
            min_x = min(min_x, x)
            min_y = min(min_y, y)
            max_x = max(max_x, x + width)
            max_y = max(max_y, y + height)

        overall_bbox = [min_x, min_y, max_x, max_y]
        return overall_bbox

    def pixel_augmentation(self, check_CANCEL=None, progress_callback=None):
        """Performs pixel-level augmentation(s) to images in dataset.

        :param check_CANCEL: function that checks cancel flag
        :param progress_callback: a class object that facilitates progress callback
        """
        if progress_callback: progress_callback("Pixel-level Augmentation ..." , 0)

        for k, img_path in enumerate(self.img_paths):
            #region check cancel and callback
            if not self.__to_continue(check_CANCEL): return # check whether to continue
            if progress_callback: progress_callback("Pixel-level Augmentation {}/{}...".format(k+1, len(self.img_paths)),
                                                    int(k/len(self.img_paths)*100))
            #endregion
                
            file_name = os.path.basename(img_path)
            old_id = int(file_name.split(".jpg")[0])

            coco = COCO(os.path.join(self.coco_data_dir, "coco_annotations.json"))
            annotations =  coco.dataset["annotations"]
            images = coco.dataset["images"]

            old_id_images = [x for x in images if x["id"]==old_id]
            old_id_annotations = [x for x in annotations if x["image_id"]==old_id]

            new_img_id = len(images)
            new_file_name = str(new_img_id).zfill(6)+".jpg"
            
            transform = albu.Compose([
                albu.SomeOf(self.pixel_transforms, n=random.randint(1,len(self.pixel_transforms)), p=1)
            ])

            image = cv2.imread(img_path)
            transformed = transform(image=image)
            transformed_image = transformed["image"]
            cv2.imwrite(os.path.join(self.images_dir, new_file_name), transformed_image)

            new_id_images = old_id_images[0].copy()
            new_id_images.update({"id": new_img_id})
            new_id_images.update({"file_name": "images/"+new_file_name})
            new_id_images.update({"date_captured": ""})
            images.append(new_id_images)

            for _old_id_annotation in old_id_annotations:
                new_anno_id = len(annotations)+1
                old_id_annotation = _old_id_annotation.copy()
                old_id_annotation.update({"id": new_anno_id})
                old_id_annotation.update({"image_id": new_img_id})
                annotations.append(old_id_annotation)

            new_coco_annotations = {
                "info": coco.dataset["info"],
                "licenses": coco.dataset["licenses"],
                "categories": coco.dataset["categories"],
                "images": images,
                "annotations": annotations
            }        
            with open(os.path.join(self.coco_data_dir, "coco_annotations.json"), 'w', encoding="utf-8") as json_file:
                json.dump(new_coco_annotations, json_file)

            if self.annotate_image:
                os.makedirs(self.anno_images_dir, exist_ok=True)
                coco_utils.save_annotated_image(self.coco_data_dir, "coco_annotations.json")

        if progress_callback: progress_callback("Pixel-level Augmentation ..." , 100)
        return True

    def spatial_augmentation(self, check_CANCEL=None, progress_callback=None):
        """Performs spatial-level augmentation(s) to images in dataset. 

        :param check_CANCEL: function that checks cancel flag
        :param progress_callback: a class object that facilitates progress callback
        """
        if progress_callback: progress_callback("Spatial-level Augmentation ..." , 0)

        for k, img_path in enumerate(self.img_paths):
            #region check cancel and callback
            if not self.__to_continue(check_CANCEL): return # check whether to continue
            if progress_callback: progress_callback("Spatial-level Augmentation {}/{}...".format(k+1, len(self.img_paths)),
                                                    int(k/len(self.img_paths)*100))
            #endregion
                
            file_name = os.path.basename(img_path)
            old_id = int(file_name.split(".jpg")[0])

            coco = COCO(os.path.join(self.coco_data_dir, "coco_annotations.json"))
            annotations =  coco.dataset["annotations"]
            images = coco.dataset["images"]

            old_id_images = [x for x in images if x["id"]==old_id]
            old_id_annotations = [x for x in annotations if x["image_id"]==old_id]
            old_rle_masks = [x["segmentation"] for x in old_id_annotations]
            old_binary_masks = [coco_mask.decode(coco_mask.frPyObjects(x, x["size"][1], x["size"][0])) for x in old_rle_masks]
            new_img_id = len(images)
            new_file_name = str(new_img_id).zfill(6)+".jpg"
            
            
            transform = albu.Compose([
                albu.OneOf(self.spatial_transforms, p=1)
            ])

            image = cv2.imread(img_path)
            transformed = transform(image=image, masks=old_binary_masks)
            transformed_image = transformed["image"]
            transformed_binary_masks = transformed["masks"]
            transformed_rle_masks = [coco_utils.binary_mask_to_rle(x) for x in transformed_binary_masks]
            cv2.imwrite(os.path.join(self.images_dir, new_file_name), transformed_image)

            new_id_images = old_id_images[0].copy()
            new_id_images.update({"id": new_img_id})
            new_id_images.update({"file_name": "images/"+new_file_name})
            new_id_images.update({"date_captured": ""})
            images.append(new_id_images)

            for i, _old_id_annotation in enumerate(old_id_annotations):
                new_anno_id = len(annotations)+1
                old_id_annotation = _old_id_annotation.copy()
                old_id_annotation.update({"id": new_anno_id})
                old_id_annotation.update({"image_id": new_img_id})
                old_id_annotation.update({"area": coco_utils.calc_binary_mask_area(transformed_binary_masks[i])})
                old_id_annotation.update({"bbox": coco_utils.bbox_from_binary_mask(transformed_binary_masks[i])})
                old_id_annotation.update({"segmentation": transformed_rle_masks[i]})
                old_id_annotation.update({"width": transformed_rle_masks[i]["size"][1]})
                old_id_annotation.update({"height": transformed_rle_masks[i]["size"][1]})
                annotations.append(old_id_annotation)

            new_coco_annotations = {
                "info": coco.dataset["info"],
                "licenses": coco.dataset["licenses"],
                "categories": coco.dataset["categories"],
                "images": images,
                "annotations": annotations
            }
            with open(os.path.join(self.coco_data_dir, "coco_annotations.json"), 'w', encoding="utf-8") as json_file:
                json.dump(new_coco_annotations, json_file)

            if self.annotate_image:
                os.makedirs(self.anno_images_dir, exist_ok=True)
                coco_utils.save_annotated_image(self.coco_data_dir, "coco_annotations.json")
        
        if progress_callback: progress_callback("Spatial Augmentation ..." , 100)
        return True
    
    def spatial_augmentation2(self, check_CANCEL=None, progress_callback=None):
        """Performs spatial-level augmentation(s) to images in dataset. 

        :param check_CANCEL: function that checks cancel flag
        :param progress_callback: a class object that facilitates progress callback
        """
        if progress_callback: progress_callback("Spatial-level Augmentation ..." , 0)
        
        self.img_paths = self.img_paths[917:2125]

        for k, img_path in enumerate(self.img_paths):
            #region check cancel and callback
            if not self.__to_continue(check_CANCEL): return # check whether to continue
            if progress_callback: progress_callback("Spatial-level Augmentation {}/{}...".format(k+1, len(self.img_paths)),
                                                    int(k/len(self.img_paths)*100))
            #endregion
                
            file_name = os.path.basename(img_path)
            old_id = int(file_name.split(".jpg")[0])

            coco = COCO(os.path.join(self.coco_data_dir, "coco_annotations.json"))
            annotations =  coco.dataset["annotations"]
            images = coco.dataset["images"]

            old_id_images = [x for x in images if x["id"]==old_id]
            old_id_annotations = [x for x in annotations if x["image_id"]==old_id]
            old_rle_masks = [x["segmentation"] for x in old_id_annotations]
            old_binary_masks = [coco_mask.decode(coco_mask.frPyObjects(x, x["size"][1], x["size"][0])) for x in old_rle_masks]
            new_img_id = len(images)
            new_file_name = str(new_img_id).zfill(6)+".jpg"
            
            
            transform = albu.Compose([
                albu.OneOf(self.spatial_transforms, p=1)
            ])

            image = cv2.imread(img_path)
            transformed = transform(image=image, masks=old_binary_masks)
            transformed_image = transformed["image"]
            transformed_binary_masks = transformed["masks"]
            transformed_rle_masks = [coco_utils.binary_mask_to_rle(x) for x in transformed_binary_masks]
            cv2.imwrite(os.path.join(self.images_dir, new_file_name), transformed_image)

            new_id_images = old_id_images[0].copy()
            new_id_images.update({"id": new_img_id})
            new_id_images.update({"file_name": "images/"+new_file_name})
            new_id_images.update({"date_captured": ""})
            images.append(new_id_images)

            for i, _old_id_annotation in enumerate(old_id_annotations):
                new_anno_id = len(annotations)+1
                old_id_annotation = _old_id_annotation.copy()
                old_id_annotation.update({"id": new_anno_id})
                old_id_annotation.update({"image_id": new_img_id})
                old_id_annotation.update({"area": coco_utils.calc_binary_mask_area(transformed_binary_masks[i])})
                old_id_annotation.update({"bbox": coco_utils.bbox_from_binary_mask(transformed_binary_masks[i])})
                old_id_annotation.update({"segmentation": transformed_rle_masks[i]})
                old_id_annotation.update({"width": transformed_rle_masks[i]["size"][1]})
                old_id_annotation.update({"height": transformed_rle_masks[i]["size"][1]})
                annotations.append(old_id_annotation)

            new_coco_annotations = {
                "info": coco.dataset["info"],
                "licenses": coco.dataset["licenses"],
                "categories": coco.dataset["categories"],
                "images": images,
                "annotations": annotations
            }
            with open(os.path.join(self.coco_data_dir, "coco_annotations.json"), 'w', encoding="utf-8") as json_file:
                json.dump(new_coco_annotations, json_file)

            if self.annotate_image:
                os.makedirs(self.anno_images_dir, exist_ok=True)
                coco_utils.save_annotated_image(self.coco_data_dir, "coco_annotations.json")
        
        if progress_callback: progress_callback("Spatial Augmentation ..." , 100)
        return True

    def cropping(self, keep_size=True, check_CANCEL=None, progress_callback=None):
        """Performs cropping augmentation(s) to images in dataset. 

        :param keep_size: if True, resizes images to image's original size before cropping. Optical distortion could be observed
        :param check_CANCEL: function that checks cancel flag
        :param progress_callback: a class object that facilitates progress callback
        """
        if progress_callback: progress_callback("Cropping ..." , 0)
        
        img_paths =  glob.glob(self.images_dir + "/*.jpg")
        img_paths.sort()

        p_size = 0
        if keep_size:
            p_size = 1

        for k, img_path in enumerate(img_paths):
            #region check cancel and callback
            if not self.__to_continue(check_CANCEL): return # check whether to continue
            if progress_callback: progress_callback("Cropping {}/{}...".format(k+1, len(img_paths)) , int(k/len(img_paths)*100))
            #endregion

            file_name = os.path.basename(img_path)
            old_id = int(file_name.split(".jpg")[0])

            coco = COCO(os.path.join(self.coco_data_dir, "coco_annotations.json"))
            annotations =  coco.dataset["annotations"]
            images = coco.dataset["images"]

            old_id_images = [x for x in images if x["id"]==old_id]
            old_height = old_id_images[0]["height"]
            old_width = old_id_images[0]["width"]
            old_id_annotations = [x for x in annotations if x["image_id"]==old_id]
            old_rle_masks = [x["segmentation"] for x in old_id_annotations]
            old_binary_masks = [coco_mask.decode(coco_mask.frPyObjects(x, x["size"][1], x["size"][0])) for x in old_rle_masks]
            old_bboxes = [x["bbox"] for x in old_id_annotations]
            overall_bbox = self.universal_bbox_from_bboxes(old_bboxes)
            old_ids = [x["category_id"] for x in old_id_annotations]

            new_img_id = len(images)
            new_file_name = str(new_img_id).zfill(6)+".jpg"

            transform = albu.Compose([
                albu.OneOf(self.cropping_transforms, p=1),
                albu.Resize(old_height,old_width, p=p_size)
            ],bbox_params=albu.BboxParams(format='coco', label_fields=['ids']))

            image = cv2.imread(img_path)
            transformed = transform(image=image, cropping_box=overall_bbox,
                                    bboxes=old_bboxes, masks=old_binary_masks,
                                    ids=old_ids)
            transformed_image = transformed["image"]
            transformed_binary_masks = transformed["masks"]
            transformed_rle_masks = [coco_utils.binary_mask_to_rle(x) for x in transformed_binary_masks]
            cv2.imwrite(os.path.join(self.images_dir, new_file_name), transformed_image)

            new_id_images = old_id_images[0].copy()
            new_id_images.update({"id": new_img_id})
            new_id_images.update({"file_name": "images/"+new_file_name})
            new_id_images.update({"date_captured": ""})
            images.append(new_id_images)

            for i, _old_id_annotation in enumerate(old_id_annotations):
                new_anno_id = len(annotations)+1
                old_id_annotation = _old_id_annotation.copy()
                old_id_annotation.update({"id": new_anno_id})
                old_id_annotation.update({"image_id": new_img_id})
                old_id_annotation.update({"area": coco_utils.calc_binary_mask_area(transformed_binary_masks[i])})
                old_id_annotation.update({"bbox": coco_utils.bbox_from_binary_mask(transformed_binary_masks[i])})
                old_id_annotation.update({"segmentation": transformed_rle_masks[i]})
                old_id_annotation.update({"width": transformed_rle_masks[i]["size"][1]})
                old_id_annotation.update({"height": transformed_rle_masks[i]["size"][1]})
                annotations.append(old_id_annotation)

            new_coco_annotations = {
                "info": coco.dataset["info"],
                "licenses": coco.dataset["licenses"],
                "categories": coco.dataset["categories"],
                "images": images,
                "annotations": annotations
            }
            with open(os.path.join(self.coco_data_dir, "coco_annotations.json"), 'w', encoding="utf-8") as json_file:
                json.dump(new_coco_annotations, json_file)

            if self.annotate_image:
                os.makedirs(self.anno_images_dir, exist_ok=True)
                coco_utils.save_annotated_image(self.coco_data_dir, "coco_annotations.json")

        if progress_callback: progress_callback("Cropping ..." , 100)
        return True

    def augmentate(self, check_CANCEL=None, progress_callback=None):
        if self.pixel_transforms:
            self.pixel_augmentation(check_CANCEL=check_CANCEL, progress_callback=progress_callback)
        if self.spatial_transforms:
            self.spatial_augmentation(check_CANCEL=check_CANCEL, progress_callback=progress_callback)
        if self.cropping_transforms:
            self.cropping(check_CANCEL=check_CANCEL, progress_callback=progress_callback)
        return True

if __name__ == '__main__':
    test_dir = "/BlenderProc2/Dataset/Dataset_2/training"
    Aug = Augmentator(test_dir, annotate_image=True)
    # Aug.pixel_augmentation()
    Aug.spatial_augmentation2()
    Aug.cropping()
