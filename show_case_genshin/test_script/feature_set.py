from autohelper.feature.FeatureSet import FeatureSet

# Example usage
coco_folder = 'genshin/assets/coco_feature'
feature_set = FeatureSet(coco_folder, 2560, 1440)

feature_set.save_images('images')