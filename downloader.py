from pytube import YouTube
import os
from pathlib import Path
from PySimpleGUI import FolderBrowse
import PySimpleGUI as sg
import pyperclip
import threading
import time

done = False
streams = None
title = ''


def dexit():
    print("Exit command received - Exiting program.")
    exit()


def download_thread(stream, file_path):
    global done, title
    title = stream.title
    stream.download(file_path)
    done = True


def fetch_directory(directory_name):
    provided_dirs = ["desktop", "documents", "downloads"]
    if directory_name in provided_dirs:
        path = Path.home() / directory_name.capitalize()
        if path.exists() and path.is_dir():
            return path
        else:
            custom_path = Path(directory_name)
            if custom_path.exists() and custom_path.is_dir():
                return custom_path

        return None
    else:
        return None


def get_clipboard_text():
    return pyperclip.paste()


def get_stream(url):
    yt = YouTube(url)
    if not yt:
        sg.popup_error(title='Download Error: Unable to fetch desired YouTube video! Please verify URL and try again.')

    streams = yt.streams.all()

    layout = [[sg.Text('Choose Stream')]]
    for i, s in enumerate(streams):
        layout += [[sg.CB(str(s), key=i)]]

    layout += [[sg.Ok(), sg.Cancel()]]
    event, values = sg.Window('Choose Stream', layout).read(close=True)
    choices = [k for k in values if values[k]]
    if not choices:
        sg.popup_error("Error: You must choose a stream choice to download.")
        # exit()
    else:
        print(f"You chose {choices[0]}")
        print(streams[choices[0]])

    return streams[choices[0]]


def menu():
    global done, title
    sg.theme('DarkGrey8')
    sg.theme_border_width(2)
    layout = [
        [sg.Text('', size=(1, 1))],
        [sg.Text('Video URL:', size=(17, 1), font=("Rubik", 13), tooltip='Your desired video URL'), sg.InputText(key='-URL-', size=(56, 2), pad=5, font=("Helvetica", 16)), sg.Button(button_text='Paste Clipboard', pad=5, size=(15, 1), font=("Helvetica", 11), key='-PASTE-')],
        [sg.HorizontalSeparator(color='white', pad=5)],
        [sg.Text('Download Directory:', size=(17, 1), font=("Rubik", 13)), sg.InputText(key='-DIRECTORY-', size=(56, 2), pad=5, font=("Helvetica", 16)), FolderBrowse(button_text="Browse Files", pad=5, size=(15, 1), font=("Helvetica", 11), key='-BROWSE-')],
        [sg.Text('', size=(1, 2))],
        [sg.Text(size=(50, 2), key='-OUTPUT-')],
        [sg.Button(button_text='Download', size=(12, 1), pad=5, font=("Helvetica", 14)), sg.Stretch(), sg.Button(button_text='Exit', size=(12, 1), pad=5, font=("Helvetica", 14), key='-DOWNLOAD-')]
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
                    stream = get_stream(values['-URL-'])
                    done = False
                    thread = threading.Thread(target=download_thread, args=(stream, values['-DIRECTORY-']), daemon=True)
                    thread.start()

                except:
                    done = True
                    print("Error occurred fetching URL from user input.")
                    sg.popup_error("Please enter a valid YouTube URL.")

        while not done:
            sg.popup_animated(sg.DEFAULT_BASE64_LOADING_GIF, 'Downloading', time_between_frames=30)
            time.sleep(.3)
            sg.popup_animated(image_source=None)
            window['-OUTPUT-'].update(f"{title} is finished downloading!")

        # print(f"You entered: {values[0]}")

    window.close()


def main():
    try:
        # download_video()
        menu()

#        layout = [[sg.Text('URL', size=(20, 1)), sg.InputText(key='-URL-') ],
#                  [sg.Text('Download Directory', size=(20, 1)), sg.InputText(key='-DIRECTORY-'),
#                   FolderBrowse(button_text="Browse", key="-BROWSE-")],
#                  [sg.Text(size=(50, 2), key='-OUTPUT-')],
#                  [sg.Button('Download'), sg.Button('Exit')]]
#
#        window = sg.Window('YouTube Downloader', layout)
#
#        while True:
#            event, values = window.read()
#
#            match event:
#                case sg.WIN_CLOSED | 'Exit':
#                    break
#                case _:
#                    print('Unknown Event')



    except Exception as e:
        print("An error occurred with the program:", str(e))


if __name__ == "__main__":
    main()


    def download_video():
        qcmds = ["quit", "exit"]
        video = None

        while True:
            target_dest = input(
                "Where would you like the file to be downloaded? (ex /File/Path, Desktop, Documents, Downloads").lower()
            if target_dest in qcmds:
                dexit()
                break

            match_dest = fetch_directory(target_dest)
            if match_dest:
                print(f"Directory located! Files wll be downloaded to: {match_dest}")
                break
            else:
                print(
                    "The specified directory does not exist, or is not a valid directory. Please enter a valid directory.")

        while True:
            url = input("Enter the URL of the video you would like to download:")
            if url in qcmds:
                dexit()
                break
            try:
                print(url)
                video = YouTube(url)
                print(video)
                if not video:
                    print("Invalid YouTube video URL! Unable to fetch. Please verify the URL and try again.")
                else:
                    print("Fetched your video!")
                    print(f"Title: {video.title}")
                    print(f"Length: {video.length}")
                    print(f"Publish Date: {video.publish_date}")
                    break
            except Exception as e:
                print(e)
                print("Invalid YouTube video URL! Unable to fetch. Please verify the URL and try again.")

        while True:
            valid_types = ["mp3", "mp4"]
            file_type = input("Enter the file type you would like to download the video as: (mp3, mp4)")
            if file_type in qcmds:
                dexit()
                break

            if file_type not in valid_types:
                print("Invalid file type submitted. Please try again.")
            else:
                break

        print(video.streams)

class YouTubeSearch():
    def __init__(self, title='', length=0, publish_date=''):
        self.title = title
        self.length = length
        self.publish_date = publish_date

