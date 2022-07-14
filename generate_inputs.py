import os


def create_feff_input_file(Cu_location=[0, 0, 0], O_location=[2, 0, 0], folder="feff_inputs"):
    os.makedirs(folder, exist_ok=True)
    
    Cu_location_str = "_".join(list(map(str, Cu_location)))
    O_location_str = "_".join(list(map(str, O_location)))
    input_file_path = os.path.join(folder, f"feff_Cu_{Cu_location_str}_O_{O_location_str}.inp")
    with open(input_file_path, "w") as f:
        f.write("HOLE  1  1.0\n\n")
        f.write("CONTROL  1  1  1  1\n")
        f.write("PRINT    1  0  0  0\n\n")
        f.write("POTENTIALS\n")
        f.write("  0  29  Cu\n")
        f.write("  1  8   O\n\n")
        f.write("ATOMS\n")
        f.write(f"  {Cu_location[0]:.3f}  {Cu_location[1]:.3f}  {Cu_location[2]:.3f}  0\n")
        f.write(f"  {O_location[0]:.3f}  {O_location[1]:.3f}  {O_location[2]:.3f}  1\n")

if __name__ == "__main__":
    for dx in range(-10, 10):
        O_location = [(2+dx/10), 0, 0]
        create_feff_input_file(O_location=O_location)

    for dy in range(-10, 10):
        O_location = [2, (dy/10), 0]
        create_feff_input_file(O_location=O_location)

    for dz in range(-10, 10):
        O_location = [2, 0, (dz/10)]
        create_feff_input_file(O_location=O_location)