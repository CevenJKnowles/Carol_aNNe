"""Class labels, defined once and imported wherever they are needed.

To retarget the model, change N_CLASSES or replace LABELS with real names.
"""

N_CLASSES = 10
LABELS = [f"Class{i:02d}" for i in range(1, N_CLASSES + 1)]
LABEL_TO_IDX = {label: i for i, label in enumerate(LABELS)}
IDX_TO_LABEL = {i: label for label, i in LABEL_TO_IDX.items()}
