'''
A script that contains dict for mapping ui selection and corresponding functions
'''
import albumentations as albu
import cv2

ui_function_mapping = {
    "Gaussian Noise": albu.GaussNoise((15,50)),
    "Gaussian Blur": albu.GaussianBlur(),
    "Random Brightness Contrast": albu.RandomBrightnessContrast(),
    "Hue Saturation Value": albu.HueSaturationValue(25,35,25),
    "Random Gamma": albu.RandomGamma(),
    "Motion Blur": albu.MotionBlur(blur_limit=(3,10)),
    "CLAHE": albu.CLAHE(),
    "Vertical Flip": albu.VerticalFlip(),
    "Horizontal Flip": albu.HorizontalFlip(),
    "Rotate": albu.Rotate(limit=(-90, 90),border_mode=cv2.BORDER_CONSTANT, value=(0,0,0)),
    "Random Crop Near Bounding Box (+Resize)": albu.BBoxSafeRandomCrop(),
    "Random Sized Bounding Box Safe Crop (+Resize)": albu.RandomCropNearBBox(max_part_shift=0, cropping_box_key='cropping_box', p=1),
}