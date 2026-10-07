# MRI DeCal — Lab 2: Single Spin Dynamics

Student materials for Lab 2 of the MRI DeCal. This assignment builds a simple Bloch-equation simulator: representing magnetization as a vector, rotation, relaxation, and precession of a single spin.

This repository does **not** include solutions.

## Requirements

- Python 3.12 or newer (`python3 --version`)
- A way to run Jupyter notebooks, such as [Cursor](https://cursor.com), [VS Code](https://code.visualstudio.com/) with the Jupyter extension, JupyterLab, or Jupyter Notebook

## Setup

1. Clone this repository and enter the folder:

```bash
git clone https://github.com/rYan-theusername/mri_decal_lab_2.git
cd mri_decal_lab_2
```

2. Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

3. Install the Python packages:

```bash
pip install -r requirements.txt
```

4. Open `lab_2.ipynb` and run the first cell. If it prints `All libraries are installed.`, you are ready to start.

If you prefer the Jupyter web interface:

```bash
pip install notebook
jupyter notebook lab_2.ipynb
```

## Working on the lab

- Fill in every `# TODO` in `lab_2.ipynb`.
- Helper plotting and animation functions live in `visualizations.py`. You do not need to edit that file.
- `extra.py` is used by a later part of the notebook. You do not need to edit that file either.
- Keep `visualizations.py` and `extra.py` in the same folder as the notebook.
- This lab uses interactive 3D plots. If the notebook starts to slow down, clear the output of those visualization cells.

## Files

| File | What it is |
| --- | --- |
| `lab_2.ipynb` | The assignment notebook |
| `visualizations.py` | 3D plotting and animation helpers used by the notebook |
| `extra.py` | A small helper used later in the notebook |

If you have questions about the lab, reach out to the course staff.
