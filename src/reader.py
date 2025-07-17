"""
Andrew Kim

27 June 2025

Version 1.0.0

Reads LDF files
"""

import numpy as np
import cv2

from ldf import LinkamDataFile


def extract_utf8(data: bytes) -> str:
    """ Extracts UTF-8 encoded string from bytes """
    return ''.join(
        chr(b) if 32 <= b < 127 else '' for b in data
    )


# JPEG start marker
START_MARKER = b'\xff\xd8'

# number of bytes to extract before the image
BYTES_TO_EXTRACT = 1000



class LinkamDataReader:
    """ Parses Linkam Data Files to extract images and data """

    @staticmethod
    def extract_data(filepath: str) -> LinkamDataFile:
        """ Extracts data from Linkam Data File """

        file_name = f"{filepath[filepath.rindex('/') + 1 : ]}"

        with open(filepath, "rb") as file:
            data = file.read()

        temperatures = []
        ramps = []
        rates = []
        limits = []
        images = []

        offset = 0

        while offset < len(data):
            start = data.find(START_MARKER, offset)
            if start == -1:
                break

            extract_start = max(0, start - BYTES_TO_EXTRACT)
            region = data[extract_start:start]

            # convert to readable UTF-8
            readable_text = extract_utf8(region)

            if "Temp" not in readable_text:
                # Advance offset to avoid infinite loop
                offset = start + 2
                continue

            temp_index = readable_text.index("Temp ")
            ramp_index = readable_text.index("Ramp Row ")
            rate_index = readable_text.index("Rate ")
            limit_index = readable_text.index("Limit ")

            temperature = float(readable_text[temp_index + 5 : ramp_index - 2].strip())
            ramp = int(readable_text[ramp_index + 9 : rate_index - 1].strip())
            rate = float(readable_text[rate_index + 5 : limit_index - 6].strip())
            limit_start = limit_index + 6
            limit_str = ""
            for i, c in enumerate(readable_text[limit_start:]):
                if c.isalpha():
                    break
                if c == '-' and i != 0:
                    break
                if c.isdigit() or c == '.' or (c == '-' and i == 0):
                    limit_str += c
                elif c.strip() == "":
                    continue
                else:
                    break
            limit = float(limit_str.strip())

            temperatures.append(temperature)
            ramps.append(ramp)
            rates.append(rate)
            limits.append(limit)

            end = data.find(b'\xff\xd9', start)
            if end == -1:
                offset = start + 2
                break

            # Extract JPEG bytes and decode to np.ndarray
            jpeg_bytes = data[start:end + 2]
            img_array = np.frombuffer(jpeg_bytes, dtype=np.uint8)
            img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
            if img is not None:
                images.append(img)

            offset = end + 2

        return LinkamDataFile(
            file=file_name,
            ramp=ramps,
            temp=temperatures,
            temp_limit=limits,
            temp_rate=rates,
            raw=images
        )
