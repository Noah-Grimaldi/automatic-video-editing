# `automaticVideoEditing`

This is a tool for editors that removes silent portions and adds automatic captions to your video file with a simple GUI.

## Usage

Run editorGUI.py, which programmatically references the other files or [download the EXE](https://github.com/Noah-Grimaldi/automatic-video-editing/releases/download/pyinstaller/automatic-video-editing.exe).

**If you want to run the argparse files individually:**

For [video-remove-silence](video-remove-silence): 

```
python video-remove-silence video_file output_directory adjust_silence_threshold
```

adjust_silence_threshold is the decibal threshold that video-remove-silence considers as "silence." (avg. -40 or -50)

For [video_transcribe_audio.py](video_transcribe_audio.py): 

```
python video_transcribe_audio.py video_file 'True' output_directory model_size text_color font position text_size
```

model_size can be tiny, base, small, medium, large; text_color (e.g. white); font (e.g. Arial-Black or ''); position (e.g. ('center', 'bottom')); text_size (e.g. 80.0)

## Dependencies
`pip install -r requirements.txt`
- Python 3.5+
- FFmpeg

## Platform Support 
Windows/Mac/Linux

## Credits
Credit to @excitoon for [video-remove-silence](https://github.com/excitoon/video-remove-silence)
