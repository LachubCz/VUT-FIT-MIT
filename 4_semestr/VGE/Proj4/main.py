import numpy as np
import cv2
import cvui

from ear_clipping import get_ec_steps

if __name__ == '__main__':
	WINDOW_NAME = 'Ear clipping method'

	frame = np.zeros((720, 1280, 3), np.uint8)
	cvui.init(WINDOW_NAME)

	#process images and store them in memory
	coords = np.array([[350, 75], [379, 161], [469, 161], [397, 215], [423, 301], [350, 250], [277, 301], [303, 215], [231, 161], [321, 161]])
	steps = get_ec_steps(coords)
	state = 0
	state_count = len(steps)
	while True:
		frame[:] = (49, 52, 49)

		if (cvui.button(frame, 555, 40, "Previous")):
			# render previous image
			if state > 0:
				state -= 1
		if (cvui.button(frame, 650, 40, "Next")):
			# render next image
			if state < (state_count - 1):
				state += 1

		cvui.image(frame, 310, 100, steps[state])

		cvui.imshow(WINDOW_NAME, frame)

		if cv2.waitKey(20) == 27:
			break
