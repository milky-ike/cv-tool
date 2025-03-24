# cv-tools

## Overview
The `cv-tools` script is designed to perform preprocessing on image and video data based on user-defined configurations.
It supports various preprocessing operations, including resizing, cropping, brightness adjustment, saturation control, rotation, and flipping.

## Prerequisites
Ensure that your system has one of the following Python versions installed:
- Python 3.10.x
- Python 3.11.x
- Python 3.12.x
- Python 3.13.x

Additionally, you will need `conda` for environment management and package installations.

## Installation

### 1. Clone the Repository
First, clone the repository to your local machine:
```bash
git clone https://github.com/milky-ike/cv-tool.git
cd cv-tool
```

### 2. Create and Activate a Conda Environment
Create a new conda environment with your desired Python version (e.g., Python 3.11):
```bash
conda create -n cv311 python=3.11
conda activate cv311
```

### 3. Install Dependencies
Install the necessary dependencies listed in `requirements.txt`:
```bash
pip install -r requirements.txt
```

After this, the tool will be ready to use.

## Usage

### Command Line Arguments
To run the preprocessing script, use the following command format:
```bash
python main.py [-h] [-t {image,i,video,v}] [-p PATH] [-c CONFIG] [-o OUTPUT]
```

#### Arguments:
- `-t, --type`: Specify the type of data: 'image' (i) or 'video' (v) (default: 'image')
- `-p, --path`: Path to the image or video files (default: `./assets`)
- `-c, --config`: Path to the configuration file (default: `./config.yaml`)
- `-o, --output`: Path to the output directory (default: `./result`)

#### Examples:
```bash
# Example 1: Process an image
python main.py -t i -p ./assets/teddybear.jpeg -c config.yaml -o ./result

# Example 2: Process a video
python main.py -t v -p ./assets/asakusa.mp4 -c config.yaml -o ./result
```

### Configuration File
The configuration file (`config.yaml`) defines the settings for preprocessing images and videos.
You can customize the file according to your needs.

#### Example `config.yaml`:
```yaml
# Example Image Settings
image_settings:
  cropped:
    enabled: true
    coordinates: [10, 20, 200, 180]  # [x1, y1, x2, y2]
  resize:
    enabled: true
    output_size: [300, 200]  # [width, height]
  brightness:
    enabled: true
    factor: 1.5  # Increase brightness by a factor of 1.5
  saturation:
    enabled: true
    factor: 0.8  # Decrease saturation by a factor of 0.8
  rotate:
    enabled: true
    angle: 1  # Rotate by 90 degrees (1 means 90°, 2 means 180°, etc.)
  flip:
    enabled: true
    options: horizontally  # Options: horizontally, vertically

# Example Video Settings
video_settings:
  cropped:
    enabled: true
    coordinates: [10, 20, 200, 180]
  resize:
    enabled: true
    output_size: [640, 480]
  brightness:
    enabled: true
    factor: 1.2
  saturation:
    enabled: true
    factor: 0.9
  rotate:
    enabled: true
    angle: 2  # Rotate by 180 degrees
  flip:
    enabled: true
    options: vertically
  preview: true  # Show preview during processing
  save_video: true  # Save the processed video
  save_image: true  # Save frames as images
```

### Run Unit Tests
To ensure everything is working correctly, you can run the unit tests with the following command:
```bash
python -m unittest discover -s test -p 'UT*.py'
```