"""
A script to generate images in a loop.
"""
from glob import glob
import os
import sys
import subprocess
from timeit import default_timer as timer
import pickle
import pandas as pd
sys.path.append("/BlenderProc2/DataGenerator")

from utility import sampler
from utility import feeder
from DataGenerator.utility.config import Config 
from renderer import dummy

def execute_command(cmd: list):
    """ Executes the command to run BlenderProc scripting

    :param cmd: the command-line text
    :return: True if the script is successful, False if failed and None if ended unexpectedly
    """
    p = subprocess.Popen(" ".join(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
    ret = None

    while True:
        out = p.stdout.readline()
        if out == '' and p.poll() is not None:
            break
        if out != '':
            if out.startswith("Successfull"):
                ret = True
            if out.startswith("Failed"):
                ret = False
            sys.stdout.write(out)
            sys.stdout.flush()
    return ret

def create_new_dataset_folder(base_dir: str):
    """ Creates new dataset folder in base_dir.

    :param base_dir: the directory that holds different dataset from generation.
    :return: the path to new dataset folder
    """
    folders = glob(base_dir + "/*", recursive = True)
    folders = [x for x in folders if not "coco_data" in x and "Dataset_" in os.path.basename(x)]
    if not folders:
        new_folder_path = os.path.join(base_dir, "Dataset_1")
    else:
        num = [int(os.path.basename(x).split('_')[-1]) for x in folders]
        new_num =  max(num) + 1
        new_folder_path = os.path.join(base_dir, "Dataset_"+str(new_num))
    
    os.makedirs(new_folder_path)
    return new_folder_path

def load_failed_images(data_file_path: str):
    """ Load the failed images stored in pickle file.

    :param data_file_path: pickle file containing a list of failed images
    :return: an empty list if file path not found and list of index of failed images if found
    """
    if not os.path.isfile(data_file_path):
        return []
    else:
        with open(data_file_path, 'rb') as f:
            failed_images = pickle.load(f)
        return failed_images

def generate_dataset(obj_dir = "/BlenderProc2/object/Ball Socket Head Screw",
                     gnd_dir = "/BlenderProc2/ground/tisch",
                     output_dir = "/BlenderProc2/Dataset",
                     config_file = "/BlenderProc2/Config/config.json",
                     num_of_images = 3,
                     min_occurences = 0,
                     max_occurences = 2,
                     total_occurences = 3,
                     new_Folder = True,
                     check_CANCEL = None,
                     progress_callback=None):
    """ Generate a dataset by running BlenderProc with python script in a loop.

    :param obj_dir: the directory that holds the objects .obj file and .mtl file
    :param gnd_dir: the directory that holds the ground .obj file with .mtl file
    :param output_dir: the output directory of the image generation
    :param config_file: the path to configuration file of the generation pipeline
    :param num_of_images: number of images in dataset
    :param min_occurences: min. occurrence of a class in each image of dataset
    :param max_occurences: max. occurrence of a class in each image of dataset
    :param total_occurences: total class instances per class in whole dataset
    :param check_CANCEL: function that checks cancel flag
    :param progress_callback: a class object that facilitates progress callback
    :return: a tuple of variables - (True if success, folder path, total time, failed images if any)
    """
    def to_continue():
        if check_CANCEL:
            ret = check_CANCEL()
            return ret
        else:
            return "continue"

    script = "/BlenderProc2/DataGenerator/renderer/main.py"
    cmd = ['blenderproc', 'run']

    if not to_continue(): return # check whether to continue
    CONF = Config.load_json(config_file)
    file_type = CONF.Object3D_loader.file_type
    if new_Folder:
        folder_path = create_new_dataset_folder(output_dir)
    else:
        folder_path = output_dir

    # sample class instances
    if not to_continue(): return # check whether to continue
    obj_dir = obj_dir.replace(os.sep, '/')
    obj_paths = glob(obj_dir + "/**/*" + file_type, recursive=True)
    classes = [os.path.basename(x).split('.')[0] for x in obj_paths]
    dict_list, start_index = sampler.random_instance_distribution(min_occurences, max_occurences,
                                                     num_of_images, total_occurences, classes,
                                                     folder_path)
    undone = [*range(0, len(dict_list), 1)]
    undone = [x+start_index for x in undone] 
    loop_start = timer()
    failed_imgs = load_failed_images(os.path.join(folder_path, "failed_imgs.pkl"))
    for i, __dict in enumerate(dict_list):
        start = timer()
        if not to_continue():
            return None, folder_path, 0, [*failed_imgs, *undone]
        if progress_callback: progress_callback("Generating {}/{} ...".format(start_index+i+1, len(dict_list)), int((i/len(dict_list))*100))
        feeder.feed_into_script(script, folder_path, "obj_dir = ", "\""+obj_dir+"\"")
        if not to_continue():
            return None, folder_path, 0, [*failed_imgs, *undone]
        script = os.path.join(folder_path, os.path.basename(script))
        feeder.feed_into_script(script, folder_path, "gnd_dir = ", "\""+gnd_dir+"\"")
        if not to_continue():
            return None, folder_path, 0, [*failed_imgs, *undone]
        feeder.feed_into_script(script, folder_path, "output_dir = ", "\""+folder_path+"\"")
        if not to_continue():
            return None, folder_path, 0, [*failed_imgs, *undone]
        feeder.feed_into_script(script, folder_path, "config_file = ", "\""+config_file+"\"")
        if not to_continue():
            return None, folder_path, 0, [*failed_imgs, *undone]
        feeder.feed_into_script(script, folder_path, "class_instance_num = ", __dict)
        
        # 2 trials
        for trial in range(2):
            if not to_continue():
                return None, folder_path, 0, [*failed_imgs, *undone]
            result = execute_command(cmd + [script])
            if result:
                break
            else:
                if trial == 1:
                    failed_imgs.append(start_index + i)
                    dummy.create_dummy(dataset_dir=folder_path,
                                       annotate_image=CONF.save_coco_annotated_image)
        end = timer()
        with open(os.path.join(folder_path,"time_stamp.txt"), "a") as myfile:
            myfile.write("Image {} -- {}s\n".format(start_index + i, end - start))
        
        undone.pop(0)

    if progress_callback: progress_callback("Generating ...", 100)
    loop_end = timer()
    
    total_time = loop_end - loop_start
    with open(os.path.join(folder_path,"time_stamp.txt"), "a") as myfile:
        myfile.write("Total time -- {}s\n".format(total_time))

    if failed_imgs:
        with open(os.path.join(folder_path, "failed_imgs.pkl"), 'wb') as f:
            pickle.dump(failed_imgs, f)
        
    return True, folder_path, total_time, failed_imgs

def generate_failed_imgs(dataset_dir = "/BlenderProc2/Dataset/Dataset_0",
                         gnd_dir = "/BlenderProc2/ground/tisch",
                         config_file = "/BlenderProc2/Config/BallSocketheadScrew_Tisch.json",
                         check_CANCEL = None,
                         progress_callback=None):
    """ Generates the failed images.

    :param dataset_dir: the dataset with failed images
    :param gnd_dir: the directory that holds the ground .obj file with .mtl file
    :param output_dir: the output directory of the image generation
    :param config_file: the path to configuration file of the generation pipeline
    :param check_CANCEL: function that checks cancel flag
    :param progress_callback: a class object that facilitates progress callback
    :return: a tuple of variables - (True if success, folder path, total time, failed images if any)
    """
    def to_continue():
        if check_CANCEL:
            ret = check_CANCEL()
            return ret
        else:
            return "continue"
    
    sampling_csv = os.path.join(dataset_dir, "class_sampling.csv")
    failed_imgs = load_failed_images(os.path.join(dataset_dir, "failed_imgs.pkl"))
    if not failed_imgs:
        return False, dataset_dir, 0, failed_imgs
    
    CONF = Config.load_json(config_file)
    script = "/BlenderProc2/DataGenerator/renderer/main.py"
    script = os.path.join(dataset_dir, os.path.basename(script))
    cmd = ['blenderproc', 'run']

    df = pd.read_csv(sampling_csv)
    if "Total instances per image" in df.columns:
        df = df.drop('Total instances per image', axis=1)

    _df = df.loc[df["image_id"].isin(failed_imgs)]
    _df.set_index('image_id',inplace=True)
    _df = _df.transpose()
    dict_list = _df.to_dict()
    
    loop_start = timer()
    failed_imgs = []
    undone = list(dict_list.keys())
    for i, (index, _dict) in enumerate(dict_list.items()):
        start = timer()
        if not to_continue(): 
            return None, dataset_dir, 0, [*failed_imgs, *undone]
        if progress_callback: progress_callback("Generating image {} ({}/{})...".format(index, i+1, len(dict_list)),
                                                int((i/len(dict_list))*100))
        feeder.feed_into_script(script, dataset_dir, "gnd_dir = ", "\""+gnd_dir+"\"")
        if not to_continue():
            return None, dataset_dir, 0, [*failed_imgs, *undone]
        feeder.feed_into_script(script, dataset_dir, "config_file = ", "\""+config_file+"\"")
        if not to_continue():
            return None, dataset_dir, 0, [*failed_imgs, *undone]
        feeder.feed_into_script(script, dataset_dir, "class_instance_num = ", _dict)
        
        # 3 trials
        for trial in range(3):
            if not to_continue():
                return None, dataset_dir, 0, [*failed_imgs, *undone]
            result = execute_command(cmd + [script])
            if result:
                dummy.replace_dummy_img_with_latest(dataset_dir=dataset_dir,
                                                annotate_image=CONF.save_coco_annotated_image,
                                                index=index)
                break
            else:
                if trial == 2:
                    failed_imgs.append(i)

        end = timer()
        with open(os.path.join(dataset_dir,"re_time_stamp.txt"), "a") as myfile:
            myfile.write("Image {} -- {}s\n".format(index, end - start))
        
        undone.pop(0)

    if progress_callback: progress_callback("Generating ...", 100)

    loop_end = timer()
    
    total_time = loop_end - loop_start
    with open(os.path.join(dataset_dir,"re_time_stamp.txt"), "a") as myfile:
        myfile.write("Total time -- {}s\n".format(total_time))

    os.remove(os.path.join(dataset_dir, "failed_imgs.pkl"))

    if failed_imgs:
        with open(os.path.join(dataset_dir, "failed_imgs.pkl"), 'wb') as f:
            pickle.dump(failed_imgs, f)
        
    return True, dataset_dir, total_time, failed_imgs
