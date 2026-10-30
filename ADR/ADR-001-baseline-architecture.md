---
id: ADR-001
title: Baseline Architecture
type: adr
status: accepted
version: v1.0
canonical: true
scope: carol-anne
audience:
  - developer
  - maintainer
created: "2026-10-30"
updated: "2026-10-30"
tags:
  - carol-anne
  - adr
  - architecture
  - baseline
provenance:
  - human
  - Claude Sonnet 5.5
---

# ADR-001: Baseline Architecture

## Status

Accepted

---

## 1. Context

Carol aNNe is a convolutional neural network (CNN) template for classification over small, fixed-format inputs, intended to run on hardware from microcontrollers to mobile devices. This ADR records the architecture at the start of the project, so that later ADRs can amend individual decisions against a defined baseline.

### Decision drivers

- Parameter and memory budgets that fit a microcontroller at the low end and a mobile device at the high end.
- A model small enough for a developer to read and modify in full.
- Inference cost that depends only on input size.
- Reported uncertainty: a classifier that states when its output should not be relied on.
- Local operation: inference and adaptation without network access, and without data leaving the device.

### Rationale

A CNN over a two-dimensional grid provides a locality prior and weight sharing at a low parameter count, and one feature extractor can serve audio spectrograms, images and signals rendered as grids. Global average pooling decouples the parameter count from the input extent. The baseline network exists as a trained implementation of 106,538 parameters (ten classes), which fixes the starting topology.

---

## 2. Decision

### §1 Model family and baseline topology

Carol aNNe is a CNN with no recurrent or attention components. The baseline topology, `CNNBaseline`, is:

| Stage | Specification |
|-------|---------------|
| Feature extractor | Four blocks of 3×3 convolution (padding 1), batch normalisation and ReLU, with 16, 32, 64 and 128 channels; 2×2 max pooling after blocks 1 to 3; global average pooling to 128 features |
| Classifier | Dropout (0.3), linear 128 → 64, ReLU, dropout (0.3), linear 64 → N classes |
| Size | 106,538 parameters at N = 10; each class adds 65 (the 64 weights and 1 bias of its output unit) |

### §2 Input representation

The input is a tensor of shape C × H × W. For audio, the front end produces a single-channel log-mel spectrogram from mono audio at 32 kHz (64 mel bands, FFT size 1024, hop 512), standardised per clip to zero mean and unit variance. Images and signals enter through front ends that produce the same grid form. The channel count C is a configuration parameter. Inputs of variable extent are accepted without cropping or padding at inference, because global average pooling removes the dependence on H and W. The minimum extent is 8 positions per axis, since three 2×2 poolings precede the global pooling; on the baseline, a width of 8 passes and a width of 7 fails.

### §3 Size family

Three configurations are built from one recipe: Nano, Micro and Standard. Each targets a hardware floor and also runs on larger hardware.

| Size | Indicative parameters | Hardware floor |
|------|-----------------------|----------------|
| Nano | 20,000 to 50,000 | Microcontroller |
| Micro | 100,000 to 300,000 | Single-board computer |
| Standard | 500,000 to 2,000,000 | Mobile device |

The parameter ranges are design targets, not measurements. This ADR does not fix how the sizes are scaled (channel width, block depth or both).

### §4 Output and uncertainty

The output is a softmax distribution over N classes. Besides a confident prediction, the system distinguishes four outcomes:

| Outcome | Condition |
|---------|-----------|
| Ambiguous | Two or more classes score closely |
| Low confidence | No class scores highly |
| Out of scope | The input lies outside the training distribution |
| Invalid | The input cannot be processed, for example because it is empty, corrupt or shorter than the minimum extent |

Confidence is calibrated after training on held-out data, so that a reported probability corresponds to observed accuracy. The method for detecting out-of-scope input (a threshold on calibrated confidence, a distance in feature space, or an explicit reject class) is not fixed by this ADR. The wording shown to a user is a presentation concern outside the model.

