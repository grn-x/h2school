import matplotlib.pyplot as plt
from matplotlib.patches import Patch

import numpy as np

# ==============================================================================
# Konfiguration
# ==============================================================================
#
# 1. COMBINE_SECTORS (True/False)
#    - False:   2 Kuchendiagramme pro Sektor (erneuerbare vs fossils nebeinander)
#    - True:    1 gemeinsames Diagramm pro Sektor mit allen Energiequellen
#
# 2. SHOW_LABELS_ON_CHART (True/False)
#    - True:    Segmentbeschriftungen werden direkt in die Sektoren im Diagramm geschrieben
#    - False:   Segmentnamen werden lediglich in Legende am linken Rad erwähnt
#    - Prozent-beschriftungen bleiben von dieser Flag unverändert und würden in jedem Fall ins Chart geschrieben
#
# 3. CRAMMING_THRESHOLD (int; z.b. 8.0)
#    - Schwellwert; bestimmt "große" vs "kleine" Segmente
#    - Beinflusst Verhalten nur, wenn AVOID_PERCENTAGE_CRAMMING oder USE_LEGEND_FOR_SMALL_VALUES True ist
#    - Genaues Verhalten siehe 4. & 5.
#
# 4. AVOID_PERCENTAGE_CRAMMING (True/False) - Inaktiv(!) wenn USE_LEGEND_FOR_SMALL_VALUES True ist
#    - False: "Standart"-Verhalten: alle labels/Prozentbeschriftungen werden unabhängig von ihrer Größe gleich behandelt
#    - True: Veränderte Positionierung um hoffentlich label-clipping zu verhindern:
#      * Bei großen Segmenten (>= threshold) ist genug Platz und die Labels und/oder Prozente bleiben im Chart
#      * Bei kleinen Segmenten (< threshold) ist zu wenig Platz und die Labels und/oder Prozente werden außerhalb des
#                                                       Diagramms in Form von Tafeln angezeigt und per Linie verbunden
#      * Funktioniert mit SHOW_LABELS_ON_CHART = True (Labels im Diagramm) und False (Labels in der Legende)
#
# 5. USE_LEGEND_FOR_SMALL_VALUES (True/False) - Überschreibt(!) AVOID_PERCENTAGE_CRAMMING
#    - False: "Normales" Beschriftungsverhalten; siehe Flags 2. und 4. oben
#    - True: Platzsparender bei kleinen Werten
#      * Bei großen Segmenten (>= threshold) werden die Prozentbeschriftungen in die Segmente geschrieben Large segments (≥ threshold): Show percentage labels ON the chart
#      * Bei kleinen kleinen Segmenten (< threshold) werden die Prozente nur in der Legende erwähnt! Sie werden weder
#                                       ins Chart geschrieben, noch außerhalb gerendert und per Linie verbunden!
#      * Diese Option erzeugt immer eine Legende; SHOW_LABELS_ON_CHART kontrolliert unverändert ob die
#                                             Segmentbeschriftungen auf dem Chart vorkommen oder nicht
#
# ==============================================================================
#   Grober Aufbau:
#
#   Der Programmeinstieg erfolgt Script-gemäß gegen Ende der Datei
#   Basierend auf der COMBINE_SECTORS Flag wird entweder create_sector_pie_charts
#   oder create_combined_sector_pie_chart aufgerufen, welche dann wiederum jeweils
#   entweder sub_plot_pie_legend oder sub_plot_pie_labels ausführen
#
#   Dabei werden die Plot-Objekte (matplotlibs axs') unten im offenen Skriptabschnitt instantiert,
#   die Referenzen dann an die Methodenkette durchgereicht und dort bearbeitet
#


SHOW_LABELS_ON_CHART = False  # Set to False to use legend instead
COMBINE_SECTORS = True  # Set to True to show one combined pie chart per sector
AVOID_PERCENTAGE_CRAMMING = True  # Set to True to move labels below threshold outside
CRAMMING_THRESHOLD = 8.0  # Percentage threshold; labels below this go outside
USE_LEGEND_FOR_SMALL_VALUES = True  # Set to True to omit small values from chart, show only in legend

