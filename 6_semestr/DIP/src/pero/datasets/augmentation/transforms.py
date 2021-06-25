import numpy as np
import cv2
from typing import List, Tuple
from scipy.signal import convolve2d
from abc import ABC, abstractmethod


class Transform(ABC):
    @abstractmethod
    def __call__(self, image: np.ndarray) -> np.ndarray:
        pass


class Transformer:
    """
    Class used for transforming images and pages with given probability.
    """

    def __init__(self, transforms: List[Tuple[float, Transform]], rng=np.random):
        """
        Parameters
        ----------
        transforms: list of transform object with it's probability of actually applying
        rng: possible to pass np.random.Seed()
        """
        self.transforms = transforms
        self.rng = rng

    def __call__(self, images):
        for idx, image in enumerate(images):
            for (prob, transform) in self.transforms:
                if self.rng.rand() < prob:
                    image = transform(image)
            images[idx] = image
        return images


class MotionBlur(Transform):
    def __init__(self, min_res=10, max_res=15, rng=np.random):
        """
        np.random.RandomState(rng_seed) can be passed
        """
        self.rng = rng
        self.kernel_count = 2000
        self.min_res = min_res
        self.max_res = max_res
        self.kernels = [self.get_kernel(resolution=self.rng.randint(self.min_res, self.max_res)) for i in
                        range(self.kernel_count)]

    def __call__(self, image: np.ndarray) -> np.ndarray:
        kernel = self.kernels[np.random.randint(len(self.kernels)-1)]
        new_image = np.copy(image)
        for c in range(3):
            new_image[:, :, c] = convolve2d(new_image[:, :, c], kernel, mode='same', boundary='wrap')

        return new_image

    def get_kernel(self, start_samples=500, length=300, halflife=0.5, resolution=15):
        supersampling = 5

        # generate random acceleration
        a = self.rng.randn(2, length + start_samples)

        # integrate speed
        a[0, :] = MotionBlur.ewma(a[0, :], halflife * length)
        a[1, :] = MotionBlur.ewma(a[1, :], halflife * length)

        # integrate position
        a = np.cumsum(a, axis=1)

        # skip first startSamples
        a = a[:, start_samples:]

        # center the kernel
        a = a - np.mean(a, axis=1).reshape((2, 1))

        # normalize size
        maxDistance = ((a[0, :] ** 2 + a[1, :] ** 2) ** 0.5).max()
        a = a / maxDistance

        psf, t, t = np.histogram2d(a[0, :], a[1, :], bins=resolution * supersampling,
                                   range=[[-1.0, +1.0], [-1.0, +1.0]], normed=True)
        psf = cv2.resize(psf, (resolution, resolution), interpolation=cv2.INTER_AREA)
        psf = psf.astype(np.float32)
        psf = psf / np.sum(psf)
        return psf

    @staticmethod
    def ewma(data, halflife, offset=None, dtype=None, order='C', out=None):
        """
        Calculates the exponential moving average over a vector.
        Will fail for large inputs.

        Source: https://stackoverflow.com/questions/42869495/numpy-version-of-exponential-weighted-moving-average-equivalent-to-pandas-ewm

        :param data: Input data
        :param alpha: scalar float in range (0,1)
            The alpha parameter for the moving average.
        :param offset: optional
            The offset for the moving average, scalar. Defaults to data[0].
        :param dtype: optional
            Data type used for calculations. Defaults to float64 unless
            data.dtype is float32, then it will use float32.
        :param order: {'C', 'F', 'A'}, optional
            Order to use when flattening the data. Defaults to 'C'.
        :param out: ndarray, or None, optional
            A location into which the result is stored. If provided, it must have
            the same shape as the input. If not provided or `None`,
            a freshly-allocated array is returned.
        """
        data = np.array(data, copy=False)
        row_size = len(data)

        alpha = 1 - np.exp(np.log(0.5) / halflife)

        if dtype is None:
            if data.dtype == np.float32:
                dtype = np.float32
            else:
                dtype = np.float64
        else:
            dtype = np.dtype(dtype)

        if data.ndim > 1:
            # flatten input
            data = data.reshape(-1, order)

        if out is None:
            out = np.empty_like(data, dtype=dtype)
        else:
            assert out.shape == data.shape
            assert out.dtype == dtype

        if data.size < 1:
            # empty input, return empty array
            return out

        if offset is None:
            offset = data[0]

        alpha = np.array(alpha, copy=False).astype(dtype, copy=False)

        # scaling_factors -> 0 as len(data) gets large
        # this leads to divide-by-zeros below
        scaling_factors = np.power(1. - alpha, np.arange(row_size + 1, dtype=dtype),
                                   dtype=dtype)

        # create cumulative sum array
        np.multiply(data, (alpha * scaling_factors[-2]) / scaling_factors[:-1],
                    dtype=dtype, out=out)
        np.cumsum(out, dtype=dtype, out=out)

        # cumsums / scaling
        out /= scaling_factors[-2::-1]

        if offset != 0:
            offset = np.array(offset, copy=False).astype(dtype, copy=False)
            # add offsets
            out += offset * scaling_factors[1:]

        return out


