# Battery Hazard Analysis Dashboards
Web application describing the explosion hazards from Lithium-Ion battery vent
gas.

### Table of Contents

- [About](#about)
- [Set Up](#set-up)
- [Launching the Web App Locally](#launching-the-web-app-locally)

## About

Lithium-ion battery failures can lead the battery cell to undergo what’s known
as thermal runaway, resulting in a potentially catastrophic fire or explosion.
During a thermal runaway event a series of chemical reactions take place,
increasing the cell temperature and resulting in the generation of a flammable
gas mixture.

The University of Texas Fire Research Group has developed two models to evaluate
fire and explosion hazard for lithium-ion batteries. The first model aims to
estimate the upper and lower flammability limits, laminar flame speed, and
maximum overpressure of the gases released during thermal runaway. While the
second model predicts the pressure time history of an explosion. Both of these
models are intended to provide a framework for evaluating the overall safety of
lithium- ion cells.

To enable our researches to perform rapid data analysis as
more experimental data becomes available, a web application that presents the
above-mentioned models in the form of interactive dashboards was developed and
deployed using Python and a framework for building data visualization web
applications called Dash.

## Set Up

Follow these instructions to get the project running on your local machine for
development and testing.

### Prerequisites

* [Miniconda](https://docs.conda.io/en/latest/miniconda.html): Miniconda is a free minimal installer for `conda`. It is a small, bootstrap version of
Anaconda that includes only `conda`, Python, the packages they depend on, and a
small number of other useful packages, including pip, zlib and a few others.


### Setting Up the Conda Environment

1) Checkout this GitHub repository

```bash
$ git checkout https://github.com/UTFireResearch/hazard-analysis-dashboards.git
```

2) Navigate to the working directory `hazard-analysis-dashboards`

```bash
$ cd hazard-analysis-dashboards
```

3) Create a virtual environment named `fire` using `conda`. The new environment
will contain the packages specified in `environment.yml`:

```bash
$ conda env create -n fire -f environment.yml
```

4) Activate the newly created `fire` environment:

```bash
$ conda activate fire
```

## Launching the Web App Locally

To launch the web application locally, first ensure the `fire` environment is
activated, then run the following:

```bash
$ python dashboards/index.py
```

To view the application navigate to either http://127.0.0.1:8050/apps/vent_calculator, or http://127.0.0.1:8050/apps/hazard_analysis using your
preferred web browser.
