## University of Chicago Econometrics Game Preliminary Round

### Prerequisites
    - Python 3.8+, Matlab
    - pip packages: numpy, pandas

### Overleaf template
    - https://www.overleaf.com/4675637344jpschnzhsnwb#95a705

### Reproduction steps
    - `source/derived/prepare_data.py` -> `source/analysis/run_regressoin.py`

### Notes
    - We originally intended to use the matlab code from Hsiang, 2010, but faced errors with imaginary standard errors. Our implementation in matlab is in `source/analysis/get_estimates.m`. We reimplemented in python.
    - Final paper is stored in `output/paper/uofc_prelim.pdf`. Latex is in the overleaf document above
