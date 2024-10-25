"""
A script containing functions to split a dataset into smaller set of
training, validation and testing datasets.
"""
import os
import glob
import shutil
import json

import statistics
import pandas as pd
from sklearn.model_selection import train_test_split
from pycocotools.coco import COCO

def find_optimal_split(dataset_dir: str, 
                       train_size: float=0.7,
                       valid_size: float=0.15,
                       test_size: float=0.15,
                       max_iter: int=10000, 
                       progress_callback=None):
    """Returns optimal balanced sub-datasets' indexes.
    :param dataset_dir: A directory which holds 'coco_data'.
    :param train_size (float, optional): Sum of train_size, valid_size and test_size should be 
                                      between 0.0 and 1.0 and represent the proportion of the 
                                      dataset to include in the split. Defaults to 0.7.
    :param valid_size (float, optional): Defaults to 0.15.
    :param test_size (float, optional): Defaults to 0.15.
    :param max_iter: The number of repitition of splitting process in order to find the
                     splitting with optimal balanced sub-datasets.
    """
    if progress_callback: progress_callback("Finding Optimal Split ..." ,0)
    
    df = pd.read_csv(dataset_dir + "/class_sampling.csv")
    df = df[df.columns[:-1]]
    # groups = list(set(df["Image"]))
    results = []
    temp = []
    for it in range(max_iter):
        if progress_callback: progress_callback("Finding Optimal Split ..." ,int(it/max_iter*2*100))
        a_set, bc_set, a_index, bc_index = train_test_split(df.to_numpy(), df.index.to_list(),test_size=valid_size+test_size, shuffle=True)
        bc_index.sort()
        if temp:
            if bc_index in temp:
                continue
        temp.append(bc_index)
        std = statistics.stdev(bc_set.sum(axis=0).tolist())
        results.append({
            'a_index': a_index,
            # 'a_set': a_set,
            'bc_index': bc_index,
            # 'b_set': bc_set,
            'std': std
        })
    results_df = pd.DataFrame(results).sort_values(by='std')
    train_index, bc_index = results_df.iloc[0]['a_index'], results_df.iloc[0]['bc_index']
    if progress_callback: progress_callback("Finding Optimal Split ..." ,100)

    if test_size>0:
        bc_df = df.iloc[bc_index]
        results = []
        temp = []
        for it in range(max_iter):
            if progress_callback: progress_callback("Finding Optimal Split ..." ,int(max_iter+it/max_iter*100))
            b_set, c_set, b_index, c_index = train_test_split(bc_df.to_numpy(), bc_index,test_size=test_size/(valid_size+test_size), shuffle=True)
            b_index.sort()
            if temp:
                if b_index in temp:
                    continue
            temp.append(b_index)
            std = statistics.stdev(b_set.sum(axis=0).tolist())
            results.append({
                'b_index': b_index,
                # 'b_set': b_set,
                'c_index': c_index,
                # 'c_set': c_set,
                'std': std
            })
        results_df = pd.DataFrame(results).sort_values(by='std')
        validate_index, test_index = results_df.iloc[0]['b_index'], results_df.iloc[0]['c_index']
    else:
        validate_index, test_index = bc_index, []
    if progress_callback: progress_callback("Finding Optimal Split ..." ,100)

    train_index.sort()
    validate_index.sort()
    test_index.sort()
    return train_index, validate_index, test_index

