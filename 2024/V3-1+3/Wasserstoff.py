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


class Wasserstoff(Scene):
    def construct(self):
        x_min, x_max, x_step = 0, 6, 1
        y_min, y_max, y_step = 0, 28, 0.5
        x_length = x_max - x_min
        y_length = y_max - y_min
        data = ticks_to_exclude(np.arange(y_min, y_max + y_step, y_step), 0.3,0.5)
        rangex, rangey =[x_min, x_max + x_step, x_step], [y_min, y_max + y_step, y_step]
        axes = Axes(
            x_range=rangex,
            y_range=rangey,
            x_axis_config={
                "numbers_to_include": np.arange(x_min, x_max + x_step, x_step),
                "decimal_number_config": {"num_decimal_places": 0},
            },
            y_axis_config={
                "numbers_to_include": np.arange(y_min, y_max + y_step-1, 2),
                #"numbers_to_include": data["nums"],
                "decimal_number_config": {"num_decimal_places": 0},
                "tick_size": 0.05,
                #"numbers_to_exclude": data["nums"],
                "numbers_with_elongated_ticks": np.arange(y_min, y_max + y_step-1, 2),

            },
        )

        axes_width = axes.get_width()
        axes_height = axes.get_height()

        #adjust step
        rangex_a, rangey_a =[x_min, x_max + x_step, x_step], [0, 14, 1]


        plane = NumberPlane(
            x_range=rangex_a,
            y_range=rangey_a,
            x_length=axes_width-0.6,#0.645
            y_length=axes_height-0.6,#0.8
            axis_config={"include_numbers": False},
            background_line_style={
                "stroke_color": BLUE_D,
                "stroke_width": 2,
                "stroke_opacity": 0.3,
            },
        )


        # Move the NumberPlane to the center of the Axes .move_to(axes.get_center()).
        plane.shift(LEFT*0.02).shift(DOWN*0.064)#0.078
        #plane.get_center().move_to(axes.get_center())
        x_label = axes.get_x_axis_label(Tex("Time in min").scale(0.7))
        y_label = axes.get_y_axis_label(Tex("Volume in cm$^3$").scale(0.7)).shift(LEFT*0.6).shift(UP*0.03)


        x = [0, 1, 2, 3, 4, 5, 6]
        sauerstoff = [0, 2.5, 5, 7.5, 9, 10, 12.5]
        wasserstoff = [0, 5, 9, 12.5, 15, 20, 26.5]
        wasserstoffHalf = [0, 2.5, 4.5, 6.25, 7.5, 10, 13.25]
        current = [0.703 ,0.689, 0.670, 0.644, 0.654, 0.653, 0.645]
        #y2 = [2.810, 2.676, 2.535, 2.309, 2.084, 1.832]
        sauerstoff_str = [f"{num:.1f}" for num in sauerstoff]
        wasserstoff_str = [f"{num:.1f}" for num in wasserstoff]
        current_str = [f"{num:.3f}" for num in current]
        #y2_str = [f"{num:.2f}" for num in y2]

        amperageScalar = (max(wasserstoff) / max(current)) / 1.5
        current = [i * amperageScalar for i in current]






        title = Text("Gas Volume as a Function of Time")
        title.next_to(axes, UP)
        title.scale(0.7)
        title.shift(LEFT+0.2)
        #self.play(Create(axes), Write(x_label), Write(y_label), Write(title))
        line1 = build_line(axes, x, sauerstoff, color=RED)
        line2 = build_line(axes, x, wasserstoff, color=BLUE)
        line3 = build_line(axes, x, wasserstoffHalf, color=PURPLE)
        line4= build_line(axes, x, current, color=GRAY)

        col_labels = [Text(f"{i}min") for i in x]
        if(not(len(col_labels)==len(x)==len(sauerstoff)==len(wasserstoff))):
            print("Number of column labels must match the number of columns")

        print(len(col_labels), "col_labels")
        print(len(x), "x")
        print(len(sauerstoff), "sauerstoff")
        print(len(wasserstoff), "wasserstoff")



        t_start = Table(
            [wasserstoff_str, sauerstoff_str, current_str
             ],
            #row_labels=[Tex("H2 Volume in cm$^3$").scale(1.5), Tex("O2 Volume in cm$^3$").scale(1.5)],
            row_labels=[
                VGroup(MathTex("H_{2}"), MathTex(" Volume\\ in\\ cm^3")).arrange(RIGHT).scale(1.5),
                VGroup(MathTex("O_{2}"), MathTex(" Volume\\ in\\ cm^3")).arrange(RIGHT).scale(1.5),
                VGroup(MathTex("Current\\ in\\ A")).arrange(RIGHT).scale(1.5)
            ],
            col_labels=col_labels, )



        t_start.next_to(title, DOWN).scale(0.3).shift(UP*1.9).shift(LEFT*0.4)
        t_start.get_rows()[1].set_opacity(0)
        t_start.get_rows()[2].set_opacity(0)
        t_start.get_rows()[3].set_opacity(0)

        entry = t_start.get_entries()[len(x)]#label
        entry.set_opacity(1)
        entry = t_start.get_entries()[1+(len(x)*2)]  # label
        entry.set_opacity(1)
        entry = t_start.get_entries()[2+(len(x)*3)]  # label
        entry.set_opacity(1)


        # t_start_first_row_pos = t_start.get_rows()[0].get_center()
        # t_end_first_row_pos = t_end.get_rows()[0].get_center()
        # vertical_shift = t_start_first_row_pos[1] - t_end_first_row_pos[1]
        # t_end.shift(UP * vertical_shift)

        ##t_start.shift(RIGHT * 1)

        t_start_first_row_pos = t_start.get_rows()[0].get_center()


        start_point_h2 = axes.c2p(4, 9)
        end_point_h2 = axes.c2p(6, 9)

        start_point_o2 = axes.c2p(4, 5)
        end_point_o2 = axes.c2p(6, 5)


        #plot the lines 🤩
        line_h2 = Line(start_point_h2, end_point_h2, color=BLUE_B)
        dot_h2 = Dot(start_point_h2, color=BLUE_B)
        line_o2 = Line(start_point_o2, end_point_o2, color=RED_B)
        dot_o2 = Dot(start_point_o2, color=RED_B)




        scalarLabel = Tex("Current values are multiplied by " + str(f"{amperageScalar:.2f}") + " to adapt to the y-scale").scale(0.4).next_to(t_start, DOWN).shift(UP*0.1)
        roomtemperatureLabel = Tex("Room Temperature: 25°C").scale(0.4).next_to(t_start, RIGHT).shift(UP*1.1)
        waterTemperatureLabel = Tex("Water Temperature: 21°C").scale(0.4).next_to(roomtemperatureLabel, DOWN)
        self.add(plane, axes, x_label, y_label, title)
        self.add(t_start, entry.set_opacity(1))
        self.add(scalarLabel, roomtemperatureLabel, waterTemperatureLabel)
        self.wait(1)
        for i in range(len(x)):
            #entry = t_start.get_entries()[i+len(x)+1]
            #entry2 = t_start.get_entries()[i+len(x)*2+1]
            entry= t_start.get_rows()[1][i+1]
            entry2 = t_start.get_rows()[2][i+1]
            entry3 = t_start.get_rows()[3][i+1]
            #print(entry.get_y())
            dot = Dot(axes.c2p(x[i], sauerstoff[i]), color=RED)
            dot2 = Dot(axes.c2p(x[i], wasserstoff[i]), color=BLUE)
            dot3 = Dot(axes.c2p(x[i], current[i]), color=GRAY)

            self.play(Write(entry.set_opacity(1), run_time=0.4),Write(entry2.set_opacity(1), run_time=0.4),Write(entry3.set_opacity(1), run_time=0.4))
            #self.play()
            self.play(TransformFromCopy(entry, dot), TransformFromCopy(entry2, dot2), TransformFromCopy(entry3, dot3))
        self.play(Create(line1), Create(line2), Create(line4))

        self.wait(1)

        self.play(Create(dot_h2), Create(dot_o2))
        self.wait(1)
        self.play(Create(line_h2), Create(line_o2))
        self.wait(2)
        self.play(TransformFromCopy(line2, line3))

        self.wait(5)