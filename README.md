# `automaticVideoEditing`

This is a tool for editors that removes silent portions and adds automatic captions to your video file with a simple GUI.

## Usage

Run editorGUI.py, which programmatically references the other files.

**If you want to run the argparse files individually:**

For [video-remove-silence](video-remove-silence): `python video-remove-silence video_file output_directory adjust_silence_threshold`
adjust_silence_threshold is the decibal threshold that video-remove-silence considers as "silence." (avg. -40 or -50)

For [video_transcribe_audio.py](video_transcribe_audio.py): `python video_transcribe_audio.py video_file 'True' output_directory model_size text_color font position text_size`

model_size can be tiny, base, small, medium, large; text_color (e.g. white); font (e.g. Arial-Black or ''); position (e.g. ('center', 'bottom')); text_size (e.g. 80.0)

## Dependencies
`pip install -r requirements.txt`
- Python 3.5+
- FFmpeg

## Platform Support
This current program only works for windows 64-bit users, if you're on a different platform you need to change magick.exe to your version of magick.exe which you can [download here](https://imagemagick.org/script/download.php).
