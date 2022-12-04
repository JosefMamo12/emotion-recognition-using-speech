import os

import pydub.generators
from pydub import generators
from create_csv import write_emodb_csv as wec
from pydub import AudioSegment
from pydub.playback import play
import subprocess
import random

"""Emotions to recognize separated by a comma ',', available emotions are
"neutral", "calm", "happy" "sad", "angry", "fear", "disgust", "ps" (pleasant surprise)
and "boredom", default is "sad,neutral,happy"""

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
matches = ['M', 'manipulated','cut']
valid_check = ['test', 'validation', 'emodb']

positive_emotions = ['ps', 'happy']
neutral_emotions = ['calm', 'calm', 'boredom']
negative_emotions = ['fear', 'disgust', 'sad', 'angry']

emotions = ['positive', 'neutral', 'negative']


def insert_manipulate(string, index, extra_string='-manipulated-'):
    return string[:index - 1] + extra_string + string[index - 1:]


def index_finder(param):
    if param.find(emotions[0]) != -1:
        return param.find(emotions[0])
    elif param.find(emotions[1]) != -1:
        return param.find(emotions[1])
    elif param.find(emotions[2]) != -1:
        return param.find(emotions[2])


def rename_files(file) -> str:
    file_name = file.split('.')[0]
    if any(x in file_name for x in positive_emotions):
        index = index_finder(file_name)
        new_file = file_name[:index[0]] + 'positive'
        print("New file name: " + new_file + '\n')
    elif any(x in file_name for x in neutral_emotions):
        index = index_finder(file_name)
        new_file = file_name[:index[0]] + 'neutral'
        print("New file name: " + new_file + '\n')
    else:
        index = index_finder(file_name)
        new_file = file_name[:index[0]] + 'negative'
        print("New file name: " + new_file + '\n')
    return new_file


def emotion_changer():
    count = 0
    for subdir, dirs, files in os.walk('data'):
        if 'emodb' in subdir:
            continue
        for file in files:
            if file.endswith('.wav') and (
                    any(x in file for x in neutral_emotions) or (
                    any(x in file for x in positive_emotions)) or (
                            any(x in file for x in negative_emotions)) and not
                    any(x in file for x in emotions)):
                original_path = os.path.join(subdir, file)
                subdir_path = os.path.join(subdir)
                new_path = subdir_path + '\\' + rename_files(file) + '.wav'
                if os.path.isfile(new_path):
                    new_path = subdir_path + '\\' + rename_files(str(count) + '_' + file) + '.wav'
                    os.rename(original_path, new_path)
                    count += 1
                else:
                    os.rename(original_path, new_path)


def dir_clean_manipulated():
    print('Cleaning all the manipulated wav files')
    for subdir, dirs, files in os.walk('data'):
        for file in files:
            if file.endswith('wav') and any(x in file for x in matches):
                path = os.path.join(subdir, file)
                os.remove(path)


def random_background_cut(src_path, backgrounds_path, volume=0, manipulated_name='-cut-'):
    for subdir, dirs, files in os.walk(src_path):
        if any(x in subdir for x in valid_check):
            continue
        for file in files:
            if file.endswith('wav') and not any(x in file for x in matches):
                random_seed = random.randint(1, 3)
                if random_seed == 1:
                    path = os.path.join(subdir, file)
                    str_sound = file.split('.')[0]
                    background_file = random.choice(os.listdir(backgrounds_path))
                    background_audio = convert_to_audiosegment(backgrounds_path + '/' + background_file, volume)
                    index = index_finder(str_sound)
                    manipulated = insert_manipulate(str_sound, index=index, extra_string=manipulated_name)
                    sound = AudioSegment.from_wav(path)
                    add_background_voices(sound, background_audio, manipulated, subdir)


def one_background_voice_for_all(src_path, background_sound_path, volume_of_background=0,
                                 mixed_name='-manipulated', mixed=False):
    audio_seg_background = convert_to_audiosegment(background_sound_path, volume_of_background)
    for subdir, dirs, files in os.walk(src_path):
        if any(x in subdir for x in valid_check):
            continue
        for file in files:
            if file.endswith('wav') and not any(x in file for x in matches):
                path = os.path.join(subdir, file)
                str_sound = file.split('.')[0]
                index = index_finder(str_sound)
                manipulated = insert_manipulate(str_sound, index)
                sound = AudioSegment.from_wav(path)
                add_background_voices(sound, audio_seg_background, manipulated, subdir)


def convert_to_audiosegment(path, vol):
    audio = AudioSegment.from_wav(path)
    audio += vol
    return audio


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


random_background_cut('data', 'background/youtube', -2)
# iterative_directory_sound_convertor('background', 'wav')
# dir_clean_manipulated()
# emotion_changer()
#
# one_background_voice_for_all('data',
#                              background_sound_path='background/jet-plane-flybyflac-14641.wav',
#                              volume_of_background=-7)
