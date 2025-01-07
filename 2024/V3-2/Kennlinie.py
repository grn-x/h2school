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


class Kennlinie(Scene):
    def construct(self):
        x_min, x_max, x_step = 0, 3, 0.5
        y_min, y_max, y_step = 0, 0.4, 0.05
        data = ticks_to_exclude(np.arange(y_min, y_max + y_step, y_step), 0.3,0.5)
        axes = Axes(
            x_range=[x_min, x_max + x_step, x_step],
            y_range=[y_min, y_max + y_step, y_step],
            x_axis_config={
                "numbers_to_include": np.arange(x_min, x_max + x_step, x_step),
                "decimal_number_config": {"num_decimal_places": 2},
            },
            y_axis_config={
                "numbers_to_include": np.arange(y_min, y_max + y_step, y_step),
                #"numbers_to_include": data["nums"],
                "decimal_number_config": {"num_decimal_places": 3},
                "tick_size": 0.05,
                #"numbers_to_exclude": data["nums"],
                "numbers_with_elongated_ticks": np.arange(y_min, y_max + y_step, y_step),

            },
        )

        x_label = axes.get_x_axis_label(Text("Voltage in V").scale(0.5))
        y_label = axes.get_y_axis_label(Text("Current in A").scale(0.5))


        x = [0.76, 0.99, 1.05, 1.3, 1.5, 1.7, 1.9, 2.1, 2.3, 2.5, 2.7, 2.9, 3.1]
        y = [0, 0, 0.001, 0.004, 0.007, 0.008, 0.01, 0.017, 0.045, 0.111, 0.167, 0.24, 0.326]
        #y2 = [2.810, 2.676, 2.535, 2.309, 2.084, 1.832]
        y_str = [f"{num:.3f}" for num in y]
        #y2_str = [f"{num:.2f}" for num in y2]

        title = Text("Current as a Function of Voltage")
        title.next_to(axes, UP)
        title.scale(0.7)
        title.shift(LEFT+0.2)
        #self.play(Create(axes), Write(x_label), Write(y_label), Write(title))
        line1 = build_line(axes, x, y, color=RED)

        col_labels = [Text(f"{i}V") for i in x]

        t_start = Table(
            [y_str],
            row_labels=[Text("Current in A:")],
            col_labels=col_labels, )



        t_start.next_to(title, DOWN).scale(0.25)
        t_start.get_rows()[1].set_opacity(0)
        entry = t_start.get_entries()[len(x)]#label
        entry.set_opacity(1)



        # t_start_first_row_pos = t_start.get_rows()[0].get_center()
        # t_end_first_row_pos = t_end.get_rows()[0].get_center()
        # vertical_shift = t_start_first_row_pos[1] - t_end_first_row_pos[1]
        # t_end.shift(UP * vertical_shift)

        t_start.shift(RIGHT * 1)

        t_start_first_row_pos = t_start.get_rows()[0].get_center()



        self.add(axes, x_label, y_label, title)
        self.add(t_start, entry.set_opacity(1))
        self.wait(1)
        for i in range(len(x)):
            entry = t_start.get_entries()[i+len(x)+1]
            print(entry.get_y())
            dot = Dot(axes.c2p(x[i], y[i]), color=RED)

            self.play(Write(entry.set_opacity(1), run_time=0.4))
            self.play(TransformFromCopy(entry, dot))
        self.play(Create(line1))

        self.wait(1)

        self.wait(1)


        self.wait(5)