# Untangling the Osquery❓ tables web🕸 using Jupyter Notebooks📓 - Part 2 | With Data📜
This repository is used to hold Jupyter Notebooks that are used to work with Osquery table **DATA**.  

![TreeBeard](https://github.com/sevickson/Osquery_Data_Graph/workflows/TreeBeard/badge.svg)
![Lint Code Base](https://github.com/sevickson/Osquery_Data_Graph/workflows/Lint%20Code%20Base/badge.svg)
![Clean Jupyter NB](https://github.com/sevickson/Osquery_Data_Graph/workflows/Clean%20Jupyter%20NB/badge.svg)
![Python Script CI](https://github.com/sevickson/Osquery_Data_Graph/workflows/Python%20Script%20CI/badge.svg)

This work is based on my prior work on Osquery Tables:
- [Repository](https://github.com/sevickson/osquery_tables_graph)
- [Blog](https://medium.com/@sevickson/untangling-the-osquery-tables-web-using-jupyter-notebooks-7c979c03f42d)

This repository is divided as follows:
- [Generate Osquery Data](./Jupyter NBs/1_Get_Osquery_Data.ipynb)
- [Create Graph Osquery Graphistry](./Jupyter NBs/3_Graph_Osquery_Data.ipynb)
- [REQ](REQ)
  - Requirements folder

This repository is based on blog ...
The graphs are based on Osquery data for Windows and Linux.

To set the secrets, copy `.env_template` and rename to `.env` and set your secrets there.

------------------------

From my prior work on `OSQuery-Tables` this repository handles following points:
- [X] Check the data returned from the tables when querying and use that data to further fine-tune the filtering.
- [X] Make it possible to use other column names to create graphs with, maybe based on same returned data from a query.
