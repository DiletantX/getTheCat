# GetTheCat

## Installation

- Download the YOLOv3 model
https://github.com/OlafenwaMoses/ImageAI/releases/download/3.0.0-pretrained/yolov3.pt

- Install dependencies for imageAI (GPU):

pip install cython pillow>=7.0.0 numpy>=1.18.1 opencv-python>=4.1.2 torch>=1.9.0 --extra-index-url https://download.pytorch.org/whl/cu102 torchvision>=0.10.0 --extra-index-url https://download.pytorch.org/whl/cu102 pytest==7.1.3 tqdm==4.64.1 scipy>=1.7.3 matplotlib>=3.4.3 mock==4.0.3

(cu101 is given as an example, you can change it to the most suitable CUDA version.)

Alternatively, install dependencies CPU as described in https://github.com/OlafenwaMoses/ImageAI

The project uses imageAI library, you can read more at https://github.com/OlafenwaMoses/ImageAI

-  Install other dependencies:

pip install imageai

pip install --upgrade setuptools wheel

pip install playsound

## Usage
Run python3.9 ReadFramesAndWorkWithLastFrame.py