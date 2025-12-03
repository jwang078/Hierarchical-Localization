from pathlib import Path

from hloc import (
    extract_features,
    match_features,
    reconstruction,
    visualization,
    pairs_from_retrieval,
)

import os
import subprocess

import gc

import argparse

def main(args):
    # 10/24/25 new bedford engine room visit
    video_path = Path(args.video_path)
    images = Path(args.images)
    num_matched = args.num_matched

    image_height = 540 # only used if video_path is converted in this notebook

    # Everything after the data/ folder prefix
    experiment_name = "_".join(images.parts[4:]) + f"_{num_matched}match" + f"_{image_height}height"
    outputs = Path("/home/jennyw2/code/Hierarchical-Localization/outputs/") / experiment_name

    print("Outputting to:", outputs)

    sfm_pairs = outputs / "pairs-netvlad.txt"

    # sfm_dir = outputs / "sfm_superpoint+superglue"
    # retrieval_conf = extract_features.confs["netvlad"]
    # feature_conf = extract_features.confs["superpoint_aachen"]
    # matcher_conf = match_features.confs["superglue"]

    sfm_dir = outputs / "sfm_disk_disk+lightglue" / "distorted"
    retrieval_conf = extract_features.confs["netvlad"]
    feature_conf = extract_features.confs["disk"]
    matcher_conf = match_features.confs["disk+lightglue"]

    print(video_path)
    print(images)
    print(outputs)

    if video_path is not None:
        # Create the directory
        os.makedirs(images, exist_ok=True)

        # Construct the command
        cmd = [
            "conda", "run", "--no-capture-output", "-n", "nerfstudio",
            "python", os.path.expanduser("~/code/nerf_dataset_preprocessing_helper/01_filter_raw_data.py"),
            "--input_path", video_path,
            "--output_path", images,
            "--target_count", "500",
            "--scalar", "3",
            "-y"
        ]

        # Run the command
        subprocess.run(cmd, check=True)
    else:
        print("Skipping video to image conversion because video_path is not provided")

    import os
    import subprocess

    resized_image_dir = images / "resized_images"
    os.makedirs(resized_image_dir, exist_ok=True)

    for fname in os.listdir(images):
        if fname.endswith(".jpg"):
            in_path = os.path.join(images, fname)
            out_path = os.path.join(resized_image_dir, f"{os.path.splitext(fname)[0]}.jpg")
            cmd = [
                "ffmpeg", "-y", "-i", in_path,
                "-vf", f"scale=-1:{image_height}",
                out_path
            ]
            subprocess.run(cmd, check=True)

    gc.collect()

    import shutil
    for f in images.glob("*.jpg"):
        f.unlink()  # delete unresized images
    for f in resized_image_dir.glob("*.jpg"): 
        shutil.move(str(f), images / f.name) # move resized images to the original locations
    shutil.rmtree(resized_image_dir)

    print("done")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--video_path", type=str, help="Example: /home/jennyw2/data/2025-10-24_new_bedford_engine_visit/GX010012_open_space/GX010012_open_space.MP4")
    parser.add_argument("--images", type=str, help="Example: /home/jennyw2/data/2025-10-24_new_bedford_engine_visit/GX010012_open_space/images_500")
    parser.add_argument("--num_matched", type=int, default=20, help="Number of images to match together for COLMAP; less than exhaustive search")
    args = parser.parse_args()
    main(args)