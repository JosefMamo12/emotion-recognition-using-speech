import os
import convert_wavs
import numpy as np
import augmentation

positive_emotions = ['ps', 'happy']
neutral_emotions = ['calm', 'boredom']
negative_emotions = ['fear', 'disgust', 'sad', 'angry']

all_emo_combined = np.hstack((positive_emotions, neutral_emotions, negative_emotions)).ravel()

emotions = ['positive', 'neutral', 'negative']


def index_finder_for_change_emotions(file_name, param):
    return file_name.find(param)


def rename_files(file) -> str:
    file_name = file.split('.')[0]
    split_sentence = file_name.split('_')
    only_emotion = split_sentence[len(split_sentence) - 1]
    if any(x in only_emotion for x in positive_emotions):
        index = index_finder_for_change_emotions(file_name, only_emotion)
        new_file = file_name[:index] + 'positive'
        print("New file name: " + new_file + '\n')
    elif any(x in file_name for x in neutral_emotions):
        index = index_finder_for_change_emotions(file_name, only_emotion)
        new_file = file_name[:index] + 'neutral'
        print("New file name: " + new_file + '\n')
    else:
        index = index_finder_for_change_emotions(file_name, only_emotion)
        new_file = file_name[:index] + 'negative'
        print("New file name: " + new_file + '\n')
    return new_file


def emotion_changer():
    count = 0
    for subdir, dirs, files in os.walk('data'):
        if 'emodb' in subdir:
            continue
        for file in files:
            if file.endswith('.wav') and (
                    any(x in file for x in all_emo_combined) and not
            any(x in file for x in emotions)):
                original_path = os.path.join(subdir, file)
                subdir_path = os.path.join(subdir)
                new_path = subdir_path + '\\' + rename_files(file) + '.wav'
                if os.path.isfile(new_path):
                    new_path = subdir_path + '\\' + rename_files(str(count) + '_' + file) + '.wav'
                    convert_wavs.convert_audio(original_path, new_path, True)
                    count += 1
                else:
                    convert_wavs.convert_audio(original_path, new_path, True)


if __name__ == '__main__':
    emotion_changer()