# Farbpalette; Blau für Erneuerbare und Rot für Fossile
BLUE_PALETTE = ['#1f77b4', '#5DA5DA', '#60B5E8', '#8EC5E8', '#B8D9F0', '#D9EAF7']
RED_PALETTE = ['#d62728', '#E85D5D', '#F08080', '#F5A3A3', '#FFC0C0', '#FFD9D9']

# ==============================================================================
# Rohdaten
# ======================== 1) Stromsektor
strom_renewable = {
    'Windkraft': 136.0,
    'Biogas': 28.1,
    'Photovoltaik': 59.5,
    'Wasserkraft': 20.4
}

strom_fossil = {
    'Kohle': 97.2,
    'Erdgas': 64.1,
    'Kernenergie': 0.0
}

# ======================== 2) VERKEHRSSEKTOR (Transport Sector)
# Erneuerbare in kWh, Fossile in Mio. t SKE TODO

verkehr_renewable = {
    'Biodiesel': 21.1,
    'Bioethanol': 9.1,
    'Biomethan': 3.5,
    'Erneuerbarer Strom': 9.2
}

verkehr_fossil = {
    'Mineralöle': 78.2,
    'Gase': 0.1,
    'Erdgas/Erdölgas': 0.1,
    'Strom': 2.1
}


# ======================== 3) Wärmesektor
waerme_renewable = {
    'Feste Biomasse': 121.7,
    'Flüssige Biomasse': 2.2,
    'Gasförmige Biomasse': 22.6,
    'Biogener Abfall': 14.5,
    'Solarthermie': 8.8,
    'Geothermie/Umweltwärme': 21.7
}

# Rohdaten in PetaJoule; PJ_TO_TWH Konstante zur Umwandlung in Terrawattstunden
# für einheitliche Vergleichsmetrik
PJ_TO_TWH = 0.2778
waerme_fossil = {
    'Mineralöl': 569.8 * PJ_TO_TWH,
    'Gase': 1899.3 * PJ_TO_TWH,
    'Strom': 404.9 * PJ_TO_TWH,
    'Fernwärme': 383.7 * PJ_TO_TWH,
    'Kohlen': 351.4 * PJ_TO_TWH,
    'Sonstige': 72.6 * PJ_TO_TWH
}


# ============================================================================
# Plots
# ============================================================================
def sub_plot_pie_legend(ax, sizes, labels, colors, threshold, show_labels=True):
    """
    Untermethode für Kuchendiagramm mit Legende
    und zusätzlich großen Werten in Kreissegmenten
    """
    total = sum(sizes)
    percentages = [(size / total) * 100 for size in sizes]

    large_indices = [i for i, pct in enumerate(percentages) if pct >= threshold]
    #deprecated
    #small_indices = [i for i, pct in enumerate(percentages) if pct < threshold]

    # pie chart with all segments
    def autopct_format(pct):
        # show percentage if >= threshold
        for i, p in enumerate(percentages):
            if abs(pct - p) < 0.01:
                if i in large_indices:
                    return f'{pct:.1f}%' # => result if larger
                else:
                    return ''  # => no label for small segments
        return ''

    if show_labels:
        wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors,
                                          autopct=autopct_format, startangle=90,
                                          wedgeprops=dict(edgecolor='white', linewidth=1.5))
    else:
        wedges, texts, autotexts = ax.pie(sizes, colors=colors,
                                          autopct=autopct_format, startangle=90,
                                          wedgeprops=dict(edgecolor='white', linewidth=1.5))

    for autotext in autotexts:
        if autotext.get_text():
            autotext.set_color('white')
            autotext.set_fontweight('bold')

    legend_labels = []
    legend_colors = []

    # Keep order when adding value-color combinations
    for i, (label, pct, color) in enumerate(zip(labels, percentages, colors)):
        legend_labels.append(f'{pct:.1f}% - {label}')
        legend_colors.append(color)

    legend_patches = [Patch(facecolor=color, edgecolor='white') for color in legend_colors]

    ax.legend(legend_patches, legend_labels, loc='center left',
              bbox_to_anchor=(-0.5, 0.5), fontsize=8, framealpha=0.9)