def reindex(dataset_dir: str, progress_callback=None):
    """
    Reindexes the images in the dataset starting from 0 and update its 'coco_annotations.json' file.
    Args:
        dataset_dir (str): The dataset directory to be reindexed, that contains 'coco_data'.
    """
    coco_data_path = os.path.join(dataset_dir, "coco_data")
    image_path = os.path.join(coco_data_path, "images")
    annotated_image_path = os.path.join(coco_data_path, "annotated_images")

    img_paths =  glob.glob(image_path + "/*.jpg")
    img_paths.sort(key=lambda x: int(os.path.basename(x).split(".jpg")[0]))

    coco = COCO(os.path.join(coco_data_path, "coco_annotations.json"))
    img_annos = coco.dataset["images"]
    seg_annos = coco.dataset["annotations"]

    for i, img_path in enumerate(img_paths):
        if progress_callback: progress_callback("Re-indexing Annotations ..." , int(i/len(img_paths)*100))
        file_name = os.path.basename(img_path)
        old_id = int(file_name.split(".jpg")[0])
        new_file_name = str(i).zfill(6)+".jpg"
        if img_path == os.path.join(image_path, new_file_name):
            continue
        if os.path.exists(os.path.join(image_path, new_file_name)):
            shutil.copy(os.path.join(image_path, new_file_name), os.path.join(image_path, new_file_name+"_copy"))
        os.rename(img_path, os.path.join(image_path, new_file_name))

        for img_anno in img_annos:
            if img_anno["id"] == old_id:
                img_anno["id"] = i
                img_anno["file_name"] = "images/" + new_file_name
                img_anno["date_captured"] = ""

        for seg_anno in seg_annos:
            if seg_anno["image_id"] == old_id:
                seg_anno["image_id"] = i

    anno_img_paths =  glob.glob(annotated_image_path + "/*.png")
    anno_img_paths.sort(key=lambda x: int(os.path.basename(x).split(".png")[0].split('_')[-1]))

    for i, anno_img_path in enumerate(anno_img_paths):
        if progress_callback: progress_callback("Re-indexing Annotations ..." , int(i/len(img_paths)*100))
        file_name = os.path.basename(anno_img_path)
        prefix = '_'.join(file_name.split(".png")[0].split('_')[:-1])
        old_id = int(file_name.split(".png")[0].split('_')[-1])
        new_file_name = prefix + '_' + str(i)+".png"
        if anno_img_path == os.path.join(annotated_image_path, new_file_name):
            continue                                         
        if os.path.exists(os.path.join(annotated_image_path, new_file_name)):
            shutil.copy(os.path.join(annotated_image_path, new_file_name), os.path.join(annotated_image_path, new_file_name+"_copy"))
        os.rename(anno_img_path, os.path.join(annotated_image_path, new_file_name))

    new_coco_annotations = {
        "info": coco.dataset["info"],
        "licenses": coco.dataset["licenses"],
        "categories": coco.dataset["categories"],
        "images": img_annos,
        "annotations": seg_annos
    }

    with open(os.path.join(coco_data_path, "coco_annotations.json"), 'w', encoding='utf-8') as json_file:
        json.dump(new_coco_annotations, json_file)

