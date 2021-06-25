import arabic_reshaper
import re


def normalize_text(text):
    text = reverse_transcription(text)
    text = arabic_reshaper.reshape(text)
    text = reverse_transcription(text)
    return text


def reverse_transcription(transcription):
    transcription = transcription[::-1]

    number_patter = r"[0-9]+"
    matches = re.findall(number_patter, transcription)
    if matches:
        for match in matches:
            i = transcription.index(match)
            transcription = transcription[:i] + match[::-1] + transcription[i+len(match):]

    return transcription
