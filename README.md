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
   conda install conda-forge::nomad-lab
   ```

Getting Started
---------------

Once you've completed the installation steps, you can start using Nomad-Lab by running `python` in your terminal and then importing the package:

```
import nomad
```
Hopefully this works without errors



MacOS specific additional errors
-----------------------

 In order to fix the `AttributeError: module 'numpy' has no attribute 'float128'` error upon importing EntryArchive from nomad, you can modify the `utils` function initialization in the `nomad/metainfo/util.py` file as follows:
```python
try:
    float_numpy = {np.float16, np.float32, np.float64, np.longdouble}
except AttributeError:
    # numpy does not have a longdouble attribute, use the largest available dtype instead
    float_numpy = {np.float16, np.float32, np.float64}

if os.name == 'nt':
    float_numpy.discard(np.float128)
```

To find the exact location of the util.py file simply try importing 

```python
from nomad.datamodel import EntryArchive, EntryMetadata
```
which will try to import it and fail but give you the exact location of the file you need to change :-).

This code first attempts to create a set of all available floating-point data types in numpy, including `np.longdouble`. If this attribute is not available (as in the case of macOS or certain versions of 
Python), it instead creates a set with only the available float data types up to `np.float64`.

The rest of the code checks if the operating system is Windows and removes `np.float128` from the set, since this data type is not supported on Windows either.

By using this modified initialization, you can ensure that your code will work across different platforms and versions of numpy without raising an `AttributeError`.
