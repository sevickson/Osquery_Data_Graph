# Run Osquery on Linux to get needed data for the graphs

## Get requirements
[Python](https://www.microsoft.com/store/productId/9MSSZTT1N39L) needs to be installed, can be installed through the Windows Store
```cmd
python -m pip install --user --upgrade pip
pip install --user --upgrade -r requirements.txt
```

## Run the script
Run this script in an Administrator `cmd` terminal.
```cmd
python Generate_Osquery_Data-Windows_Linux.py
```
Run following for tests, set SQL query limit as a number.
```cmd
python Generate_Osquery_Data-Windows_Linux.py 1
```
