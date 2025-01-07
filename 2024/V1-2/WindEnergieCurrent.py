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


class WindEnergieCurrent(Scene):
    def construct(self):
        x_min, x_max, x_step = 0, 50, 10
        y_min, y_max, y_step = 0, 1.8, 0.1
        data = ticks_to_exclude(np.arange(y_min, y_max + y_step, y_step), 0.2,1.6)
        axes = Axes(
            x_range=[x_min, x_max + x_step, x_step],
            y_range=[y_min, y_max + y_step, y_step],
            x_axis_config={
                "numbers_to_include": np.arange(x_min, x_max + x_step, x_step),
                "decimal_number_config": {"num_decimal_places": 2},
            },
            y_axis_config={
                #"numbers_to_include": np.arange(y_min, y_max + y_step, y_step),
                "numbers_to_include": data["ticks"],
                "decimal_number_config": {"num_decimal_places": 2},
                "numbers_to_exclude": data["nums"],
                "numbers_with_elongated_ticks": data["ticks"],

            },
        )

        x_label = axes.get_x_axis_label(Text("Distance in cm").scale(0.5))
        y_label = axes.get_y_axis_label(Text("Current in Amp").scale(0.5))
        y_label.shift(LEFT *1)

        x = [0, 10, 20, 30, 40, 50]
        y = [1.69, 0.95, 0.28, 0.11, 0.05, 0.02]
        y2 = [1.5, 0.91, 0.28, 0.1, 0.05, 0.02]
        y_str = [f"{num:.2f}" for num in y]
        y2_str = [f"{num:.2f}" for num in y2]

        title = Text("Current as a Function of Distance")
        title.next_to(axes, UP)
        title.scale(0.7)
        title.shift(UP*0.2)

        line1 = build_line(axes, x, y, color=RED)
        line3 = build_line(axes, x, y2, color=BLUE)






        t_start = Table(
            [y_str],
            row_labels=[Text("Run 1 Amps:"),],
            col_labels=[Text("0cm"), Text("10cm"), Text("20cm"), Text("30cm"), Text("40cm"), Text("50cm")],)

        t_end = Table(
            [y_str,
             y2_str],
            row_labels=[Text("Run 1 Amps:"), Text("Run 2 Amps:")],
            col_labels=[Text("0cm"), Text("10cm"), Text("20cm"), Text("30cm"), Text("40cm"), Text("50cm")],)

        t_start.scale(0.45)
        t_start.get_rows()[1].set_opacity(0)
        entry = t_start.get_entries()[6]
        entry.set_opacity(1)

        t_end.scale(0.45)
        t_end.get_rows()[2].set_opacity(0)
        entry_end = t_end.get_entries()[13]


        # t_start_first_row_pos = t_start.get_rows()[0].get_center()
        # t_end_first_row_pos = t_end.get_rows()[0].get_center()
        # vertical_shift = t_start_first_row_pos[1] - t_end_first_row_pos[1]
        # t_end.shift(UP * vertical_shift)

        t_start.shift(UP*2).shift(RIGHT*1.5)

        # Step 1: Get the position of the first row of t_start
        t_start_first_row_pos = t_start.get_rows()[0].get_center()

        # Step 2: Get the position of the first row of t_end
        t_end_first_row_pos = t_end.get_rows()[0].get_center()

        # Step 3: Calculate the vertical and horizontal shifts needed
        vertical_shift = t_start_first_row_pos[1] - t_end_first_row_pos[1]
        horizontal_shift = t_start_first_row_pos[0] - t_end_first_row_pos[0]

        # Step 4: Apply these shifts to t_end
        t_end.shift(UP * vertical_shift + RIGHT * horizontal_shift)


        self.add(axes, x_label, y_label, title)
        self.add(t_start,entry.set_opacity(1))
        self.wait(1)
        for i in range(7,13,1):
            j=i-7
            entry = t_start.get_entries()[i]
            dot = Dot(axes.c2p(x[j], y[j]), color=RED)

            self.play(Write(entry.set_opacity(1), run_time=0.4))
            self.play(TransformFromCopy(entry, dot))
        self.play(Create(line1))

        self.wait(1)
        self.play(Create(t_end, run_time=1.9), Uncreate(t_start, run_time=2))
        self.play(Create(entry_end.set_opacity(1)))

        self.wait(1)

        for i in range(14,20,1):
            j=i-14
            entry = t_end.get_entries()[i]
            dot = Dot(axes.c2p(x[j], y2[j]), color=BLUE)

            self.play(Write(entry.set_opacity(1), run_time=0.4))
            self.play(TransformFromCopy(entry, dot))

        self.play(TransformFromCopy(line1, line3))
        self.wait(5)