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
import nomad_lab
```
Hopefully this works without errors

Documentation & Support
-----------------------

TBD
