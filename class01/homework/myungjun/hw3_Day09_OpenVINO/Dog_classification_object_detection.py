# 미완성 코드, ssd512 모델을 사용하려고 했으나 개를 인식하지 못한다는 문제 발생.

import os
import sys
from pathlib import Path
from typing import Tuple

import cv2
import numpy as np
import matplotlib.pyplot as plt
import openvino as ov

sys.path.append("../utils")
import notebook_utils as utils

# A directory where the model will be downloaded.
base_model_dir = Path("model")

# The name of the model from Open Model Zoo.
detection_model_name = "VGG_VOC0712Plus_SSD_512x512_iter_240000"
classification_model_name = ""
detection_model_path = (base_model_dir / "SSD_512x512" / detection_model_name).with_suffix('.xml')

print(detection_model_path)

# Initialize OpenVINO Runtime runtime.
core = ov.Core()


def model_init(model_path: str) -> Tuple:
    """
    Read the network and weights from file, load the
    model on the CPU and get input and output names of nodes

    :param: model: model architecture path *.xml
    :retuns:
            input_key: Input node network
            output_key: Output node network
            exec_net: Encoder model network
            net: Model network
    """

    # Read the network and corresponding weights from a file.
    model = core.read_model(model=model_path)
    compiled_model = core.compile_model(model=model, device_name="AUTO")
    # Get input and output names of nodes.
    input_keys = compiled_model.input(0)
    output_keys = compiled_model.output(0)
    return input_keys, output_keys, compiled_model


# de -> detection
# re -> recognition
# Detection model initialization.
input_key_de, output_keys_de, compiled_model_de = model_init(detection_model_path)
print(compiled_model_de)
# Recognition model initialization.
#input_key_re, output_keys_re, compiled_model_re = model_init(recognition_model_path)

# Get input size - Detection.
height_de, width_de = list(input_key_de.shape)[2:]
print(height_de, " & ", width_de)
# Get input size - Recognition.
#height_re, width_re = list(input_key_re.shape)[2:]


def plt_show(raw_image):
    """
    Use matplot to show image inline
    raw_image: input image

    :param: raw_image:image array
    """
    plt.figure(figsize=(10, 6))
    plt.axis("off")
    plt.imshow(raw_image)


# Load an image.
url = "https://storage.openvinotoolkit.org/repositories/openvino_notebooks/data/data/image/coco.jpg"
filename = "dog.jpg"
directory = "data"
image_file = utils.download_file(
    url, filename=filename, directory=directory, show_progress=False, silent=True,timeout=30
)
assert Path(image_file).exists()

# Read the image.
image_de = cv2.imread("data/dog.jpg")
# Resize it to [3, 256, 256].
resized_image_de = cv2.resize(image_de, (width_de, height_de))
# Expand the batch channel to [1, 3, 256, 256].
input_image_de = np.expand_dims(resized_image_de.transpose(2, 0, 1), 0)
print(input_image_de.shape)
# Show the image.
plt_show(cv2.cvtColor(image_de, cv2.COLOR_BGR2RGB))


# Run inference.
boxes = compiled_model_de([input_image_de])[output_keys_de]
#print(boxes[0][0][0])
# Delete the dim of 0, 1.
boxes = np.squeeze(boxes, (0, 1))
#print(len(boxes))
#print(boxes[0][1])
re_boxes = np.zeros(10)
for idx in range(len(boxes)):
    if boxes[idx][1] == 12.0:
        print(boxes[idx])
        re_boxes.append(boxes[idx])



#After squeezing: print(boxes[0][0][0]) == print(boxes[0])
# Remove zero only boxes.
#boxes = boxes[~np.all(boxes == 0, axis=1)]
#print(boxes[0])
#print(boxes)
        

def crop_images(bgr_image, resized_image, boxes, threshold=0.6) -> np.ndarray:
    """
    Use bounding boxes from detection model to find the absolute car position
    
    :param: bgr_image: raw image
    :param: resized_image: resized image
    :param: boxes: detection model returns rectangle position
    :param: threshold: confidence threshold
    :returns: car_position: car's absolute position
    """
    # Fetch image shapes to calculate ratio
    (real_y, real_x), (resized_y, resized_x) = bgr_image.shape[:2], resized_image.shape[:2]
    ratio_x, ratio_y = real_x / resized_x, real_y / resized_y

    # Find the boxes ratio
    boxes = boxes[:, 2:] 
    print(boxes)
    # Store the vehicle's position
    car_position = []
    # Iterate through non-zero boxes
    for box in boxes:
        # Pick confidence factor from last place in array
        conf = box[0]
        if conf > threshold:
            print(conf)
            # Convert float to int and multiply corner position of each box by x and y ratio
            # In case that bounding box is found at the top of the image, 
            # upper box  bar should be positioned a little bit lower to make it visible on image 
            (x_min, y_min, x_max, y_max) = [
                int(max(corner_position * ratio_y * resized_y, 10)) if idx % 2 
                else int(corner_position * ratio_x * resized_x)
                for idx, corner_position in enumerate(box[1:])
            ]
            
            car_position.append([x_min, y_min, x_max, y_max])
            
    return car_position

