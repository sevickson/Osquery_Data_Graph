# Untangling the Osquery❓ tables web🕸 using Jupyter Notebooks📓 - Part 2 | With Data📜
This repository is used to hold Jupyter Notebooks that are used to work with Osquery table **DATA**.  

[![Treebeard notebook status](https://api.treebeard.io/sevickson/Jupyter_NBs/master/buildbadge)](https://treebeard.io/admin/sevickson/Jupyter_NBs/master "Latest notebook run")
![Lint Code Base](https://github.com/sevickson/Osquery_Data_Graph/workflows/Lint%20Code%20Base/badge.svg)
![Clean Jupyter NB](https://github.com/sevickson/Osquery_Data_Graph/workflows/Clean%20Jupyter%20NB/badge.svg)
![Windows | Linux | macOS Build](https://github.com/sevickson/Osquery_Data_Graph/workflows/Windows%20%7C%20Linux%20%7C%20macOS%20Build/badge.svg)

This work is based on my prior work on Osquery Tables:
- [Repository](https://github.com/sevickson/osquery_tables_graph)
- [Blog](https://medium.com/@sevickson/untangling-the-osquery-tables-web-using-jupyter-notebooks-7c979c03f42d)

This repository is divided as follows:
- [Generate Osquery Data](./1_Get_Data/Generate_Osquery_Data.py)
- [Merge Osquery Data](./Jupyter_NBs/2_Merge_Osquery_Data.ipynb)
- [Create Graph Osquery Graphistry](./Jupyter_NBs/3_Graph_Osquery_Data.ipynb)
- [REQ](REQ)
  - Requirements folder

This repository is based on [Untangling the Osquery❓ tables 🕸 using Data📜 | Part 2](https://sevickson.medium.com/untangling-the-osquery-tables-using-data-part-2-9579f997676d) blog.  
The graphs are based on Osquery data for Windows, Linux and MacOS.

To show the full potential of the graphs I created a dashboard that is hosted on Streamlit.
- [Dashboard](https://share.streamlit.io/sevickson/osquerygraphs_dashboard/main/osquerygraphs.py)
- [Repository Dashboard](https://github.com/sevickson/osquerygraphs_dashboard)

To set the graphistry account details to be able to create the graphs, copy `.env_template` and rename to `.env` and set your secrets there.

------------------------

From my prior work on `OSQuery-Tables` this repository handles following points:
- [X] Check the data returned from the tables when querying and use that data to further fine-tune the filtering.
- [X] Make it possible to use other column names to create graphs with, maybe based on same returned data from a query.
