### I ended up not using this at all
from manim import *
import numpy as np
from scipy.optimize import curve_fit

# Define the function to fit a polynomial of given degree
def fit_polynomial(x, y, degree):
    return np.polyfit(x, y, degree)

# Define your data points
points = np.array([
    (0, 15),
    (1, 9),
    (2, 2.8),
    (3, 1),
    (4, 0.5),
    (5, 0.2)
])

# Separate the points into x and y components
x_data = points[:, 0]
y_data = points[:, 1]

# Fit polynomials of various degrees and calculate their RSS
min_rss = float('inf')
best_degree = 0
best_params = None

for degree in range(1, 6):  # Try polynomial degrees from 1 to 5
    params = fit_polynomial(x_data, y_data, degree)
    p = np.poly1d(params)
    rss = np.sum((p(x_data) - y_data) ** 2)
    if rss < min_rss:
        min_rss = rss
        best_degree = degree
        best_params = params

# Create a string representation of the polynomial
poly_str = np.poly1d(best_params)
print(f"Best degree: {best_degree}")
print(f"Polynomial: {poly_str}")

# Create a Manim scene
class Approximation(Scene):
    def construct(self):
        # Axes
        axes = Axes(
            x_range=[0, 6, 1],
            y_range=[0, 16, 1],
            axis_config={"include_numbers": True}
        )

        # Plot the points
        dots = VGroup(*[
            Dot(axes.coords_to_point(x, y), color=BLUE)
            for x, y in points
        ])

        # Plot the fitted polynomial function
        p = np.poly1d(best_params)
        graph = axes.plot(p, color=RED)

        # Add labels for clarity
        axes_labels = axes.get_axis_labels(x_label="x", y_label="y")

        # Add the polynomial function as a text label
        poly_text = Text(f"Best polynomial: {poly_str}", font_size=24)
        poly_text.next_to(axes, DOWN)

        # Add all elements to the scene
        self.play(Create(axes), Write(axes_labels))
        self.play(Create(dots))
        self.play(Create(graph))
        self.play(Write(poly_text))
        self.wait()

# To render the scene, save this code in a file (e.g., `approximation.py`), then run:
# manim -pql approximation.py Approximation
