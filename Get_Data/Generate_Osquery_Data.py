#  Imports and Functions
import platform, requests, os, pathlib, shutil, sys # pylint: disable=import-error
# Standard modules to use and manipulate dataframes
import pandas as pd, numpy as np # pylint: disable=import-error

#Varables
hname = "osquery.io"

#command line arguments for CI testing
if len(sys.argv) == 2:
    limit = ' LIMIT ' + sys.argv[1]
else:
    limit = ''

def create_folder(p,tlocation):
    #Create folder for the tables
    try:
        p.mkdir()
    except:
        print ("Creation of the directory %s failed, location probably already exists" % tlocation)
    else:
        print ("Successfully created the directory %s " % tlocation)

def install_on_linux():
    if platform.system() == "Darwin":
        os.system('brew update')
        os.system('brew cask install osquery')
    elif platform.system() == "Linux":
        os.system('sudo apt-get update')
        os.system('sudo apt-get -y install gnupg software-properties-common')
        OSQUERY_KEY='1484120AC4E9F8A1A577AEEE97A80C63C9D8B80B'
        os.system('sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys ' + OSQUERY_KEY)
        os.system("sudo add-apt-repository 'deb [arch=amd64] https://pkg.osquery.io/deb deb main'")
        os.system('sudo apt-get update')
        os.system('sudo apt-get -y install osquery')

def install_osquery_wsl_linux():
    if shutil.which("osqueryi") is None:
        install_on_linux()
    else:
        print("Osquery already installed")

def install_osquery_windows():#win_osq):
    if os.path.isfile('C:\\Program Files\\osquery\\osqueryi.exe'):
        print("Osquery already installed")
    else:
        version = "4.4.0"
        url = f'https://pkg.osquery.io/windows/osquery-{version}.msi'
        #First find name of file to be used for installing
        if url.find('/'):
            osquery_filename = url.rsplit('/', 1)[1]
            #Download file to current location
            r = requests.get(url, allow_redirects=True)
            open(osquery_filename, 'wb').write(r.content)
        #Install the Osquery MSI without interaction and also write out a log file in the same location to check if anything went wrong.
        os.system('msiexec /i ' + osquery_filename + ' /quiet /log "osquery-install.log"')
        print("Osquery installed")

def osquery_tables_os(os_osq):
    osq_tables = os.popen('\"' + os_osq + 'osqueryi\" .tables').read().strip().split("\n")
    osq_tables = [o.strip('   =>') for o in osq_tables]
    return(osq_tables)

def run_on_wsl_linux(tables,tlocation):
    osquery_bin = shutil.which("osqueryi")
    for wt in tables:
        if wt not in error_tables_l and wt not in osquery_tables:
            flocation = tlocation + '/' + wt 
            if wt in curl_tables:
                if wt == 'curl':
                    command = 'osqueryi "SELECT * from ' + wt + ' WHERE url = \'https://' + hname + '\'' + limit + ';" --json > ' + flocation + '.json'
                    os.system(command)
                else:
                    command = 'osqueryi "SELECT * from ' + wt + ' WHERE hostname = \'' + hname + '\'' + limit + ';" --json > ' + flocation + '.json'
                    os.system(command)
            elif wt in where_tables_l:
                command = 'osqueryi "SELECT * from ' + wt + ' WHERE path = \'' + osquery_bin + '\'' + limit + ';" --json > ' + flocation + '.json'
                os.system(command)
            else:
                command = 'osqueryi "SELECT * from ' + wt + limit + ';" --json > ' + flocation + '.json'
                os.system(command)

