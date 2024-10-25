"""
A script to randomize instance distribution of classes for a set of images.
"""
import os
import sys
import random
from typing import List, Dict
from functools import wraps
import pandas as pd

sys.setrecursionlimit(5000)  # Change the limit as needed

# Memoization decorator
def memoize(func):
    memo = {}
    @wraps(func)
    def wrapper(*args):
        if args in memo:
            return memo[args]
        result = func(*args)
        memo[args] = result
        return result
    return wrapper

@memoize
def p_count(n, m, my_max):
    if my_max * m < n:
        return 0
    if my_max * m == n:
        return 1

    if m < 2:
        return m
    if n < m:
        return 0
    if n <= m + 1:
        return 1

    n_iter = n // m
    count = 0

    for _ in range(n_iter):
        count += p_count(n - 1, m - 1, my_max)
        n -= m
        my_max -= 1
    return count

def unrank(n, m, my_max, nth):
    z = [0] * m
    count = 0
    j = 0

    for i in range(m):
        temp = p_count(n - 1, m - 1, my_max)

        while count + temp < nth and n - m > 0 and my_max > 0:
            count += temp
            n -= m
            my_max -= 1
            j += 1
            temp = p_count(n - 1, m - 1, my_max)

        m -= 1
        n -= 1
        z[i] = j
    return z

def restricted_partitions(min_val: int, max_val: int, N: int, sum_val: int, K: int):
    m = N
    n = sum_val - m * (min_val - 1)
    my_max = max_val - min_val + 1
    total_num = p_count(n, m, my_max)

    index_list = list(range(1, total_num + 1))
    rand_list = random.choices(index_list, k=K)

    result = []
    for i, index in enumerate(rand_list):
        z = unrank(n, m, my_max, index)
        z = random.sample(z, len(z))
        result.append(z)

    return [list(i) for i in zip(*result)]

def save_class_sampling_csv(list_of_dict: List[Dict], dest_dir: str) -> int:
    """Saves the distribution of class instances across images in a dataset into a csv.
    
    :param list_of_dict: List of dictionary of class instance distribution for each image in dataset
    :param dest_dir: The directory to save the csv 'class_sampling.csv'
    :return: starting index of the images in dataset
    """
    start_index = 0
    _classes = list_of_dict[0].keys()
    df = pd.DataFrame(list_of_dict, columns=_classes)
    df["Total instances per image"] = df.sum(axis=1, numeric_only=True)
    df.index.name = "image_id"
    
    os.makedirs(dest_dir, exist_ok=True)
    if os.path.exists(os.path.join(dest_dir,'class_sampling.csv')):
        old_df = pd.read_csv(os.path.join(dest_dir,'class_sampling.csv')).set_index('image_id')
        continue_index = len(old_df)
        start_index = continue_index
        df.index += continue_index
        df = pd.concat([old_df, df], ignore_index=False, sort=False)
    df.to_csv(os.path.join(dest_dir,'class_sampling.csv'), header=True)

    return start_index
    
def random_instance_distribution(min_inst_num_of_a_class_per_image: int,
                                 max_inst_num_of_a_class_per_image: int,
                                 number_of_images: int,
                                 sum_of_inst_per_class: int,
                                 class_in_images: List[str],
                                 dataset_dir: str) -> tuple:
    """Samples a random distribution of class instances for a balanced dataset.

    :param min_inst_num_of_a_class_per_image: min. num of occurrences of a class in an image
    :param max_inst_num_of_a_class_per_image: max. num of occurrences of a class in an image
    :param number_of_images: number of images in a dataset
    :param sum_of_inst_per_class: Sum of occurences of a class from all images in dataset
    :param class_in_images: List of class/category names
    :param dataset_dir: The directory that will hold the csv containing the sampling details 
                        and the 'coco_data' of synthetic generated images
    :return: List of dictionary of class instance distribution for each image in dataset and start index
    """
    res = restricted_partitions(min_inst_num_of_a_class_per_image,
                                max_inst_num_of_a_class_per_image,
                                number_of_images,
                                sum_of_inst_per_class,
                                len(class_in_images))

    dict_in_list = [dict(zip(class_in_images, x)) for x in res]
    start_index = save_class_sampling_csv(dict_in_list, dataset_dir)

    return dict_in_list, start_index

if __name__ == "__main__":
    classes = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l"]
    random_instance_distribution(0, 5, 750, 1000, classes, "DatasetXXX")
    