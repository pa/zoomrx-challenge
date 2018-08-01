#!/usr/bin/python

"""
This module is developed for downloading files from
FTP server("ftp.ncbi.nlm.nih.gov") and save it to the local filesystem.

"""

import sys
import ftplib
import os
import time
import errno
from retrying import retry


def main_ftp_downloader():
    """
    Main function which calls download_files function to download files.
    """
    server = "ftp.ncbi.nlm.nih.gov"
    source = "/pubchem/Substance/CURRENT-Full/XML/"
    destination = os.getcwd()

    try:
        ftp = ftplib.FTP(server)
        ftp.login()
    except:
        print("Error: Could not connect to FTP server")
        quit()
    download_files(source, destination, ftp)
    print("\nFiles Downloaded...!")



@retry(retry_on_exception=Exception)
def download(file, destination, ftp):
    """
    Downloads files from FTP Server.
    :param file: source path from FTP Server
    :param destination: local filesyatem path to store downloaded files
    :param ftp: module object
    """
    try:
        ftp.retrbinary("RETR " + file, open(os.path.join(destination + "\Substances_Zip\\", file),"wb").write)
        print ("Downloaded: " + file)
    except:
        print ("Error: File could not be downloaded " + file)

def download_files(path, destination, ftp):
    """
    Creates the directory to save downloaded files and calls download function to download.
    :param path: source path from FTP Server
    :param destination: local filesyatem path to store downloaded files
    :param ftp: module object
    """
    number_of_xml = 0
    try:
        ftp.cwd(path)
        os.chdir(destination)
        mkdir_p(os.path.join(destination, 'Substances_Zip'))
        print ("\nDownloading to path : " + destination +"\Substances_Zip\n")
    except OSError:
        pass
    except ftplib.error_perm:
        print ("Error: could not change to " + path)
        sys.exit("Ending Application")

    filelist=ftp.nlst()

    for file in filelist:
        if(file == "README-Substance-XML"):
            continue
        number_of_xml = number_of_xml + 1

        try:
            if(number_of_xml <= 20):
                ftp.cwd(path)
                download(file, destination, ftp)

            else:
                break

        except ftplib.error_perm:
            os.chdir(destination)
    return

def mkdir_p(path):
    """
    Creates directory
    :param path: source path from FTP Server
    """
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

main_ftp_downloader()

from data_processor import main_data_processor
