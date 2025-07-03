from junction import Junction
from green_wave_finder import find_complete_green_waves
from typing import List

def best_offsets (junctions: List[Junction])-> list[int]:
    max_band_size: float = 0
    best_offsets: list[int] = (0,0,0,0)
    for j in range(0, 85):
        for k in range(0, 85):
            for z in range(0, 85):
                offsets = [0, j, k, z]
                for i, offset in enumerate(offsets):
                    junctions[i].set_offset(offset)

                complete_green_waves = find_complete_green_waves(junctions, speed_kmh=40)
                band_size: float = 0

                for through_wave in complete_green_waves.chained_green_waves:
                    band_size += through_wave.band_size
                    #print("Through green wave:", through_wave, "CRITERIA", through_wave.band_size)
                if band_size > max_band_size:
                    max_band_size = band_size
                    best_offsets = offsets
    return best_offsets