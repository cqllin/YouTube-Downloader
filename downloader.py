from pytube import YouTube
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
                    url_value = values['-URL-']
                    dir_value = values['-DIRECTORY-']
                    if not url_value and not dir_value:
                        is_error = True
                        sg.popup_error("You must provide a URL to search, and a directory to save the video to!", title="Missing Values")
                    elif not url_value:
                        is_error = True
                        sg.popup_error("You must provide a URL to search!", title="Missing Values")
                    elif not dir_value:
                        is_error = True
                        sg.popup_error("You must select or provide a directory to save the video to!", title="Missing Values")
                    else:
                        done = False
                        is_okay = True
                        stream = get_stream(url_value)
                        thread = threading.Thread(target=download_thread, args=(stream, values['-DIRECTORY-']), daemon=True)
                        thread.start()

                except Exception as e:
                    print(e)
                    done = True
                    print("Error occurred fetching URL from user input.")
                    sg.popup_error("Please enter a valid YouTube URL.")

        while not done and is_okay:
            sg.popup_animated(sg.DEFAULT_BASE64_LOADING_GIF, 'Downloading', time_between_frames=30)
            time.sleep(.3)
            sg.popup_animated(image_source=None)
            window['-OUTPUT-'].update(f"{title} is finished downloading!")

        # print(f"You entered: {values[0]}")

    window.close()


def main():
    try:
        menu()
    except Exception as e:
        print("An error occurred with the program:", str(e))


if __name__ == "__main__":
    main()

