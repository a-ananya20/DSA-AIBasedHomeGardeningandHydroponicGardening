def clear_dir(folder_path):
    if os.path.exists(folder_path):
        for root, dirs, files in os.walk(folder_path, topdown=False):
            for name in files:
                try:
                    os.remove(os.path.join(root, name))
                except Exception as e:
                    print(f"❌ Error deleting file {name}: {e}")
            for name in dirs:
                try:
                    os.rmdir(os.path.join(root, name))
                except Exception as e:
                    print(f"❌ Couldn't delete directory: {name}. Reason: {e}")




import os
import shutil
import random

def split_data(source, train, val, split_size=0.8):
    for category in os.listdir(source):
        category_path = os.path.join(source, category)
        if not os.path.isdir(category_path):
            continue

        files = os.listdir(category_path)

        # ✅ Normalize to lowercase before checking file extensions
        files = [f for f in files if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        if len(files) == 0:
            print(f"⚠️ No image files found in: {category}")
            continue

        random.shuffle(files)

        split_index = int(len(files) * split_size)
        train_files = files[:split_index]
        val_files = files[split_index:]

        os.makedirs(os.path.join(train, category), exist_ok=True)
        os.makedirs(os.path.join(val, category), exist_ok=True)

        for file in train_files:
            shutil.copy(os.path.join(category_path, file), os.path.join(train, category))
        for file in val_files:
            shutil.copy(os.path.join(category_path, file), os.path.join(val, category))

        print(f"✅ Processed category: {category}, Train: {len(train_files)}, Val: {len(val_files)}")



source_dir = 'plant_disease_dataset/raw'
train_dir = 'plant_disease_dataset/dataset/train'
val_dir = 'plant_disease_dataset/dataset/val'

# Check original counts
raw_path = source_dir
for category in os.listdir(raw_path):
    category_path = os.path.join(raw_path, category)
    if os.path.isdir(category_path):
        images = [f for f in os.listdir(category_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        print(f"{category}: {len(images)} images")

# Split and copy
clear_dir(train_dir)
clear_dir(val_dir)
split_data(source_dir, train_dir, val_dir)
