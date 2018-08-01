import gzip
import xml.etree.ElementTree as ET
import csv
import os
import threading

def main_data_processor():
    """
    Creates Substances.csv in local filesyastem and calls extract function.
    """

    try:
        substance_flie_list = os.listdir(os.path.join(os.getcwd(), 'Substances_Zip\\'))
        with open('Substances.csv', 'w', newline='') as csvfile:
            csvfile.truncate(0)
            fieldnames = ['PC-ID_id', 'PC-Substance_synonyms_E']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            pc_substance_synonyms_e = []
            pc_id = []

            for file_list in substance_flie_list:
                t1 = threading.Thread(target=parser(file_list, writer, pc_substance_synonyms_e, pc_id), name='t1')
                t1.start()

        csvfile.close()
    except:
        pass

def parser(file_list, writer, pc_substance_synonyms_e, pc_id):
    """
    Decompress the downloaded files and parse it to the CSV file.
    :param file_list: list of files to be parsed
    :param writer: Module object
    :param pc_substance_synonyms_e: array for storing PC-Substance_synonyms_E
    :param pc_id: array for storing PC-ID_id
    """
    with gzip.open(os.path.join(os.getcwd(), 'Substances_Zip\\') + file_list, 'rb') as f:
        file_content = f.read()

    print("\nExtracting...\n")

    tree = ET.ElementTree(ET.fromstring(file_content))
    root = tree.getroot()

    for elem in root:
        for subelem in elem:
            for sub1elem in subelem:
                if(sub1elem.tag == '{http://www.ncbi.nlm.nih.gov}PC-Substance_synonyms_E'):
                    pc_substance_synonyms_e.append(sub1elem.text)
                for sub2elem in sub1elem:
                    if(sub2elem.tag == '{http://www.ncbi.nlm.nih.gov}PC-ID_id'):
                        pc_id.append(sub2elem.text)

    length=len(pc_substance_synonyms_e)
    try:
        for current_length in range(0,length):
            writer.writerow({'PC-ID_id': pc_id[current_length],'PC-Substance_synonyms_E': pc_substance_synonyms_e[current_length] })

    except IndexError:
        pass

    pc_substance_synonyms_e.clear()
    pc_id.clear()

    print("Extracted to Substances.csv file in path :  " + os.getcwd())

main_data_processor()
