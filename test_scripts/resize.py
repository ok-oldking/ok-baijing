import cv2
import numpy as np
from matplotlib import pyplot as plt

#wget https://github.com/ultralytics/ultralytics/blob/796bac229eb5040159d7dff549f136f8c7e1c64e/ultralytics/assets/bus.jpg
img = cv2.imread("images/1.jpg")
print(img.shape) # (h,w,c) -> (1080, 810, 3)
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

original_aspect_ratio = img.shape[1] / img.shape[0]

new_size = (640, 640) # our new size
new_w = int(640 * original_aspect_ratio) # new width

print(f"new h,w : {new_h, new_w}") # -> new h,w : (640, 480)

# resize with OpenCV
img_new_shape = cv2.resize(img, (new_w, new_h))

# display our resized image
plt.imshow(cv2.cvtColor(img_new_shape, cv2.COLOR_BGR2RGB))