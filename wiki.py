import subprocess
from pathlib import Path
import shutil

foldx_dir = Path(r"C:\Users\alyar\Downloads\foldx5Windows64")
foldx_exe = foldx_dir / "foldx_20241231.exe"
pdb_file_name = "4qvx_t.pdb"
pdb_file = foldx_dir / pdb_file_name

repaired_pdb_file_name = pdb_file_name.replace(".pdb", "_Repair.pdb")
repaired_pdb_file = foldx_dir / repaired_pdb_file_name

if not pdb_file.exists():
    print(f" файл {pdb_file} не найден.")
else:
    repair_command = [
        str(foldx_exe),
        "--command=RepairPDB",
        f"--pdb={pdb_file_name}"
    ]

    try:
        repair_process = subprocess.run(repair_command, cwd=foldx_dir, capture_output=True, text=True, timeout=300)

        print("RepairPDB output:")
        print(repair_process.stdout)
        print(repair_process.stderr)

        if repair_process.returncode == 0:
            print("RepairPDB завершен.")
        else:
            print("Ошибка RepairPDB.")
    except subprocess.TimeoutExpired:
        print("RepairPDB таймаут.")

    mutation_file = foldx_dir / "individual_list.txt"


    with open(mutation_file, "w") as f:
        f.write("TA106N;")

    build_model_command = [
        str(foldx_exe),
        "--command=BuildModel",
        f"--pdb={repaired_pdb_file_name}",
        "--mutant-file=individual_list.txt"
    ]

    try:
        build_model_process = subprocess.run(build_model_command, cwd=foldx_dir, capture_output=True, text=True, timeout=300)

        print("BuildModel output:")
        print(build_model_process.stdout)
        print(build_model_process.stderr)

        if build_model_process.returncode == 0:
            print("BuildModel завершен.")
        else:
            print("ошибка BuildModel.")
            exit()

    except subprocess.TimeoutExpired:
        print(" BuildModel таймаут.")
        exit()


    energy_file = foldx_dir / f"Dif_{repaired_pdb_file_name.replace('.pdb', '')}.fxout"

    if energy_file.exists():
        print(f"результаты с разницей энергий между wt и мутантом: {energy_file}")
        with open(energy_file, "r") as f:
            print(f.read())
    else:
        print(f"ошибка {energy_file} не найден.")


raw_fxout_file = foldx_dir / f"Raw_{repaired_pdb_file_name.replace('.pdb', '.fxout')}"

if raw_fxout_file.exists():
    print(f"результаты для wt и мутанта: {raw_fxout_file}")
    with open(raw_fxout_file, "r") as f:
        raw_fxout_data = f.read()

    lines_of_interest = [line for line in raw_fxout_data.splitlines() if "pdb" in line and "total energy" not in line]

    with open(mutation_file, "r") as f:
        mutation = f.read().strip()

    with open(foldx_dir / "results.txt", "a") as f:
        f.write(f"{mutation}: {lines_of_interest[0].split()[0]} {lines_of_interest[0].split()[1]} {lines_of_interest[1].split()[0]} {lines_of_interest[1].split()[1]}\n")

else:
    print(f"Ошибка: файл с результатами {raw_fxout_file} не найден.")