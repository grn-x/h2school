# H2@School

## About

This repository contains a collection of scripts used to create and analyze data for our contribution to the H2@School competition.
This multi-stage tournament, hosted by OTH Regensburg, focuses on [global warming](https://www.youtube.com/watch?v=1WCOjiKI8vU&list=PLbyh8sxxqPC6YoN5vQR9Yh3V1dD0inNu7&index=11)
and solutions for transitioning to a more sustainable energy system.

The repository is organized according to the different phases of the contest.

For transparency, as required by the jury, this project is publicly accessible.

> [!NOTE]  
> For this year’s contribution, we created a [website](https://github.com/grn-x/H2Sites) hosted in a different repository.

---

## `2024`

This directory contains my ManimCE workspace.

<details>
<summary>Manim is a feature-rich Python math animation engine</summary>

Originally created by <a href="https://www.3blue1brown.com/">3Blue1Brown's</a> Grant Sanderson, Manim was
initially a personal tool designed to help him create complex, high-quality animations programmatically.

Since then its gotten so powerful that a fork (the <u>C</u>ommunity <u>E</u>dition) of the original project was created to speed up development.

To install it, follow the official instructions in the <a href="https://docs.manim.community/en/stable/installation.html">Manim Community Edition Documentation</a>.

</details>

<br>



This folder is further subdivided into different sections of this stage, each containing multiple scripts.

To run a ManimCE script, navigate to the folder containing the script and use the following command:

```shell
manim -pql script_name.py SceneName
```

### Useful command-line arguments:

- `-p`: Preview the animation after rendering.
- `-ql`: Render in low quality (854x480, 15 FPS) — useful for rapid prototyping.
- `-qm`: Render in medium quality (1280x720, 30 FPS).
- `-qh`: Render in high quality (1920x1080, 60 FPS).
- `-qp`: Render in 2K quality (2560x1440, 60 FPS).
- `-qk`: Render in 4K quality (3840x2160, 60 FPS).
- `-s`: Skip to the end and display only the final frame.
- `-n <number>`: Skip ahead to the n-th animation of a scene.
- `-f`: Show the rendered file in the file browser.

> [!TIP]  
> The `-p` flag can be combined with any quality flag, such as `-pql` for low-quality previews.

### Demo
Small overview of some results:
<!--Make the GIF redirect to the original resolution and smaller-sized MP4. GIFs fucking suck.-->
<a href="https://github.com/user-attachments/assets/d524e1d9-1984-40d3-962e-2f462cfa0638">
  <img src="https://github.com/user-attachments/assets/c649719d-00cb-4bf1-b18c-a36bb26e654b" alt="Manim Demo">
</a>

---

## `2025`

This directory contains simple Matplotlib scripts used for data analysis and visualization. These scripts were essential for our extensive academic paper, as required by the first task of the following year’s competition.

### Demo

<div style="display: flex; justify-content: space-around;">
  <div style="flex: 1; text-align: center;">
    <img src="https://github.com/user-attachments/assets/c6b25b54-61bc-40f7-9fcd-c738049958ec" alt="Matplotlib Visualization" style="height: 200px;">
    <p>Difference in concentration and impact</p>
  </div>
  <div style="flex: 1; text-align: center;">
    <img src="https://github.com/user-attachments/assets/bb67437e-6454-40ca-887c-bcd92c528ae9" alt="Matplotlib Visualization" style="height: 200px;">
    <p>Comparing emission trends</p>
  </div>
</div>