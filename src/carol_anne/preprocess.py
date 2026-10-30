import numpy as np
import librosa

SR = 32000
SECONDS = 11.0

N_FFT = 1024
HOP_LENGTH = 512
N_MELS = 64


def load_clip(path, sr=SR, seconds=SECONDS):
    y, sr = librosa.load(path, sr=sr, mono=True)

    window = int(seconds * sr)

    rms = librosa.feature.rms(y=y, frame_length=N_FFT, hop_length=HOP_LENGTH)[0]
    loudest_frame = int(np.argmax(rms))
    center = loudest_frame * HOP_LENGTH

    start = center - window // 2
    if start < 0:
        start = 0
    if start + window > len(y):
        start = len(y) - window
    if start < 0:
        start = 0
    y = y[start:start + window]

    if len(y) < window:
        y = np.pad(y, (0, window - len(y)))

    return y


def logmel(y, sr=SR):
    mel = librosa.feature.melspectrogram(y=y, sr=sr, n_fft=N_FFT, hop_length=HOP_LENGTH, n_mels=N_MELS)
    mel_db = librosa.power_to_db(mel, ref=np.max)
    return mel_db
