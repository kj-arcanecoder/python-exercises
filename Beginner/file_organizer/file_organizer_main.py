import os
import time
import organizer_core as core_organizer

def main():
    start_app()

def start_app():
    invalid_input = True
    while(invalid_input):
        os.system("cls")
        print("====================File Organizer====================\n")
        target_dir = input("Input target directory: ")
        try:
            if os.path.exists(target_dir):
                organize_folder(target_dir)
                invalid_input = False
            else:
                raise FileNotFoundError
        except(FileNotFoundError):
            print("Invalid path, try again.")
            time.sleep(1)

def organize_folder(target_dir):
    organizer = core_organizer.FileOrganizer(target_dir)
    dir_list = organizer.scan_files(target_dir)
    if dir_list:
        categorized_files = organizer.categorize_files(dir_list)
        organizer.move_files(categorized_files)
    organizer.show_summary()

if __name__=='__main__':
    main()