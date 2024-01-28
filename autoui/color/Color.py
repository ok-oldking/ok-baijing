import cv2


def calculate_color_percentage(image, box, color_ranges):
    # Check if the ROI is within the image bounds
    if (box.x >= 0 and box.y >= 0 and
            box.x + box.width <= image.shape[1] and  # image.shape[1] is the width of the image
            box.y + box.height <= image.shape[0]):  # image.shape[0] is the height of the image

        # Extract the region of interest (ROI) using slicing
        roi = image[box.y:box.y + box.height, box.x:box.x + box.width, :3]

        # Create a mask for the pixels within the desired color range
        mask = cv2.inRange(roi,
                           (color_ranges['b'][0], color_ranges['g'][0], color_ranges['r'][0]),
                           (color_ranges['b'][1], color_ranges['g'][1], color_ranges['r'][1]))

        # Calculate the percentage of pixels within the color range
        target_pixels = cv2.countNonZero(mask)
        total_pixels = roi.size / 3  # Divide by 3 for an RGB image
        percentage = target_pixels / total_pixels
        return percentage
    else:
        # Return some error value or raise an exception
        # For example, return 0 or None
        return 0  # or None, or raise an exception
