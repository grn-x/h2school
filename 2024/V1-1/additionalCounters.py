from manim import *

config.frame_size = (2160, 3840)

class addCounters(Scene):
    CONFIG = {
        "camera_config": {"aspect_ratio": 16.0 / 9.0},
    }

    def construct(self):
        heading1 = Text("4.1V, 0.5A, 1cm").scale(1.1)
        heading2 = Text("5V, 0.5A, 1cm").scale(1.1)
        heading3 = Text("6V, 0.5A, 1cm").scale(1.1)
        heading4 = Text("6V 0.5A 0cm").scale(1.1)

        heading4.to_edge(UP,UP).shift(UP*6)#why can i even do this, and why is it that only after shifting its truly aligned at the top??
        heading3.next_to(self.camera.frame_center, UP).shift(UP*3)
        heading2.move_to(self.camera.frame_center, UP).shift(DOWN*2)
        heading1.to_edge(DOWN, UP).shift(DOWN*5)


        counter_label = Text("Counter:").scale(0.75)
        time_label = Text("Time:").scale(0.75)
        counter_label.next_to(heading1, DOWN)
        time_label.next_to(counter_label, DOWN)
        counter = MathTex("10").next_to(counter_label, RIGHT)
        time = MathTex("4.91").next_to(time_label, RIGHT)
        freq = float(counter.get_tex_string()) / float(time.get_tex_string())  # Convert the time to float and calculate the frequency
        freq_tex = MathTex(f"\\frac{{{counter.get_tex_string()}}}{{{time.get_tex_string()}}} \\approx {freq:.2f} \\, \\text{{Hz}}")
        rpm = freq * 60
        rpm_tex = MathTex(f"{freq:.2f} \\cdot 60 = {rpm:.0f} \\, \\text{{RPM}}")
        freq_tex.next_to(time_label, DOWN)
        rpm_tex.next_to(freq_tex, DOWN)


        counter_label2 = Text("Counter:").scale(0.75)
        time_label2 = Text("Time:").scale(0.75)
        counter_label2.next_to(heading2, DOWN)
        time_label2.next_to(counter_label2, DOWN)
        counter2 = MathTex("38").next_to(counter_label2, RIGHT)
        time2 = MathTex("2.74").next_to(time_label2, RIGHT)
        freq2 = float(counter2.get_tex_string()) / float(time2.get_tex_string())  # Convert the time to float and calculate the frequency
        freq_tex2 = MathTex(f"\\frac{{{counter2.get_tex_string()}}}{{{time2.get_tex_string()}}} \\approx {freq2:.2f} \\, \\text{{Hz}}")
        rpm2 = freq2 * 60
        rpm_tex2 = MathTex(f"{freq2:.2f} \\cdot 60 \\approx {rpm2:.0f} \\, \\text{{RPM}}")
        freq_tex2.next_to(time_label2, DOWN)
        rpm_tex2.next_to(freq_tex2, DOWN)

        counter_label3 = Text("Counter:").scale(0.75)
        time_label3 = Text("Time:").scale(0.75)
        counter_label3.next_to(heading3, DOWN)
        time_label3.next_to(counter_label3, DOWN)
        counter3 = MathTex("46").next_to(counter_label3, RIGHT)
        time3 = MathTex("2.36").next_to(time_label3, RIGHT)
        freq3 = float(counter3.get_tex_string()) / float(time3.get_tex_string())  # Convert the time to float and calculate the frequency
        #freq_tex3 = MathTex(f"\\frac{{{counter3.get_tex_string()}}}{{{time3.get_tex_string()}}} = {freq3:.2f} \\, \\text{{Hz}}")
        freq_tex3 = MathTex(f"\\frac{{{counter3.get_tex_string()}}}{{{time3.get_tex_string()}}} \\approx {freq3:.2f} \\, \\text{{Hz}}")
        rpm3 = freq3 * 60
        #rpm_tex3 = MathTex(f"{freq3:.2f} \\cdot 60 = {rpm3:.2f} \\, \\text{{RPM}}")
        rpm_tex3 = MathTex(f"{freq3:.2f} \\cdot 60 \\approx {rpm3:.0f} \\, \\text{{RPM}}")
        freq_tex3.next_to(time_label3, DOWN)
        rpm_tex3.next_to(freq_tex3, DOWN)

        frequency_label4 = Text("Frequency:").scale(0.75)
        rpm_label4 = Text("RPM:").scale(0.75)
        frequency_label4.next_to(heading4, DOWN)
        rpm_label4.next_to(frequency_label4, DOWN)

        self.add(heading1, heading2, heading3, heading4, counter_label, time_label, counter_label2, time_label2, counter_label3,
                 time_label3, frequency_label4, rpm_label4)
        self.play(Write(counter), Write(time), Write(counter2), Write(time2), Write(counter3), Write(time3))


        self.play(Write(freq_tex), Write(freq_tex2), Write(freq_tex3))
        self.play(Write(rpm_tex), Write(rpm_tex2),Write(rpm_tex3))

        self.wait(2)