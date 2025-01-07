# Sources: https://www.ipcc.ch/report/ar6/wg1/#FullReport
# https://www.ipcc.ch/sr15/
# https://www.ipcc.ch/report/ar6/wg1/downloads/report/IPCC_AR6_WGI_AnnexIII.pdf
# https://www.ipcc.ch/site/assets/uploads/2018/02/WG1AR5_all_final.pdf
import matplotlib
# GWP Explanation: https://en.wikipedia.org/wiki/Global_warming_potential
# GWP Values: https://ghgprotocol.org/sites/default/files/2024-08/Global-Warming-Potential-Values%20%28August%202024%29.pdf
import matplotlib.pyplot as plt
matplotlib.use('Qt5Agg')

import matplotlib.pyplot as plt

# GWP concentration data 2019
gas_gwp_ppt_dict = {
    ('CO2', 1): 410 * 10 ** 6,
    ('CH4', 25): 1866 * 10 ** 3,
    ('N2O', 273): 332 * 10 ** 3,
    ('HCFC-22', 1960): 247,
    ('CFC-11', 6230): 226,
    ('HFC-134a', 1530): 107.6,
    ('CF4 ', 7380): 85.5,
    ('CCl4', 2200): 78,
    ('CFC-113', 6520): 70,
    ('HFC-23', 14600): 32.4,
    ('HFC-125', 3740): 29.4,
    ('HCFC-141b', 860): 24.4,
    ('HFC-143a', 5810): 24,
    ('HCFC-142b', 2300): 22.3,
    ('HFC-32', 771): 20,
    ('CFC-114', 9430): 16,
    ('SF6', 24300): 9.95,
    ('CFC-115', 9600): 8.67,
    ('HFC-152a', 164): 7.1,
    ('C2F6', 12400): 4.85,
    ('CFC-13', 16200): 3.28,
    ('SO2F2', 4630): 2.5,
    ('NF3', 17400): 2.05,
    ('CH3CCl3', 161): 1.6
}

# GWP concentration data 1750 (pre-industrial, commonly used as baseline)
gas_gwp_ppt_dict_1750 = {
    ('CO2', 1): 278 * 10 ** 6,
    ('CH4', 25): 700 * 10 ** 3,
    ('N2O', 273): 270 * 10 ** 3,
    ('HCFC-22', 1960): 0,
    ('CFC-11', 6230): 0,
    ('HFC-134a', 1530): 0,
    ('CF4 ', 7380): 40,
    ('CCl4', 2200): 0,
    ('CFC-113', 6520): 0,
    ('HFC-23', 14600): 0,
    ('HFC-125', 3740): 0,
    ('HCFC-141b', 860): 0,
    ('HFC-143a', 5810): 0,
    ('HCFC-142b', 2300): 0,
    ('HFC-32', 771): 0,
    ('CFC-114', 9430): 0,
    ('SF6', 24300): 0,
    ('CFC-115', 9600): 0,
    ('HFC-152a', 164): 0,
    ('C2F6', 12400): 0,
    ('CFC-13', 16200): 0,
    ('SO2F2', 4630): 0,
    ('NF3', 17400): 0,
    ('CH3CCl3', 161): 0
}

#calculate difference between 2019 and 1750
#gas_gwp_ppt_dict = {gas: (gwp, ppt - gas_gwp_ppt_dict_1750[(gas, gwp)]) for (gas, gwp), ppt in gas_gwp_ppt_dict_2019.items()}
"""gas_gwp_ppt_dict = {
    (gas, gwp): ppt_2019 - gas_gwp_ppt_dict_1750.get((gas, gwp), 0)
    for (gas, gwp), ppt_2019 in gas_gwp_ppt_dict_2019.items()
}"""

absolute_gwp_dict = {gas: gwp * ppt for (gas, gwp), ppt in gas_gwp_ppt_dict.items()}
absolute_ppm_dict = {gas: ppt for (gas, gwp), ppt in gas_gwp_ppt_dict.items()}

sorted_gwp = dict(sorted(absolute_gwp_dict.items(), key=lambda x: x[1], reverse=True))
sorted_ppm = dict(sorted(absolute_ppm_dict.items(), key=lambda x: x[1], reverse=True))

labels_gwp = list(sorted_gwp.keys())
sizes_gwp = list(sorted_gwp.values())

labels_ppm = list(sorted_ppm.keys())
sizes_ppm = list(sorted_ppm.values())

