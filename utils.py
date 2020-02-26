import os
import requests
import shutil
from tqdm import tqdm_notebook as tqdm
import gzip

DATA_FOLDER = 'data'
PREDICTIONS_FOLDER = 'predictions'

GSPREADHSEET_DOWNLOAD_URL = "https://docs.google.com/spreadsheets/d/{gid}/export?format=xlsx&id={gid}".format

ESTACIONES_URL = GSPREADHSEET_DOWNLOAD_URL(gid="1YYACNoVCzvC6Cauayw6-OEvvD7fIB72f")
NCEP_NCAR_URL = GSPREADHSEET_DOWNLOAD_URL(gid="1AFHz-USHQN6Y5zLkEYWPQ2hWJT8LhDg6")
NDEFM_URL = GSPREADHSEET_DOWNLOAD_URL(gid="1jEitBJocFEEdo-VJagWAKxc-_bN8LKOt")

ESTACIONES_XLSX = os.path.join(DATA_FOLDER, 'estaciones.xlsx')
NCEP_NCAR_XLSX = os.path.join(DATA_FOLDER, 'ncep_ncar.xlsx')
NDEFM_XLSX = os.path.join(DATA_FOLDER, 'ndefm.xlsx')


DRIVE_DOWNLOAD_URL = "https://drive.google.com/uc?id={gid}&export=download".format


def download_file(url, dest, override=False, chunksize=4096):
    if os.path.exists(dest) and not override:
        return
    with requests.get(url, stream=True) as r:
        try:
            file_size = int(r.headers['Content-Length'])
        except KeyError:
            file_size = 0
        chunks = file_size // chunksize
        
        with open(dest, 'wb') as f, tqdm(total=file_size, unit='iB', unit_scale=True) as t:
            for chunkdata in r.iter_content(chunksize):
                f.write(chunkdata)
                t.update(len(chunkdata))


def ggunzip(source_filepath, dest_filepath, block_size=65536, override=False):
    if os.path.exists(dest_filepath) and not override:
        return
    source_size = os.path.getsize(source_filepath)
    with gzip.open(source_filepath, 'rb') as s_file, \
            open(dest_filepath, 'wb') as d_file, \
                tqdm(unit='iB', unit_scale=True) as t:
        while True:
            block = s_file.read(block_size)
            if not block:
                break
            else:
                d_file.write(block)
                t.update(len(block))
        d_file.write(block)
        t.update(len(block))


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
        download_file(url, item_path)
    
    # init predictions
    if not os.path.exists(PREDICTIONS_FOLDER):
        os.mkdir(PREDICTIONS_FOLDER)
        
    EXAMPLE_URL = DRIVE_DOWNLOAD_URL(gid="1ymp3mUPx-iU6nOoWLkvqxJSKS7biZCaf")
    
    example_path = os.path.join(PREDICTIONS_FOLDER, 'example.csv')
    
    download_file(EXAMPLE_URL, example_path)