def sub_plot_pie_labels(ax, sizes, labels, colors, threshold, show_labels=True):
    """
    Untermethode für Kuchendiagramm mit Labels anstatt Prozente in Legende
    - Bei großen Segmenten (>= threshold) werden die Prozente in den Segmenten angezeigt
    - Bei kleinen Segmenten (< threshold) werden die Prozente außerhalb platziert
                                            und per Linie mit Segmentrand verbunden
    - Wenn show_labels == True werden zusätzlich die Segmentnamen ins Diagramm geschrieben
        bzw außerhalb platziert und per Linie verbunden, ansonsten werden nur die Prozentzahlen gerendert
    """
    total = sum(sizes)
    percentages = [(size / total) * 100 for size in sizes]

    # create pie chart without labels first
    wedges, texts = ax.pie(sizes, colors=colors, startangle=90,
                           wedgeprops=dict(width=1, edgecolor='white', linewidth=1.5))

    # track external label positions for collision detection
    external_labels_left = []
    external_labels_right = []

    # first run: add all labels
    temp_external_labels = []

    for i, (wedge, label, pct, size) in enumerate(zip(wedges, labels, percentages, sizes)):
        angle = (wedge.theta2 - wedge.theta1) / 2 + wedge.theta1

        if pct >= threshold: # large segment:
            # put percentage inside pie sector
            x = wedge.r * 0.7 * np.cos(np.radians(angle))
            y = wedge.r * 0.7 * np.sin(np.radians(angle))
            ax.text(x, y, f'{pct:.1f}%', ha='center', va='center',
                    fontsize=9, fontweight='bold', color='white')

            if show_labels:
                # put sector name label on the edge, inside
                x_label = wedge.r * 0.85 * np.cos(np.radians(angle))
                y_label = wedge.r * 0.85 * np.sin(np.radians(angle))
                ax.text(x_label, y_label, label, ha='center', va='center',
                        fontsize=8, fontweight='normal', color='white')
        else: # small segment:
            # percentage text will be placed outside
            if show_labels:
                text_content = f'{label}\n{pct:.1f}%'
            else:
                text_content = f'{pct:.1f}%'

            temp_external_labels.append({
                'angle': angle,
                'wedge': wedge,
                'text': text_content,
                'pct': pct
            })

    # second run: place external labels with "collision detection"
    for item in temp_external_labels:
        angle = item['angle']
        wedge = item['wedge']
        text_content = item['text']

        # avoid clipping? //TODO
        base_x = wedge.r * 1.5 * np.cos(np.radians(angle))
        base_y = wedge.r * 1.5 * np.sin(np.radians(angle))

        is_right = base_x >= 0
        ha = 'left' if is_right else 'right'

        target_y = base_y
        label_height = 0.15

        if is_right:
            for existing_y, existing_height, _ in external_labels_right:
                if abs(target_y - existing_y) < (label_height + existing_height) / 2 + 0.05:
                    if target_y > 0:
                        target_y = existing_y + (label_height + existing_height) / 2 + 0.05
                    else:
                        target_y = existing_y - (label_height + existing_height) / 2 - 0.05
            external_labels_right.append((target_y, label_height, text_content))
        else:
            for existing_y, existing_height, _ in external_labels_left:
                if abs(target_y - existing_y) < (label_height + existing_height) / 2 + 0.05:
                    if target_y > 0:
                        target_y = existing_y + (label_height + existing_height) / 2 + 0.05
                    else:
                        target_y = existing_y - (label_height + existing_height) / 2 - 0.05
            external_labels_left.append((target_y, label_height, text_content))

        # draw connecting line from wedge to label with "dent"
        x_line_start = wedge.r * 1.0 * np.cos(np.radians(angle))
        y_line_start = wedge.r * 1.0 * np.sin(np.radians(angle))
        x_line_mid = wedge.r * 1.35 * np.cos(np.radians(angle))
        y_line_mid = wedge.r * 1.35 * np.sin(np.radians(angle))

        ax.plot([x_line_start, x_line_mid], [y_line_start, y_line_mid],
                color='gray', linewidth=1, linestyle='-', alpha=0.6)
        ax.plot([x_line_mid, base_x], [y_line_mid, target_y],
                color='gray', linewidth=1, linestyle='-', alpha=0.6)

        ax.text(base_x, target_y, text_content, ha=ha, va='center',
                fontsize=8, fontweight='normal',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                          edgecolor='gray', alpha=0.9))

    ax.set_xlim(-1.9, 1.9)
    ax.set_ylim(-1.9, 1.9)


