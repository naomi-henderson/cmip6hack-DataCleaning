# CMIP6 Hackathon Data Cleaning/Preprocessing Project  
Oct 18, 2019

## The CMIP6 Data Challenge
Our Google Cloud CMIP6 zarr repository currently contains contributions from 23 institutions with 48 models. As Gerald Meehl/UCAR explained in the opening session of the Hackathon, as has happened with prior CMIPs, the modelers initially promised to run many experiments, but the time goes by quickly, deadlines are missed and there is now a rush to get the data out, leading to inevitable inconsistencies.

Although the amount of data is overwhelming, it is all very precious.  It has been a labor of love for all involved and we would like to make it as accessible to the world-wide community as possible. For CMIP3 and expecially CMIP5 collections, we each faced the Data Cleaning chore on our own - every researcher going through essentially the same process of discovering and fixing a myriad of little issues in order to calculate multimodel statistics, often with erroneous results. One of the goals of this CMIP hackathon is to develop methods to streamline this often extremely tedious but essential process. The integrity of our science depends on it.

## Current Status of our Google Cloud and NCAR/Glade CMIP6 collections
- Some data is collected at a few large sites - the ESGF nodes.  Most remains at home institution - must be downloaded from there. Transfers are between 100Mbps to 100Kbps. All servers go up and down. Recently, even the LLNL ESGF search API goes down every weekend.

- We have collected a very small subset - about 600,000 netcdf files at NCAR/Glade, most < 2.1 G, split in `time` dimension.

- We have concatenated netcdf in time (using `xarray`, saving as `zarr` stores) - about 30,000 zarr stores in Google Cloud. The time concatenation is problematic, but greatly reduces the work needed to prepare data.

## Data Cleaning has many aspects:

Types of issues:
- Hopeless cases, or those needing to be fixed by their creators.
- Fixable cases (duplicate times, mismatched coordinate names, time gaps in data, etc)
- Improvements we would like to make before aggregating the data in order to expedite our Pangeo methods

Existing and proposed solutions:
- The official CMIP6 errata database: [The ES-DOC Errata Search](https://errata.es-doc.org/static/index.html) for withdrawn, incorrect data with unknown fixes
- Database of datasets which need special treatment when concatenating the netcdf files in time (@naomi-henderson)
- Methods for preprocessing the dataset grids (@jbusecke)
- A crowd-sourced database of how to fix various datasets (correct units, deal with slightly offset grids, etc)

## This Project

Part 1. 
Turning the ES-DOC Errata Search into a database in python to quickly identify and isolate troublesome data.  This involves parsing the online search tool to obtain a spreadsheet of issues, current status and list of affected files. The spreadsheet uses the same keywords as the catalogs, which allows for easy identification.

Part 2. 
Making Naomi's list of time concatenation exceptions into the same python database.

Part 3.
Incorporating preprocessing into `intake-esm` to process the various model-dependent coordinates in such a way that we can easily use model independent analysis methods.

Part 4.
Constructing a new database for collecting common issues and solutions going forward from here.

