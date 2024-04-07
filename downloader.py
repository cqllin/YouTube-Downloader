from pytube import YouTube
from PySimpleGUI import FolderBrowse
import PySimpleGUI as sg
import pyperclip
import threading
import time
from moviepy.editor import *
import os
import re

done = False
streams = None
title = ''


def MP4toMP3(mp4, mp3):
    FILETOCONVERT = AudioFileClip(mp4)
    FILETOCONVERT.write_audiofile(mp3)
    FILETOCONVERT.close()


def download_thread(stream, file_path, window, convert_to_mp3=False):
    global done, title
    sanitized_title = re.sub(r'[<>:"/\\|?*]', '_', stream.title)
    title = sanitized_title.replace('/', '_').replace('\\', '_')
    original_extension = ".mp4" if "mp4" in stream.mime_type else ".webm"
    base_file_path = os.path.join(file_path, f"{title}{original_extension}")

    stream.download(output_path=file_path, filename=f"{title}{original_extension}")

    if convert_to_mp3 and "mp4" in stream.mime_type:
        mp3_file_path = f"{file_path}/{title}.mp3"
        try:
            MP4toMP3(base_file_path, mp3_file_path)
            window.write_event_value('Conversion Finished', title)
        except Exception as e:
            print(f"Error occurred in download_thread attempting to call convert function: {str(e)}")
    else:
        window.write_event_value('Download Finished', title)
    done = True


def get_clipboard_text():
    return pyperclip.paste()


def get_stream(url):
    yt = YouTube(url)
    if not yt:
        sg.popup_error(title='Download Error: Unable to fetch desired YouTube video! Please verify URL and try again.')

    streams = yt.streams
    audio_streams = streams.filter(only_audio=True)
    video_streams = streams.filter(only_video=True)

    layout = [[sg.Text(f'Choose Download Option - {yt.title}')]]
    stream_options = {}

    for i, s in enumerate(video_streams):
        layout += [[sg.Radio(f"Video - {s.resolution} {s.mime_type}", "STREAM", key=str(i))]]
        stream_options[str(i)] = (s, False)

    audio_index_offset = len(video_streams)
    for i, s in enumerate(audio_streams):
        key = str(audio_index_offset + i)
        layout += [[sg.Radio(f"Audio - {s.abr} {s.mime_type}", "STREAM", key=key)]]
        stream_options[key] = (s, False)

        if "mp4" in s.mime_type:
            mp3_key = f"mp3_{key}"
            layout += [[sg.Radio(f"Convert - {s.abr} MP4 to MP3", "STREAM", key=mp3_key)]]
            stream_options[mp3_key] = (s, True)

    layout += [[sg.Ok(), sg.Cancel()]]
    window = sg.Window('YouTube Downloader | Choose Download', layout)
    event, values = window.read(close=True)
    window.close()

    if event in (sg.WIN_CLOSED, 'Cancel'):
        return None, False

    for k, v in values.items():
        if v:
            selected_stream, convert_to_mp3 = stream_options[k]
            return selected_stream, convert_to_mp3

    return None, False


def menu():
    global done, title
    is_okay = False
    sg.theme('DarkGrey8')
    sg.theme_border_width(2)
    layout = [
        [sg.Text('', size=(1, 1))],
        [sg.Text('Video URL:', size=(17, 1), font=("Rubik", 13), tooltip='Your desired video URL'), sg.InputText(key='-URL-', size=(56, 2), pad=5, font=("Helvetica", 16)), sg.Button(button_text='Paste Clipboard', pad=5, size=(15, 1), font=("Helvetica", 11), key='-PASTE-')],
        [sg.HorizontalSeparator(color='white', pad=5)],
        [sg.Text('Download Directory:', size=(17, 1), font=("Rubik", 13)), sg.InputText(key='-DIRECTORY-', size=(56, 2), pad=5, font=("Helvetica", 16)), FolderBrowse(button_text="Browse Files", pad=5, size=(15, 1), font=("Helvetica", 11), key='-BROWSE-')],
        [sg.Text('', size=(1, 2))],
        [sg.Text(size=(50, 2), key='-OUTPUT-')],
        [sg.Button(button_text='Download', size=(12, 1), pad=5, font=("Helvetica", 14)), sg.Stretch(), sg.Button(button_text='Exit', size=(12, 1), pad=5, font=("Helvetica", 14))]
    ]

    window = sg.Window('YouTube Downloader', layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break

        match event:
            case '-PASTE-':
                clipboard_text = get_clipboard_text()
                window['-URL-'].update(clipboard_text)
            case 'Download':
                try:
                    url_value = values['-URL-']
                    dir_value = values['-DIRECTORY-']
                    if not url_value and not dir_value:
                        sg.popup_error("You must provide a URL to search, and a directory to save the video to!", title="Missing Values")
                    elif not url_value:
                        sg.popup_error("You must provide a URL to search!", title="Missing Values")
                    elif not dir_value:
                        sg.popup_error("You must select or provide a directory to save the video to!", title="Missing Values")
                    else:
                        done = False
                        stream, should_convert_to_mp3 = get_stream(url_value)
                        if stream:
                            is_okay = True
                            thread = threading.Thread(target=download_thread, args=(stream, values['-DIRECTORY-'], window, should_convert_to_mp3), daemon=True)
                            thread.start()
                        else:
                            is_okay = False

                except Exception as e:
                    done = True
                    print(f"Error occurred fetching URL from user input: {str(e)}")
                    sg.popup_error("Please enter a valid YouTube URL.")
            case 'Download Finished':
                window['-OUTPUT-'].update(f"{values[event]} is finished downloading!")
            case 'Conversion Finished':
                window['-OUTPUT-'].update(f"{values[event]} is finished being converted and has been downloaded.")

        while not done and is_okay:
            window['-OUTPUT-'].update(f"{title} is downloading...")
            sg.popup_animated(sg.DEFAULT_BASE64_LOADING_GIF, 'Downloading', time_between_frames=30)
            time.sleep(.3)
            sg.popup_animated(image_source=None)

        window.refresh()

    window.close()


def main():
    try:
        menu()
    except Exception as e:
        print("An error occurred with the program:", str(e))


if __name__ == "__main__":
    main()

