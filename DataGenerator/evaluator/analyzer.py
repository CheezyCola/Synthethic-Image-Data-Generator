'''
A script with functions to analyse dataset and visualize its characteristics.
'''
import os
import json
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

from pycocotools.coco import COCO

def collate_class_occlusion_level(dataset_dir: str, difficult_treshold: float = 20.0,
                                  progress_callback=None) -> None:
    """Collates object occlusion percentage from each image into class occlusion data.

    :param dataset_dir: a directory which holds 'coco_data'
    :param difficult_treshold: Occlusion percentage greater than this treshold will be considered difficult for learning task
    :param progress_callback: a class object that facilitates progress callback
    """
    coco_data_dir = os.path.join(dataset_dir, "coco_data")
    json_file = os.path.join(coco_data_dir, "coco_annotations.json")
    coco = COCO(json_file)

    new_coco_anno = coco.dataset.copy()
    categories = coco.dataset["categories"]
    for k, image in enumerate(coco.dataset["images"]):
        if progress_callback: progress_callback("Collating Object Occlusion Difficulty from Images ..." , int(k/len(coco.dataset["images"])*100))
        obj_occlusion_perc = image.get("object_occlusion")
        if obj_occlusion_perc:
            class_occlusion = {"Easy": {}, "Difficult": {}}
            name_list = [k.split(".")[0] for k in obj_occlusion_perc.keys()]
            id_list = [cat["id"] for name in name_list for cat in categories if cat["name"]==name]

            for i, (k, perc) in enumerate(obj_occlusion_perc.items()):
                if perc < difficult_treshold:
                    if class_occlusion["Easy"].get(id_list[i]):
                        class_occlusion["Easy"][id_list[i]]["no_of_instance"] += 1
                    else:
                        class_occlusion["Easy"][id_list[i]] = {"name": name_list[i], "no_of_instance": 1}
                else:
                    if class_occlusion["Difficult"].get(id_list[i]):
                        class_occlusion["Difficult"][id_list[i]]["no_of_instance"] += 1
                    else:
                        class_occlusion["Difficult"][id_list[i]] = {"name": name_list[i], "no_of_instance": 1}

            image.update({"class_occlusion": {"data": class_occlusion, "treshold": difficult_treshold}})

    with open(json_file, "w", encoding='utf-8') as f:
        json.dump(new_coco_anno, f)

def collect_occlusion_data(dataset_dir: str, progress_callback=None) -> dict:
    """Collect occlusion data from each image into a dictionary.

    :param dataset_dir: a directory which holds 'coco_data'
    :param progress_callback: a class object that facilitates progress callback
    """
    coco_data_dir = os.path.join(dataset_dir, "coco_data")
    json_file = os.path.join(coco_data_dir, "coco_annotations.json")
    coco = COCO(json_file)

    class_occlusion_dict_list = [x.get("class_occlusion") for x in coco.dataset["images"]]

    joined_occlussion_data = {}
    for k, class_occlusion_dict in enumerate(class_occlusion_dict_list):
        if progress_callback: progress_callback("Collecting Class Occlusion Difficulty from Images ..." ,
                                                int(k/len(class_occlusion_dict_list)*100))
        if not class_occlusion_dict:
            continue
        if joined_occlussion_data:
            for key, value in joined_occlussion_data.items():
                for k, v in class_occlusion_dict["data"][key].items():
                    if k in joined_occlussion_data[key]:
                        joined_occlussion_data[key][k]["no_of_instance"] = joined_occlussion_data[key][k]["no_of_instance"] + v["no_of_instance"]
                    else:
                        joined_occlussion_data[key][k] = v
        else:
            joined_occlussion_data = class_occlusion_dict["data"]

    return joined_occlussion_data

