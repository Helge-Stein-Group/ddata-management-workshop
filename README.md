TUM-Nat Data Management Workshop
=============================

First you need to install Nomad-lab to start developing your own parser!

 Nomad-Lab Installation Guide
=============================

This  will guide you through the process of setting up Nomad Lab on your local machine using Conda.

Prerequisites
-------------

Before we begin, make sure you have the following installed:

* [Conda](https://docs.conda.io/en/latest/miniconda.html) (version 4.10 or higher)

Installing Nomad Lab
--------------------

YOU NEED TO HAVE THE LATEST CONDA

```
conda update -n base conda
```

To install Nomad Lab and its dependencies, follow these steps:

1. Create a new Conda environment named `nomad` with Python 3.9 (higher versions are not currently supported):

   ```
   conda create -n nomad python==3.9
   ```

2. Activate the newly created Conda environment:

   ```
   conda activate nomad
   ```

3. Install Elasticsearch-dsl using the anaconda channel:

   ```
   conda install anaconda::elasticsearch-dsl
   ```

4. Finally, install Nomad-Lab from the conda-forge channel:

   ```
   conda install conda-forge::nomad-lab==1.2.1
   ```

Getting Started
---------------

Once you've completed the installation steps, you can start using Nomad-Lab by running `python` in your terminal and then importing the package:

```
import nomad
```
Hopefully this works without errors

If you have persisting errors with numpy we recommend the following:
Install cython via
```
pip install cython
```
then reinstall the latest numpy:
```
pip install -U numpy
```

MacOS specific additional errors
-----------------------

You will get an error upon importing 

```python
from nomad.datamodel import EntryArchive, EntryMetadata
```

To fix it you will need to replace all 'numpy.float128' with 'numpy.longdouble' and all 'numpy.complex128' with 'numpy.complex64'. Your errormessage will refer to a file like nomad/metainfo/util.py which you will need to open and then simply to a search and replace for the float128 and complex128.

By using this modified initialization, you can ensure that your code will work across different platforms and versions of numpy without raising an `AttributeError`.

Then you need to do the same in:

nomad/datamodel/metainfo/simulation/method.py

nomad/datamodel/metainfo/simulation/calculation.py


Making Conda faster
-----------------------

Run these three commands to make conda work better:

```python
conda update -n base conda
```


```python
conda install -n base conda-libmamba-solver
```


```python
conda config --set solver libmamba
```
