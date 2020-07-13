# Run Osquery on Windows and Linux to get needed data for the graphs

![Lint Code Base](https://github.com/sevickson/Osquery_Data_Graph/workflows/Lint%20Code%20Base/badge.svg)
![Python Script CI](https://github.com/sevickson/Osquery_Data_Graph/workflows/Python%20Script%20CI/badge.svg)

## Windows
### Get Windows requirements 
[Python](https://www.microsoft.com/store/productId/9MSSZTT1N39L) needs to be installed, can be installed through the Windows Store
```cmd
python -m pip install --user --upgrade pip
pip install --user --upgrade -r requirements.txt
```

### Run the script on Windows
Run this script in an Administrator `cmd` terminal.
```cmd
python Generate_Osquery_Data-Windows_Linux.py
```

## Linux
Python >= 3.6 is needed.
If python3 is not already installed, please run following command.
```bash
sudo apt-get install python3
```
### Get Linux requirements 
```bash
python -m pip install --user --upgrade pip
pip install --user --upgrade -r requirements.txt
```

### Run the script on Linux
Run this script in a terminal.
`sudo` is needed to get all possible data from Osquery.
```bash
sudo python Generate_Osquery_Data-Windows_Linux.py
```

## MacOS
Python >= 3.6 is needed.
If python3 is not already installed, please run following command.
```bash
brew install python3
```
### Get MacOS requirements 
```bash
python -m pip install --user --upgrade pip
pip install --user --upgrade -r requirements.txt
```

### Run the script on MacOS
Run this script in a terminal.
`sudo` is needed to get all possible data from Osquery.
```bash
sudo python Generate_Osquery_Data-Windows_Linux.py
```

## CI/CD Test run
Run following for tests, set SQL query limit as a number.
```cmd
python Generate_Osquery_Data-Windows_Linux.py 1
```