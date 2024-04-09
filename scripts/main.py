from etl import Etlnequi
import json
import os
from run_everything import orquestador

rut_base = os.getcwd()
path_json =  os.path.join(rut_base,'scripts','read','params.json')

with open(path_json, 'r') as archivo:
    datos = json.load(archivo)

config = datos['config']
run = datos['run']

def main():

    orquestador(config,run)

main()