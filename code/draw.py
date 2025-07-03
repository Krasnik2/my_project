import matplotlib.pyplot as plt
from junction import Junction
from typing import List
from green_wave import GreenWave, ThroughGreenWave

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
    cycle_length = max(j.full_cycle_seconds for j in junctions)

    for junction in junctions:
        y_center = junction.y
        y_bottom = y_center - rect_height / 2
        current_time = junction.cycle_offset_seconds % cycle_length

        # Отрисовываем сигналы с учетом смещения
        for phase in junction.full_cycle:
            for signal in phase.signals:
                start_time = current_time % cycle_length
                end_time = (start_time + signal.duration_seconds) % cycle_length

                if end_time > start_time:
                    # Прямоугольник не пересекает границу цикла
                    ax.add_patch(plt.Rectangle(
                        (start_time, y_bottom),
                        width=signal.duration_seconds,
                        height=rect_height,
                        facecolor=str(signal.color),
                        edgecolor='black',
                        linewidth=0.5
                    ))
                else:
                    # Прямоугольник пересекает границу цикла
                    ax.add_patch(plt.Rectangle(
                        (start_time, y_bottom),
                        width=cycle_length - start_time,
                        height=rect_height,
                        facecolor=str(signal.color),
                        edgecolor='black',
                        linewidth=0.5
                    ))
                    ax.add_patch(plt.Rectangle(
                        (0, y_bottom),
                        width=end_time,
                        height=rect_height,
                        facecolor=str(signal.color),
                        edgecolor='black',
                        linewidth=0.5
                    ))

                current_time += signal.duration_seconds

    # Настройки осей и оформления
    ax.set_xlim(0, cycle_length)
    ax.set_ylim(min_y - rect_height, max_y + rect_height)
    ax.set_xlabel("t, секунды", fontsize=12, fontweight='bold')
    ax.set_ylabel("Светофорные объекты, метры", fontsize=12, fontweight='bold')

    # Подписи светофоров
    for junction in junctions:
        ax.text(
            0.05 * cycle_length,  # отступ
            junction.y,
            junction.name,
            ha='right',
            va='center',
            fontsize=10
        )

    ax.grid(True, axis='x', linestyle='--', alpha=0.7)
    ax.grid(True, axis='y', linestyle=':', alpha=0.5)
    plt.tight_layout()
    return plt

def plot_green_waves(plt: plt, junctions: List[Junction], green_waves: list[list[GreenWave]]) -> plt:
    ax = plt.gca()
    wave_color = "#57B844"
    alpha = 0.3
    # Для каждого сегмента между перекрёстками
    for segment_idx, segment_waves in enumerate(green_waves):
        if segment_idx >= len(junctions) - 1:
            # Защита от несоответствия количества сегментов и перекрёстков
            break
        
        j1 = junctions[segment_idx]
        j2 = junctions[segment_idx + 1]
        y1 = j1.y
        y2 = j2.y
        # Для каждой зелёной волны в сегменте
        for wave in segment_waves:
            start_j1, end_j1 = wave.interval_j1.start, wave.interval_j1.end
            start_j2, end_j2 = wave.interval_j2.start, wave.interval_j2.end
            polygon = [
                (start_j1, y1),
                (start_j2, y2),
                (end_j2, y2),
                (end_j1, y1),
                (start_j1, y1)
            ]
            xs, ys = zip(*polygon)
            ax.fill(
                xs, ys,
                color=wave_color,
                alpha=alpha,
                edgecolor=wave_color,
                linewidth=0.5,
                zorder=2
            )
    return plt

def plot_through_wave_bands(plt: plt, junctions: List[Junction], through_waves: List[ThroughGreenWave]) -> plt:
    ax = plt.gca()
    wave_color = "#541FE4"
    alpha = 0.2
    for wave in through_waves:
        starts = []
        ends = []
        for j, interval in enumerate(wave.intervals):
            junction = junctions[j]
            y = junction.y
            starts.append((interval.start, y))
            ends.append((interval.end, y))
        ends.reverse()

        polygons = starts + ends
        xs, ys = zip(*polygons)
        ax.fill(xs, ys, color=wave_color, alpha=alpha, edgecolor=wave_color, linewidth=0.5, zorder=2)
    return plt