import json
import cv2
import numpy as np
from typing import Dict
from cv2.typing import MatLike
import os
from autoui.feature.Feature import Feature
from autoui.feature.Box import Box
from typing import List

class FeatureSet:
    # Category_name to OpenCV Mat
    featureDict: Dict[str, Feature] = {}

    def __init__(self, coco_folder: str, width: int, height: int) -> None:
        """
        Initialize the FeatureSet by loading images and annotations from a COCO dataset.

        Args:
            coco_folder (str): Directory containing the JSON file and images.
            width (int): Scale images to this width.
            height (int): Scale images to this height.
        """
        json_path = f'{coco_folder}/_annotations.coco.json'

        # Read the JSON file
        with open(json_path, 'r') as file:
            data = json.load(file)

        # Process images and annotations
        self.width = width
        self.height = height
        self.process_data(data, coco_folder)

    def process_data(self, data: dict, coco_folder: str) -> None:
        """
        Process the images and annotations from the COCO dataset.

        Args:
            data (dict): Parsed JSON data.
            coco_folder (str): Directory containing the images.
            width (int): Target width for scaling images.
            height (int): Target height for scaling images.
        """

        # Create a map from image ID to file name
        image_map = {image['id']: image['file_name'] for image in data['images']}

        # Create a map from category ID to category name
        category_map = {category['id']: category['name'] for category in data['categories']}

        for annotation in data['annotations']:
            image_id = annotation['image_id']
            category_id = annotation['category_id']
            bbox = annotation['bbox']

            # Load and scale the image
            image_path = f'{coco_folder}/{image_map[image_id]}'
            image = cv2.imread(image_path)
            if image is None:
                continue
            scale_x, scale_y = self.width / image.shape[1], self.height / image.shape[0]
            image = cv2.resize(image, (self.width, self.height))
            print(f"FeatureSet: self.width / image.shape {self.width} / {image.shape[1]},scale_x:{scale_x} scale_y:{scale_y}")
            # Calculate the scaled bounding box
            x, y, w, h = bbox
            x, y, w, h = round(x * scale_x), round(y * scale_y), round(w * scale_x), round(h * scale_y)

            # Crop the image to the bounding box
            cropped_image = image[y:y+h, x:x+w, :3]

            # Store in featureDict using the category name
            category_name = category_map[category_id]
            if category_name in self.featureDict:
                raise ValueError(f"Multiple boxes found for category '{category_name}'")
            self.featureDict[category_name] = Feature(cropped_image,x,y,w,h)
    
    def save_images(self, target_folder: str) -> None:
        """
        Save all images in the featureDict to the specified folder.

        Args:
            target_folder (str): The folder where images will be saved.
        """
        # Ensure the target folder exists
        os.makedirs(target_folder, exist_ok=True)

        # Iterate through the featureDict and save each image
        for category_name, image in self.featureDict.items():
            # Construct the filename
            file_name = f"{category_name}.jpg"
            file_path = os.path.join(target_folder, file_name)

            # Save the image
            cv2.imwrite(file_path, image.mat)
            print(f"Saved {file_path}")

    def findFeature(self, mat: MatLike, category_name: str, horizontal_variance: float = 0, vertical_variance: float = 0) -> List[Box]:
        """
        Find a feature within a given variance.

        Args:
            mat (MatLike): The image in which to find the feature.
            category_name (str): The category name of the feature to find.
            horizontal_variance (float): Allowed horizontal variance as a percentage of width.
            vertical_variance (float): Allowed vertical variance as a percentage of height.

        Returns:
            List[Box]: A list of boxes where the feature is found.
        """
        if category_name not in self.featureDict:
            return []

        feature = self.featureDict[category_name]
        feature_width, feature_height = feature.width, feature.height

        # Define search area using variance
        search_x1 = max(0, round(feature.x - self.width * horizontal_variance))
        search_y1 = max(0, round(feature.y - self.height * vertical_variance))
        search_x2 = min(self.width, round(feature.x + feature_width + self.width * horizontal_variance))
        search_y2 = min(self.height, round(feature.y + feature_height + self.height * vertical_variance))

        search_area = mat[search_y1:search_y2, search_x1:search_x2, :3]
        # Crop the search area from the image
        print(f"search_area: ({search_x1},{search_x2},{search_y1},{search_y2}) ({get_depth(search_area),get_depth(feature.mat)})")
        
        #cv2.imwrite("images/test.jpg", search_area)

        # Template matchingTM_CCORR_NORMED
        # result = cv2.matchTemplate(search_area, feature.mat, cv2.TM_CCOEFF_NORMED)
        result = cv2.matchTemplate(search_area, feature.mat, cv2.TM_CCOEFF_NORMED)
        
        threshold = 0.8  # Define a threshold for acceptable matches
        locations = filter_and_sort_matches(result, threshold,feature_width, feature_height)
        boxes = []

        for loc in locations:  # Iterate through found locations
            print(f"found loc {loc}")
            x, y = loc[0] + search_x1, loc[1] + search_y1
            boxes.append(Box(x, y, feature_width, feature_height))

        return boxes

def get_depth(mat:MatLike):
    data_type = mat.dtype
    if data_type == np.uint8:
        bit_depth = 8
    elif data_type == np.uint16:
        bit_depth = 16
    elif data_type == np.float32:
        bit_depth = 32
    else:
        bit_depth = "Unknown"
    return bit_depth

def filter_and_sort_matches(result, threshold, width, height):
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
    
    print(f"result {len(result)} loc {len(loc)} matches {len(matches)} unique_matches {unique_matches}")
    return unique_matches