import numpy as np

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from enum import Enum

from src import arabic_helper
from pero_ocr import sequence_alignment


class Color(Enum):
    RED = 1

    def __init__(self, value):
        self._console_end = '\033[0m'
        self._console_colors = {
            'red': '\033[91m'
        }

        self._pixel_colors = {
            'red': (239, 41, 44)
        }

    def to_console_colors(self):
        """ Returns start and end tags for given color. """
        return self._console_colors[self.name.lower()], self._console_end

    def color_console_text(self, text):
        start, end = self.to_console_colors()
        return start + text + end

    def to_pixel_color(self):
        """ Returns (R,G,B) tuple for given color. """
        return self._pixel_colors[self.name.lower()]


def render_predictions_and_ground_truth(predicted, ground_truth, line_height=40, error_color=Color.RED, 
                                        font=None, background_color=(0, 0, 0), font_color=(255, 255, 255)):
    if font is None:
        font = ImageFont.truetype('Ubuntu-R.ttf', 24)

    predicted_images = []
    ground_truth_images = []

    for p, g in zip(predicted, ground_truth):
        ground_truth_image = render_simple_text(g, font, line_height, background_color=background_color, font_color=font_color)

        if p == g:
            predicted_color = font_color
        else:
            predicted_color = error_color.to_pixel_color()

        predicted_image = render_simple_text(p, font, line_height, background_color=background_color, font_color=predicted_color)

        ground_truth_images.append(ground_truth_image)
        predicted_images.append(predicted_image)
            
    predictions_image = stack_images(predicted_images, background_color)
    ground_truths_image = stack_images(ground_truth_images, background_color)

    image = np.hstack((predictions_image, ground_truths_image))

    return image


def image_transcriptions_errors(transcriptions, ground_truths, line_height=32, arabic=False, error_color=Color.RED,
                                missing_char="_", font=None, background_color=(0, 0, 0), font_color=(255, 255, 255)):
    if font is None:
        font = ImageFont.truetype('Ubuntu-R.ttf', 24)

    transcription_images = []
    ground_truth_images = []

    for (transcription, ground_truth) in zip(transcriptions, ground_truths):
        transcription_image, ground_truth_image = image_transcription_errors(transcription, ground_truth, font,
                                                                             line_height, arabic, missing_char,
                                                                             background_color, font_color,
                                                                             error_color.to_pixel_color())

        transcription_images.append(transcription_image)
        ground_truth_images.append(ground_truth_image)

    transcriptions_image = stack_images(transcription_images, background_color)
    ground_truths_image = stack_images(ground_truth_images, background_color)

    image = np.hstack((transcriptions_image, ground_truths_image))

    return image


def stack_images(images, background_color=(0, 0, 0), padding=10):
    height = sum([i.shape[0] for i in images])
    width = max([i.shape[1] for i in images]) + 2*padding

    result = np.full((height, width, 3), background_color, dtype=np.uint8)
    current_y = 0

    for index, image in enumerate(images):
        height, width, _ = image.shape
        result[current_y:current_y + height, padding:width+padding, :] = image
        current_y += height

    return result


def image_transcription_errors(transcription, ground_truth, font, line_height=32, arabic=False, missing_char="_",
                               background_color=(0, 0, 0), font_color=(255, 255, 255), error_color=(255, 0, 0)):
    if arabic:
        transcription = arabic_helper.normalize_text(transcription)
        ground_truth = arabic_helper.normalize_text(ground_truth)
        errors_transcription = None
        errors_ground_truth = None

    else:
        _output = error_chars(transcription, ground_truth, missing_char)
        transcription, ground_truth, errors_transcription, errors_ground_truth = _output

    transcription_image = render_text(transcription, errors_transcription, font, line_height, background_color,
                                      font_color, error_color)
    ground_truth_image = render_text(ground_truth, errors_ground_truth, font, line_height, background_color, font_color,
                                     error_color)

    return transcription_image, ground_truth_image


def error_chars(transcription, ground_truth, missing_char="_"):
    alignment = sequence_alignment.levenshtein_alignment(list(transcription), list(ground_truth))

    source_transcription = ""
    target_transcription = ""
    errors_source = []
    errors_target = []

    for (source_char, target_char) in alignment:
        if source_char != target_char:
            color_target = False

            if source_char is None:
                source_char = missing_char

            if target_char is None:
                target_char = missing_char
                color_target = True

            errors_source.append(True)
            errors_target.append(color_target)

        else:
            errors_source.append(False)
            errors_target.append(False)

        source_transcription += source_char
        target_transcription += target_char

    return source_transcription, target_transcription, errors_source, errors_target


def render_text(text, errors, font, line_height=32, background_color=(0, 0, 0), font_color=(255, 255, 255),
                error_color=(255, 0, 0)):
    text_width, text_height = font.getsize(text)
    padding_top = int((line_height - text_height) / 2)

    if text_width == 0:
        text_width = 1

    image = Image.fromarray(np.full((line_height, text_width, 3), background_color, dtype=np.uint8))
    ImageDraw.Draw(image).text((0, padding_top), text, font=font, fill=font_color)
    image = np.array(image)

    if errors is not None:
        positions = find_char_positions(text, font)
        color_errors(image, errors, positions, error_color)

    return image


def render_simple_text(text, font, line_height=40, background_color=(0, 0, 0), font_color=(255, 255, 255)):
    text_width, text_height = font.getsize(text)    
    padding_top = int((line_height - text_height) / 2)

    if text_width == 0:
        text_width = 1

    image = Image.fromarray(np.full((line_height, text_width, 3), background_color, dtype=np.uint8))
    ImageDraw.Draw(image).text((0, padding_top), text, font=font, fill=font_color)
    image = np.array(image)

    return image


def find_char_positions(text, font):
    positions = []
    line = ""

    for char in text:
        line += char
        positions.append(font.getsize(line)[0])

    return positions


def color_errors(image, errors, positions, color):
    height = image.shape[0]

    positions = [0] + positions
    for index, error in enumerate(errors):
        if error:
            start = positions[index]
            end = positions[index + 1]

            for col in range(start, end):
                for row in range(height):
                    (b, g, r) = image[row, col]
                    intensity = r / 255.

                    if type(color) == int:
                        image[row, col] = (0, 0, color*intensity)
                    else:
                        R, G, B = color
                        image[row, col] = (B*intensity, G*intensity, R*intensity)

    return image


def console_transcriptions_errors(transcriptions, ground_truths, color=Color.RED, missing_char="_"):
    transcriptions_output = []
    ground_truths_output = []

    for (transcription, ground_truth) in zip(transcriptions, ground_truths):
        transcription_output, ground_truth_output = console_transcription_errors(transcription, ground_truth,
                                                                                 color, missing_char)

        transcriptions_output.append(transcription_output)
        ground_truths_output.append(ground_truth_output)

    return transcriptions_output, ground_truths_output


def console_transcription_errors(transcription, ground_truth, color=Color.RED, missing_char="_"):
    alignment = sequence_alignment.levenshtein_alignment(list(transcription), list(ground_truth))

    source_transcription = ""
    target_transcription = ""

    for pair in alignment:
        source_char, target_char = pair

        if source_char != target_char:
            color_target = False

            if source_char is None:
                source_char = missing_char

            if target_char is None:
                target_char = missing_char
                color_target = True

            source_char = color.color_console_text(source_char)

            if color_target:
                target_char = color.color_console_text(target_char)

        source_transcription += source_char
        target_transcription += target_char

    return source_transcription, target_transcription
