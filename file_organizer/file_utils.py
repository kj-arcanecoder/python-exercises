import json
import time
import shutil
import os
from datetime import datetime

category_filename = 'category_map.json'

def load_file_categories():
    try:
        with open(category_filename, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print("File not found")
        time.sleep(2)
        return {}
    except json.JSONDecodeError:
        print("Corrupted file, starting fresh.")
        time.sleep(2)
        return {}
    
def move_file(source_path, folder, dest_path, summary):
    if not os.path.exists(dest_path):
        print(f"Creating directory {dest_path}")
        os.makedirs(dest_path)
    shutil.move(source_path,dest_path)
    if folder in summary:
        summary[folder] += 1
    else:
        summary[folder] = 1
    log_activity(source_path, dest_path)

def log_activity(source_path, dest_path):
    with open('organizer_log.txt', 'a',encoding="utf-8") as f:
        current_time = t_date = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        f.write(f"{current_time}: Moved {source_path} -> {dest_path}\n")