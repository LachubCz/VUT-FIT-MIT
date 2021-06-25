import numpy as np

from .transforms import Transformer
from .transforms import MotionBlur, DefocusBlur, GaussNoise, Gamma, ColorJitter, LineGeometry, LineMasking


class UniversalTextLineTransformer(Transformer):
    def __init__(self, line_height,
                       motion_blur_prob, motion_blur_min_res, motion_blur_max_res,
                       defocus_blur_prob, defocus_blur_max_scale, defocus_blur_max_radius,
                       gauss_noise_prob, gauss_noise_max_noise_range,
                       gamma_prob, gamma_range,
                       color_jitter_prob, color_jitter_brightness, color_jitter_contrast_factor,
                       color_jitter_saturation, color_jitter_hue,
                       line_geometry_prob, line_geometry_speed_scale, line_geometry_scale_scale,
                       line_geometry_shift_scale, line_geometry_skew_scale,
                       line_masking_prob=0, line_masking_frequency=0.003, corrupt_width_min_lh=0.125, corrupt_width_max_lh=1.0
                 ):
        transforms = []
        if motion_blur_prob > 0 and motion_blur_max_res > 0:
            transforms.append((motion_blur_prob, MotionBlur(min_res=motion_blur_min_res, max_res=motion_blur_max_res)))
        if defocus_blur_prob > 0 and defocus_blur_max_radius > 0:
            transforms.append((defocus_blur_prob, DefocusBlur(max_scale=defocus_blur_max_scale, max_radius=defocus_blur_max_radius)))
        if gauss_noise_prob > 0:
            transforms.append((gauss_noise_prob, GaussNoise(max_noise_range=gauss_noise_max_noise_range)))
        if gamma_prob > 0:
            transforms.append((gamma_prob, Gamma(range=gamma_range)))
        if color_jitter_prob > 0:
            transforms.append((color_jitter_prob, ColorJitter(brightness=color_jitter_brightness,
                                                              contrast_factor=color_jitter_contrast_factor,
                                                              saturation=color_jitter_saturation,
                                                              hue=color_jitter_hue)))
        if line_geometry_prob > 0:
            transforms.append((line_geometry_prob, LineGeometry(line_height=line_height,
                                                                speed_scale=line_geometry_speed_scale,
                                                                scale_scale=line_geometry_scale_scale,
                                                                shift_scale=line_geometry_shift_scale,
                                                                skew_scale=line_geometry_skew_scale)))
        if line_masking_prob > 0:
            transforms.append((line_masking_prob, LineMasking(line_height=line_height,
                                                              corrupt_frequency=line_masking_frequency,
                                                              corrupt_width_min_lh=corrupt_width_min_lh,
                                                              corrupt_width_max_lh=corrupt_width_max_lh)))

        super().__init__(transforms=transforms, rng=np.random)

    def __call__(self, images):
        return super(UniversalTextLineTransformer, self).__call__(images=images)

