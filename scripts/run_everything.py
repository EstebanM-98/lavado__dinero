from etl import Etlnequi
from loggs import logs
import os


def orquestador(params,run):


    orq = Etlnequi(params,run)

    # Subir tabla
    if run['create_table_insum'] == 'si':
        try:
            print('Creando tabla de insumos')
            orq.querie_tools.create_table()

        except Exception as e:
            print(f'Error creando la tabla:{e}')

        # Subir tabla
        try:
            print('Insertando datos')
            orq.querie_tools.execute_many()

        except Exception as e:
            print(f'Error en la insercion de datos:{e}')

    try:
        print('Iniciando ejecucion de SQL')
        orq.run_sqls()

    except Exception as e:
        print(f'Error en la ejecucion de queries:{e}')

    try:
        print('Iniciando prueba de duplicados')
        orq.duplicatesTest()

    except Exception as e:
        print(f'Error en la ejecucion de campos nulos:{e}')

    try:
        print('Iniciando prueba de campos nulos')
        orq.nullTest()

    except Exception as e:
        print(f'Error en la ejecucion de campos nulos:{e}')

    try:
        print('Iniciando prueba de campos nulos')
        orq.nullTest()

    except Exception as e:
        print(f'Error en la ejecucion de campos nulos:{e}')

    try:
        print('Desconectando, gracias!')
        orq.querie_tools.getDisconnected()
    except Exception as e:
        print(f'Error en la insercion de datos:{e}')