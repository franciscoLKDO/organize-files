import os
import argparse
import re

def list_files(path):
    """
    List all files in a directory
    """
    files = []
    for file in os.listdir(path):
      if os.path.isfile(os.path.join(path,file)):
        files.append(file)
    return files

def group_files(path,files):
    """
    Group files into groups of group_size
    """
    groups = {}
    regex = "f([0-9].+)p"
    for file in files:
        result = re.search(regex, file)
        group_name = f"f{result.group(1)}"
        if group_name not in groups:
            groups[group_name] = []
        groups[group_name].append(os.path.join(path,file))
    return groups

def apply_directories(groups,output):
    """
    Apply directories to groups
    """
    for directory, files in groups.items():
      directory_path = os.path.join(output,directory)
      for file in files:
          os.makedirs(directory_path, exist_ok=True)
          os.rename(file,os.path.join(directory_path,os.path.basename(file)))

if __name__ == "__main__" :
    parser = argparse.ArgumentParser(prog='organize',
                                  formatter_class=argparse.RawDescriptionHelpFormatter,
                                  description='''\
    organize files into folders based on prefixes:
    -----------------------------
    ''')
    parser.add_argument('-p', '--path', help='path to the folder to organize', default=os.getcwd())
    parser.add_argument('-o', '--output', help='path to the output folder', default=os.getcwd())
    args = parser.parse_args()
    files = list_files(args.path)
    print(files)
    groups = group_files(args.path,files)
    print(groups)
    apply_directories(groups,args.output)
    print("Done")
