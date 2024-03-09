from pytube import YouTube
import os
from pathlib import Path


def dexit():
    print("Exit command received - Exiting program.")
    exit()


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


def download_video():
    qcmds = ["quit", "exit"]

    while True:
        target_dest = input("Where would you like the file to be downloaded? (ex /File/Path, Desktop, Documents, Downloads").lower()
        if target_dest in qcmds:
            dexit()
            break

        match_dest = fetch_directory(target_dest)
        if match_dest:
            print(f"Directory located! Files wll be downloaded to: {match_dest}")
            break
        else:
            print("The specified directory does not exist, or is not a valid directory. Please enter a valid directory.")

    while True:
        url = input("Enter the URL of the video you would like to download:")
        if url in qcmds:
            dexit()
            break
        try:
            video = YouTube(url)
            if not video:
                print("Invalid YouTube video URL! Unable to fetch. Please verify the URL and try again.")
            else:
                print("Fetched your video!")
                print(f"Title: {video.title}")
                print(f"Length: {video.length}")
                print(f"Publish Date: {video.publish_date}")
                break
        except Exception as e:
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





    # target_dest = input("Where would you like the file to be downloaded? (ex /File/Path, Desktop, Documents, Downloads").lower()
    # if target_dest == "quit" or target_dest == "exit":
    #     dexit()
    # else:
    #     match_dest = fetch_directory(target_dest)
    #     if match_dest:
    #         print(f"Directory located! Files wll be downloaded to: {match_dest}")
    #         # logic here
    #
    #         url = input("Enter the URL of the video you would like to download:")
    #         if url == "quit" or url == "exit":
    #             dexit()
    #         else:
    #             video = YouTube(url)
    #             if not video:
    #                 print("Invalid YouTube video URL! Unable to fetch. Please verify the URL and try again.")
    #                 download_video()
    #             else:
    #                 file_type = input("Enter the file type you would like to download the video as: (mp3, mp4)")
    #                 valid_types = ["mp3", "mp4"]
    #                 if not file_type in valid_types:
    #                     print("Invalid file type submitted. Please try again.")
    #                     download_video()
    #
    #     else:
    #         print("The specified directory does not exist, or is not a valid directory. Please enter a valid directory.")
    #         download_video()


def main():
    try:
        download_video()
    except Exception as e:
        print("An error occurred with the program:", str(e))


if __name__ == "__main__":
    main()
