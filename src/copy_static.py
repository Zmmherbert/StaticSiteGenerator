import os
import shutil

def copy_static(name=""):
    static_path = os.path.join(os.getcwd(), f"static/{name[name.find("/")+1:]}")
    dest_path = os.path.join(os.getcwd(), f"{name}")
    if os.path.exists(dest_path):
        shutil.rmtree(dest_path)
    os.mkdir(dest_path)

    for item in os.listdir(static_path):
        new_path = os.path.join(static_path, item)
        if os.path.isfile(new_path):
            shutil.copy(new_path, dest_path)
        elif os.path.isdir(new_path):
            copy_static(os.path.join(name, f"{item}/"))
        else:
            print("SOMETHING WENT WRONG")