# Run Osquery on Linux to get needed data for the graphs

## Get requirements
```bash
sudo apt-get install -y python3 python3-pip ipython3
python3 -m pip install --user --upgrade pip
python3 -m pip install --user --upgrade -r requirements.txt
```

## Run the script
```bash
sudo -E ipython3 Generate_Osquery_Data-Linux.py
```