def create_sector_pie_charts(renewable_data, fossil_data, sector_name, renewable_unit, fossil_unit, ax1, ax2):
    """
    ZWEI Kuchendiagramme, jeweils eines erneuerbar und eines fossil erstellen
    """
    labels_ren = list(renewable_data.keys())
    sizes_ren = list(renewable_data.values())
    colors_ren = BLUE_PALETTE[:len(labels_ren)]

    labels_fos = list(fossil_data.keys())
    sizes_fos = list(fossil_data.values())
    colors_fos = RED_PALETTE[:len(labels_fos)]

    # Erneuerbare
    if USE_LEGEND_FOR_SMALL_VALUES:
        sub_plot_pie_legend(ax1, sizes_ren, labels_ren, colors_ren,
                            CRAMMING_THRESHOLD, show_labels=SHOW_LABELS_ON_CHART)
    elif SHOW_LABELS_ON_CHART:
        if AVOID_PERCENTAGE_CRAMMING:
            sub_plot_pie_labels(ax1, sizes_ren, labels_ren, colors_ren, CRAMMING_THRESHOLD, show_labels=True)
        else:
            wedges1, texts1, autotexts1 = ax1.pie(sizes_ren, labels=labels_ren, colors=colors_ren,
                                                  autopct='%1.1f%%', startangle=90)
            for autotext in autotexts1:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
    else:
        if AVOID_PERCENTAGE_CRAMMING:
            sub_plot_pie_labels(ax1, sizes_ren, labels_ren, colors_ren, CRAMMING_THRESHOLD, show_labels=False)
            ax1.legend(labels_ren, loc='center left', bbox_to_anchor=(-0.5, 0.5), fontsize=8, framealpha=0.9)
        else:
            wedges1, texts1, autotexts1 = ax1.pie(sizes_ren, colors=colors_ren,
                                                  autopct='%1.1f%%', startangle=90)
            ax1.legend(labels_ren, loc="best", fontsize=8)
            for autotext in autotexts1:
                autotext.set_color('white')
                autotext.set_fontweight('bold')

    total_ren = sum(sizes_ren)
    ax1.set_title(f'Erneuerbare Energien\n{total_ren:.1f} {renewable_unit}',
                  fontsize=11, fontweight='bold', color='#1f77b4')

    # Fossile
    if USE_LEGEND_FOR_SMALL_VALUES:
        sub_plot_pie_legend(ax2, sizes_fos, labels_fos, colors_fos,
                            CRAMMING_THRESHOLD, show_labels=SHOW_LABELS_ON_CHART)
    elif SHOW_LABELS_ON_CHART:
        if AVOID_PERCENTAGE_CRAMMING:
            sub_plot_pie_labels(ax2, sizes_fos, labels_fos, colors_fos, CRAMMING_THRESHOLD, show_labels=True)
        else:
            wedges2, texts2, autotexts2 = ax2.pie(sizes_fos, labels=labels_fos, colors=colors_fos,
                                                  autopct='%1.1f%%', startangle=90)
            for autotext in autotexts2:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
    else:
        if AVOID_PERCENTAGE_CRAMMING:
            sub_plot_pie_labels(ax2, sizes_fos, labels_fos, colors_fos, CRAMMING_THRESHOLD, show_labels=False)
            ax2.legend(labels_fos, loc='center left', bbox_to_anchor=(-0.5, 0.5), fontsize=8, framealpha=0.9)
        else:
            wedges2, texts2, autotexts2 = ax2.pie(sizes_fos, colors=colors_fos,
                                                  autopct='%1.1f%%', startangle=90)
            ax2.legend(labels_fos, loc="best", fontsize=8)
            for autotext in autotexts2:
                autotext.set_color('white')
                autotext.set_fontweight('bold')

    total_fos = sum(sizes_fos)
    ax2.set_title(f'Fossile Energien\n{total_fos:.1f} {fossil_unit}',
                  fontsize=11, fontweight='bold', color='#d62728')


