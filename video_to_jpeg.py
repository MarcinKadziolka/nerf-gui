import subprocess
import os

def video_to_jpegs(video_path, output_folder):
    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Use ffmpeg to convert the video to a series of JPEGs
    command = [
        'ffmpeg',
        '-i', video_path,          # Input file
        '-qscale:v', '2',          # Quality scale for JPEGs (lower is better quality)
        os.path.join(output_folder, '%03d.jpg')  # Output pattern
    ]

    subprocess.run(command, check=True)

if __name__ == "__main__":
    video_path = 'videos/fakes_nocrop.mp4'  # Replace with your video file path
    output_folder = 'mednerf_dataset/chest_nerfgan_aug_gen'  # Replace with your desired output folder

    video_to_jpegs(video_path, output_folder)
