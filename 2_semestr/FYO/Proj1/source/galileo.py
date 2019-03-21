import cv2
import cvui
from tools import exp_type, get_graph
from timeit import default_timer as timer

WINDOW_NAME = 'Speed of Light Measurement'

def galileo(frame):
    curr_expr = 0
    experiments = [[False] for i in range(6)]

    restart = True
    distance_tr = [1.1]

    galileo_default = cv2.imread("images/galileo_default.png", 1)
    galileo_yellow_dot = cv2.imread("images/galileo_yellow_dot.png", 1)
    galileo_fire = cv2.imread("images/galileo_fire.png", 1)
    
    while (True):
        frame[:] = (49, 52, 49)

        if restart:
            animation = 0
            animate = False
            galileo_coord_bottom = 385
            galileo_coord_top = 985
            first_graph_f = False
            second_graph_f = False
            first_graph = False
            second_graph = False
            first_delay = 0
            second_delay = 0
            delay = 0
            speed_of_light = 299792
            half = False
            first_after_half = 0
            first_after_end = 0
            restart = False

        if not first_graph_f:
            first_graph, lag = get_graph()
            first_delay = lag
            first_graph_f = True
        if not second_graph_f:
            second_graph, lag = get_graph()
            second_delay = lag
            second_graph_f = True

        #Animation window
        cvui.image(frame, 0, 0, galileo_default)
        
        if animate:
            galileo_coord_bottom = 368
            galileo_coord_top = 968
            cvui.image(frame, 314, 393, galileo_fire)
            if animation < 21:
                for _ in range(animation+1):
                    cvui.image(frame, galileo_coord_bottom, 400, galileo_yellow_dot)
                    galileo_coord_bottom = galileo_coord_bottom + 30
            else:
                for _ in range(21):
                    cvui.image(frame, galileo_coord_bottom, 400, galileo_yellow_dot)
                    galileo_coord_bottom = galileo_coord_bottom + 30

            if animation >= 21 and animation < 42:
                cvui.image(frame, 960, 200, first_graph)
                cvui.text(frame, 1079, 278, str(int(first_delay))+"ms", 0.4);
        
                cvui.image(frame, 1036, 390, galileo_fire)
                for _ in range(animation+1-21):
                    cvui.image(frame, galileo_coord_top, 375, galileo_yellow_dot)
                    galileo_coord_top = galileo_coord_top - 30
            elif animation == 42:
                if first_after_end != 0:
                    if (timer() - first_after_end) > (second_delay/1000):
                        first_after_end = 0
                        cvui.image(frame, 131, 205, second_graph)
                        cvui.text(frame, 248, 285, str(int(second_delay))+"ms", 0.4);
                        delay = static_distance/speed_of_light + (first_delay/1000) + (second_delay/1000)
                        

                else:
                    cvui.image(frame, 131, 205, second_graph)
                    cvui.text(frame, 248, 285, str(int(second_delay))+"ms", 0.4);

                cvui.image(frame, 1036, 390, galileo_fire)
                for _ in range(21):
                    cvui.image(frame, galileo_coord_top, 375, galileo_yellow_dot)
                    galileo_coord_top = galileo_coord_top - 30

            if animation < 42:
                act_time = timer() - start_time
                whole_distance = static_distance
                if half:
                    traveled_distance = (act_time-(first_delay/1000)) * speed_of_light
                else:
                    traveled_distance = act_time * speed_of_light
                piece_of_distance = whole_distance / 21
                traveled_parts = traveled_distance / piece_of_distance
                if first_after_half != 0:
                    if (timer() - first_after_half) > (first_delay/1000):
                        first_after_half = 0
                else:
                    if not half:
                        if traveled_parts >= 21:
                            animation = 20
                            half = True
                            first_after_half = timer()
                        else:
                            animation = int(traveled_parts)
                    else:
                        if traveled_parts >= 42:
                            animation = 42
                            first_after_end = timer()
                        else:
                            animation = int(traveled_parts)
            else:
                cvui.image(frame, 960, 200, first_graph)
                cvui.text(frame, 1079, 278, str(int(first_delay))+"ms", 0.4);
                if delay != 0:
                    cvui.text(frame, 660, 343, str(round(delay, 2))+"s", 0.5);
                    cvui.text(frame, 345, 90, "c=(2*s)/(t-2*o)=(2*{:,})/({}-2*0.25)={:,} km/s"
                        .format(static_distance/2, str(round(delay, 2)), round(static_distance/(round(delay, 2)-2*0.25), 2)), 0.5)

        #Experiment settings window
        cvui.window(frame, 1033.5, 2, 243.5, 133, 'Experiment settings')
        
        cvui.trackbar(frame,  1030, 39, 249, distance_tr, 1.1, 10.0);
        cvui.rect(frame, 1035, 39, 240, 12, 0x313431, 0x313431);
        cvui.rect(frame, 1035, 74, 240, 25, 0x313431, 0x313431);
        cvui.text(frame, 1041, 32, "Distance")
        cvui.text(frame, 1042, 82, "{:,} km".format(round((distance_tr[0])**8, 0)))
        if cvui.button(frame, 1040, 102, "Execute"):
            if not animate:
                static_distance = round((distance_tr[0])**8, 0) * 2
            animate = True
            start_time = timer()
        if cvui.button(frame, 1125, 102, "Clear"):
            restart = True
        
        #Experiments window
        cvui.window(frame, 2, 2, 155, 165, 'Experiments')

        cvui.checkbox(frame, 10,  30, "1638 - Galileo",   experiments[0])
        cvui.checkbox(frame, 10,  53, "1676 - Roemer",    experiments[1])
        cvui.checkbox(frame, 10,  76, "1729 - Bradley",   experiments[2])
        cvui.checkbox(frame, 10,  99, "1849 - Fizeau",    experiments[3])
        cvui.checkbox(frame, 10, 122, "1862 - Foucalt",   experiments[4])
        cvui.checkbox(frame, 10, 145, "1879 - Michelson", experiments[5])

        curr_expr = exp_type(curr_expr, experiments)
        experiments = [[False] for i in range(6)]
        experiments[curr_expr] = [True]

        cvui.update()

        cv2.imshow(WINDOW_NAME, frame)

        if cv2.waitKey(20) == 27:
            return -1

        if curr_expr != 0:
            return curr_expr
