import os
import random
from pydub import AudioSegment
import convert_wavs
import wave

CHANNELS = 1
swidth = 2
Change_RATE = 1.25

matches = ['M', 'manipulated', 'cut', 'analyzed']
valid_check = ['test', 'validation', 'emodb']

emotions = ['positive', 'neutral', 'negative']


def speed_changer(path_in, subdir, file):
    """"
    this part we took from
    https://stackoverflow.com/questions/22755558/increase-decrease-play-speed-of-a-wav-file-python
    """
    spf = wave.open(path_in, 'rb')
    RATE = spf.getframerate()
    signal = spf.readframes(-1)
    str_sound = file.split('.')[0]
    index = index_finder(str_sound)
    manipulated = insert_manipulate(str_sound, index, '-manipulated-')
    old_path = f"{subdir}/{manipulated}.wav"

    wf = wave.open(old_path, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(swidth)
    wf.setframerate(RATE * Change_RATE)
    wf.writeframes(signal)
    wf.close()


def index_finder(param):
    if param.find(emotions[0]) != -1:
        return param.find(emotions[0])
    elif param.find(emotions[1]) != -1:
        return param.find(emotions[1])
    elif param.find(emotions[2]) != -1:
        return param.find(emotions[2])


def random_background(src_path, background_path, youtube_background, volume):
    background_counter = 0
    speed_counter = 0
    youtube_counter = 0
    for subdir, dirs, files in os.walk(src_path):
        if any(x in subdir for x in valid_check):
            continue
        for file in files:
            random_number = random.randint(1, 3)
            if file.endswith('wav'):
                if random_number == 1:
                    path = os.path.join(subdir, file)
                    duplicated_func(path, file, background_path, subdir, volume, '-manipulated-')
                    background_counter = background_counter + 1
                elif random_number == 2:
                    path = os.path.join(subdir, file)
                    speed_changer(path, subdir, file)
                    speed_counter = speed_counter + 1
                else:
                    path = os.path.join(subdir, file)
                    duplicated_func(path, file, youtube_background, subdir, volume, '-manipulated-')
                    youtube_counter = youtube_counter + 1
    return background_counter, speed_counter, youtube_counter


def convert_to_audiosegment(path, vol):
    audio = AudioSegment.from_wav(path)
    audio += vol
    return audio


def insert_manipulate(string, index, extra_string):
    return string[:index - 1] + extra_string + string[index - 1:]


def insert_manipulate2(string, index, extra_string) -> str:
    return string[:index] + extra_string + string[index:]


def add_background_voices(major_sound, background_sound, original_with_background, destination, count):
    combined = major_sound.overlay(background_sound)
    path = f"{destination}/{original_with_background}.wav"
    combined.export(out_f=path, format='wav')
    index = path.find("-manipulated-")
    new_path = insert_manipulate2(path, index, f'-converted{count}')
    convert_wavs.convert_audio(path, new_path, True)


def duplicated_func(path, file, background_path, subdir, volume, identify_str):
    str_sound = file.split('.')[0]
    index = index_finder(str_sound)
    manipulated = insert_manipulate(str_sound, index, identify_str)
    background_file = random.choice(os.listdir(background_path))  # Choose one of the backgrounds!
    audio_seg_background = convert_to_audiosegment(f"{background_path}/{background_file}", volume)
    sound = AudioSegment.from_wav(path)
    sound = sound + 15  # Adding volume to the main sound
    add_background_voices(sound, audio_seg_background, manipulated, subdir)


def dir_clean_manipulated():
    print('Cleaning all the manipulated wav files')
    for subdir, dirs, files in os.walk('data'):
        for file in files:
            if file.endswith('wav') and any(x in file for x in matches):
                path = os.path.join(subdir, file)
                os.remove(path)


if __name__ == '__main__':
    dir_clean_manipulated()
    background, speed, youtube = random_background("data", "background/random_background",
                                                   youtube_background="background/youtube", volume=-10)
    print(f"Background count: {background} SpeedChange count: {speed} Youtube count: {youtube}")
