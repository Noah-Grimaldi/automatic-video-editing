import os
import re
import ast
import subprocess
import argparse

from faster_whisper import WhisperModel
from moviepy.config import change_settings
from moviepy.editor import VideoFileClip, TextClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip

parser = argparse.ArgumentParser(description="Example with variable number of arguments")
parser.add_argument('args', nargs='+', help="One or more arguments")
args = parser.parse_args()
arguments = args.args

text_position = ast.literal_eval(arguments[6])
font_size_int = float(arguments[7])

if os.path.exists("processing_config_file.txt"):
    os.remove("processing_config_file.txt")
change_settings({"IMAGEMAGICK_BINARY": 'magick.exe'})
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
    text_clips = []
    for word in info[0][0]:
        start_time = word.start
        end_time = word.end
        word_text = re.sub(r'\W+', '', word.word)
        # Create a TextClip with the word and position it on the video
        text_clip = TextClip(word_text, fontsize=font_size_int, color=arguments[4], font=arguments[5])
        text_clip = text_clip.set_position(text_position)
        text_clip = text_clip.set_start(start_time)
        text_clip = text_clip.set_end(end_time)
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
            ['python', 'video-remove-silence', f"{outputFolder}{file_name_without_extension}_output.mp4",
             outputFolder, arguments[9]], creationflags=0x08000000)
        while process.poll() is None:
            if os.path.exists("processing_config_file.txt"):
                process.terminate()
                os.remove(f"{outputFolder}{file_name_without_extension}_output.mp4")
        os.remove(f"{outputFolder}{file_name_without_extension}_output.mp4")
except:
    pass
