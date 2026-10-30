---
id: README
title: "Carol aNNe: a small convolutional neural network template"
type: overview
status: draft
version: v0.1
canonical: pending
scope: carol-anne
audience:
  - developer
  - maintainer
created: "2026-10-29"
updated: "2026-10-30"
tags:
  - carol-anne
  - overview
  - purpose
  - cnn
  - licence
maturity: alpha
provenance:
  - human
---

# Carol aNNe: a small convolutional neural network template

## Purpose

Carol aNNe is a small convolutional neural network, built from scratch and designed as a general template, so that a builder can read her from the first layer to the last, train her on their own audio, images or signals, and run her in one of three planned sizes: Nano from a microcontroller upward, Micro from a single-board computer upward and Standard on a mobile device.

## Design goals

At about 107,000 parameters (106,538 in the current version) she is small enough to be understood completely, so that the curious builder has something to read from end to end and the builder who already knows the task has a short path from a configuration file to a trained, exported model. Each model is fully trainable, can say when it is unsure, and gives an error message for bad input. It is open source, free and belongs fully to its owner, which underlines privacy, and it is made primarily to be altered to the developer's needs. Each model is to be published with its notebooks, benchmarks and tests as a public service, so that anyone can check what it does and reproduce it.

## What Carol aNNe is

| Component | Description |
|---|---|
| Architecture | `CNNBaseline`: four 3×3 convolution blocks (16, 32, 64 and 128 channels) with batch normalisation and ReLU, 2×2 max pooling after the first three, global average pooling, and a two-layer classifier head (128 → 64 → classes) with dropout of 0.3 |
| Parameters | 106,538 with ten output classes |
| Input | A single-channel, 64-band log-mel spectrogram (32 kHz, FFT size 1,024, hop 512), normalised per clip. The pooling makes the model independent of input length |
| Output | Softmax scores over the classes |
| Sizes | Nano, Micro and Standard: one recipe scaled by width and depth, with one configuration each |
| Input types | Audio, images and signals, selected by the number of input channels and the front end that builds the input grid |
| Behaviour | Calibrated confidence; reports when it is unsure and when an input lies outside what it was trained on |
| Adaptation | Learns from corrections by updating only the classifier head, locally by default |
| Interface | FastAPI service with `GET /`, `GET /health` and `POST /predict` |

## Status

Current phase: 2 of 5. Last updated 2026-10-30.

| Phase | Scope | Status |
|---|---|---|
| **1. Core network and service** | `CNNBaseline`, log-mel preprocessing, trained checkpoint, FastAPI prediction service | **Complete** |
| ◆ *Milestone* | *A from-scratch CNN of 106,538 parameters, served over an API* | *Reached* |
| **2. Configurable template** | One recipe with one configuration per size (Nano, Micro, Standard); input channels and front ends for audio, images and signals | **Current** |
| ◆ *Milestone* | *Three models built from one configuration, with published parameter counts and file sizes* | *Planned* |
| **3. Honest behaviour and adaptation** | Calibrated confidence, rejection of out-of-scope input, an error message for bad input, learning from corrections | Planned |
| ◆ *Milestone* | *Reliability and rejection results: a model that reports when it does not know* | *Planned* |
| **4. Pretrained examples** | Dataset selection; a signal example (Nano), an audio example (Micro) and an image example (Standard), each with a model card and tests | Planned |
| ◆ *Milestone* | *Three pretrained models with published accuracy, calibration and size across three input types* | *Planned* |
| **5. Deployment and release** | Export for a microcontroller, a single-board computer and a mobile device; benchmarks measured on real hardware; a web front end for the API (to be decided); public release of notebooks, benchmarks and tests | Planned |

## Repository layout

| Path | Contents |
|---|---|
| `src/carol_anne/` | The Python package: the CNN, preprocessing, prediction and a minimal API |
| `notebooks/` | The main model notebook, and one example notebook per size (`nano/`, `micro/`, `standard/`) |
| `configs/` | One configuration per size |
| `benchmarks/` | Benchmark reports per size |
| `tests/` | Code and behaviour tests |
| `ADR/` | Architecture decision records and their index (`ADR-NNN`) |
| `docs/architecture/` | Pipeline explanations (`DOC-ARCH-NNN`) |
| `docs/overview/` | Model cards (`DOC-OVW-NNN`) |
| `docs/diagrams/` | Diagram sources, rendered images and export scripts |
| `models/` | Trained checkpoints (not tracked in git) |

## Getting started

Requires [uv](https://docs.astral.sh/uv/) and Python 3.12.

```
git clone https://github.com/CevenJKnowles/Carol_aNNe.git
cd Carol_aNNe
uv sync
uv run uvicorn carol_anne.api:app
curl -X POST -F "file=@<PLACEHOLDER: path to a clip>" http://127.0.0.1:8000/predict
uv run python -m ipykernel install --user --name carol-anne --display-name "carol-anne"
```

| Command | Effect |
|---|---|
| `uv sync` | Creates `.venv` from `uv.lock` |
| `uv run uvicorn …` | Serves the API on port 8000, with interactive documentation at `/docs`. A checkpoint must exist at `models/cnn_baseline/cnn_baseline_best.pt`, otherwise `POST /predict` returns `503` |
| `curl …` | Sends one file to `POST /predict` and returns the label and per-class probabilities |
| `ipykernel install …` | Registers the `carol-anne` kernel the notebooks expect |

Paths inside the notebooks are written as `<PLACEHOLDER: …>` and must be filled in before a cell is run.

## Release and licences

Carol aNNe is released to the general public. The code is free, open-source software, and **each kind of content has its own licence**:

| Content | Licence | Terms |
|---|---|---|
| Code (the package, notebooks and scripts) | **Apache-2.0** | Completely free to use, modify and redistribute, with an explicit patent grant that ends for anyone who sues over the work. |
| Documentation (the README, ADRs, guides and write-ups) | **CC BY-NC 4.0** | Free and stays free. Anyone may use it as a template or for inspiration, with credit, but not sell it or use it commercially. Code samples that appear inside documents follow the code licence. |
| Third-party libraries and models | Their own | Not part of the repository; each keeps its own licence. See `NOTICE`. |

Copyright 2026 Ceven Jupiter Knowles.
