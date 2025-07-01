import matplotlib.pyplot as plt
from junction import Junction
from typing import List

dpi = 150
plt.rcParams['figure.dpi'] = dpi
plt.rcParams["figure.figsize"] = (10, 6) # Дюймы
plt.ioff()

def plot_time_space_diagram(junctions: List[Junction]):

    fig, ax = plt.subplots()


    rect_height = 20  # Высота прямоугольников

    y_coords = [j.y for j in junctions]


    max_y = max(y_coords)
    min_y = min(y_coords)
    max_time = max(j.full_cycle_seconds for j in junctions) * 2


    for junction in junctions:
        y_center = junction.y
        y_bottom = y_center - rect_height / 2

        current_time = junction.cycle_offset_seconds

        while current_time < max_time:
            for phase in junction.full_cycle:
                for signal in phase.signals:
                    ax.add_patch(plt.Rectangle(
                        (current_time, y_bottom),
                        width=signal.duration_seconds,
                        height=rect_height,
                        facecolor=str(signal.color),
                        edgecolor='black',
                        linewidth=0.5
                    ))
                    current_time += signal.duration_seconds


    ax.set_xlabel("t, секунды", fontsize=12, fontweight='bold')
    ax.set_ylabel("Светофорные объекты, метры", fontsize=12, fontweight='bold')
    ax.set_title("Диаграммы лент времени", fontsize=14, fontweight='bold')

    # Подписи светофоров
    for junction in junctions:
        ax.text(
            max_time * 0.05,  # Отступ
            junction.y,
            junction.name,
            ha='right',
            va='center',
            fontsize=10
        )

    ax.set_xlim(-max_time*0.01, max_time)
    ax.set_ylim(min_y - rect_height, max_y + rect_height)

    # Сетка
    ax.grid(True, axis='x', linestyle='--', alpha=0.7)
    ax.grid(True, axis='y', linestyle=':', alpha=0.5)

    plt.tight_layout()
    return plt