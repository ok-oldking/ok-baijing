import cv2
import numpy as np

def filter_and_sort_matches(result, width, height, threshold):
    # Filter matches based on the threshold
    loc = np.where(result >= threshold)

    # Zip the locations into a list of tuples and sort by threshold in descending order
    matches = sorted(zip(*loc[::-1]), key=lambda p: result[p[::-1]], reverse=True)

    # Filter out overlapping matches
    unique_matches = []
    for pt in matches:
        if all(not (pt[0] >= m[0] - width and pt[0] <= m[0] + width and
                    pt[1] >= m[1] - height and pt[1] <= m[1] + height)
                for m in unique_matches):
            unique_matches.append(pt)
    
    print(f"result {len(result)} loc {loc} matches {len(matches)} unique_matches {len(unique_matches)}")
    return unique_matches
# Load images
main_image = cv2.imread('images/test.jpg')  # Replace with your main image file
template = cv2.imread('images/button_f.jpg')  # Replace with your template image file
h, w = template.shape[:2]

# Template matching
method = cv2.TM_CCOEFF_NORMED
result = cv2.matchTemplate(main_image, template, method)

# Define a threshold
threshold = 0.8  # You might need to adjust this threshold
filter_and_sort_matches(result,template.shape[1],template.shape[0],threshold)
# Find where the matching result exceeds the threshold
locations = np.where(result >= threshold)
locations = list(zip(*locations[::-1]))  # Swap and group x, y locations
print(f"result {len(result)}, locations {len(locations)}")

# Draw rectangles and annotate confidence scores
for loc in locations:
    bottom_right = (loc[0] + w, loc[1] + h)
    cv2.rectangle(main_image, loc, bottom_right, (0, 255, 0), 2)
    cv2.putText(main_image, f'{result[loc[1], loc[0]]:.2f}', (loc[0], loc[1] - 10), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)


# Save or display the result
output_filename = 'images/result.jpg'
cv2.imwrite(output_filename, main_image)
# cv2.imshow('Matched Results', main_image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