### §5 Adaptation

Adaptation is limited to corrections of the model's own predictions. The feature extractor stays frozen, and only classifier-level state (the classifier head or stored class prototypes) changes. Adaptation state is stored on the device and leaves it only when the user exports it; an export contains no raw input. Adding classes on the device is deferred beyond the baseline and may be addressed by a later ADR. Each correction must be individually reversible, the full state must be resettable to the shipped model, and confidence is recalibrated after adaptation.

### §6 Service interface and class vocabulary

Prediction is exposed by a stateless HTTP service (FastAPI):

| Endpoint | Behaviour |
|----------|-----------|
| `GET /` | Service information |
| `GET /health` | Service status, whether a checkpoint is loaded, and the class labels |
| `POST /predict` | Multipart file in; `{label, probs, filename}` out; `503` when no checkpoint is loaded |

The class vocabulary is a configuration value of each model: the developer chooses the number of classes and their labels, and the vocabulary is defined in one place per model and imported by the service, the classifier and the notebooks. At the baseline that place is the module `src/carol_anne/labels.py` (`N_CLASSES`, `LABELS`, `LABEL_TO_IDX`, `IDX_TO_LABEL`), which defines ten classes. The output width of the classifier follows from the class count, and a checkpoint stores the label list with the weights.

### §7 Toolchain and deployment

The implementation uses Python 3.12 and PyTorch, with dependencies locked by `uv`. Training and analysis run in notebooks. Deployment to the smaller targets requires an export path that does not depend on the PyTorch runtime or on the Python preprocessing. The export format is not fixed by this ADR.

### §8 Audience

The audience is developers who train, adapt and deploy the models. There is no end-user product. Calibration, rejection and adaptation are capabilities that a developer enables.

---

## 3. Consequences

### Positive

- At 106,538 parameters, the baseline can be understood in full, and its inference cost depends only on input size.
- One feature-extractor design serves all three input types.
- Local-only operation by default supports privacy requirements.
- A single label source per model prevents drift between the classifier, the service and the notebooks.
- The developer chooses the number of classes and the labels for each model, at a cost of 65 parameters per class.

### Negative

- The receptive field is limited. By calculation it spans 38 × 38 input positions, which is about 0.6 s of audio at the baseline front end, so tasks that depend on longer-range context are out of reach without a change of topology.
- Calibration, out-of-scope detection and adaptation need held-out data and evaluation work beyond training an ordinary classifier.
- The parameter ranges and hardware floors are unverified until each size is benchmarked on real devices.
- Microcontroller targets cannot run the current PyTorch model or the Python preprocessing, so both need an export path and a reimplemented front end.
- Front ends for images and signals do not yet exist.
- The sizing of the classifier head (128 → 64 → N) has not been evaluated for large class counts.

### Implementation notes

State of each element at the baseline:

| Element | State |
|---------|-------|
| Baseline network, audio preprocessing, trained checkpoint, HTTP service, label module | Implemented |
| Nano, Micro and Standard configurations | Template stems only (configuration, notebook, model card) |
| Per-model class count and labels | A module constant (`N_CLASSES = 10`) at the baseline; moving it into the per-model configuration is part of the configurable template |
| Front ends for images and signals | Not implemented |
| Calibration, out-of-scope detection, invalid-input handling | Not implemented |
| Adaptation from corrections | Not implemented |
| Export to a non-PyTorch runtime | Not implemented |
| Datasets for the pretrained examples | Not selected |

### Related

- ADR-000 (structure and conventions of this directory)
- README, section Status (phase plan)

---

## 4. Non-goals

- Tasks that depend on long-range temporal or spatial context, generative models, and open-vocabulary recognition.
- Retraining the feature extractor on the device.
- Transmitting user data off the device by default.
- An end-user application.

---

## 5. Amendment record

| Version | Date | Summary |
|---------|------|---------|
| v1.0 | 2026-10-30 | Initial baseline; accepted |
