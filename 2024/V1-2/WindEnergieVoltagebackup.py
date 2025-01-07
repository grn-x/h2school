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


class WindEnergieVoltage(Scene):
    def construct(self):
        x_min, x_max, x_step = 0, 50, 10
        y_min, y_max, y_step = 0, 3.5, 0.1
        data = ticks_to_exclude(np.arange(y_min, y_max + y_step, y_step), 0.5,3)
        axes = Axes(
            x_range=[x_min, x_max + x_step, x_step],
            y_range=[y_min, y_max + y_step, y_step],
            x_axis_config={
                "numbers_to_include": np.arange(x_min, x_max + x_step, x_step),
                "decimal_number_config": {"num_decimal_places": 2},
            },
            y_axis_config={
                "numbers_to_include": np.arange(y_min, y_max + y_step, y_step),
                "decimal_number_config": {"num_decimal_places": 2},
                #"tick_size": 0.05,
                "numbers_to_exclude": data["nums"],
                "numbers_with_elongated_ticks": data["ticks"],

            },
        )

        x_label = axes.get_x_axis_label(Text("Distance in cm").scale(0.5))
        y_label = axes.get_y_axis_label(Text("Voltage in v").scale(0.5))


        x = [0, 10, 20, 30, 40, 50]
        y = [2.815, 2.738, 2.506, 2.329, 2.101, 1.826]
        y2 = [2.810, 2.676, 2.535, 2.309, 2.084, 1.832]

        title = Text("Voltage as a Function of Distance")
        title.next_to(axes, UP)
        title.scale(0.7)
#        title.shift(UP+0.5)
        #self.play(Create(axes), Write(x_label), Write(y_label), Write(title))
        self.add((axes), (x_label), (y_label), (title))
        for i in range(0, y.__len__()):
            dot = Dot(axes.c2p(x[i], y[i]), color=RED)
            self.play(Create(dot, run_time=0.2))

        line1 = build_line(axes, x, y, color=RED)
        line2 = build_line(axes, x, y, color=RED)
        line3 = build_line(axes, x, y2, color=BLUE)
        self.play(Create(line1))
        self.add(line2)
        for i in range(0, y2.__len__()):
            dot = Dot(axes.c2p(x[i], y2[i]), color=BLUE)
            self.play(Create(dot, run_time=0.2))
        self.play(Transform(line2, line3))
        self.wait()