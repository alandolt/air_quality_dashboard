# Air quality dashboard in Python
This repository contains a simple air quality dashboard programmed in Python. 

As this repository is part of a group project in an university course dedicated to Python, we will implement to dashboard from A to Z in python. Data is thereby pulled from the World Health Organization (WHO) air quality database, as well as some local resources for some countries (e.g. Switzerland). Our goal is further to render the dashboard interactive by using Dash, a Python framework for building dynamic analytical web application. 

## Installation

To install the required packages, clone this repository. Then create a new environment in Conda / Mamba by running the following command: 
    
```
conda env create --file environment.yml 
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

The dashboard will then be available at `http://127.0.0.1:8081/` in your browser.

## Docker

To run the dashboard in a Docker container, you can use the supplied ```Dockerfile```, and ```docker-compose``` file.
Simply clone the repository, change the current working directory to ```air_quality_dashboard``` and launch the container with ```docker-compose up .```:

```bash
git clone https://github.com/alandolt/air_quality_dashboard/
cd air_quality_dashboard
docker-compose up . 
```

The dashboard will then be available at `http://127.0.0.1:8081/` in your browser.

## Progress
- *0.0.1*: Data can be imported from WHO, as well as from a local source (Switzerland -> NABEL database). Summary statistics, like how many entries are present, when the NABEL database got last updated, etc. are displayed in the dashboard.
- *0.0.2*: Add some interactive filtering for the user to select countries and time spans to select PM10, PM25, and NO2 values. Code refactoring, bug fixing (see commit messages for details) and linting.
- *0.0.3*: Add a map to the dashboard, which displays the average PM10/PM25/NO2 values for each country. The map is interactive. 
  
## Contributors: 
- [Anmol Ratan](https://www.linkedin.com/in/anmol-ratan-8a801b166/)
- [Alex Landolt](https://github.com/alandolt/)
- Paula Laukel
- [Yannic Eltschinger](https://www.linkedin.com/in/yannic-eltschinger-798175221/)

