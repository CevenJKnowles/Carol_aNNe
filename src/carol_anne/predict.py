from carol_anne.labels import IDX_TO_LABEL
from carol_anne.models import cnn


def available():
    return cnn.available()


def predict(audio_bytes):
    if not cnn.available():
        raise FileNotFoundError("CNN checkpoint not found: " + str(cnn.MODEL_PATH))
    scores = cnn.run(audio_bytes)["scores"]

    probs = {}
    for i in range(len(scores)):
        probs[IDX_TO_LABEL[i]] = scores[i]

    best_label = max(probs, key=probs.get)
    return {"label": best_label, "probs": probs}
