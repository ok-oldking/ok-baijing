import cv2
import numpy as np

# Load images
full_image = cv2.imread('images/ba_char_list.png', cv2.IMREAD_COLOR)  # Target image
template = cv2.imread('images/ba_char_template.png', cv2.IMREAD_COLOR)  # Template image

w, h = template.shape[:-1]

# Perform template matching
res = cv2.matchTemplate(full_image, template, cv2.TM_CCOEFF_NORMED)

# Define a threshold for matching
threshold = 0.4
loc = np.where(res >= threshold)

# Draw rectangles around detected areas
for pt in zip(*loc[::-1]):  # Switch columns and rows
    cv2.rectangle(full_image, pt, (pt[0] + h, pt[1] + w), (0, 255, 0), 2)

# Show the result
cv2.imshow('Detected', full_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