def create_combined_sector_pie_chart(renewable_data, fossil_data, sector_name, unit, ax):
    """
    EIN Kuchendiagramm mit erneuerbaren UND fossilen Energieträgern erstellen
    """
    labels = list(renewable_data.keys()) + list(fossil_data.keys())
    sizes = list(renewable_data.values()) + list(fossil_data.values())
    colors = BLUE_PALETTE[:len(renewable_data)] + RED_PALETTE[:len(fossil_data)]

    total = sum(sizes)

    if USE_LEGEND_FOR_SMALL_VALUES:
        sub_plot_pie_legend(ax, sizes, labels, colors,
                            CRAMMING_THRESHOLD, show_labels=SHOW_LABELS_ON_CHART)
    elif SHOW_LABELS_ON_CHART:
        if AVOID_PERCENTAGE_CRAMMING:
            sub_plot_pie_labels(ax, sizes, labels, colors, CRAMMING_THRESHOLD, show_labels=True)
        else:
            wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors,
                                              autopct='%1.1f%%', startangle=90)
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
                autotext.set_fontsize(8)
    else:
        if AVOID_PERCENTAGE_CRAMMING:
            sub_plot_pie_labels(ax, sizes, labels, colors, CRAMMING_THRESHOLD, show_labels=False)
            ax.legend(labels, loc='center left', bbox_to_anchor=(-0.5, 0.5), fontsize=7, framealpha=0.9)
        else:
            wedges, texts, autotexts = ax.pie(sizes, colors=colors,
                                              autopct='%1.1f%%', startangle=90)
            ax.legend(labels, loc="best", fontsize=7)
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
                autotext.set_fontsize(8)

    ren_total = sum(renewable_data.values())
    fos_total = sum(fossil_data.values())
    ren_percent = 100 * ren_total / total
    fos_percent = 100 * fos_total / total

    ax.set_title(f'{sector_name}\n{total:.1f} {unit}\n' +
                 f'Erneuerbar: {ren_percent:.1f}% | Fossil: {fos_percent:.1f}%',
                 fontsize=12, fontweight='bold')


# ============================================================================
# Entrypoint -> Plots ausführen / Main
# ============================================================================
if not COMBINE_SECTORS:
    fig = plt.figure(figsize=(18, 12))
    fig.suptitle('Energieverbrauch in Deutschland nach Sektoren',
                 fontsize=16, fontweight='bold', y=0.98)

    ax1 = plt.subplot(3, 2, 1)
    ax2 = plt.subplot(3, 2, 2)
    create_sector_pie_charts(strom_renewable, strom_fossil, 'Stromsektor',
                             'Mrd. kWh', 'Mrd. kWh', ax1, ax2)
    fig.text(0.5, 0.66, 'STROMSEKTOR', ha='center', fontsize=13,
             fontweight='bold', style='italic')

    ax3 = plt.subplot(3, 2, 3)
    ax4 = plt.subplot(3, 2, 4)
    create_sector_pie_charts(verkehr_renewable, verkehr_fossil, 'Verkehrssektor',
                             'Mrd. kWh', 'Mio. t SKE', ax3, ax4)
    fig.text(0.5, 0.365, 'VERKEHRSSEKTOR', ha='center', fontsize=13,
             fontweight='bold', style='italic')
    fig.text(0.5, 0.345, '(Unterschiedliche Einheiten: Links in Mrd. kWh, Rechts in Mio. t SKE)',
             ha='center', fontsize=9, style='italic', color='gray')

    ax5 = plt.subplot(3, 2, 5)
    ax6 = plt.subplot(3, 2, 6)
    create_sector_pie_charts(waerme_renewable, waerme_fossil, 'Wärmesektor',
                             'Mrd. kWh', 'Mrd. kWh', ax5, ax6)
    fig.text(0.5, 0.05, 'WÄRMESEKTOR', ha='center', fontsize=13,
             fontweight='bold', style='italic')

    #plt.tight_layout(rect=[0.05, 0.01, 1, 0.97])
    plt.tight_layout()
