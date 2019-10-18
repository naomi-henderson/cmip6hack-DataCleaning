# CMIP6 Hackathon Data Cleaning/Preprocessing Project

## Data Cleaning has many aspects:


Types of issues:
- Hopeless cases, or those needing to be fixed by their creators.
- Fixable cases (duplicate times, mismatched coordinate names, time gaps in data, etc)
- Improvements we would like to make before aggregating the data in order to expedite our Pangeo methods

Existing and proposed solutions:
- The official CMIP6 errata database: [The ES-DOC Errata Search](https://errata.es-doc.org/static/index.html) for withdrawn, incorrect data with unknown fixes
- Database of datasets which need special treatment when concatenating the netcdf files in time
- Methods for aggregating ensembles and variables in xarray datasets
