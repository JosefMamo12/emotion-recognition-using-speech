import urllib.request
import re
import time
from random import random

import os

from pytube import YouTube
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import moviepy.editor


def creating_youtube_cuts(search_keyword="rihannaringtones", num=10):
    html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + search_keyword)
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    # print(video_ids)
    # print("https://www.youtube.com/watch?v=" + video_ids[0])
    for i in range(num):
        # print("https://www.youtube.com/watch?v=" + video_ids[i])
        link = "https://www.youtube.com/watch?v=" + video_ids[i]

        def download(link, i):
            youtube_object = YouTube(link)
            try:
                youtube_object = youtube_object.streams.get_highest_resolution()
            except:
                print("An error live has occurred")
            try:

                output = youtube_object.download()
                print("output before: " + output)

                os.rename(output, str(i) + ".mp4")

                print("output: " + output)

            except:
                print("An error has occurred")
            print("Download is completed successfully")

        download(link, i)

        video = moviepy.editor.VideoFileClip(str(i) + ".mp4")
        aud = video.audio
        aud.write_audiofile("audio " + str(i) + ".mp3")
        minit = int(random() * 35)
        max = minit + 1
        # ffmpeg_extract_subclip(str(i) + ".mp4", 20, 21, targetname="cut" + str(i) + ".mp4")
        ffmpeg_extract_subclip("audio " + str(i) + ".mp3", minit, max,
                               targetname="background/youtube/cut" + str(i) + ".mp3")


def delete_unnecessary_files():
    for i in range(10):
        try:
            os.remove(str(i) + ".mp4")
            os.remove("audio " + " " + str(i) + ".mp3")
        except:
            "cant delete because already in use"
        # os.system('ffmpeg -i {} -acodec pcm_s16le -ar 16000 {}/{}.wav'.format(filename, outdir, actual_filename))
        # youtube = etree.HTML(urllib.request.urlopen(link).read())   # to get the name of the video
        # video_title = youtube.xpath("/html/head/title")
        # text = (video_title[0].text)

        # os.rename(video_title[i].text, str(i) + ".mp4")
        # print(text)
        # print(text[0:-10])
        # name = text[0:-10]
        # name = re.sub('[\\:/?<>*".,]', '', name)
        # name = name + ".mp4"
        # print(name)
        # ffmpeg_extract_subclip(str(i)+".mp4", 20, 23, targetname="cut"+str(i)+".mp4")


if __name__ == '__main__':
    creating_youtube_cuts()
    delete_unnecessary_files()
