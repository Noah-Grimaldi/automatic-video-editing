import platform
import PySimpleGUI as sg
import subprocess
import os
from PIL import ImageColor
import matplotlib.font_manager as fm
import shutil

base64_image = b'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAMAAABEpIrGAAAAIGNIUk0AAHomAACAhAAA+gAAAIDoAAB1MAAA6mAAADqYAAAXcJy6UTwAAAH+UExURQAAAP87If87If87If87If87If87If87If87If87If87ISUjJFAlIe5sFiUjJCMgIfU5IP87If46IPI5IKszH7lxFf93Fv90Fv9xF+pbGsMzINQ2IaovH62jC//xANnNBZGID6yKEfmAE/d4FL9JG9s2IKaRDvPOA+/FBX5UF89EHe04IF9YFf/wAPjeAe/DBL2VENA/Iek6IH9bFv7wAPvlAcKeC7Z1Eug5IKNlFO3gAv7xAPniAfDTA8N6EYstIMyUDuvdAvPNBJF7EfZcGeE3IPmQEfnsAP7oAfjWAvC3B/C1B/CzCIYrIP49IP63Cv+7Cf++Cf/BCNjMBfvoAO/CBdWkCfxBH6EvH6+lC/faAr6bC/CJELkyIP9IL/5zFsi2B/zpAPTRA+m3C7tQKHVTT/7sAPDFBGtZFftJHvw8I/k6IIpCG9WtCHwtH5k7HczABvzsAO7CBYNsE+BYGbIxILUxIOc4IP6UEcq+B/3tAPjfAvjeAtzHBaOZDZZ7EIpDG/5AH+5IJFk/KzYyHaCWDfrjAfHKA3dEGtw/H+o4IU9JGP3sAOK7BquCENc1IO44IIpYGfvnAfnhAc6RDXEvHn9CHOLVBPTUA6yTDfVzFMw0IGknIOPRBPDJBFw8GuVBHtVaGcilCcKQDMEzIPlnGMGLDYU8HMYzIP///xk1TTUAAAARdFJOUwAMWp+/Hg+PLc/vBoP2ARovY7xO3wAAAAFiS0dEqScPBgQAAAAHdElNRQfnCw0WKRQEGPwCAAABjklEQVQ4y2NggANGJmYWQSBgYWZiZMAErMyCSICZFU2ajV0QDbCzIctzcApiAE4OJHkuuLCQMJzJxYFFXlBEVExcQlJKGlkFG5L5MrJyQCCvoKikrAK0BeIOJPepqslBgLqGphbIpWD/IeS1dUCSunJ6+gaGELeAfIvwv5ExSN7E1MzcAh4ewPBDGGBpJSdnbWNrZ4/kWUYGJjjbwREo7+Ts4oocGkwIG9xMwBa4e3h6efv4IuxggbL8/AMCg4JBSkJCw8LhJrAwIJsXEQlUEBUdE4skBlYQB2HHJ8jJJSYlp6BECZIJqWlAV6RnZGZhV5CdYy1nHZWbhx6pcEfmF8hZFxYVl5SWlSPLs8C8WVEJDISq6prauvoGZAXMsIBqbGpuabWWk2tr7+hEDSh4UHd1y8n19Pb1ozqBER5ZEybqTpo8ZSqaE5kR0T1t+oyZs2aj+4EVnmDmzJ03fwG6NCTBgJPcwkWLl2BIw5IcMNEuXbYcUxqRrLl5eFfgk2fg4xcgkHEIZz3CmRd39gcA0k9l8LbQyIEAAAAldEVYdGRhdGU6Y3JlYXRlADIwMjMtMTEtMTNUMjI6NDE6MjArMDA6MDC1A2E6AAAAJXRFWHRkYXRlOm1vZGlmeQAyMDIzLTExLTEzVDIyOjQxOjIwKzAwOjAwxF7ZhgAAACh0RVh0ZGF0ZTp0aW1lc3RhbXAAMjAyMy0xMS0xM1QyMjo0MToyMCswMDowMJNL+FkAAAAASUVORK5CYII='

def retrieve_available_fonts():
    system_fonts = fm.findSystemFonts(fontpaths=None, fontext='ttf')
    font_names = [os.path.splitext(os.path.basename(font))[0] for font in system_fonts]
    return font_names


