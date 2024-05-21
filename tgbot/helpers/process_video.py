import threading
import io
from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip
from PIL import Image, ImageDraw
import numpy as np


def create_loading_bar(width, height, duration, output_file):
    # Создаем изображение с белой полоской загрузки
    img = Image.new("RGB", (width, height), color="black")
    draw = ImageDraw.Draw(img)
    bar_width = int(width * 0.2)  # Пример: полоска будет занимать 20% ширины
    bar_height = height
    top_offset = height / 2
    draw.rectangle([0, top_offset, bar_width, top_offset + bar_height], fill="white")

    # Создаем GIF-изображение из загруженного изображения
    clip = ImageClip(np.array(img))
    clip = clip.set_duration(duration)  # Устанавливаем продолжительность
    clip.write_gif(output_file, fps=12)


def add_progress_bar(clip):
    def make_frame(get_frame, t):
        frame = get_frame(t)
        img = Image.fromarray(frame)
        create_loading_bar(img.width, 30, clip.duration)
        # Resizing video
        target_resolution = (int(img.width / 2), int(img.height / 2))
        small_img = img.resize(target_resolution, Image.Resampling.LANCZOS)
        draw = ImageDraw.Draw(small_img)

        # Progress bar (white line) at the top of the video
        bar_width = small_img.width * (t / clip.duration)
        bar_height = 15
        top_offset = 30
        draw.rectangle([0, top_offset, bar_width, top_offset + bar_height], fill="white")

        return np.array(small_img)

    return clip.fl(make_frame)


def process_video(input_file, output_file):
    if input_file.endswith(('jpg', 'jpeg', 'png')):
        # Create a 5-second video clip from an image
        image_clip = ImageClip(input_file, duration=5)
        video_clip = image_clip.set_duration(5)
    else:
        # Upload the video and trim it to 5 seconds
        video_clip = VideoFileClip(input_file).subclip(0, 5)

    # Add progress animation
    video_with_progress = add_progress_bar(video_clip)

    # Save the result in GIF format
    video_with_progress.write_gif(output_file, fps=12)


# def process_video_in_thread(input_file, output_file):
#     video_thread = threading.Thread(target=process_video, args=(input_file, output_file))
#     video_thread.start()
#     return video_thread