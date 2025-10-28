from collections import defaultdict
import file_utils as file_utils
import os
import time

class FileOrganizer:
    def __init__(self, target_folder):
        self.target_folder = target_folder
        self.summary = defaultdict(list)

    def scan_files(self, target_dir):
        print("Scanning files...")
        all_entries = os.listdir(target_dir)
        dir_files = [name for name in all_entries if os.path.isfile(os.path.join(target_dir, name))]
        time.sleep(1)
        return dir_files


    def categorize_files(self, dir_list):
        categorized_files = defaultdict(list)
        print("Categorizing files...")
        for file_name in dir_list:
            if os.path.isdir(file_name):
                continue
            _, ext = os.path.splitext(file_name)
            ext = ext.lower().lstrip('.') or 'no_extension'
            categorized_files[ext].append(file_name)
        time.sleep(1)
        return categorized_files

    def move_files(self, categorized_files):
        print("Moving files...")
        category_map = file_utils.load_file_categories()
        self.check_categorized_files(categorized_files, category_map)  
        time.sleep(1)

    def check_categorized_files(self, categorized_files, category_map):
        for ext, file_names in categorized_files.items():
            for file_name in file_names:
                source_path = self.target_folder+"\\"+file_name 
                self.check_category_map(category_map, ext, source_path)

    def check_category_map(self, category_map, ext, source_path):
        for folder, values in category_map.items():
            dest_path = self.target_folder+"\\"+folder
            for value in values:
                value = value.lstrip('.')
                if ext == value:
                    file_utils.move_file(source_path, folder, dest_path, self.summary)

    def show_summary(self):
        if self.summary:
            print("\nFiles have been organized, here is the summary: \n")
            for folder, count in self.summary.items():
                print(f"Files moved to {folder} = {count}")
        else:
            print("\nNo files found to be moved.")
        print("\nThank you.")
        time.sleep(3)            
