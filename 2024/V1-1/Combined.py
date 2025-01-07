import math

from manim import *




class Combined(Scene):

    def construct(self):
        counter = Integer(0)
        interval_rev = 1050  # Update the counter every 500 milliseconds
        interval_time = 0.24

        global eTime_rev
        global eTime_eTime
        global eTime_time

        eTime_rev = 0
        eTime_eTime = 0
        eTime_time = 0

        global end_rev_counter
        end_rev_counter = 0
        global end_eTime_counter
        end_eTime_counter = 0
        global end_time_counter
        end_time_counter = 0

        def updater(m, dt):
            global eTime_rev
            eTime_rev += dt
            if eTime_rev >= interval_rev / 1000 and m.get_value() < 8:
                m.increment_value()
                global end_rev_counter
                end_rev_counter= m.get_value()
                eTime_rev = 0  # Reset the elapsed time7
                print(m.get_value())#necessary print because else the timer doesnt stop? wtf python

        counter.add_updater(updater)
        counter.shift(RIGHT * 4 + UP * 2)
        counter_label = Text("Revolution Counter: ").scale(0.7)
        counter_label.next_to(counter, LEFT)


        start_time = 0.00
        end_time = 0.33
        time_counter = DecimalNumber(end_time)
        time_counter.increment_value(-end_time)
        time_elapsed = 0

        def time_updater(m, dt):
            global eTime_eTime
            eTime_eTime += dt
            if eTime_eTime >= interval_time and m.get_value() < 0.33:
                eTime_eTime = 0
                m.increment_value(0.01)
                global end_eTime_counter
                end_eTime_counter = m.get_value()
                print(m.get_value())#necessary print because else the timer doesnt stop? wtf python

        time_counter.add_updater(time_updater)
        time_counter.next_to(counter, UP)
        time_counter_label = Text("Elapsed Time: ").scale(0.7)
        time_counter_label.next_to(time_counter, LEFT)

        starting_value = 3.13
        end_value = 3.46
        additional_counter = DecimalNumber(end_value)
        additional_counter.increment_value(-(end_value-starting_value))
        additional_elapsed = 0
        def additional_updater(m, dt):
            global eTime_time
            eTime_time += dt
            if eTime_time >= interval_time and m.get_value() < 3.46:
                m.increment_value(0.01)
                global end_time_counter
                end_time_counter = m.get_value()
                eTime_time = 0

        additional_counter.add_updater(additional_updater)
        additional_counter.next_to(time_counter, UP)
        additional_counter_label = Text("Total Time: ").scale(0.7)
        additional_counter_label.next_to(additional_counter, LEFT)

        self.add(counter, counter_label, time_counter, time_counter_label, additional_counter, additional_counter_label)
        self.wait(8.9)
        counter.remove_updater(updater)
        time_counter.remove_updater(time_updater)
        additional_counter.remove_updater(additional_updater)

        additional_counter.set_value(end_time_counter)
        time_counter.set_value(end_eTime_counter)
        counter.set_value(end_rev_counter)


        """question = MathTex("{3", "^x", "+", "63", "\\over", "21", "^{ x-2 }", "+", "7", "^{ x-1 }}").set_color(
            RED_E).to_edge(UL)
        question[5::].set_color(0)
        question[:4:].set_color(0)
        self.play(DrawBorderThenFill(question), run_time=1.6)
        self.wait(1.5)
        self.play(question[5::].set_color(RED_E).animate(run_time=1.5))
        self.wait(1.5)
        self.play(question[:4:].set_color(RED_E).animate(run_time=1.5))
        self.play(question[5::].animate(run_time=1.5).shift(RIGHT * 7 + UP))
        self.wait(1.5)
        ques2 = MathTex("{(7 \cdot 3)}^{ x-2 }", "+", "7", "^{ x-1 }}").set_color(BLUE_D).move_to(question[5::])
        self.play(ReplacementTransform(question[5::], ques2), run_time=3)"""

        frac = MathTex("{0}", "\\over", "{0}")
        frac.next_to(counter_label, DOWN).shift(DOWN*1.01)
        frac[0].set_color(0)
        frac[2].set_color(0)
        self.play(DrawBorderThenFill(frac))
        denominator = MathTex(counter.get_value()).move_to(frac[0])
        numerator = MathTex(round(time_counter.get_value(),2)).move_to(frac[2])

        numerator_value = float(numerator.get_tex_string())
        denominator_value = float(denominator.get_tex_string())
        result_value = round(denominator_value/numerator_value, 2)
        print(str(result_value) + "result")
        print (str(numerator_value) + "numerator")
        print(str(denominator_value) + "denominator")
        result = MathTex("\\approx ", str(result_value)).next_to(frac, RIGHT).shift(RIGHT*0.1)
        resultUnit = MathTex("Hz").next_to(result, RIGHT)

        result2 = MathTex(str(result_value)).next_to(frac, DOWN).set_color(0).shift(DOWN*1.01)
        ###perMinute = MathTex(str(result_value),"\\cdot", "60"," = ", str(result_value*60), "{Rotations \\hspace per \\hspace Minute}").next_to(result2, RIGHT)
        ##perMinute = MathTex(str(result_value), "\\cdot", "60", " = ", str(result_value * 60), "\\newline{\\ Rotations \\, per \\, Minute}").move_to(result2)
        #perMinute = MathTex(str(result_value), r" \, \cdot {} \, 60 = {} \\",           str(math.trunc(round(result_value * 60, 1))),               r"Rotations \, per \, Minute").move_to(result2)
        rpm_value = math.trunc(round(result_value * 60, 1))
        perMinute = MathTex(str(result_value), r" \, \cdot {} \, 60 = {} ",
                            str(rpm_value),
                            r"\\Rotations \, per \, Minute").move_to(result2)
        perMinute[0].set_color(0)

        self.play(
        TransformMatchingShapes(counter.copy(), denominator.set_color(WHITE)),
        ReplacementTransform(time_counter.copy(), numerator.set_color(WHITE)),
        )
        self.play(Write(result))
        self.play(Write(resultUnit))
        self.wait(1.5)
        #self.play(ReplacementTransform(result.copy(), perMinute[0].set_color(WHITE)), Write(perMinute))
        self.play(ReplacementTransform(result.copy(), perMinute[0]), Write(perMinute),
                  perMinute[0].set_color(WHITE).animate(run_time=1.5))
        #self.play(ReplacementTransform(denominator, frac[0].set_color(WHITE)), ReplacementTransform(numerator, frac[2].set_color(WHITE) ))

       # self.play(counter.move_to(frac[0]).animate(run_time=1.5))
        #self.play(time_counter.move_to(frac[2]).animate(run_time=1.5))
        #frac[0].set_value(counter.get_value())
        #frac[2].set_value(time_counter.get_value())
        #self.play(TransformMatchingShapes(counter.copy(), frac[0]), frac[0].set_color(WHITE).animate())
        #self.play(TransformMatchingShapes(time_counter.copy(), frac[2]), frac[2].set_color(WHITE).animate())

        self.wait(4)
        #all visible objects:
        #objects = [counter, counter_label, time_counter, time_counter_label, additional_counter, additional_counter_label, frac, denominator, numerator, result, resultUnit, result2, perMinute]
        objects = [counter, counter_label, time_counter, time_counter_label, additional_counter,
                   additional_counter_label, frac, denominator, numerator, result[0], resultUnit, result2, perMinute[0], perMinute[1], perMinute[3]]#perMinute[2] is the rmp and result[1] is the hz

        Animations = []
        for obj in objects:
            try:
                Animations.append(obj.animate.to_edge(LEFT).shift(LEFT * 10))
            except:
                print(f"Could not move {obj} to the left")
        self.play(*Animations)



        self.part2(perMinute[2], result[1], rpm_value, result_value)





    def part2(self, MathTexPerMinute, MathTexHz, rpm_value, result_value):
        ##### ----- part 2 ----- #####us
        # Create headings
        heading1 = Text("4.1V, 0.5A, 1cm").scale(0.3)
        heading2 = Text("5V, 0.5A, 1cm").scale(0.3)
        heading3 = Text("6V, 0.5A, 1cm").scale(0.3)
        heading4 = Text("6V, 0.5A, 0cm").scale(0.3)

        # Position headings
        heading4.to_edge(UP, UP).shift(UP * 0.5)  # why can i even do this, and why is it that only after shifting its truly aligned at the top??
        heading3.next_to(self.camera.frame_center, UP).shift(UP * 1.6)
        heading2.move_to(self.camera.frame_center, UP).shift(UP * 0.2)
        heading1.to_edge(DOWN, UP).shift(UP * 1.2)

        counter_label = Text("Counter:").scale(0.2)
        time_label = Text("Time:").scale(0.2)
        counter_label.next_to(heading1, DOWN)
        time_label.next_to(counter_label, DOWN)
        counter = MathTex("10").next_to(counter_label, RIGHT).scale(0.3)
        time = MathTex("4.91").next_to(time_label, RIGHT).scale(0.3)
        freq = float(counter.get_tex_string()) / float(
            time.get_tex_string())
        freq_tex = MathTex(
            f"\\frac{{{counter.get_tex_string()}}}{{{time.get_tex_string()}}} \\approx {freq:.2f} \\, \\text{{Hz}}").scale(0.3)
        rpm = freq * 60
        rpm_tex = MathTex(f"{freq:.2f} \\cdot 60 = {rpm:.0f} \\, \\text{{RPM}}").scale(0.3)
        freq_tex.next_to(time_label, DOWN)
        rpm_tex.next_to(freq_tex, DOWN)

        counter_label2 = Text("Counter:").scale(0.2)
        time_label2 = Text("Time:").scale(0.2)
        counter_label2.next_to(heading2, DOWN)
        time_label2.next_to(counter_label2, DOWN)
        counter2 = MathTex("38").next_to(counter_label2, RIGHT).scale(0.3)
        time2 = MathTex("2.74").next_to(time_label2, RIGHT).scale(0.3)
        freq2 = float(counter2.get_tex_string()) / float(
            time2.get_tex_string())
        freq_tex2 = MathTex(
            f"\\frac{{{counter2.get_tex_string()}}}{{{time2.get_tex_string()}}} \\approx {freq2:.2f} \\, \\text{{Hz}}").scale(0.3)
        rpm2 = freq2 * 60
        rpm_tex2 = MathTex(f"{freq2:.2f} \\cdot 60 \\approx {rpm2:.0f} \\, \\text{{RPM}}").scale(0.3)
        freq_tex2.next_to(time_label2, DOWN)
        rpm_tex2.next_to(freq_tex2, DOWN)

        counter_label3 = Text("Counter:").scale(0.2)
        time_label3 = Text("Time:").scale(0.2)
        counter_label3.next_to(heading3, DOWN)
        time_label3.next_to(counter_label3, DOWN)
        counter3 = MathTex("46").next_to(counter_label3, RIGHT).scale(0.3)
        time3 = MathTex("2.36").next_to(time_label3, RIGHT).scale(0.3)
        freq3 = float(counter3.get_tex_string()) / float(
            time3.get_tex_string())
        # freq_tex3 = MathTex(f"\\frac{{{counter3.get_tex_string()}}}{{{time3.get_tex_string()}}} = {freq3:.2f} \\, \\text{{Hz}}")
        freq_tex3 = MathTex(
            f"\\frac{{{counter3.get_tex_string()}}}{{{time3.get_tex_string()}}} \\approx {freq3:.2f} \\, \\text{{Hz}}").scale(0.3)
        rpm3 = freq3 * 60
        rpm_tex3 = MathTex(f"{freq3:.2f} \\cdot 60 \\approx {rpm3:.0f} \\, \\text{{RPM}}").scale(0.3)
        freq_tex3.next_to(time_label3, DOWN)
        rpm_tex3.next_to(freq_tex3, DOWN)

        frequency_label4 = Text("Frequency:").scale(0.2)
        rpm_label4 = Text("RPM:").scale(0.2)
        frequency_label4.next_to(heading4, DOWN)
        rpm_label4.next_to(frequency_label4, DOWN)
        frequency4 = MathTex(str(result_value)).scale(0.3)
        rpm4 = MathTex(str(rpm_value)).scale(0.3)
        #MathTexPerMinute.copy().next_to(frequency_label4, RIGHT).scale(0.01)
        #MathTexHz.copy().next_to(rpm_label4, RIGHT).scale(0.01)

        objects = [heading1, heading2, heading3, heading4, counter_label, time_label, counter_label2, time_label2,
                   counter_label3, time_label3, frequency_label4, rpm_label4]
        for obj in objects:
            obj.to_edge(RIGHT).shift(RIGHT * 1.7)
            obj.to_edge(LEFT).shift(LEFT * 10)
            #obj.shift(LEFT*30)





        Animations = []
        for obj in objects:
            try:
                Animations.append(obj.animate.shift(RIGHT * 19))
            except:
                print(f"Could not move {obj} to the left")
        self.play(*Animations)

        # i need to realign all the lables and values since the moving confused everything
        counter_label.shift(UP*0.1)
        time_label.shift(UP*0.2)
        counter.next_to(counter_label, RIGHT)
        time.next_to(time_label, RIGHT)
        freq_tex.next_to(time_label, DOWN).shift(RIGHT*0.32)
        rpm_tex.next_to(freq_tex, DOWN).shift(RIGHT*0.2)

        counter_label2.shift(UP*0.1)
        time_label2.shift(UP*0.2)
        counter2.next_to(counter_label2, RIGHT)
        time2.next_to(time_label2, RIGHT)
        freq_tex2.next_to(time_label2, DOWN).shift(RIGHT*0.32)
        rpm_tex2.next_to(freq_tex2, DOWN).shift(RIGHT*0.2)

        counter_label3.shift(UP*0.1)
        time_label3.shift(UP*0.2)
        counter3.next_to(counter_label3, RIGHT)
        time3.next_to(time_label3, RIGHT)
        freq_tex3.next_to(time_label3, DOWN).shift(RIGHT*0.32)
        rpm_tex3.next_to(freq_tex3, DOWN).shift(RIGHT*0.2)

        frequency_label4.shift(UP*0.1)
        rpm_label4.shift(UP*0.2)
        frequency4.next_to(frequency_label4, RIGHT)
        rpm4.next_to(rpm_label4, RIGHT)
        frequency4unit = MathTex("Hz").next_to(frequency4, RIGHT).scale(0.3).shift(LEFT*0.4)
        rpm4unit = MathTex("RPM").next_to(rpm4, RIGHT).scale(0.3).shift(LEFT*0.6)

        self.play(Transform(MathTexPerMinute, rpm4), Transform(MathTexHz, frequency4))


        #self.add(heading1, heading2, heading3, heading4, counter_label, time_label, counter_label2, time_label2,                counter_label3,               time_label3, frequency_label4, rpm_label4)

        self.play(Write(counter), Write(time), Write(counter2), Write(time2), Write(counter3), Write(time3), Write(frequency4unit), Write(rpm4unit))

        self.play(Write(freq_tex), Write(freq_tex2), Write(freq_tex3))
        self.play(Write(rpm_tex), Write(rpm_tex2), Write(rpm_tex3))

        self.wait(2)