from lib_sql import SQLtools
import os
import pandas as pd
from loggs import logs

class Etlnequi:

    def __init__(self,params,run):
        
        self.querie_tools = SQLtools(params)
        self.run = run
        self.log_reg = logs(os.path.join(os.getcwd(),'scripts','read','logs','logs.log'))

    def run_sqls(self):

                # Obtener el directorio de trabajo actual
        ruta_base = os.getcwd()
        # Construir la ruta completa hasta el directorio 'SQL' dentro del directorio 'Scripts'
        for archiv_sql in self.run['sql']:

    # Código que puede generar un error para algunos valores
            cod_sql = self.querie_tools.getSql(os.path.join(ruta_base,'scripts','read','sql',archiv_sql))

            for queries in cod_sql:

                try:

                    exec_sql = self.querie_tools.executeSql(queries)
                    

                except Exception as e:
                    # Captura el error y muestra un mensaje
                    print(f"Error al procesar el valor {archiv_sql}: {e}")
                    # Continúa con el siguiente valor en el ciclo
                    continue

                print(f'Ejecucion exitosa del querie: {archiv_sql}')
                
    def proofDuplicates(self,table_name):
        
        # Consulta SQL para seleccionar filas duplicadas
        ruta_base = os.getcwd()
        # Intentar conectar a la base de datos y ejecutar la consulta
        try:
            print('Ejecutando prueba de duplicados')
            self.log_reg.info('Ejecutando prueba de duplicados')
            cursor = self.querie_tools.conn.cursor(buffered=True)
            cursor.execute(f"DESCRIBE {table_name}")
            columnas = [columna[0] for columna in cursor.fetchall()]
            cols = ','.join(columnas)
            consulta_sql = f"SELECT *, COUNT(*) FROM %s GROUP BY %s  HAVING COUNT(*) > 1" % (table_name,cols)

            conn = self.querie_tools.engine
  
            # Ejecutar la consulta y guardar los resultados en un DataFrame
            df = pd.read_sql_query(consulta_sql, conn)
            
            # Guardar el DataFrame en un archivo Excel
            nombre_archivo_excel = os.path.join(ruta_base,'scripts','read','excel','filas_duplicadas_usuarios.xlsx')
            
            df.to_excel(nombre_archivo_excel, index=False)

            print(f'Resultados guardados en {nombre_archivo_excel}')

            print(f'Prueba duplicados completada: {table_name}')
            self.log_reg.info(f'Prueba duplicados completada: {table_name}')

        except Exception as err:
             self.log_reg.error(f'Fallo en prueba de duplicados,{table_name} : {err}')

    def duplicatesTest(self):

        for archiv_result in self.run['archivos_resultados']:

            try:
        # Código que puede generar un error para algunos valores
                
                self.proofDuplicates(archiv_result)

            except Exception as e:
                # Captura el error y muestra un mensaje
                print(f"Error al procesar el archivo {archiv_result}: {e}")
                # Continúa con el siguiente valor en el ciclo
                continue


    def proofNull(self,table_name):
        
        # Consulta SQL para seleccionar filas duplicadas
        ruta_base = os.getcwd()
    # Intentar conectar a la base de datos y ejecutar la consulta
        cursor = self.querie_tools.conn.cursor(buffered=True)
        cursor.execute(f"DESCRIBE {table_name}")
        columnas = [columna[0] for columna in cursor.fetchall()]

        for j in columnas:

            try:
                consulta_sql = f'''SELECT 
                                SUM(CASE WHEN %s IS NULL THEN 1 ELSE 0 END) 
                                AS nulos_en_columna1 FROM %s
                                ''' % (j,table_name)

                conn = self.querie_tools.engine

                # Ejecutar la consulta y guardar los resultados en un DataFrame
                df = pd.read_sql_query(consulta_sql, conn)
            
                # Guardar el DataFrame en un archivo Excel
                nombre_archivo_excel = os.path.join(ruta_base,'scripts','read','excel','nulos.xlsx')
            
                df.to_excel(nombre_archivo_excel, index=False)

            except Exception as err:
                self.log_reg.error(f'Fallo en prueba de nulidad, {table_name} : {err}')
                  
                continue

        print(f'Resultados guardados en {nombre_archivo_excel}')

        print(f'Prueba de nulidad completada: {table_name}')
        self.log_reg.info(f'Prueba de nulidad completada: {table_name}')
            
    def nullTest(self):

        for archiv_result in self.run['archivos_resultados']:

            try:
        # Código que puede generar un error para algunos valores
                
                self.proofNull(archiv_result)

            except Exception as e:
                # Captura el error y muestra un mensaje
                print(f"Error al procesar el archivo {archiv_result}: {e}")
                # Continúa con el siguiente valor en el ciclo
                continue

    
    def proofCount(self,table_name):

        cursor = self.querie_tools.conn.cursor(buffered=True)
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        columnas = [columna[0] for columna in cursor.fetchall()]
        threshold = 1000000
        if columnas < threshold :
            print(f'El numero de registros es menor al threshold {threshold}')
        else:
            print(f'La tabla: {table_name} excede el numero de valores permitidos')


    def countTest(self):

        for archiv_result in self.run['archivos_resultados']:

            try:
        # Código que puede generar un error para algunos valores
                print(f'Prueba de conteo para la tabla: {archiv_result}')
                self.log_reg.info(f'Prueba de conteo para la tabla:{archiv_result}')

                self.proofCount(archiv_result)

            
            except Exception as e:
                # Captura el error y muestra un mensaje
                print(f"Error al procesar el archivo {archiv_result}: {e}")
                # Continúa con el siguiente valor en el ciclo
                continue

            print(f'Prueba de conteo para la tabla completa: {archiv_result}')
            self.log_reg.info(f'Prueba de conteo para la tabla completa: {archiv_result}')




