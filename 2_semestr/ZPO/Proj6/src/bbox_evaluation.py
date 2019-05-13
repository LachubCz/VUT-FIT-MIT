import cv2
import numpy as np

def evaluate_augmentation_fit(prediction, ground_truth):
    """
    method evaluates bbox by comparing its parameters to the ground truth bbox parameters
    """
    if ground_truth.augmentation:
        if prediction:
            return get_augmentation_fit_score(prediction, ground_truth)
        else:
            return 0.0
    else:
        if prediction:
            return 0.0
        else:
            return 1.0


def get_augmentation_fit_score(prediction, ground_truth):
    """
    method calculates bbox's fit score based on fitted bbox and ground truth bbox
    """
    prediction_image = draw_augmentation_box(prediction, (ground_truth.width, ground_truth.height))
    ground_truth_image = draw_augmentation_box(ground_truth.bbox, (ground_truth.width, ground_truth.height))

    return evaluate_overlap(ground_truth_image, prediction_image)


def draw_augmentation_box(bbox, image_shape):
    """
    method creates binary image containing an augmentation box
    """
    image = np.zeros(image_shape, np.uint8)

    cv2.rectangle(image, (bbox['x'], bbox['y']), (bbox['x'] + bbox['w'], bbox['y'] + bbox['h']), 1,  2)
    cv2.rectangle(image, (bbox['x'], bbox['y']), (bbox['x'] + bbox['w'], bbox['y'] + bbox['h']), 1,  -1)

    return image


def evaluate_overlap(gt_bbox_image, fit_bbox_image):
    """
    method calculates overlap of two binary images with augmentation boxes
    """
    gt_sum = np.sum(gt_bbox_image)
    fit_sum = np.sum(fit_bbox_image)

    overlap_image = gt_bbox_image & fit_bbox_image
    overlap_sum = np.sum(overlap_image)

    return overlap_sum / max(fit_sum, gt_sum)
