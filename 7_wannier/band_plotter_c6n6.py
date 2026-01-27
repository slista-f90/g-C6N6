# -*- coding: utf-8 -*-
"""
Created on Mon Oct  7 16:30:15 2024

@author: stefa
"""

import matplotlib.pyplot as plt

# Offset e scaling
gap = 1.5421
offset1 = 4.5408
offset2 = 4.5408
scale_k2 = 1.5773/1.3918  # Fattore di scala per la prima colonna del secondo file
gap_no_offset = 1.5421 / 2

def read_bands(file_name, scale_k=1.0):
    with open(file_name, 'r') as file:
        bands = []
        current_band = []
        for line in file:
            if line.strip() == '':
                if current_band:
                    bands.append(current_band)
                    current_band = []
            else:
                parts = [float(x) for x in line.split()]
                # Applica lo scaling solo alla prima colonna
                parts[0] *= scale_k
                current_band.append(parts)
        if current_band:
            bands.append(current_band)
    return bands

def plot_two_bandstructures(bands1, bands2, high_symmetry_points=None, high_symmetry_labels=None):
    plt.figure(figsize=(9, 6))

    # Struttura 1
    for band in bands1:
        band_x = [point[0] for point in band]
        band_y = [point[1] + offset1 +gap for point in band]
        plt.plot(band_x, band_y, color='black', label='DFT Band Structure' if band == bands1[0] else "")

    # Struttura 2
    for band in bands2:
        band_x = [point[0] for point in band]
        band_y = [point[1] + offset2 +gap for point in band]
        plt.scatter(band_x, band_y, color='red', marker='x', label='Wannier Interpolated Band Structure' if band == bands2[0] else "")

    # Punti di alta simmetria
    if high_symmetry_points and high_symmetry_labels:
        plt.xticks(high_symmetry_points, high_symmetry_labels)

    #plt.axhline(y=gap_no_offset - 6.0865, color='red', linestyle=':', label='Fermi Level')
    plt.xlim(band_x[0], band_x[-1])
    #plt.ylim(gap-0.05,0.545+gap)
    plt.ylim(gap-1.76,-1.47+gap)
    #plt.ylim(-1.5,5.5)
    plt.ylabel('Energy (eV)')
    plt.legend(loc='upper right', fontsize=13, facecolor='white')
    plt.grid(True, axis='x')
    plt.savefig("wannierizzation_valence.png", dpi =150)
    plt.show()

# Nomi file
file1 = 'c6n6_bands_better.dat.GNU'
file2 = 'c6n6_band.dat'

# Lettura
bands1 = read_bands(file1)
bands2 = read_bands(file2, scale_k=scale_k2)

# Punti di alta simmetria
high_symmetry_points = [0.0, 0.5774, 0.9107, 1.5773]
high_symmetry_labels = ['Γ', 'M', 'K', 'Γ']

# Plot
plot_two_bandstructures(bands1, bands2, high_symmetry_points, high_symmetry_labels)
