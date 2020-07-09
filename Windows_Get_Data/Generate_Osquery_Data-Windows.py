#!/usr/bin/env python
# coding: utf-8

# ## Import needed modules
# Standard modules to use and manipulate dataframes
import pandas as pd, numpy as np, pathlib # pylint: disable=import-error
import os
# Used to be able to access locations on disk
from IPython import get_ipython

# ## Set global variables
#run once to get location of osqueryi on this system
path = "c:\\"
name = "osqueryi.exe"
for (root, dirs, files) in os.walk(path):
    if name in files:
        osquery_location = os.path.join(root)
print(osquery_location)
location = get_ipython().run_line_magic('pwd', '')
get_ipython().run_line_magic('cd', '$location')
tlocation = location + "\\tables_win"
osquery_bin = "osqueryi.exe"
hname = "osquery.io"
limit = 50
p = pathlib.Path(tlocation)
# ### Find all tables for this distribution of Osquery
#Browse to location of osquery on system
get_ipython().run_line_magic('cd', '-q $osquery_location')
windows_tables = get_ipython().getoutput('osqueryi .tables')
windows_tables = windows_tables.fields(1)
len(windows_tables)
#Filter out tables that are not compatible? That give where error or empty results?
tables_attention = ['authenticode','file','hash','ntfs_acl_permissions']
tables_osquery = ['osquery_events','osquery_extensions','osquery_flags','osquery_info','osquery_packs','osquery_registry','osquery_schedule']
tables_events_empty = ['ntfs_journal_events','powershell_events','windows_events','carves','carbon_black_info','curl','curl_certificate','chocolatey_packages']
#remove the above list using list comprension, also remove osquery tables as you would not easily use them for joining
windows_tables = [x for x in windows_tables if x not in tables_attention + tables_osquery + tables_events_empty]
len(windows_tables)
#Create folder for the tables
try:
    p.mkdir()
except:
    print ("Creation of the directory %s failed, location probably already exists" % tlocation)
else:
    print ("Successfully created the directory %s " % tlocation)
# ### JSON output for Osquery tables
# **Consider running the Notebook once as admin to get data from all the tables, if not admin results from tables like `bitlocker_info` will be empty**
get_ipython().run_line_magic('cd', '$osquery_location')
for wt in windows_tables:
    flocation = tlocation + '\\' + wt
    #LIMIT
    #get_ipython().system('osqueryi "SELECT * from {wt} LIMIT {limit};" --json > {flocation}.json')
    #ALL
    get_ipython().system('osqueryi "SELECT * from {wt};" --json > {flocation}.json"')
# With WHERE clause
get_ipython().run_line_magic('cd', '$osquery_location')
for wt in tables_attention:
    flocation = tlocation + '\\' + wt
    #LIMIT
    #get_ipython().system('osqueryi "SELECT * from {wt} WHERE path = \'{osquery_location}\\\\{osquery_bin}\' LIMIT {limit};" --json > {flocation}.json')
    #ALL
    get_ipython().system('osqueryi "SELECT * from {wt} WHERE path = \'{osquery_location}\\\\{osquery_bin}\';" --json > {flocation}.json"')
# CURL queries
get_ipython().run_line_magic('cd', '$osquery_location')
get_ipython().system('osqueryi "SELECT * from curl WHERE url = \'https://{hname}\';" --json > {tlocation}\\\\curl.json')
get_ipython().system('osqueryi "select * from curl_certificate WHERE hostname = \'{hname}\';" --json > {tlocation}\\\\curl_certificate.json"')
# ### Import results Osquery in DF
def osquery_data_extract(os_tables):
    data_columns = []
    for path in p.rglob("*.json"):
        os_t = path.stem
        data = pd.read_json(path, orient='records', encoding='ANSI')
        data = data.add_prefix(os_t+'.')
        for i in range(0, data.shape[0]):
            column_data = list(data.columns.values)
            value_data = list(data.values[i])
            column_value_data = list(zip(column_data,value_data))
            data_columns.append(column_value_data)
    return(data_columns)
data_extract = osquery_data_extract(windows_tables)
extract_df = pd.DataFrame([t for lst in data_extract for t in lst], columns = ['Table.Column','Data'])
extract_df.shape
#split Table.Column into separate columns
temp_table = extract_df['Table.Column'].str.split(".", n = 1, expand = True)
extract_df['Table'] = temp_table[0]
extract_df['Column'] = temp_table[1]
extract_df = extract_df[['Table','Table.Column','Column','Data']]
print(extract_df.shape)
#remove null and empty data fields
extract_df_clean = extract_df[(extract_df['Data'].notnull()) & (extract_df['Data'] != '')]
extract_df_clean.shape
extract_df_clean.drop_duplicates(keep='first', inplace=True) 
extract_df_clean.shape
#Filter out all entries with 2 or less characters in the Data field, to general to make good joins
extract_df_clean_filter = extract_df_clean[extract_df_clean.Data.map(str).apply(len) > 2]
extract_df_clean_filter.shape
#remove Table.Columns that have ambiguous information, checked it by looking at the Data
filtering_columns_data = ['etc_protocols.name','groups.gid_signed','pipes.max_instances','processes.handle_count','processes.system_time','processes.threads','routes.metric','routes.netmask','users.gid_signed','users.uid_signed']
extract_df_clean_filter = extract_df_clean_filter[~extract_df_clean_filter['Table.Column'].isin(filtering_columns_data)]
extract_df_clean_filter.shape
# Create an anonymized version of data before filtering
#anonimze Data column, create new column for now, drop Data
extract_df_clean_full = extract_df_clean_filter
extract_df_clean_full['anon'] = pd.factorize(extract_df_clean_full.Data)[0]
extract_df_clean_full.shape
#remove anon = -1
extract_df_clean_full = extract_df_clean_full[extract_df_clean_full.anon != -1]
#drop data to anonimize the table completely
extract_df_clean_full.drop(columns=['Data'],inplace=True)
extract_df_clean_full.shape
# Data with basic filtering
# 
get_ipython().run_line_magic('cd', '$location')
extract_df_clean_full.to_csv('data_for_graphs_full.csv',index=False)
# Data with only duplicates
extract_df_clean_filter_dup = extract_df_clean_filter[extract_df_clean_filter.duplicated(subset='Data', keep=False)]
extract_df_clean_filter_dup.shape
#anonimze Data column, create new column for now, drop Data
extract_df_clean_dup = extract_df_clean_filter_dup
extract_df_clean_dup['anon'] = pd.factorize(extract_df_clean_dup.Data)[0]
extract_df_clean_dup.shape
#remove anon = -1
extract_df_clean_dup = extract_df_clean_dup[extract_df_clean_dup.anon != -1]
#drop data to anonimize the table completely
extract_df_clean_dup.drop(columns=['Data'],inplace=True)
extract_df_clean_dup.shape
get_ipython().run_line_magic('cd', '$location')
extract_df_clean_dup.to_csv('data_for_graphs_dup.csv',index=False)