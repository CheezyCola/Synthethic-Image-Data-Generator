'''
A script to feed data by replacing text in a python script.
'''
import os
import errno

def feed_into_script(script_path: str, output_dir: str, data_variable: str, data):
    """Feeds data assigned to variable by replacing the line in a python script and 
    creates a copy of script.
    
    :param script_path: Python script to be modified by feeding data
    :param output_dir: Output directory to save the modified python script.
                       If output dir is same, the old script will be overwritten.
    :param data_variable: Data variable, which value is to be changed. 
                          Includes "=" and spacing for this function to locate the variable.
                          Example: "class_instance_num = "
    :param data: The data to feed to the script
    """
    if not os.path.isfile(script_path):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), script_path)

    with open(script_path, "r", encoding='utf-8') as f:
        content = f.readlines()

    file_name = os.path.basename(script_path)
    with open(os.path.join(output_dir, file_name), 'w', encoding='utf-8') as f:
        for line in content:
            if line.startswith(data_variable):
                line = data_variable + str(data) + "\n"
            f.write(line)
