# Run Osquery on Windows and Linux to get needed data for the graphs

## Windows
### Get requirements
[Python](https://www.microsoft.com/store/productId/9MSSZTT1N39L) needs to be installed, can be installed through the Windows Store
```cmd
python -m pip install --user --upgrade pip
pip install --user --upgrade -r requirements.txt
```

### Run the script
Run this script in an Administrator `cmd` terminal.
```cmd
python Generate_Osquery_Data-Windows_Linux.py
```
Run following for tests, set SQL query limit as a number.
```cmd
python Generate_Osquery_Data-Windows_Linux.py 1
```

## Linux
Python >= 3.6 is needed.
If python3 is not already installed, please run following command.
```bash
sudo apt-get install python3
```
### Get requirements
```bash
python -m pip install --user --upgrade pip
pip install --user --upgrade -r requirements.txt
```

### Run the script
Run this script in a `bash` terminal.
`sudo` is needed to get all possible data from Osquery.
```bash
sudo python Generate_Osquery_Data-Windows_Linux.py
```
Run following for tests, set SQL query limit as a number.
```bash
python Generate_Osquery_Data-Windows_Linux.py 1
```