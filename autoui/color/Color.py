import cv2


def calculate_color_percentage(image, box, color_ranges):
    # Extract the region of interest (ROI) using slicing
    roi = image[box.y:box.y + box.height, box.x:box.x + box.width, :3]

    # Create a mask for the pixels within the desired color range
    # color_ranges is expected to be a dictionary like: {'r': (10, 12), 'g': (10, 11), 'b': (13, 14)}
    mask = cv2.inRange(roi,
                       (color_ranges['b'][0], color_ranges['g'][0], color_ranges['r'][0]),
                       (color_ranges['b'][1], color_ranges['g'][1], color_ranges['r'][1]))

    # Calculate the percentage of pixels within the color range
    target_pixels = cv2.countNonZero(mask)
    total_pixels = roi.size / 3  # Divide by 3 for an RGB image
    percentage = (target_pixels / total_pixels) * 100
    return percentage
