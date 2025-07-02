import matplotlib.pyplot as plt
from junction import Junction
from typing import List
from green_wave import GreenWave, ThroughGreenWave

dpi = 150
plt.rcParams['figure.dpi'] = dpi  
plt.rcParams["figure.figsize"] = (12, 9) # Дюймы
plt.ioff()

def plot_time_space_diagram(junctions: List[Junction]):
    fig, ax = plt.subplots(figsize=(6, 4))

    # Цикл по светофорам
    for junction in junctions:
        # Отрисовка светофоров
        ax.scatter(
            # 0X
            0,
            # 0Y
            junction.y,
            # Размер кружочка
            s=100,
            # Вид
            marker="o",
            # Цвет заливки, HEX
            facecolors=("#D8BFD8"),
            # Цвет контура, HEX
            edgecolors=("#4B0082"),
        )
        # Подпись светофоров
        ax.text(
            0,
            junction.y + 40,
            f"{junction.name}",
            va="center",
            ha="center",
            fontsize=8,
            fontweight="bold",
        )

        # Отрисовка лент времени
        # Сдвиг ленты 0X
        prev_cycle_x = junction.get_offset()
        # Сдвиг ленты 0Y - позиция светофора в нашем случае
        prev_cycle_y = junction.y
        # Цикл по фазам
        for phases in junction.full_cycle:
            # Цикл по сигналам
            for signal in phases.signals:
                # Ищем границы интервалов цветов x (зеленый, желтый, красный)
                # Длительность не должна превышать суммарную длительность светофорного цикла
                x_start = prev_cycle_x % junction.full_cycle_seconds
                x_end = (
                    prev_cycle_x + signal.duration_seconds
                ) % junction.full_cycle_seconds
                # Случай, когда x_end < x_start
                if x_end < x_start:
                    # Рисуем первую часть от начала сигнала до конца цикла
                    ax.plot(
                        [x_start, junction.full_cycle_seconds],
                        [prev_cycle_y, prev_cycle_y],
                        color=f"{signal.color}",
                        linewidth=2.5,
                    )
                    # Рисуем вторую часть от 0 до конца сигнала
                    ax.plot(
                        [0, x_end],
                        [prev_cycle_y, prev_cycle_y],
                        color=f"{signal.color}",
                        linewidth=2.5,
                    )
                # Случай, когда x_end > x_start
                else:
                    ax.plot(
                        [x_start, x_end],
                        [prev_cycle_y, prev_cycle_y],
                        color=f"{signal.color}",
                        linewidth=2.5,
                    )
                # Переопределяем начало отрисовки следующего сигнала светофора
                prev_cycle_x += signal.duration_seconds
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