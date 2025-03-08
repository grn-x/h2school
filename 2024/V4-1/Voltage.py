import os

import numpy as np
from manim import *

def build_plot(axes, x, y, low_q, high_q, color):
    line = axes.plot_line_graph(x, y, add_vertex_dots=False, line_color=color)
    low_q_curve = axes.plot_line_graph(x, low_q)
    high_q_curve = axes.plot_line_graph(x, high_q)
    low_points = low_q_curve["line_graph"].points
    high_points = high_q_curve["line_graph"].points
    points = np.concatenate((low_points, np.flip(high_points, 0)))
    area = Polygon(*points, fill_opacity=0.2, stroke_width=0.0, color=color)
    return VDict({"line": line, "area": area})

def build_line(axes, x, y, color):
    line = axes.plot_line_graph(x, y, add_vertex_dots=False, line_color=color)
    return line
def ticks_to_exclude(nums, real_step, real_max=None):
    if real_max is None:
        real_max = nums[-1]
    min_val = nums[0]
    current = min_val
    ticks = []
    while current < real_max:
        current += real_step
        ticks.append(current)
    # Filter out any numbers in 'ticks' from 'nums'
    nums_filtered = [num for num in nums if num not in ticks]
    return {"nums": nums_filtered, "ticks": ticks}


class Voltage(Scene):
    def construct(self):

        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))#, '..'))
        file_path = os.path.join(project_root, 'FrameExtractor', 'out', 'voltageOut.txt')

        with open(file_path, 'r') as file:
            y = [float(line.strip())/10 for line in file]
        x = list(range(len(y)))

        x_min, x_max, x_step = 0, 340, 5
        y_min, y_max, y_step = min(y)-0.1, max(y)+0.02, 0.01 #min(y)-1
        data = ticks_to_exclude(np.arange(y_min, y_max + y_step, y_step), 0.3,0.5)
        axes = Axes(
            x_range=[x_min, x_max + x_step, x_step],
            y_range=[y_min, y_max + y_step, y_step],
            x_axis_config={
                "numbers_to_include": np.arange(x_min, x_max - x_step, 30),
                "decimal_number_config": {"num_decimal_places": 0},
            },
            y_axis_config={
                "numbers_to_include": np.arange(y_min, y_max - y_step, 0.05),
                #"numbers_to_include": data["nums"],
                "decimal_number_config": {"num_decimal_places": 2},
                #"tick_size": 0.05,
                #"numbers_to_exclude": data["nums"],
                #"numbers_with_elongated_ticks": np.arange(y_min, y_max + y_step, y_step),

            },
        )

        x_label = axes.get_x_axis_label(Text("Time in s").scale(0.5))
        y_label = axes.get_y_axis_label(Text("Voltage in V").scale(0.5))



        #y2 = [2.810, 2.676, 2.535, 2.309, 2.084, 1.832]
        #y2_str = [f"{num:.2f}" for num in y2]

        title = Text("Voltage as a Function of Time")
        title.next_to(axes, UP)
        title.scale(0.7)
        title.shift(LEFT+0.2)

        labelVol = Text("Current Voltage: ").next_to(title, DOWN).scale(0.5).shift(RIGHT *2)
        labelVal = DecimalNumber(0).next_to(labelVol, RIGHT).scale(0.7)
        labelUnit = Text("V").next_to(labelVal, RIGHT).scale(0.5)
        #self.play(Create(axes), Write(x_label), Write(y_label), Write(title))
        ##line1 = build_line(axes, x, y, color=RED)

        col_labels = [Text(f"{i}V") for i in x]


        y_value_tracker = ValueTracker(y[0])

        # Create a DecimalNumber and add an updater that sets its value to the current y value
        labelVal = DecimalNumber(y[0], num_decimal_places=2).next_to(labelVol, RIGHT)
        labelVal.add_updater(lambda v: v.set_value(y_value_tracker.get_value()))

        def line_rate_func(t):
            index = int((t - 0.0001) * len(x))
            y_value_tracker.set_value(y[index])
            return t

        self.add(axes, x_label, y_label, title, labelVal, labelVol, labelUnit)
        self.wait(1)

        line1 = build_line(axes, x, y, color=RED)
        self.play(Create(line1, rate_func=line_rate_func, run_time=10))

        labelVal.clear_updaters()




        #self.play(Create(line1, run_time=5))

        self.wait(1)

        self.wait(1)


        self.wait(5)