def run_osquery_windows(tables,tlocation):
    #create_folder(p,tlocation)
    #https://stackoverflow.com/questions/56624801/os-system-with-spaces-in-path
    osquery_w_location = 'C:\\"Program Files\\osquery\\osqueryi.exe"'
    #used specifically for the queries, otherwise issues with '' and ""
    osquery_bin = "'C:\\Program Files\\osquery\\osqueryi.exe'"
    #import subprocess
    for wt in tables:
        if wt not in error_tables_w and wt not in osquery_tables:
            flocation = tlocation + '\\' + wt
            #print('run',flocation)
            if wt in curl_tables:
                if wt == 'curl':
                    command = osquery_w_location + ' "SELECT * from ' + wt + ' WHERE url = \'https://' + hname + '\'' + limit + ';" --json > ' + flocation + '.json'
                    os.system(command)
                else:
                    command = osquery_w_location + ' "SELECT * from ' + wt + ' WHERE hostname = \'' + hname + '\'' + limit + ';" --json > ' + flocation + '.json'
                    os.system(command)
            elif wt in where_tables_w:
                command = osquery_w_location + ' "SELECT * from ' + wt + ' WHERE path = ' + osquery_bin + limit + ';" --json > ' + flocation + '.json'
                os.system(command)
            else:
                command = osquery_w_location + ' "SELECT * from ' + wt + limit + ';" --json > ' + flocation + '.json'
                #print(command)
                os.system(command)
        else:
            pass

def osquery_data_extract(p):
    data_columns = []
    for path in p.rglob("*.json"):
        os_t = path.stem
        #print(os_t,path.stat().st_size)
        if platform.system() == "Windows":
            data = pd.read_json(path, orient='records', encoding='ANSI')
        else: 
            data = pd.read_json(path, orient='records')
    
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
    #.copy() to fix error: SettingWithCopyWarning: A value is trying to be set on a copy of a slice from a DataFrame.
    #https://github.com/pandas-dev/pandas/issues/17476
    extract_df_clean = df[(df['Data'].notnull()) & (df['Data'] != '')].copy()
    extract_df_clean.drop_duplicates(keep='first', inplace=True) 

    #Filter out all entries with 2 or less characters in the Data field, these entries are too general to make good joins
    extract_df_clean_filter = extract_df_clean[extract_df_clean.Data.map(str).apply(len) > 2]
    return(extract_df_clean_filter)

def anonymize_data(df):
    #Anonimze Data column, create new column for now, drop Data later
    #.copy() to fix error: SettingWithCopyWarning: A value is trying to be set on a copy of a slice from a DataFrame.
    #https://github.com/pandas-dev/pandas/issues/17476
    extract_df_clean_full = df.copy()
    extract_df_clean_full['anon'] = pd.factorize(df.Data)[0]
    extract_df_clean_full = extract_df_clean_full[extract_df_clean_full.anon != -1]
    #Drop data to anonymize the table completely
    extract_df_clean_full.drop(columns=['Data'],inplace=True)
    return(extract_df_clean_full)

def get_dup_data(df):
    extract_df_clean_filter_dup = df[df.duplicated(subset='Data', keep=False)]
    extract_df_clean_filter_dup_anon = anonymize_data(extract_df_clean_filter_dup)
    return(extract_df_clean_filter_dup_anon)

osquery_tables = ['osquery_events','osquery_extensions','osquery_flags','osquery_info','osquery_packs','osquery_registry','osquery_schedule']
curl_tables = ['curl','curl_certificate']

where_tables_l = ['elf_dynamic','elf_info','elf_sections','elf_segments','elf_symbols','file','hash','magic','yara']
#Tables that are event tables or tables that have not uniform WHERE constraints
error_tables_l = ['file_events','hardware_events','process_events','process_file_events','selinux_events','socket_events','syslog_events','user_events','yara_events','carves','device_file','device_partitions','docker_container_fs_changes','docker_container_processes','docker_container_stats','lxd_instance_config','lxd_instance_devices','prometheus_metrics','device_hash','lldp_neighbors','smart_drive_info','carbon_black_info','augeas']

where_tables_w = ['authenticode','file','hash','ntfs_acl_permissions']
#Tables that are event tables or tables that have not uniform WHERE constraints
error_tables_w = ['ntfs_journal_events','powershell_events','windows_events','carves','carbon_black_info','chocolatey_packages']

