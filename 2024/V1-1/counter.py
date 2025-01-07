import math

from manim import *




class Counter(Scene):
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
            if eTime_rev >= interval_rev / 1000 and m.get_value() < 8:  # Convert interval to seconds
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
        time_counter.next_to(counter, UP)  # Position the time counter above the existing counter
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
        perMinute = MathTex(str(result_value), r" \, \cdot {} \, 60 = {} ",
                            str(math.trunc(round(result_value * 60, 1))),
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