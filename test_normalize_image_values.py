import os
import numpy as np
from PIL import Image
from tqdm import tqdm

folder = "/home/jennyw2/data/container_scan_videos_20250903/20250903_143514000_iOS/images_500"

for filename in tqdm(os.listdir(folder)):
    if filename.lower().endswith('.jpg'):
        img_path = os.path.join(folder, filename)
        img = Image.open(img_path)
        img_array = np.array(img)
        if img_array.max() > 255 or img_array.min() < 0:
            print("FILENAME", filename, "IS BAD", "min", img_array.min(), "max", img_array.max())
        # img = img.convert('RGB')
        # img_array = np.array(img).astype(np.float32) / 255.0  # Normalize to [0, 1]
        # img_normalized = Image.fromarray((img_array * 255).astype(np.uint8))
        # img_normalized.save(img_path)