class DefocusBlur(Transform):
    def __init__(self, rng=np.random, max_scale=8, max_radius=5):
        """
        np.random.RandomState(rng_seed) can be passed
        """
        self.rng = rng
        self.max_scale = max_scale
        self.max_radius = max_radius

    def __call__(self, image: np.ndarray) -> np.ndarray:
        random_scale = self.rng.randint(1, self.max_scale)
        random_radius = self.rng.randint(1, self.max_radius)
        kernel = DefocusBlur._get_kernel(random_scale, random_radius)

        new_image = np.copy(image)
        for c in range(3):
            new_image[:, :, c] = convolve2d(new_image[:, :, c], kernel, mode='same', boundary='wrap')

        return new_image

    @staticmethod
    def _get_kernel(scale, radius):
        psf_radius = int(radius * scale + 0.5)
        center = int((int(radius) + 2) * scale + scale / 2)
        psf = np.zeros((2 * center, 2 * center))
        cv2.circle(psf, (center, center), psf_radius, color=1.0, thickness=-1, lineType=cv2.LINE_AA)
        psf = cv2.resize(psf, dsize=(0, 0), fx=1.0 / scale, fy=1.0 / scale, interpolation=cv2.INTER_AREA)
        psf = psf / np.sum(psf)
        return psf


class GaussNoise(Transform):
    def __init__(self, rng=np.random, max_noise_range=5):
        """
        np.random.RandomState(rng_seed) can be passed
        """
        self.rng = rng
        self.max_noise_range = max_noise_range

    def __call__(self, image: np.ndarray) -> np.ndarray:
        noise_range = self.rng.randint(1, self.max_noise_range)

        # generate one channel
        noise = self.rng.normal(0, noise_range, size=image.shape[:2]).astype(np.int32)

        # copy to other channels
        noise = np.repeat(noise[:, :, np.newaxis], 3, axis=2)

        return np.clip(image.astype(np.int32) + noise, 0, 255).astype(np.uint8)


class Gamma(Transform):
    def __init__(self, range=0.3, rng=np.random):
        self.rng = rng
        self.range = range

    def __call__(self, image: np.ndarray) -> np.ndarray:
        return Gamma._adjust_gamma(image, self.rng.uniform(1 - self.range, 1 + self.range))

    @staticmethod
    def _adjust_gamma(image, gamma=1.):
        """
        Parameters
        ----------
        value: 1. for unchanged picture
        """
        # build a lookup table for each pixel
        table = np.array([255 * ((i / 255.0) ** gamma) for i in np.arange(0, 256)]).astype("uint8")

        # apply gamma correction using the lookup table
        return table[image]


class Color:
    @staticmethod
    def _adjust_hue(image, value):
        """
        Parameters
        ----------
        value: int in <0, 0.5>
        """
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # uint8 addition take cares of rotation across boundaries
        with np.errstate(over='ignore'):
            hsv[:, :, 0] += np.uint8(value * 255)

        return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    @staticmethod
    def _adjust_brightness(image, bias=0.):
        """
        Parameters
        ----------
        image
        bias: brightness offset
        """
        image = image.astype(np.float)
        image = image + bias * 255
        return np.clip(image, 0, 255).astype(np.uint8)

    @staticmethod
    def _adjust_saturation(image, factor):
        """
        Parameters
        ----------
        factor: 0 - black, 1 - original image, 2 - twice the saturation
        """
        hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV).astype(np.float)
        hsv[:, :, 1] *= factor
        return cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2RGB)

    @staticmethod
    def _adjust_contrast(image, factor):
        """
        Parameters
        ----------
        factor: 0 - gray image, 1 - original image, 2 - twice the contrast
        """
        enhanced = image.astype(np.float) * factor
        return np.clip(enhanced, 0, 255).astype(np.uint8)