colors = plt.cm.tab20c(range(len(gas_gwp_ppt_dict))) # the color fuck doesnt work when rearranging the elements TODO

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

wedges1, texts1 = ax1.pie(sizes_ppm, labels=None, colors=colors, startangle=140)
ax1.set_title("GH-Gas Emission Surplus in Atmosphere since 1750\nMeasured in 2019 (in PPM)")

wedges2, texts2 = ax2.pie(sizes_gwp, labels=None, colors=colors, startangle=140)
ax2.set_title("Absolute Global Warming Potential")
ax2.set_position([0.45, 0.1, 0.4, 0.8])  # [left, bottom, width, height]

def format_label_ppm(label, size, max_label_length):
    if label == "CO2":
        value = f"{size/10e6:.1f} x 10^9"
    elif label == "CH4":
        value = f"{size/10e3:.1f} x 10^3"
    elif label == "N2O":
        value = f"{size/10e3:.1f} x 10^3"
    else:
        value = f"{size:.1f}"
    #return f"{label.ljust((max_label_length))}: {value}"
    #return f"{label.ljust((max_label_length + len(label)))}: {value}"
    #spaces = ' ' * (max_label_length - len(label))
    #return f"{label}:{spaces} {value}"
    #width = Font().get_width(label)
    #return [label, value] #im giving up on the table idea, doesnt work sadly
    return f"{label}:{' '*max_label_length} {value}"

def format_label_gwp(label, size, max_label_length):
    if label == "CO2":
        value = f"{size/10e6:.1f} / 10^3"
    elif label == "CH4":
        value = f"{size/10e6:.1f} / 10^3"
    elif label == "N2O":
        value = f"{size/10e6:.1f} / 10^3"
    elif label == "CH3CCl3":
        value = f"{size / 10e3:.3f}"
    else:
        value = f"{size/10e3:.2f}"
    #return f"{label.ljust((max_label_length))}: {value}"
    #return f"{label.ljust((max_label_length + len(label)))}: {value}"
    #spaces = ' ' * (max_label_length - len(label))
    #return f"{label}:{spaces} {value}"
    #width = Font().get_width(label)
    #return [label, value] #im giving up on the table idea, doesnt work sadly
    return f"{label}:{' '*max_label_length} {value}"


#legend_labels_ppm = [f"{label}: {size:.2e}" for label, size in zip(labels_ppm, sizes_ppm)]
#legend_labels_ppm = [f"{label}: {size*10e5:.1f}" for label, size in zip(labels_ppm, sizes_ppm)]
#legend_labels_ppm = [format_label(label, size) for label, size in zip(labels_ppm, sizes_ppm)]

max_label_length_ppm = max(len(label) for label in labels_ppm)

legend_labels_ppm = [format_label_ppm(label, size, max_label_length_ppm) for label, size in zip(labels_ppm, sizes_ppm)]
"""
table_data_ppm = [
    [label, f"{size/10e6:.1f} x 10^9"] if label == "CO2" else
    [label, f"{size/10e3:.1f} x 10^6"] if label == "CH4" else
    [label, f"{size*10e3:.1f} x 10^3"] if label == "N2O" else
    [label, f"{size*10e5:.1f}"]
    for label, size in zip(labels_ppm, sizes_ppm)
]

# Create the table for PPM values with invisible lines
table_ppm = plt.table(
    cellText=table_data_ppm,
    cellLoc="center",
    loc="right",
    bbox=[1.05, 0.1, 0.3, 0.8],  # [left, bottom, width, height]
    edges='',
)

# Set the font size for the table
table_ppm.auto_set_font_size(False)
table_ppm.set_fontsize(10)
table_ppm.auto_set_column_width(col=list(range(len(table_data_ppm[0]))))

# Add the legend title outside of the table
ax1.legend(wedges1, table_ppm, title="in PPM", loc="upper right", bbox_to_anchor=(0, 1))####///why dont you like that

# Adjust layout
plt.tight_layout()
plt.show()



"""

max_label_length_gwp = max(len(label) for label in labels_ppm)
legend_labels_gwp = [format_label_gwp(label, size, max_label_length_gwp) for label, size in zip(labels_gwp, sizes_gwp)]

ax1.legend(wedges1, legend_labels_ppm, title="Concentration in ATM in PPT", loc="upper right", bbox_to_anchor=(0, 1))
ax2.legend(wedges2, legend_labels_gwp, title="in GWP x PPM / 10^3", loc="upper right", bbox_to_anchor=(0, 1))

plt.tight_layout()
plt.show()