if platform.system() == "Windows":
    #Windows
    print(platform.system())
    location = os.getcwd()
    twlocation = location + "\\table_data_win"
    pw = pathlib.Path(twlocation)
    csvlocation = location + "\\Data"
    pcsv = pathlib.Path(csvlocation)

    #extra "" on purpose because it needs to pass this argument as-is to commandline
    osquery_w_location = '"C:\\Program Files\\osquery\\osqueryi.exe"'
    win_osq_loc = 'C:\\Program Files\\osquery\\'

    #Create folders
    create_folder(pw,twlocation)
    create_folder(pcsv,csvlocation)

    #  Install Osquery on Windows
    install_osquery_windows()

    #  Get Osquery data Windows - JSON output
    # **Consider running this part of the Jupyter Notebook once as Administrator to get data from all the tables, if not admin results from tables like `bitlocker_info` will be empty**    
    windows_tables = osquery_tables_os(win_osq_loc)

    run_osquery_windows(windows_tables,twlocation)

    #  Handling Osquery data
    # # Windows
    # Create a DataFrame from the data extracted from Osquery.
    data_extract_win = osquery_data_extract(pw)

    extract_df_win = pd.DataFrame([t for lst in data_extract_win for t in lst], columns = ['Table.Column','Data'])
    #print(extract_df_win.shape)
    # Make Table and Column columns, remove empty or NULL entries.  
    # Filter out all entries with 2 or less characters in the Data field, these entries are too generic to make good joins.
    filtered_data_win = filter_osquery_data(extract_df_win)
    #print(filtered_data_win.shape)
    # Anonymize the data and remove the Data column.
    #print(filtered_data_win.columns)
    filtered_data_win_anon = anonymize_data(filtered_data_win)
    #print(filtered_data_win_anon.columns)
    # Save CSV with only basic filtering
    #print(filtered_data_win_anon.shape)
    filtered_data_win_anon.to_csv(location + '\\Data\\data_for_graphs_full_windows.csv',index=False)
    # Create DataFrame with only duplicata data.  
    # Save CSV with duplicate filtering.
    filtered_data_win_anon_dup = get_dup_data(filtered_data_win)
    #print(filtered_data_win_anon_dup.shape)
    filtered_data_win_anon_dup.to_csv(location + '\\Data\\data_for_graphs_dup_windows.csv',index=False)

elif platform.system() == "Linux" or platform.system() == "Darwin":
    #Linux
    print(platform.system())
    location = os.getcwd()
    tllocation = location + "/table_data_lnx"
    pl = pathlib.Path(tllocation)
    csvlocation = location + "/Data"
    pcsv = pathlib.Path(csvlocation)
    lnx_osq = ''

    #Create folders
    create_folder(pl,tllocation)
    create_folder(pcsv,csvlocation)

    install_osquery_wsl_linux()
    #  Get Osquery data Linux - JSON output
    # This works directly on the Linux system.
    lnx_tables = osquery_tables_os(lnx_osq)
    run_on_wsl_linux(lnx_tables,tllocation)
    # Create a DataFrame from the data extracted from Osquery.
    data_extract_lin = osquery_data_extract(pl)
    extract_df_lin = pd.DataFrame([t for lst in data_extract_lin for t in lst], columns = ['Table.Column','Data'])
    #print(extract_df_lin.shape)
    # Make Table and Column columns, remove empty or NULL entries.  
    # Filter out all entries with 2 or less characters in the Data field, these entries are too generic to make good joins.
    #print(extract_df_lin.shape)
    filtered_data_lin = filter_osquery_data(extract_df_lin)
    #print(filtered_data_lin.shape)
    # Anonymize the data and remove the Data column.
    #print(filtered_data_lin.columns)
    filtered_data_lin_anon = anonymize_data(filtered_data_lin)
    #print(filtered_data_lin_anon.columns)
    # Save CSV with only basic filtering
    #print(filtered_data_lin_anon.shape)
    filtered_data_lin_anon.to_csv(location + '/Data/data_for_graphs_full_linux.csv',index=False)
    # Create DataFrame with only duplicata data.  
    # Save CSV with duplicate filtering.
    filtered_data_lin_anon_dup = get_dup_data(filtered_data_lin)
    #print(filtered_data_lin_anon_dup.shape)
    filtered_data_lin_anon_dup.to_csv(location + '/Data/data_for_graphs_dup_linux.csv',index=False)