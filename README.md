# The Social Brain App
This repository contains code to organize data from The Social Brain App.

### Directory Tree
```
socialbrainapp/
├─ code/
│  ├─ preprocess.ipynb
│  ├─ socialbrainapp.py
├─ data/
│  ├─ Demographics-data-Master.csv
│  ├─ Hardball-data-Master.csv
│  ├─ Journey-data-Master.csv
│  ├─ runs/
│  │  ├─ Demographics-data-*.csv
│  │  ├─ Hardball-data-*.csv
│  │  ├─ HardballSubjectiveRatings-data-*.csv
│  │  ├─ SNT-data-*.csv
│  │  ├─ SNT-memory-data-*.csv
│  │  ├─ SNT-ver-data-*.csv
│  │  ├─ LSAS-data-*.csv
│  │  ├─ OCI-data-*.csv
│  │  ├─ SDS-data-*.csv
│  │  ├─ SocialBrainAppData-*.pickle
├─ json/
│  ├─ *.json
├─ modeling/
├─ .gitignore
├─ README.md
```

### Code
- `./code/preprocess.ipynb` (Jupyter Notebook with Python code to parse json files and preprocess data)
- `./code/socialbrainapp.py` (Python module to parse json files)

### Data
- Data is not pushed to GitHub

### Required Packages
- `pandas`
- `numpy` 
- `json`
- `pickle`
- `glob`
- `datetime`