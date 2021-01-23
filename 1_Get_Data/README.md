# Run Osquery on Windows | Linux | macOS to get data📜 for the Osquery❓ tables graph🕸

![Lint Code Base](https://github.com/sevickson/Osquery_Data_Graph/workflows/Lint%20Code%20Base/badge.svg)
![Windows | Linux | macOS Build](https://github.com/sevickson/Osquery_Data_Graph/workflows/Windows%20%7C%20Linux%20%7C%20macOS%20Build/badge.svg)

<img src="https://www.game-experience.nl/wp-content/uploads/2018/04/Windows-10-logo-300x300.png" alt="Windows" width="40" height="40">  

## Windows
Python >= 3.6 is needed.  
[Python 3.8](https://www.microsoft.com/store/productId/9MSSZTT1N39L) can be installed through the Windows Store
### Get Windows requirements
```cmd
python -m pip install --user --upgrade pip
pip install --user --upgrade -r requirements.txt
```

### Run the script on Windows
Run this script in an Administrator `cmd` terminal.
```cmd
python Generate_Osquery_Data.py
```

<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/35/Tux.svg/1200px-Tux.svg.png" alt="Linux" width="40" height="40">

## Linux
Python >= 3.6 is needed.  
If python3 is not already installed, please run following command.
```bash
sudo apt-get install python3 python3-pip
```
### Get Linux requirements
```bash
python3 -m pip install --user --upgrade pip
more
```

### Run the script on Linux
Run this script in a terminal.  
`sudo` is needed to get all possible data from the Osquery tables.
```bash
sudo -E python3 Generate_Osquery_Data.py
```

<img src="https://cdn0.iconfinder.com/data/icons/flat-round-system/512/apple-512.png" alt="macOS" width="40" height="40">

## macOS
Python >= 3.6 is needed.  
If python3 is not already installed, please run following command.
```bash
brew update
brew install python3
```
### Get macOS requirements
```bash
python3 -m pip install --user --upgrade pip
python3 -m pip install --user --upgrade -r requirements.txt
```
### Install Osquery
Use the commands below to install the latest version of Osquery, if not already installed.
```bash
brew update
brew install --cask osquery
```

### Run the script on macOS
Run this script in a terminal.  
`sudo` is needed to get all possible data from the Osquery tables.
```bash
sudo python3 Generate_Osquery_Data.py
```

## CI/CD Test run
Following command van be used for tests, set SQL query output LIMIT as a number.
```cmd
python Generate_Osquery_Data.py 1
```