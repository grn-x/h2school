import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter

START_YEAR = 1973
END_YEAR = 2023
path = r'../sources/annual-co2-emissions-per-country/annual-co2-emissions-per-country.csv'
matplotlib.use('Qt5Agg')
# source: https://ourworldindata.org/grapher/annual-co2-emissions-per-country?v=1&csvType=full&useColumnShortNames=false
# https://github.com/grn-x/h2school/blob/main/sources/annual-co2-emissions-per-country/readme.md

world_data = {}
germany_data = {}

for f in open(path, 'r'):
    line = f.strip().split(',')
    if line[0] == 'Germany':
        germany_data.update({line[2]: line[3]})
        """else: #sum values if key exists already
            if line[2] in world_data:
                world_data[line[2]] += line[3]
            else:
                world_data.update({line[2]: line[3]})"""
    if line[0] == 'World':
        world_data.update({line[2]: line[3]})

x_axis = np.arange(START_YEAR, END_YEAR, 1)

wd_key_offset = [START_YEAR - int(next(iter(world_data.keys()))), END_YEAR - int(next(iter(world_data.keys())))]
wd_list = [float(value) for value in list(world_data.values())[wd_key_offset[0]:wd_key_offset[1]:1]]

gd_key_offset = [START_YEAR - int(next(iter(germany_data.keys()))), END_YEAR - int(next(iter(germany_data.keys())))]# needed
# for both seperately since the data source starts tracking the worldwide emission in 1750 and the german emission in 1792
gd_list = [float(value) for value in list(germany_data.values())[gd_key_offset[0]:gd_key_offset[1]:1]]


def millions_formatter(x, _):
    return f'{x / 1e6:.0f}M'


fig, ax1 = plt.subplots(figsize=(12, 6))

ax1.set_xlabel('Year')
ax1.set_ylabel('Germany CO2 Emissions (million tonnes)', color='tab:blue')
ax1.plot(x_axis, gd_list, label='Germany CO2 Emissions', color='tab:blue', marker='o', linestyle='-', markersize=6)
ax1.tick_params(axis='y', labelcolor='tab:blue')
ax1.yaxis.set_major_formatter(FuncFormatter(millions_formatter))

ax2 = ax1.twinx()
ax2.set_ylabel('World CO2 Emissions (million tonnes)', color='tab:red')
ax2.plot(x_axis, wd_list, label='World CO2 Emissions', color='tab:red', marker='s', linestyle='-', markersize=6)
ax2.tick_params(axis='y', labelcolor='tab:red')
ax2.yaxis.set_major_formatter(FuncFormatter(millions_formatter))

scale_text = f"Scale Germany Axis to World Axis: {(max(wd_list) - min(wd_list)) / (max(gd_list) - min(gd_list)):.1f} : 1"
ax1.text(0.25, 0.95, scale_text, transform=ax1.transAxes, fontsize=10, color='black',
         verticalalignment='top', bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))

ax1.set_xticks(np.arange(START_YEAR, END_YEAR + 1, 2))
fig.autofmt_xdate()

ax1.grid(visible=True, linestyle='--', alpha=0.5, which='both', axis='both', linewidth=0.5)

plt.title('World and Germany CO2 Emissions Over Time', pad=20)

table_offset = 2013 - START_YEAR
table_data = [
    [f"{year}", f"{germany / 1e6:.2f}", f"{world / 1e6:.0f}"]
    for year, germany, world in zip(x_axis[table_offset:], gd_list[table_offset:], wd_list[table_offset:])
]

table = plt.table(
    cellText=table_data,
    colLabels=["Year", "GER(MT)", "WLD(MT)"],
    cellLoc="center",
    loc="left",
    bbox=[-0.45, 0.1, 0.3, 0.8],
    colColours=["gray", "lightblue", "lightcoral"],
)

table.auto_set_font_size(False)
table.set_fontsize(10)
table.auto_set_column_width(col=list(range(len(table_data[0]))))  # auto column width

plt.tight_layout()
plt.show()
plt.show()
