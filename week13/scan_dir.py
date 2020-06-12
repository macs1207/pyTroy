import os
import json
import logging

PATH = "Ch07"
STATUS_PATH = "previous_status.txt"

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M',
                    handlers=[logging.FileHandler('update.log', 'a', 'utf-8'), ])

def get_previous_status():
    if os.path.exists(STATUS_PATH):
        previous_status = json.load(open(STATUS_PATH, "r"))
        return previous_status
    return None

def scan_dir(path):
    result = []
    if os.path.isdir(path):
        for name in os.listdir(path):
            fullpath = os.path.join(path, name)
            result += scan_dir(fullpath)
    else:
        result.append(path)
    return result

def compare_status(previous, current):
    result = {}
    for cur_file in current.keys():
        if cur_file in previous.keys():
            if current[cur_file][1] != previous[cur_file][1]:
                result[cur_file] = current[cur_file]
    return result
            

if __name__ == "__main__":
    file_status = {}

    for fn in scan_dir(PATH):
        file_status[fn] = (os.path.getsize(fn), os.path.getmtime(fn))

    previous_status = get_previous_status()

    diff = compare_status(previous_status, file_status)
    
    file_status_json = json.dumps(file_status)
    with open(STATUS_PATH, "w") as f:
        f.write(file_status_json)
    
    if diff:
        logging.info(json.dumps(diff))
    print(diff)
