import shutil
from larch.xafs import feff8l
import matplotlib.pyplot as plt
import numpy as np
import os
from generate_inputs import create_feff_input_file

def generate_plot(Cu_location, O_location, input_home, output_home, apply_fourier_transform=False):
    Cu_location_str = "_".join(list(map(str, Cu_location)))
    O_location_str = "_".join(list(map(str, O_location)))
    print("="*50)
    print(f"Trying simulation for Cu: {str(Cu_location)} and O: {str(O_location)}")
    basename = f"feff_Cu_{Cu_location_str}_O_{O_location_str}"
    if apply_fourier_transform:
        out_basename = basename + "_fourier"
    else:
        out_basename = basename

    in_file = basename + ".inp"
    out_file = out_basename + ".inp"

    output_folder = os.path.join(output_home, f"{out_basename}")
    src_path = os.path.join(input_home, in_file)
    chi_path = os.path.join(output_folder, "chi.dat")
    # print(chi_path)
    dest_path = os.path.join(output_folder, out_file)

    if not os.path.exists(src_path):
        print("Input file does not exist")
        print(f"Creating the feff input file: {src_path} and chi.dat file: {chi_path}")
        create_feff_input_file(Cu_location=Cu_location, O_location=O_location, folder=input_home)
        os.makedirs(output_folder, exist_ok=True)
        shutil.copy(src_path, dest_path)
        feff8l(folder=output_folder, feffinp=out_file, verbose=False)
    
    elif not os.path.exists(dest_path):
        print("Input file does not exist in the results folder")
        print(f"Creating the feff input file: {dest_path} (in the results folder), and chi.dat file: {chi_path}")
        os.makedirs(output_folder, exist_ok=True)
        shutil.copy(src_path, dest_path)
        feff8l(folder=output_folder, feffinp=out_file, verbose=False)
    
    elif not os.path.exists(chi_path):
        print("chi.dat does not exist")
        print(f"Creating the chi.dat file: {chi_path}")
        feff8l(folder=output_folder, feffinp=out_file, verbose=False)
    
    else:
        print("Simulation has already been run, using the old results")
    
    dat_file_path = os.path.join(output_folder, "chi.dat")
    dat_file = open(dat_file_path, "r")
    lines = dat_file.read().strip().split("\n")

    _k = []
    _chi = []
    for i in range(12, len(lines)):
        p = lines[i].split()
        _k.append(float(p[0]))
        _chi.append(float(p[1]))

    # k=np.zeros([int((20-0)/0.05+1),], dtype=float)
    # chi=np.zeros([int((20-0)/0.05+1),], dtype=float)
    k=np.array(_k, dtype=float)
    chi=np.array(_chi, dtype=float)

    # for i in range(0,len(k)):
    #     k[i]=_k[i]
    #     chi[i]=_chi[i]
    
    # k = np.array(_k)
    # chi = np.array(_chi)
    if apply_fourier_transform:
        chi = np.fft.fft(chi)

    x = k
    y = chi*k**2
    fig, ax = plt.subplots()

    plt.subplots_adjust(left=0.15)
    ax.plot(x, y, **{'color': 'black', 'marker': '.'})

    ax.set_title(f"Cu: {str(Cu_location)} and O: {str(O_location)}")
    ax.set_xlabel("k")
    ax.set_ylabel("chi*k^2")

    figure_path = os.path.join(output_folder, f"{out_basename}.png")
    plt.savefig(figure_path)
    plt.close(fig)
    return (k, chi)


if __name__ == "__main__":
    # for i in range(-5, 5):
    #     Cu_location = [0, 0, 0]
    #     O_location = [(2+i/10), 0, 0]
    Cu_location = [0, 0, 0]
    O_location = [2.0, 0, 0]
    generate_plot(Cu_location=Cu_location, O_location=O_location, input_home="feff_inputs", output_home="outputs", apply_fourier_transform=True)