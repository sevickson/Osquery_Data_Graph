#!/usr/bin/env python3
# coding: utf-8

from IPython import get_ipython 
# Standard modules to use and manipulate dataframes
import pandas as pd, numpy as np, pathlib,shutil

#Variables
hname = "osquery.io"
location = get_ipython().run_line_magic('pwd', '')
tllocation = location + "/table_data_lnx"
csvlocation = location + "/CSV"
pcsv = pathlib.Path(csvlocation)
pl = pathlib.Path(tllocation) 
osquery_l_location = get_ipython().getoutput('which osqueryi')
osquery_l_location = ''.join(osquery_l_location)

#Osquery table lists
osquery_tables = ['osquery_events','osquery_extensions','osquery_flags','osquery_info','osquery_packs','osquery_registry','osquery_schedule']
curl_tables = ['curl','curl_certificate']

where_tables_l = ['elf_dynamic','elf_info','elf_sections','elf_segments','elf_symbols','file','hash','magic','yara']
#Tables that are event tables or tables that have not uniform WHERE constraints
error_tables_l = ['file_events','hardware_events','process_events','process_file_events','selinux_events','socket_events','syslog_events','user_events','yara_events','carves','device_file','device_partitions','docker_container_fs_changes','docker_container_processes','docker_container_stats','lxd_instance_config','lxd_instance_devices','prometheus_metrics','device_hash','lldp_neighbors','smart_drive_info','carbon_black_info','augeas']

# ## Install Osquery on Linux
def install_osquery_linux():
    if shutil.which("osqueryi") is None:
        get_ipython().system("apt-get update")
        get_ipython().system("apt-get -y install gnupg software-properties-common")
        #OSQUERY_KEY='1484120AC4E9F8A1A577AEEE97A80C63C9D8B80B'
        get_ipython().system("apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys '1484120AC4E9F8A1A577AEEE97A80C63C9D8B80B'")
        get_ipython().system("add-apt-repository 'deb [arch=amd64] https://pkg.osquery.io/deb deb main'")
        get_ipython().system("apt-get update")
        get_ipython().system("apt-get -y install osquery")
    else:
        get_ipython().system("osqueryi --version")
        print("Osquery already installed")

def create_folder(p,tlocation):
    #Create folder for the tables
    try:
        p.mkdir()
    except:
        print ("Creation of the directory %s failed, location probably already exists" % tlocation)
    else:
        print ("Successfully created the directory %s " % tlocation) 

# ## Get Osquery data Linux - JSON output
def osquery_tables_os():
    osq_tables = get_ipython().getoutput('osqueryi .tables')
    osq_tables = osq_tables.fields(1)
    return(osq_tables)

def run_on_linux(tables,tlocation):
    for wt in tables:
        if wt not in error_tables_l and wt not in osquery_tables:
            flocation = tlocation + wt 
            if wt in curl_tables:
                if wt == 'curl':
                    command = '"SELECT * from '+wt+' WHERE url = \'https://'+hname+'\';" --json > '+flocation+'.json'
                    get_ipython().system("osqueryi $command")
                else:
                    command = '"SELECT * from '+wt+' WHERE hostname = \''+hname+'\';" --json > '+flocation+'.json'
                    get_ipython().system("osqueryi $command")
            elif wt in where_tables_l:
                command = '"SELECT * from '+wt+' WHERE path = \''+osquery_l_location+'\';" --json > '+flocation+'.json'
                get_ipython().system("osqueryi $command")
            else:
                command = '"SELECT * from '+wt+';" --json > '+flocation+'.json'
                get_ipython().system("osqueryi $command")

def run_osquery_linux(p,tables,tlocation):
    create_folder(p,tlocation)
    flocation = tlocation + '/' 
    run_on_linux(tables,flocation)

# ## Handling Osquery data
def osquery_data_extract(p):
    print('osquery_data_extract')
    data_columns = []
    for path in p.rglob("*.json"):
        os_t = path.stem
        data = pd.read_json(path, orient='records')#, encoding='ANSI')
        data = data.add_prefix(os_t+'.')
        for i in range(0, data.shape[0]):
            column_data = list(data.columns.values)
            value_data = list(data.values[i])
            column_value_data = list(zip(column_data,value_data))
            data_columns.append(column_value_data)
    return(data_columns)

def filter_osquery_data(df):
    #Split Table.Column into separate columns
    temp_table = df['Table.Column'].str.split(".", n = 1, expand = True)
    df['Table'] = temp_table[0]
    df['Column'] = temp_table[1]
    df = df[['Table','Table.Column','Column','Data']]

    #Remove null and empty data fields
    extract_df_clean = df[(df['Data'].notnull()) & (df['Data'] != '')]
    extract_df_clean.drop_duplicates(keep='first', inplace=True) 

    #Filter out all entries with 2 or less characters in the Data field, these entries are too general to make good joins
    extract_df_clean_filter = extract_df_clean[extract_df_clean.Data.map(str).apply(len) > 2]
    return(extract_df_clean_filter)

def anonymize_data(extract_df_clean_full):
    #Anonimze Data column, create new column for now, drop Data later
    extract_df_clean_full['anon'] = pd.factorize(extract_df_clean_full.Data)[0]
    extract_df_clean_full = extract_df_clean_full[extract_df_clean_full.anon != -1]
    #Drop data to anonymize the table completely
    extract_df_clean_full.drop(columns=['Data'],inplace=True)
    return(extract_df_clean_full)

def get_dup_data(df):
    extract_df_clean_filter_dup = df[df.duplicated(subset='Data', keep=False)]
    extract_df_clean_filter_dup_anon = anonymize_data(extract_df_clean_filter_dup)
    return(extract_df_clean_filter_dup_anon) 

#Check if Osquery is installed, if not install it.
install_osquery_linux()

#Get Osquery table list and get all data
lnx_tables = osquery_tables_os()
run_osquery_linux(pl,lnx_tables,tllocation) 

# ### Linux
# Create a DataFrame from the data extracted from Osquery.
data_extract_lin = osquery_data_extract(pl)
extract_df_lin = pd.DataFrame([t for lst in data_extract_lin for t in lst], columns = ['Table.Column','Data'])
print(extract_df_lin.shape) 

# Make Table and Column columns, remove empty or NULL entries.  
# Filter out all entries with 2 or less characters in the Data field, these entries are too generic to make good joins.
filtered_data_lin = filter_osquery_data(extract_df_lin)
print(filtered_data_lin.shape) 

# Anonymize the data and remove the Data column.
filtered_data_lin_anon = anonymize_data(filtered_data_lin)

# Save CSV with only basic filtering
print(filtered_data_lin_anon.shape)
create_folder(pcsv,csvlocation)
filtered_data_lin_anon.to_csv(csvlocation + '/data_for_graphs_full_linux.csv',index=False) 

# Create DataFrame with only duplicata data.  
# Save CSV with duplicate filtering.
filtered_data_lin_anon_dup = get_dup_data(filtered_data_lin)
print(filtered_data_lin_anon_dup.shape)
filtered_data_lin_anon_dup.to_csv(csvlocation + '/data_for_graphs_dup_linux.csv',index=False) 


