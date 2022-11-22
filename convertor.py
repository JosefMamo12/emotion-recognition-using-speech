import os

import pydub.generators
from pydub import generators
from create_csv import write_emodb_csv as wec
from pydub import AudioSegment
from pydub.playback import play
import subprocess

e = ['disgust', 'sad', 'ps', 'happy', 'neutral', 'fear', 'angry', 'calm']

categories = {
    "W": "angry",
    "L": "boredom",
    "E": "disgust",
    "A": "fear",
    "F": "happy",
    "T": "sad",
    "N": "neutral"
}


def insert_manipulate(string, index):
    if index[1]:
        return string[:index[0] - 1] + '-manipulated' + string[index[0] - 1:]
    return 'manipulated_' + string


def index_finder(param):
    if param.find(e[0]) != -1:
        return [param.find(e[0]), True]
    elif param.find(e[1]) != -1:
        return [param.find(e[1]), True]
    elif param.find(e[2]) != -1:
        return [param.find(e[2]), True]
    elif param.find(e[3]) != -1:
        return [param.find(e[3]), True]
    elif param.find(e[4]) != -1:
        return [param.find(e[4]), True]
    elif param.find(e[5]) != -1:
        return [param.find(e[5]), True]
    elif param.find(e[6]) != -1:
        return [param.find(e[6]), True]
    elif param.find(e[7]) != -1:
        return [param.find(e[7]), True]
    elif param.find('W') != -1:
        return [param.find('W'), False]
    elif param.find('L') != -1:
        return [param.find('L'), False]
    elif param.find('E') != -1:
        return [param.find('E'), False]
    elif param.find('A') != -1:
        return [param.find('A'), False]
    elif param.find('F') != -1:
        return [param.find('F'), False]
    elif param.find('T') != -1:
        return [param.find('T'), False]
    elif param.find('N') != -1:
        return [param.find('N'), False]


def iterative_directory_sound_combiner(src_path, background_sound, volume_of_background=0):
    audio_seg_background = convert_to_audiosegment(background_sound)
    audio_seg_background += volume_of_background
    for subdir, dirs, files in os.walk(src_path):
        for file in files:
            if file.endswith('wav') and 'manipulated' not in file:
                path = os.path.join(subdir, file)
                str_sound = file.split('.')
                index = index_finder(str_sound[0])
                manipulated = insert_manipulate(str_sound[0], index)
                sound = convert_to_audiosegment(path)
                add_background_voices(sound, audio_seg_background, manipulated, subdir)


def convert_to_audiosegment(path):
    return AudioSegment.from_wav(path)


def add_background_voices(major_sound, background_sound, original_with_background, destination):
    combined = major_sound.overlay(background_sound)
    overlay_sound = combined.set_channels(1)
    overlay_sound.export(out_f=destination + '/' + original_with_background + ".wav", format='wav')


def iterative_directory_sound_convertor(path, ending_format):
    for subdir, dirs, files in os.walk(path):
        for file in files:
            filepath = subdir + os.sep + file
            if filepath.endswith('mp3'):
                split_word = str.split(file, '.')
                dest = split_word[0]
                convert(filepath, 'background/' + dest, ending_format)


def convert(src, dst, ending_format):
    subprocess.call(['ffmpeg', '-i', src, dst + '.' + ending_format])


# iterative_directory_sound_convertor('background', 'wav')


iterative_directory_sound_combiner('data/emodb', background_sound='background/jet-plane-flybyflac-14641.wav',
                                   volume_of_background=0)
