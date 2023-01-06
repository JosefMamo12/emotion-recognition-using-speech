import os

import torchaudio
from speechbrain.pretrained import EncoderClassifier

classifier = EncoderClassifier.from_hparams(source="speechbrain/spkrec-xvect-voxceleb",
                                            savedir="pretrained_models/spkrec-xvect-voxceleb")
matches = ['M', 'manipulated', 'cut']
valid_check = ['test', 'validation']


def xvec_to_vec(src_path):
    vec_ret = []
    for subdir, dirs, files in os.walk(src_path):
        if any(x in subdir for x in valid_check):
            continue
        for file in files:
            if file.endswith('wav') and not any(x in file for x in matches):
                path = os.path.join(subdir, file)
                signal, fs = torchaudio.load(path)
                embeddings = classifier.encode_batch(signal)
                embeddings = embeddings.detach().cpu().numpy()
                embedding = embeddings[0][0]
                vec_ret.insert(embedding)
    return vec_ret


def one_to_xvec(path):
    signal, fs = torchaudio.load(path)
    embeddings = classifier.encode_batch(signal)
    embeddings = embeddings.detach().cpu().numpy()
    embedding = embeddings[0][0]
    return embedding