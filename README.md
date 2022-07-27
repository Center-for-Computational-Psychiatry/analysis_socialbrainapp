# The Social Brain App
This repository contains code to organize data from The Social Brain App.

### Directory Tree
```
socialbrainapp/
├─ code/
│  ├─ preprocess.ipynb
│  ├─ socialbrainapp.py
├─ data/
│  ├─ Demographics-data.csv
│  ├─ Hardball-data.csv
│  ├─ HardballSubjectiveRatings-data.csv
│  ├─ LSAS-data.csv
│  ├─ OCI-data.csv
│  ├─ SDS-data.csv
│  ├─ SocialBrainAppData.pickle
├─ json/
│  ├─ *.json
├─ .gitignore
├─ README.md
```

### Code
- `./code/preprocess.ipynb` (Jupyter Notebook with Python code to parse json files and preprocess data)
- `./code/socialbrainapp.py` (Python module to parse json files)

### Required Packages
- `pandas`
- `numpy` 
- `json`
- `pickle`
- `glob`
- `datetime`