class ColorJitter(Transform, Color):
    def __init__(self, brightness=.1, contrast_factor=.2, saturation=.2, hue=.1, rng=np.random):
        self.brightness = brightness
        self.contrast = contrast_factor
        self.saturation = saturation
        self.hue = hue

        self.rng = rng

    def __call__(self, image: np.ndarray) -> np.ndarray:
        if self.brightness > 0:
            bias = self.rng.uniform(-self.brightness, self.brightness)
            image = self._adjust_brightness(image, bias)

        if self.contrast > 0:
            contrast_factor = self.rng.uniform(max(0, 1 - self.contrast), 1 + self.contrast)
            image = self._adjust_contrast(image, contrast_factor)

        if self.saturation > 0:
            saturation_factor = self.rng.uniform(max(0, 1 - self.saturation), 1 + self.saturation)
            image = self._adjust_saturation(image, saturation_factor)

        if self.hue > 0:
            # TODO: negative hue factor creates weird artifacts
            hue_factor = self.rng.uniform(0, self.hue)
            image = self._adjust_hue(image, hue_factor)
        return image


class LineMasking(Transform):
    def __init__(self, line_height, corrupt_frequency=0.002, corrupt_width_min_lh=0.125, corrupt_width_max_lh=1.0):
        self.line_height = line_height
        self.corrupt_frequency = corrupt_frequency
        self.corrupt_width_min_lh = corrupt_width_min_lh
        self.corrupt_width_max_lh = corrupt_width_max_lh
        self.noise = self.precompute_noise()

    def precompute_noise(self):
        return np.random.randint(0, 255, size=(self.line_height, 10000, 3), dtype=np.uint8)

    def __call__(self, image: np.ndarray) -> np.ndarray:
        if image.shape[1] == 0:
            return image
        if self.corrupt_frequency > 0:
            width_min = image.shape[0] * self.corrupt_width_min_lh
            width_max = image.shape[0] * self.corrupt_width_max_lh

            corrupt_count = np.random.binomial(n=image.shape[1], p=self.corrupt_frequency)
            if corrupt_count > 0:
                corrupt_starts = np.random.randint(low=0, high=image.shape[1]-1, size=corrupt_count)
                noise_starts = np.random.randint(low=0, high=image.shape[1]-1, size=corrupt_count)
                corrupt_ends = corrupt_starts + np.random.randint(low=width_min, high=width_max, size=corrupt_count)
                corrupt_ends = np.minimum(corrupt_ends, image.shape[1] - 1)
                for start, end, noise_start in zip(corrupt_starts, corrupt_ends, noise_starts):
                    image[:, start:end] = self.noise[:, noise_start:noise_start+(end-start)]
        return image


class LineGeometry(Transform):
    def __init__(self, line_height, speed_scale=0.5, scale_scale=0.2, shift_scale=1, skew_scale=0.3):
        self.speed_scale = speed_scale
        self.scale_scale = scale_scale
        self.shift_scale = shift_scale
        self.skew_scale = skew_scale
        self.line_height = line_height
        self.target_grid_length = 100000
        self.x, self.y = self.precompute_grid()

    def precompute_grid(self):
        x_pos = 2**(self.gen_noise(target_length=self.target_grid_length) * self.speed_scale)
        x_scale = 2**(self.gen_noise(target_length=x_pos.shape[1]) * self.scale_scale)
        y_shift = self.gen_noise(target_length=x_pos.shape[1]) * self.shift_scale
        skew = self.gen_noise(target_length=x_pos.shape[1]) * self.skew_scale

        y = np.arange(self.line_height).reshape(-1, 1)
        y = np.tile(y, [1, x_pos.shape[1]]) - self.line_height / 2
        y = (y + y_shift) * x_scale

        x = np.cumsum(x_pos, axis=1)
        x = np.tile(x, [self.line_height, 1])
        x = x + y * skew
        y = y + self.line_height / 2
        y = np.clip(y, 0, self.line_height-1)

        return x, y

    @staticmethod
    def gen_noise(target_length, depth=8, energy_decay=0.5):
        noise = np.random.normal(size=(1, target_length // 2**depth))
        energy = 1
        while depth > 0:
            energy *= 1 / energy_decay
            noise = cv2.resize(noise, (0, 0), fx=2, fy=1, interpolation=cv2.INTER_LINEAR) * (1/energy_decay)
            noise += np.random.normal(size=noise.shape)
            depth -= 1

        return noise / energy

    def __call__(self, image: np.ndarray) -> np.ndarray:
        if image.shape[1] == 0:
            return image
        x_start = np.random.randint(0, self.x.shape[1] - image.shape[1] * 3 - 1)

        x_end = self.x[self.line_height // 2, x_start:x_start + image.shape[1] * 3] - self.x[self.line_height // 2, x_start]
        x_end = x_start + np.flatnonzero(x_end > image.shape[1])[0]
        x = self.x[:, x_start:x_end] - self.x[self.line_height // 2, x_start]
        y = self.y[:, x_start:x_end]
        out_img = cv2.remap(image, x.astype(np.float32), y.astype(np.float32), cv2.INTER_LINEAR)
        return out_img