def retrieve_available_colors():
    available_colors = list(ImageColor.colormap.keys())
    return available_colors


sg.theme('Black')
dropdown_options4 = [("center"), ("center", "top"), ("center", "bottom"), ("left", "top"), ("right", "top"),
                     ("left", "bottom"), ("right", "bottom")]
dropdown_options3 = retrieve_available_fonts()
dropdown_options2 = retrieve_available_colors()
dropdown_options = ["tiny", "base", "small", "medium", "large"]
# Define the layout of the GUI
layout = [
    [sg.InputText(key="video_file", disabled=True, default_text=r"Select a video file to edit *",
                  tooltip="The video you want to be edited", text_color='black'),
     sg.FileBrowse(file_types=(("Video Files", "*.mp4;*.avi;*.mkv;*.mov;*.wmv;*.flv;*.webm"),))],
    [sg.InputText(key="output_folder", default_text=r"Select an output folder", disabled=True,
                  tooltip="The folder where you want the edited video to export", text_color='black'),
     sg.FolderBrowse()],
    [sg.Text("Select model size: \n(smaller the model, quicker the export)"),
     sg.Drop(values=dropdown_options, background_color='white', key="dropdown_option", default_value="tiny",
             readonly=True, text_color='black',
             tooltip="It transcribes your video's audio with a model, by default it is tiny,\nyou can choose a larger model to make it more accurate at the\nexpense of taking longer")],
    [sg.Checkbox("Remove Silent Portions", key="option1",
                 tooltip="If selected, this option will cut out all detected silence from your video"),
     sg.Checkbox("Automatic Captions", key="option2",
                 tooltip="If selected, this option will automatically transcribe your\nvideo audio and place captions for every word on to the edited video")],
    [sg.Text("Adjust Silence Threshold:",
             tooltip="To remove silence, the program needs to know what\n volume is considered silence in your video, by default it is -50.")],
    [sg.Slider(range=(-100, 100), default_value=-50, orientation='h', size=(30, 10), trough_color="white",
               border_width=6, key='-THRESHOLD-',
               tooltip="To remove silence, the program needs to know what\n volume is considered silence in your video, by default it is -50.")],
    [sg.Text("Adjust Text color/size/position/font:")],
    [sg.Text("Color:    "),
     sg.Drop(values=dropdown_options2, background_color='white', key="dropdown_option2", default_value="white",
             readonly=True, text_color='black',
             tooltip="this is the text color that will overlay\non your edited video")],
    [sg.Text("Font:     "),
     sg.Drop(values=dropdown_options3, background_color='white', key="dropdown_option3", default_value="arial",
             size=(21, 1),
             readonly=True, text_color='black',
             tooltip="this is the font style for the overlay text")],
    [sg.Text("Position:"),
     sg.Drop(values=dropdown_options4, background_color='white', key="dropdown_option4",
             default_value=("center", "bottom"), size=(21, 1),
             readonly=True, text_color='black',
             tooltip="this is the position for the overlay text")],
    [sg.Text("Text Size:", tooltip="Adjust the size of the output overlay text")],
    [sg.Slider(range=(0, 200), default_value=100, orientation='h', size=(30, 10), trough_color="white",
               border_width=6,
               key='-SIZE-', tooltip="Font size/text size of overlay text")],
    [sg.Text('Loading . . .', key='loading_text', visible=False, text_color='yellow')],
    [sg.Button("Edit Video", visible=True, button_color=('white', 'green')),
     sg.Button("Cancel", visible=False, button_color=('white', 'darkred'))],
    [sg.Button("Output Folder", visible=False, button_color=('black', 'lightblue'))]
]
# Create the window
window = sg.Window("Automatic Video Editing", layout, icon=base64_image)
# Event loop
while True:
    event, values = window.read(timeout=5000)
    try:
        if dual_process.poll() is None:
            run_poll = True
        elif dual_process.poll() == 0:
            if run_poll:
                window['Edit Video'].update(visible=True)
                window['Cancel'].update(visible=False)
                window['loading_text'].update(visible=False)
                window['Output Folder'].update(visible=True)
                run_poll = False
                shutil.rmtree("output_images")
                os.remove("output_audio.wav")
    except:
        pass
    try:
        if caption_process.poll() is None:
            run_poll2 = True
        elif caption_process.poll() == 0:
            if run_poll2:
                window['Edit Video'].update(visible=True)
                window['Cancel'].update(visible=False)
                window['loading_text'].update(visible=False)
                window['Output Folder'].update(visible=True)
                run_poll2 = False
                shutil.rmtree("output_images")
                os.remove("output_audio.wav")
    except:
        pass
    try:
        if sub_process.poll() is None:
            run_poll3 = True
        elif sub_process.poll() == 0:
            if run_poll3:
                window['Edit Video'].update(visible=True)
                window['Cancel'].update(visible=False)
                window['loading_text'].update(visible=False)
                window['Output Folder'].update(visible=True)
                run_poll3 = False
                shutil.rmtree("output_images")
                os.remove("output_audio.wav")
    except:
        pass
    if event == "Output Folder":
        if values["output_folder"] == 'Select an output folder':
            output1 = os.path.dirname(values["video_file"])
        else:
            output1 = values["output_folder"]
        path_with_backslashes = output1.replace('/', '\\')
        subprocess.Popen(['explorer', path_with_backslashes])
    if event == sg.WINDOW_CLOSED:
        if os.path.exists("processing_config_file.txt"):
            os.remove("processing_config_file.txt")
        if os.path.exists("output_audio.wav"):
            os.remove("output_audio.wav")
        break
    if event == "Cancel":
        try:
            sub_process.kill()
        except:
            pass
        try:
            caption_process.kill()
        except:
            pass
        try:
            temp_file = open("processing_config_file.txt", 'w')
            temp_file.write("stop_process")
            temp_file.close()
        except:
            pass
        try:
            dual_process.kill()
        except:
            pass
        try:
            window['Edit Video'].update(visible=True)
            window['Cancel'].update(visible=False)
            window['loading_text'].update(visible=False)
            window['Output Folder'].update(visible=False)
            os.remove("output_audio.wav")
        except:
            pass
    elif event == "Edit Video":
        if values["output_folder"] == 'Select an output folder':
            output2 = os.path.dirname(values["video_file"])
        else:
            output2 = values["output_folder"]
        if values["video_file"] == "Select a video file to edit *" or (
                not values["option1"] and not values["option2"]):
            sg.popup("Please select a video file or editing style.", title="Error", icon="ERROR")
        else:
            video_file = values["video_file"]
            removeSilence = values["option1"]
            volume_low_adjuster = values["-THRESHOLD-"]
            volume_str = str(volume_low_adjuster)
            autoCaptions = values["option2"]
            dropdown_option = values["dropdown_option"]  # whisper model
            dropdown_option2 = values["dropdown_option2"]  # text color
            dropdown_option3 = values["dropdown_option3"]  # text font
            dropdown_option4 = values["dropdown_option4"]  # text position
            font_size = values["-SIZE-"]  # integer font size
            font_size = str(font_size)
            if removeSilence and autoCaptions:
                try:
                    dual_process = subprocess.Popen(
                        ["python", '-m', 'packagefiles.video_transcribe_audio',
                         video_file, "True", output2, dropdown_option,
                         dropdown_option2,
                         dropdown_option3, f'{dropdown_option4}', font_size, "True",
                         volume_str], creationflags=subprocess.CREATE_NO_WINDOW if platform.system() == 'Windows' else 0)
                except Exception as e:
                    sg.popup(e, title="Error", icon="ERROR")
            else:
                if removeSilence:
                    try:
                        sub_process = subprocess.Popen(
                            ['python', '-m', 'packagefiles.video_remove_silence', video_file, output2,
                             volume_str], creationflags=subprocess.CREATE_NO_WINDOW if platform.system() == 'Windows' else 0)
                    except Exception as e:
                        sg.popup(e, title="Error", icon="ERROR")
                else:
                    if autoCaptions:
                        try:
                            caption_process = subprocess.Popen(
                                ['python', '-m', 'packagefiles.video_transcribe_audio', video_file, "True",
                                 output2,
                                 dropdown_option, dropdown_option2, dropdown_option3, f'{dropdown_option4}',
                                 font_size], creationflags=subprocess.CREATE_NO_WINDOW if platform.system() == 'Windows' else 0)
                        except Exception as e:
                            sg.popup(e, title="Error", icon="ERROR")
            window['Output Folder'].update(visible=False)
            window['Edit Video'].update(visible=False)
            window['Cancel'].update(visible=True)
            window['loading_text'].update(visible=True)
window.close()
