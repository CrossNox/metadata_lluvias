import os
import requests
import shutil

DATA_FOLDER = 'data'
PREDICTIONS_FOLDER = 'predictions'

des
GSPREADHSEET_DOWNLOAD_URL = "https://docs.google.com/spreadsheets/d/{gid}/export?format=xlsx&id={gid}".format

ESTACIONES_URL = GSPREADHSEET_DOWNLOAD_URL(gid="1YYACNoVCzvC6Cauayw6-OEvvD7fIB72f")
NCEP_NCAR_URL = GSPREADHSEET_DOWNLOAD_URL(gid="1AFHz-USHQN6Y5zLkEYWPQ2hWJT8LhDg6")
NDEFM_URL = GSPREADHSEET_DOWNLOAD_URL(gid="1jEitBJocFEEdo-VJagWAKxc-_bN8LKOt")

ESTACIONES_XLSX = os.path.join(DATA_FOLDER, 'estaciones.xlsx')
NCEP_NCAR_XLSX = os.path.join(DATA_FOLDER, 'ncep_ncar.xlsx')
NDEFM_XLSX = os.path.join(DATA_FOLDER, 'ndefm.xlsx')


DRIVE_DOWNLOAD_URL = "https://drive.google.com/uc?id={gid}&export=download".format



def download_file(url, dest):
    with requests.get(url, stream=True) as r:
        with open(dest, 'wb') as f:
            shutil.copyfileobj(r.raw, f)


def init_data():
    # download data
    if not os.path.exists(DATA_FOLDER):
        os.mkdir(DATA_FOLDER)

    data = {
        ESTACIONES_XLSX: ESTACIONES_URL,
        NCEP_NCAR_XLSX: NCEP_NCAR_URL,
        NDEFM_XLSX: NDEFM_URL
    }

    for item_path, url in data.items():
        if not os.path.exists(item_path):
            download_file(url, item_path)
    
    # init predictions
    if not os.path.exists(PREDICTIONS_FOLDER):
        os.mkdir(PREDICTIONS_FOLDER)
        
    EXAMPLE_URL = DRIVE_DOWNLOAD_URL(gid="1ymp3mUPx-iU6nOoWLkvqxJSKS7biZCaf")
    
    example_path = os.path.join(PREDICTIONS_FOLDER, 'example.csv')
    
    if not os.path.exists(example_path):
        download_file(EXAMPLE_URL, example_path)
