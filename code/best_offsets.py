from junction import Junction, Signal
from green_wave_finder import find_complete_green_waves
from typing import List

def best_offsets (junctions: List[Junction], range_offset: List[int], start_offset: List[int])-> tuple[list[int],int]:
    max_band_size: float = 0
    best_offsets: list[int] = start_offset
    for j in range(range_offset[0], range_offset[1]):
        for k in range(range_offset[0], range_offset[1]):
            for z in range(range_offset[0], range_offset[1]):
                offsets = [0, start_offset[1]+j, start_offset[2]+k, start_offset[3]+z]
                for i, offset in enumerate(offsets):
                    junctions[i].set_offset(offset)

                complete_green_waves = find_complete_green_waves(junctions, speed_kmh=40)
                band_size: float = 0

                for through_wave in complete_green_waves.chained_green_waves:
                    if through_wave.depth == len(junctions):
                        band_size += through_wave.band_size
                    #print("Through green wave:", through_wave, "CRITERIA", through_wave.band_size)
                if band_size > max_band_size:
                    max_band_size = band_size
                    best_offsets = offsets
    return best_offsets , max_band_size

def best_duration_signal_and_offsets(junctions: List[Junction]):
    tmp_offsets: List[int]
    max_band_size: int
    corrected_best_offsets: list[int]
    tmp_offsets , max_band_size = best_offsets(junctions,[0,85],[0,0,0,0])
    for i in range(0,junctions[0].full_cycle[0].signals[0].max_duration_seconds-
                     junctions[0].full_cycle[0].signals[0].min_duration_seconds+1):

        for j in range(0,junctions[1].full_cycle[0].signals[1].max_duration_seconds -
                         junctions[1].full_cycle[0].signals[1].min_duration_seconds+1):

            junctions[0].full_cycle[0].signals[0].duration_seconds = junctions[0].full_cycle[0].signals[0].min_duration_seconds + i
            junctions[0].full_cycle[1].signals[0].duration_seconds = junctions[0].full_cycle[1].signals[0].max_duration_seconds -i
            junctions[1].full_cycle[0].signals[1].duration_seconds = junctions[1].full_cycle[0].signals[1].min_duration_seconds +j
            junctions[1].full_cycle[1].signals[1].duration_seconds = junctions[1].full_cycle[1].signals[1].max_duration_seconds -j
            offsets, band_size = best_offsets(junctions,[-10,10],tmp_offsets)
            if band_size > max_band_size:
                max_band_size = max_band_size
                corrected_best_offsets = offsets
                j1 = junctions[0].full_cycle[0].signals[0].duration_seconds
                j2 = junctions[0].full_cycle[1].signals[0].duration_seconds
                j3 = junctions[1].full_cycle[0].signals[1].duration_seconds
                j4 = junctions[1].full_cycle[1].signals[1].duration_seconds

    return corrected_best_offsets, max_band_size, j1,j2,j3,j4