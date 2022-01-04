# spheroid_simulator

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![License](https://img.shields.io/github/license/EdgarLefevre/spheroid_simulator?label=license)](https://github.com/EdgarLefevre/spheroid_simulator/blob/main/LICENSE)
<a href="https://gitmoji.dev">
  <img src="https://img.shields.io/badge/gitmoji-%20😜%20😍-FFDD67.svg?style=flat-square" alt="Gitmoji">
</a>
<!-- [![PyPI](https://img.shields.io/pypi/v/napari-deepmeta.svg?color=green)](https://pypi.org/project/napari-deepmeta)
[![Python Version](https://img.shields.io/pypi/pyversions/napari-deepmeta.svg?color=green)](https://python.org)
[![tests](https://github.com/EdgarLefevre/napari-deepmeta/workflows/tests/badge.svg)](https://github.com/EdgarLefevre/napari-deepmeta/actions)
[![codecov](https://codecov.io/gh/EdgarLefevre/napari-deepmeta/branch/main/graph/badge.svg?token=H41ZaCAg31)](https://codecov.io/gh/EdgarLefevre/napari-deepmeta)
-->



# Neuron Spheroid Simulator

This simulator is able to quickly generate thousands of spheroid of neurons, with various noise background and various neuron intensity, shape, direction.
The noise is simulated with a Poisson noise and a Perlin noise.
The neuron signal is simulated with random start and stop positions between which random splits are added before line smoothing.
Optionnaly, motion blur is also available, simulated with elastic transform.


## Install
Install dependencies with Conda
```sh
conda env create environment.yml

```
Then activate the environment:

```sh
conda activate spheroid

```

## Usage

```shell
python main.py

```
