import numpy as np
import cv2


def calculate_distance(i1, i2):
    return np.sum((i1.astype("float") - i2.astype("float")) ** 2)


class Editor:
    _image: 0
    _buffer = 0
    _ideal_image: None

    _distance = 0

    def __init__(self, ideal_image):
        shape = ideal_image.shape
        (y, x) = shape
        self._image = np.zeros(shape, dtype="uint8")
        self._image[0:y, 0:x] = 255
        self._buffer = np.zeros(shape, dtype="uint8")
        self._buffer[0:y, 0:x] = 0
        self._ideal_image = ideal_image
        self._distance = calculate_distance(self._image, ideal_image)

    def draw_line(self, x1, y1, x2, y2, color=10):
        ideal_chunk = self._ideal_image[min(y1, y2):max(y1, y2),
                                        min(x1, x2):max(x1, x2)]

        prev_chunk = self._image[min(y1, y2):max(y1, y2),
                                 min(x1, x2):max(x1, x2)]
        prev_distance = calculate_distance(ideal_chunk, prev_chunk)

        cv2.line(self._buffer, (x1, y1), (x2, y2), abs(color))
        if color < 0:
            self._image = cv2.add(self._image, self._buffer)
        else:
            self._image = cv2.subtract(self._image, self._buffer)

        cur_chunk = self._image[min(y1, y2):max(y1, y2),
                                min(x1, x2):max(x1, x2)]
        cur_distance = calculate_distance(ideal_chunk, cur_chunk)

        cv2.line(self._buffer, (x1, y1), (x2, y2), 0)

        self._distance -= prev_distance - cur_distance

    def get_distance(self):
        return self._distance

    def get_image(self):
        return self._image
