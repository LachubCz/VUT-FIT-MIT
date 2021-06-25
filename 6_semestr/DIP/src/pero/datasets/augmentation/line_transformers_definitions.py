from functools import partial
from datasets.augmentation.line_transformers import UniversalTextLineTransformer


LINE_TRANSFORMERS = {
    'FULL_LARGER': partial(UniversalTextLineTransformer,
                    motion_blur_prob=0.166,
                    motion_blur_min_res=3,
                    motion_blur_max_res=9,

                    defocus_blur_prob=0.1,
                    defocus_blur_max_scale=8,
                    defocus_blur_max_radius=3,

                    gauss_noise_prob=0.1,
                    gauss_noise_max_noise_range=12,
                    gamma_prob=0.25,
                    gamma_range=0.5,

                    color_jitter_prob=0.333,
                    color_jitter_brightness=0.3,
                    color_jitter_contrast_factor=0.4,
                    color_jitter_saturation=0.8,
                    color_jitter_hue=0.3,

                    line_geometry_prob=0.66,
                    line_geometry_speed_scale=0.2,
                    line_geometry_scale_scale=0.25,
                    line_geometry_shift_scale=1.5,
                    line_geometry_skew_scale=0.05,

                    line_masking_prob=0.5,
                    line_masking_frequency=0.005,
                    corrupt_width_min_lh=0.125,
                    corrupt_width_max_lh=1.0),
    'FULL_LARGER_NO_GEO': partial(UniversalTextLineTransformer,
                    motion_blur_prob=0.166,
                    motion_blur_min_res=3,
                    motion_blur_max_res=9,

                    defocus_blur_prob=0.1,
                    defocus_blur_max_scale=8,
                    defocus_blur_max_radius=3,

                    gauss_noise_prob=0.1,
                    gauss_noise_max_noise_range=12,
                    gamma_prob=0.25,
                    gamma_range=0.5,

                    color_jitter_prob=0.333,
                    color_jitter_brightness=0.3,
                    color_jitter_contrast_factor=0.4,
                    color_jitter_saturation=0.8,
                    color_jitter_hue=0.3,

                    line_geometry_prob=0,
                    line_geometry_speed_scale=0.2,
                    line_geometry_scale_scale=0.25,
                    line_geometry_shift_scale=1.5,
                    line_geometry_skew_scale=0.05,

                    line_masking_prob=0.5,
                    line_masking_frequency=0.005,
                    corrupt_width_min_lh=0.125,
                    corrupt_width_max_lh=1.0)
}
