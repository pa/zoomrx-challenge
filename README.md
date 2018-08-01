# CSV data processor python script (ZoomRX challenge)

This repo contains a python script module which downloads set of compressed files from FTP server and processes a CSV file based on the given constraints

## Contents

- [ftp_downloader.py](ftp_downloader.py): This script downloads the compressed files from the FTP server
- [data_processor.py](data_processor.py): This script extracts the data out of XML files and produces a CSV
- [sample_output](./sample_output): This directory contains the sample CSV output from local execution
## How to run the script

pip install -r requirements.txt\
python ftp_downloader.py
