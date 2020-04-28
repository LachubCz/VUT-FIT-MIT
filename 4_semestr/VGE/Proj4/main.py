import numpy as np
import cv2
import cvui

from ear_clipping import get_ec_steps
from sweep_line import parse_data, get_sl_steps

if __name__ == '__main__':
	WINDOW_NAME = 'Polygon triangulation'

	frame = np.zeros((720, 1280, 3), np.uint8)
	cvui.init(WINDOW_NAME)

	# ear clipping
	coords = np.array([[350, 75], [379, 161], [469, 161], [397, 215], [423, 301], [350, 250], [277, 301], [303, 215], [231, 161], [321, 161]])
	steps_0 = get_ec_steps(coords)

	# sweep line
	with open("./sweep-line/polygon_new.txt") as file:
		data = file.readlines()

	polygon, trap_edges, partition, triangles = parse_data(data)
	steps_1 = get_sl_steps(np.array(polygon), np.array(trap_edges), np.array(partition), np.array(triangles))

	state = 0
	state_count = len(steps_0)
	algorithm = 0
	algorithm_0 = [True]
	algorithm_1 = [False]
	while True:
		frame[:] = (49, 52, 49)
		cvui.window(frame, 10, 10, 116, 78, "Algorithms")

		cvui.checkbox(frame, 20, 40, "Ear clipping", algorithm_0)
		cvui.checkbox(frame, 20, 62, "Sweep line", algorithm_1)
		if algorithm == 0 and algorithm_0[0] and algorithm_1[0]:
			algorithm = 1
			algorithm_0 = [False]
			algorithm_1 = [True]
			state = 0
			state_count = len(steps_1)
		elif algorithm == 1 and algorithm_0[0] and algorithm_1[0]:
			algorithm = 0
			algorithm_0 = [True]
			algorithm_1 = [False]
			state = 0
			state_count = len(steps_0)

		if (cvui.button(frame, 555, 40, "Previous")):
			# render previous image
			if state > 0:
				state -= 1
		if (cvui.button(frame, 650, 40, "Next")):
			# render next image
			if state < (state_count - 1):
				state += 1

		if algorithm == 0:
			cvui.image(frame, 310, 100, steps_0[state])
		elif algorithm == 1:
			cvui.image(frame, 310, 100, steps_1[state])

		cvui.imshow(WINDOW_NAME, frame)

		if cv2.waitKey(20) == 27:
			break
