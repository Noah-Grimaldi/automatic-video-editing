import os
import re
import subprocess
import argparse
import ast
import platform
from pathlib import Path
venv_activate_script = Path("venv") / "Scripts" / "activate_this.py"
exec(open(str(venv_activate_script), "r").read(), dict(__file__=str(venv_activate_script)))

from PIL import Image, ImageDraw, ImageFont
from faster_whisper import WhisperModel
from moviepy.editor import VideoFileClip, ImageClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip

parser = argparse.ArgumentParser(description="Example with variable number of arguments")
parser.add_argument('args', nargs='+', help="One or more arguments")
args = parser.parse_args()
arguments = args.args


def create_text_image(text, output_path, fontstyle, fontsize, text_color):
    image_width = 600
    image_height = 300
    img = Image.new("RGBA", (image_width, image_height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    font_settings = ImageFont.truetype(fontstyle, fontsize)

    bbox = draw.textbbox((0, 0), text, font=font_settings)
    x = (image_width - (bbox[2] - bbox[0])) // 2
    y = (image_height - (bbox[3] - bbox[1])) // 2
    draw.text((x, y), text, fill=text_color, font=font_settings)
    img.save(output_path)


if os.path.exists("processing_config_file.txt"):
    os.remove("processing_config_file.txt")
outputFolder = arguments[2]
if arguments[1]:
    if arguments[2] == 'Select an output folder':
        outputFolder = ''
    else:
        outputFolder += '/'


    def convert_video_to_audio(video_path, audio_path):
        video = VideoFileClip(video_path)
        audio = video.audio
        audio.write_audiofile(audio_path)
        audio.close()


    video_file_path = arguments[0]
    video_clip = VideoFileClip(video_file_path)
    audio_file_path = 'output_audio.wav'
    convert_video_to_audio(video_file_path, audio_file_path)
    model_size = arguments[3]
    model = WhisperModel(model_size, device="cpu", compute_type="int8")
    segments, info = model.transcribe(audio_file_path, beam_size=5, word_timestamps=True)
    os.makedirs("output_images", exist_ok=True)
    text_clips = []
    for inner_list in info.word_info:
        for word in inner_list:
            start_time = word.start
            end_time = word.end
            word_text = re.sub(r'\W+', '', word.word)
            text_image_path = f"output_images/{word_text}.png"
            create_text_image(word_text, text_image_path, arguments[5], float(arguments[7]), arguments[4])

            image_clip = ImageClip(text_image_path, duration=end_time - start_time)
            text_clip = image_clip.set_start(start_time).set_end(end_time).set_position(ast.literal_eval(arguments[6]))
            text_clips.append(text_clip)
    # Composite the video with the text clips
    video_with_text = CompositeVideoClip([video_clip] + text_clips)
    # default video path name for output of export
    file_name = os.path.basename(video_file_path)
    file_name_without_extension = os.path.splitext(file_name)[0]
    # Export the final video
    video_with_text.write_videofile(f"{outputFolder}{file_name_without_extension}_output.mp4", codec='libx264',
                                    fps=video_clip.fps)
try:
    if arguments[8] == 'True':
        process = subprocess.Popen(
            ['python', '-m', 'packagefiles.video_remove_silence', f"{outputFolder}{file_name_without_extension}_output.mp4",
             outputFolder, arguments[9]], creationflags=subprocess.CREATE_NO_WINDOW if platform.system() == 'Windows' else 0)
        while process.poll() is None:
            if os.path.exists("processing_config_file.txt"):
                process.terminate()
                os.remove(f"{outputFolder}{file_name_without_extension}_output.mp4")
        os.remove(f"{outputFolder}{file_name_without_extension}_output.mp4")
except:
    pass
