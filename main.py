import cv2
from numpy import random, square, sqrt

import image_editor

FILENAME = 'pic.jpg'
LINES_QUANTITY = 500000
MAX_LINE_LENGTH = 30
LINES_LENGTH_QUANTITY = 3
LINES_PER_LENGTH_QUANTITY = 3
INTENSITY = 15

input_image = cv2.cvtColor(cv2.imread(FILENAME), cv2.COLOR_BGR2GRAY)
(image_high, image_width) = input_image.shape

editor = image_editor.Editor(input_image)

cur_x = int(random.randint(0, image_width))
cur_y = int(random.randint(0, image_high))

for i in range(LINES_QUANTITY):
    results = {}

    lines_length = random.randint(2,
                                  MAX_LINE_LENGTH + 1,
                                  LINES_LENGTH_QUANTITY)
    for length in lines_length:
        lines_x = random.randint(max(cur_x - length, 0),
                                 min(cur_x + length, image_width),
                                 LINES_PER_LENGTH_QUANTITY)
        for x in lines_x:
            k = 1
            if random.randint(2) == 1:
                k *= -1

            y = k * sqrt(square(length) - square(x - cur_x)) + cur_y

            if y < 0:
                y = 0
            if y >= image_high:
                y = image_high - 1

            x = int(x)
            y = int(y)

            prev_err = editor.get_distance()
            editor.draw_line(cur_x, cur_y, x, y, INTENSITY)
            new_err = editor.get_distance()
            editor.draw_line(cur_x, cur_y, x, y, -INTENSITY)

            results[x, y] = new_err - prev_err

    best = min(results.items(), key=lambda pair: pair[1])
    (pos, err) = best
    if err < 0:
        editor.draw_line(cur_x, cur_y, pos[0], pos[1], INTENSITY)

    (cur_x, cur_y) = pos

cv2.imwrite("result.jpg", editor.get_image())
