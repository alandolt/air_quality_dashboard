# Air quality dashboard in Python
This repository contains a simple air quality dashboard programmed in Python. 

As this repository is part of a group project in an university course dedicated to Python, we will implement to dashboard from A to Z in python. Data is thereby pulled from the World Health Organization (WHO) air quality database, as well as some local resources for some countries (e.g. Switzerland). Our goal is further to render the dashboard interactive by using Dash, a Python framework for building dynamic analytical web application. 

## Installation

To install the required packages, clone this repository. Then create a new environment in Conda / Mamba by running the following command: 
    
```
conda env create --file requirements.yml 
```

Activate the environment by running: 

```
conda activate air_quality_dashboard
```

## Usage

To run the dashboard locally, run the following command in the terminal: 

```
python main.py
```

The dashboard will then be available at `http://127.0.0.1:8080/` in your browser.

## Progress
- *0.0.1*: Data can be imported from WHO, as well as from a local source (Switzerland -> NABEL database). Summary statistics, like how many entries are present, when the NABEL database got last updated, etc. are displayed in the dashboard.


## Contributors: 
- [Anmol Ratan](https://www.linkedin.com/in/anmol-ratan-8a801b166/)
- [Alex Landolt](https://github.com/alandolt/)
- Paula Laukel
- [Yannic Eltschinger](https://www.linkedin.com/in/yannic-eltschinger-798175221/)

