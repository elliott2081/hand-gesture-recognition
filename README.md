TRY THIS SHELL SCRIPT FIRST
#!/usr/bin/env bash
# setup_handgestures.sh
# Creates a Conda env named "handgestures" with all dependencies for
# hand-crop data collection and real-time gesture classification.

set -euo pipefail

ENV_NAME="handgestures"
PYTHON_VERSION="3.10"

echo
echo "🛠  Creating Conda environment '${ENV_NAME}' with Python ${PYTHON_VERSION}..."
conda create -n "${ENV_NAME}" python=${PYTHON_VERSION} -y

echo
echo "🔄  Activating environment..."
# shellcheck disable=SC1091
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate "${ENV_NAME}"

echo
echo "📦  Installing OpenCV from conda-forge..."
conda install -c conda-forge opencv -y

echo
echo "🔧  Installing MediaPipe (Apple Silicon wheel)..."
pip install mediapipe-silicon

echo
echo "⚙️  Installing TensorFlow for macOS + Metal acceleration..."
# Install low-level deps via apple channel
conda install -c apple tensorflow-deps -y
# Then install the runtime
pip install tensorflow-macos tensorflow-metal

echo
echo "🧰  Installing CVZone (wrappers for OpenCV+MediaPipe)..."
pip install cvzone

echo
echo "✅  All dependencies installed successfully!"
echo
echo "Next steps:"
echo "1. Activate the env:   conda activate ${ENV_NAME}"
echo "2. Verify imports:     python - <<EOF"
echo "import cv2, mediapipe, tensorflow, cvzone"
echo "print('OK!')"
echo "EOF"
echo "3. Place your model files under ./Model (keras_model.h5 + labels.txt)"
echo "4. Run your scripts:   python collect_data.py"
echo "                      python gesture_classifier.py"
echo


















to get the initial app runnning (dataCollection.py and test.py) 
Do the following for Mac OS 

1. Install Homebrew & Miniforge3
Install Homebrew:
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
Homebrew is the preferred way to install Miniforge for arm64 conda 

Install Miniforge3:


brew install miniforge


Miniforge3 from conda-forge has long-standing arm64 support, unlike standard Anaconda 

Initialize Conda for your shell:

conda init zsh

Restart your terminal or source ~/.zshrc to load conda commands. 

2. Create & Activate Conda Environment
Create an environment with Python 3.10:

conda create -n handgestures python=3.10
Python 3.12+ isn’t yet fully supported by MediaPipe on Silicon 


Activate it:

conda activate handgestures


3. Install OpenCV

conda install -c conda-forge opencv
OpenCV 4.x is available as a prebuilt package on conda-forge for arm64 


4. Install MediaPipe for Apple Silicon

pip install mediapipe-silicon
pip install "protobuf>=3.11,<4"


The mediapipe-silicon wheel is a drop-in replacement optimized for M1/M2 


5. Install TensorFlow-macOS & TensorFlow-Metal

conda install -c apple tensorflow-deps

Installs low-level deps for TensorFlow on Apple Silicon 

Install TensorFlow runtime:

python -m pip install tensorflow-macos tensorflow-metal

6. Install CVZone

pip install cvzone

7. Verify Installation

Run a quick Python check:

python
import cv2; print("OpenCV:", cv2.__version__)
import mediapipe; print("MediaPipe:", mediapipe.__version__)
import tensorflow as tf; print("TensorFlow:", tf.__version__)
import cvzone; print("CVZone:", cvzone.__version__)
