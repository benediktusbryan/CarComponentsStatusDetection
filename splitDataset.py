import os
import shutil
import random

# Path asal dataset (6 folder)
SOURCE_DIR = "dataset"
TARGET_DIR = "dataset_fix"

SPLIT_RATIOS = [0.7, 0.2, 0.1]  # train, val, test

def split_dataset():
    for folder in os.listdir(SOURCE_DIR):
        folder_path = os.path.join(SOURCE_DIR, folder)
        if not os.path.isdir(folder_path):
            continue

        # List semua file gambar
        files = [f for f in os.listdir(folder_path) if f.lower().endswith((".png", ".jpg", ".jpeg"))]
        random.shuffle(files)

        n_total = len(files)
        n_train = int(n_total * SPLIT_RATIOS[0])
        n_val   = int(n_total * SPLIT_RATIOS[1])
        n_test  = n_total - n_train - n_val

        splits = {
            "train": files[:n_train],
            "val": files[n_train:n_train+n_val],
            "test": files[n_train+n_val:]
        }

        # Copy ke target folder
        for split_name, split_files in splits.items():
            split_folder = os.path.join(TARGET_DIR, split_name, folder)
            os.makedirs(split_folder, exist_ok=True)

            for f in split_files:
                src = os.path.join(folder_path, f)
                dst = os.path.join(split_folder, f)
                shutil.copy(src, dst)

        print(f"{folder}: {n_total} images → {n_train} train, {n_val} val, {n_test} test")

if __name__ == "__main__":
    split_dataset()