def train_valid_test_split(dataset_dir: str, train_size: float=0.7,
                           valid_size: float=0.15, test_size: float=0.15,
                           max_iter: int=10000,
                           check_CANCEL=None, progress_callback=None):
    """
    Splits the dataset into 3 subsets of training, validation and testing.
    The sub-datasets will be saved as sub-directories in dataset folder.

    |---Dataset
        |---training
            |---coco_data
                |---coco_annotations.json
                |---images
                    |---00000.jpg
                    |---00002.jpg
                |---annotated_images
        |---validation
            |---coco_data
                |---coco_annotations.json
                |---images
                    |---00001.jpg
                |---annotated_images
        |---testing
            |---coco_data
                |---coco_annotations.json
                |---images
                    |---00003.jpg
                |---annotated_images
    Args:
        dataset_dir (str): The dataset directory to be splitted, that contains 'coco_data'.
        train_size (float, optional): Sum of train_size, valid_size and test_size should be 
                                      between 0.0 and 1.0 and represent the proportion of the 
                                      dataset to include in the split. Defaults to 0.7.
        valid_size (float, optional): Defaults to 0.15.
        test_size (float, optional): Defaults to 0.15.
    """
    def to_continue():
        if check_CANCEL:
            ret = check_CANCEL()
            return ret
        else:
            return "continue"
        
    if not to_continue(): return # check whether to continue

    train_index, validate_index, test_index = find_optimal_split(dataset_dir, train_size=train_size,
                                                                 valid_size=valid_size, test_size=test_size,
                                                                 max_iter=max_iter,
                                                                 progress_callback=progress_callback)
    
    if not to_continue(): return # check whether to continue
    if progress_callback: progress_callback("Splitting Images..." , 0)
    coco_data_dir = os.path.join(dataset_dir, "coco_data")
    images_dir = os.path.join(coco_data_dir, "images")
    train_dir = os.path.join(os.path.join(os.path.join(dataset_dir, "training"), "coco_data"), "images")
    os.makedirs(train_dir,exist_ok=True)  
    valid_dir = os.path.join(os.path.join(os.path.join(dataset_dir, "validation"), "coco_data"), "images")
    os.makedirs(valid_dir, exist_ok=True)  
    test_dir = os.path.join(os.path.join(os.path.join(dataset_dir, "testing"), "coco_data"), "images")
    os.makedirs(test_dir, exist_ok=True)

    files = glob.glob(train_dir+'/*')
    for f in files:
        os.remove(f)
    files = glob.glob(valid_dir+'/*')
    for f in files:
        os.remove(f)
    files = glob.glob(test_dir+'/*')
    for f in files:
        os.remove(f)

    img_files = [f for f in os.listdir(images_dir) if os.path.isfile(os.path.join(images_dir, f)) and ".jpg" in f]
    for i, file_name in enumerate(img_files):
        if not to_continue(): return # check whether to continue
        if progress_callback: progress_callback("Splitting Images..." ,int(i/len(img_files)*100))
        img_path = os.path.join(images_dir, file_name)
        _id = int(file_name.split(".jpg")[0])
        if _id in train_index:
            shutil.copy(img_path, os.path.join(train_dir, file_name))
        elif _id in validate_index:
            shutil.copy(img_path, os.path.join(valid_dir, file_name))
        elif _id in test_index:
            shutil.copy(img_path, os.path.join(test_dir, file_name))
    
    if progress_callback: progress_callback("Splitting Images..." , 100)

    if not to_continue(): return # check whether to continue
    if progress_callback: progress_callback("Splitting \'coco_annotations.json\'..." , 0)
    coco = COCO(os.path.join(coco_data_dir, "coco_annotations.json"))
    lists = [train_index, validate_index, test_index]
    dirs = [train_dir, valid_dir, test_dir]
    df = pd.read_csv(dataset_dir + "/class_sampling.csv", index_col=0)
    new_df = []
    for i, index_list in enumerate(lists):
        if not to_continue(): return # check whether to continue
        new_coco_annotations = {
            "info": coco.dataset["info"],
            "licenses": coco.dataset["licenses"],
            "categories": coco.dataset["categories"],
            "images": [],
            "annotations": []
        }

        for j, img_id in enumerate(index_list):
            if not to_continue(): return # check whether to continue
            if progress_callback: progress_callback("Splitting \'coco_annotations.json\'..." , int(j/len(index_list)*100))
            the_img_anno = [x for x in coco.dataset["images"] if x["id"]==img_id]
            new_coco_annotations["images"].extend(the_img_anno)
            annotations = [x for x in coco.dataset["annotations"] if x["image_id"]==img_id]
            for ann in annotations:
                ann["id"] = len(new_coco_annotations['annotations']) + 1
                new_coco_annotations["annotations"].append(ann)
        
        _coco_path = os.path.abspath(os.path.join(dirs[i], os.pardir))
        with open(os.path.join(_coco_path,"coco_annotations.json"), 'w', encoding='utf-8') as json_file:
            json.dump(new_coco_annotations, json_file)
        
        _df = df.iloc[index_list].copy()
        _df = _df.reset_index(drop=True)
        _df.index.name = df.index.name
        _dataset_dir = os.path.abspath(os.path.join(_coco_path, os.pardir))
        new_df.append(_df)
        _df.to_csv(os.path.join(_dataset_dir,'class_sampling.csv'), header=True)
    if progress_callback: progress_callback("Splitting \'coco_annotations.json\'..." , 100)

    if not to_continue(): return # check whether to continue
    # create split of annotated images if exists
    anno_images_dir = os.path.join(coco_data_dir, "annotated_images")
    if os.path.isdir(anno_images_dir):
        if progress_callback: progress_callback("Splitting Annotated Images..." , 0)
        anno_train_dir = os.path.join(os.path.join(os.path.join(dataset_dir, "training"), "coco_data"), "annotated_images")
        os.makedirs(anno_train_dir,exist_ok=True)  
        anno_valid_dir = os.path.join(os.path.join(os.path.join(dataset_dir, "validation"), "coco_data"), "annotated_images")
        os.makedirs(anno_valid_dir, exist_ok=True)  
        anno_test_dir = os.path.join(os.path.join(os.path.join(dataset_dir, "testing"), "coco_data"), "annotated_images")
        os.makedirs(anno_test_dir, exist_ok=True)

        img_files = [f for f in os.listdir(anno_images_dir) if os.path.isfile(os.path.join(anno_images_dir, f)) and ".png" in f] 

        for i, file_name in enumerate(img_files):
            if not to_continue(): return # check whether to continue
            if progress_callback: progress_callback("Splitting Annotated Images..." , int(i/len(img_files)*100))
            img_path = os.path.join(anno_images_dir, file_name)
            id = int(file_name.split(".png")[0].split('_')[-1])
            if id in train_index:
                shutil.copy(img_path, os.path.join(anno_train_dir, file_name))
            elif id in validate_index:
                shutil.copy(img_path, os.path.join(anno_valid_dir, file_name))
            elif id in test_index:
                shutil.copy(img_path, os.path.join(anno_test_dir, file_name))
    
    if progress_callback: progress_callback("Splitting Annotated Images..." , 100)

    if not to_continue(): return # check whether to continue

    if progress_callback: progress_callback("Re-indexing Annotations ..." , 0)
    for _dir in dirs:
        if not to_continue(): return # check whether to continue
        dataset_dir = os.path.abspath(os.path.join(os.path.abspath(os.path.join(_dir, os.pardir)), os.pardir))
        if progress_callback: progress_callback("Re-indexing {} ...".format(os.path.basename(dataset_dir)) , 0)
        reindex(dataset_dir, progress_callback=progress_callback)
    if progress_callback: progress_callback("Re-indexing Annotations ..." , 100)
    
    return True, new_df, lists

if __name__ == '__main__':
    Dataset_dir =  "/BlenderProc2/Dataset/Dataset_0"
    train_valid_test_split(Dataset_dir, train_size=0.7, valid_size=0.15, test_size=0.15)
