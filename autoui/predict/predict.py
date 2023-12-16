import torch
from PIL import Image, ImageDraw
import numpy as np
from ultralytics import YOLO

# Load the model
# model = torch.hub.load('ultralytics/yolov8', 'custom', path='models/best.pt')
model = YOLO('models/best.pt')  # pretrained YOLOv8n model

# Run batched inference on a list of images
# results = model(['im1.jpg', 'im2.jpg'])  # return a list of Results objects

# Load an image
image_path = 'images/3.jpg'
image = Image.open(image_path)

# Perform inference
results = model(image)

# Extract data
for result in results:
    boxes = result.boxes  # Boxes object for bbox outputs
    print(boxes)
    masks = result.masks  # Masks object for segmentation masks outputs
    keypoints = result.keypoints  # Keypoints object for pose outputs
    probs = result.probs  # Probs object for classification outputs

for r in results:
    im_array = r.plot()  # plot a BGR numpy array of predictions
    im = Image.fromarray(im_array[..., ::-1])  # RGB PIL image
    im.show()  # show image
    im.save('results.jpg')  # save image
# labels, cord = results.xyxyn[0][:, -1], results.xyxyn[0][:, :-1]

# # Draw bounding boxes and labels
# draw = ImageDraw.Draw(image)
# for label, (*xyxy,) in zip(labels, cord):
#     label = model.module.names[int(label)]  # Get label name
#     xyxy = (xyxy * np.array([image.width, image.height, image.width, image.height])).tolist()  # Scale coords
#     draw.rectangle(xyxy, outline='red', width=3)
#     draw.text(xyxy[:2], label, fill='red')

# Save or display image
# image.save('output/1.jpg')
# image.show()