else:
    fig = plt.figure(figsize=(14, 14))
    fig.suptitle('Energieverbrauch in Deutschland nach Sektoren',
                 fontsize=16, fontweight='bold', y=0.98)

    ax1 = plt.subplot(3, 1, 1)
    create_combined_sector_pie_chart(strom_renewable, strom_fossil,
                                     'STROMSEKTOR', 'Mrd. kWh', ax1)

    ax2 = plt.subplot(3, 1, 2)
    verkehr_fossil_converted = {k: v * 11.63 for k, v in verkehr_fossil.items()}
    create_combined_sector_pie_chart(verkehr_renewable, verkehr_fossil_converted,
                                     'VERKEHRSSEKTOR', 'Mrd. kWh (geschätzt)', ax2)

    ax3 = plt.subplot(3, 1, 3)
    create_combined_sector_pie_chart(waerme_renewable, waerme_fossil,
                                     'WÄRMESEKTOR', 'Mrd. kWh', ax3)

    #plt.tight_layout(rect=[0.05, 0.01, 1, 0.97])
    plt.tight_layout()

plt.show()

# ============================================================================
# Debug prints
# ============================================================================
print("\n" + "=" * 60)
print("Kontroll-Ausgabe")
print("=" * 60)

strom_ren_total = sum(strom_renewable.values())
strom_fos_total = sum(strom_fossil.values())
strom_total = strom_ren_total + strom_fos_total
print(f"\n1) Stromsektor:")
print(f"   Erneuerbar: {strom_ren_total:.1f} Mrd. kWh ({100 * strom_ren_total / strom_total:.1f}%)")
print(f"   Fossil:     {strom_fos_total:.1f} Mrd. kWh ({100 * strom_fos_total / strom_total:.1f}%)")

verkehr_ren_total = sum(verkehr_renewable.values())
verkehr_fos_total = sum(verkehr_fossil.values())
print(f"\n2) Verkehrssektor:")
print(f"   Erneuerbar: {verkehr_ren_total:.1f} Mrd. kWh")
print(f"   Fossil:     {verkehr_fos_total:.1f} Mio. t SKE") #TODO

waerme_ren_total = sum(waerme_renewable.values())
waerme_fos_total = sum(waerme_fossil.values())
waerme_total = waerme_ren_total + waerme_fos_total
print(f"\n3) Wärmesektor:")
print(f"   Erneuerbar: {waerme_ren_total:.1f} Mrd. kWh ({100 * waerme_ren_total / waerme_total:.1f}%)")
print(f"   Fossil:     {waerme_fos_total:.1f} Mrd. kWh ({100 * waerme_fos_total / waerme_total:.1f}%)")
print("\n" + "=" * 60)

# ============================================================================
# Quellen:
# https://www.destatis.de/DE/Presse/Pressemitteilungen/2025/03/PD25_091_43312.html
# https://www.ise.fraunhofer.de/de/presse-und-medien/presseinformationen/2025/oeffentliche-stromerzeugung-2024-deutscher-strommix-so-sauber-wie-nie.html
# https://www.umweltbundesamt.de/themen/klima-energie/erneuerbare-energien/erneuerbare-energien-in-zahlen
# https://ag-energiebilanzen.de/wp-content/uploads/EBD24p2_AnwBil.pdf
# https://ag-energiebilanzen.de/wp-content/uploads/EBD24p2_Auswertungstabellen_deutsch.pdf
# ============================================================================