def visualize_class_occlusion(dataset_dir: str, difficult_threshold: float,
                              check_CANCEL=None, progress_callback=None) -> None:
    """Visualizes the difficulty caused by occlusion in dataset and saves the column chart. 

    :param dataset_dir: a directory which holds 'coco_data'
    :param difficult_treshold: Occlusion percentage greater than this treshold will be considered difficult for learning task
    :param check_CANCEL: function that checks cancel flag
    :param progress_callback: a class object that facilitates progress callback
    """
    def to_continue():
        if check_CANCEL:
            ret = check_CANCEL()
            return ret
        else:
            return "continue"
        
    if not to_continue(): return # check whether to continue
    if progress_callback: progress_callback("Collating Object Occlusion Difficulty from Images ..." , 0)
    collate_class_occlusion_level(dataset_dir, difficult_threshold, progress_callback)
    if progress_callback: progress_callback("Collating Object Occlusion Difficulty from Images ..." , 100)

    if not to_continue(): return # check whether to continue
    if progress_callback: progress_callback("Collecting Class Occlusion Difficulty from Images ..." , 0)
    class_occlusion_dict = collect_occlusion_data(dataset_dir, progress_callback)
    if progress_callback: progress_callback("Collecting Class Occlusion Difficulty from Images ..." , 100)

    if not to_continue(): return # check whether to continue
    if progress_callback: progress_callback("Visualizing Occlusion Difficulty in Dataset ..." , 0)
    __dict = {}
    for k,v in class_occlusion_dict.items():
        _dict = {}
        for k2,v2 in v.items():
            _dict[v2["name"]] = v2["no_of_instance"]
        __dict[k] = _dict

    df = pd.DataFrame(__dict)
    df = df.fillna(0)
    df = df.reset_index()
    df.rename(columns={'index': 'Name'}, inplace=True)
    df.index.name="Class"
    df.index = df.index.astype(int)
    df.index += 1
    df.sort_index(inplace=True)

    class_ids = df.index.to_list()
    class_names = df['Name'].to_list()
    class_labels = ["{} - {} ".format(x[0], x[1]) for x in zip(class_ids, class_names)]
    
    if not to_continue(): return # check whether to continue
    if progress_callback: progress_callback("Visualizing Occlusion Difficulty in Dataset ..." , 20)
    if df.empty:
        return
    # get the total for each row
    plot_df = df[['Easy', 'Difficult']]
    total = plot_df.sum(axis=1)
    # calculate the percent for each row
    per = plot_df.div(total, axis=0).mul(100).round(2)

    if not to_continue(): return # check whether to continue
    if progress_callback: progress_callback("Visualizing Occlusion Difficulty in Dataset ..." , 40)
    # plot the pivoted dataframe
    ax = plot_df.plot(use_index=True, kind='bar', stacked=True, figsize=(13, 9), rot=0,
                      title="Number of Instances by Class and Occlusion Difficulty with threshold {}%".format(difficult_threshold))
    # set the colors for each Class
    segment_colors = {'Easy': 'black', 'Difficult': 'red'}

    if not to_continue(): return # check whether to continue
    if progress_callback: progress_callback("Visualizing Occlusion Difficulty in Dataset ..." , 60)
    # iterate through the containers
    for c in ax.containers:
        # get the current segment label (a string); corresponds to column / legend
        label = c.get_label()
        # create custom labels with the bar height and the percent from the per column
        # the column labels in per and dfp are int, so convert label to int
        labels = [f'{int(v.get_height())}\n({row}%)' if v.get_height() > 0 else '' for v, row in zip(c, per[label])]
        # add the annotation
        ax.bar_label(c, labels=labels, label_type='center', fontweight='bold', color=segment_colors[label])

    mean = total.sum()/len(total)
    ax.axhline(mean, color='darkgreen', ls='--')
    ax.text(1, mean, f'mean: {mean:.3f}\n',ha='right',
            va='center', color='darkgreen', transform=ax.get_yaxis_transform())

    # move the legend
    class_handles = [Line2D([0], [0], c='k', marker='o', linestyle='') for x in class_labels]
    handles, labels = ax.get_legend_handles_labels()
    _ = ax.legend(handles=handles+class_handles, labels=labels+class_labels,
                  bbox_to_anchor=(1, 1.01), loc='upper left')
    
    plt.tight_layout()
    plt.savefig(os.path.join(dataset_dir, "class_occlusion.png"))

    if not to_continue(): return # check whether to continue
    if progress_callback: progress_callback("Visualizing Occlusion Difficulty in Dataset ..." , 80)
    # save csv
    df["Total"] = total
    df.to_csv(os.path.join(dataset_dir,'class_occlusion.csv'), header=True)

    if not to_continue(): return # check whether to continue
    if progress_callback: progress_callback("Visualizing Occlusion Difficulty in Dataset ..." , 100)
    return True, df, ax

if __name__ == '__main__':
    DIR = "/BlenderProc2/Dataset/Dataset_0"
    visualize_class_occlusion(DIR, difficult_threshold=15.0)
