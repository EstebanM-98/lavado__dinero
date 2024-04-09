import logging

class logs:
    def __init__(self, log_file):
        # Configurar el módulo logging para escribir en el archivo especificado
        logging.basicConfig(filename=log_file, level=logging.INFO,
                            format='%(asctime)s %(levelname)s: %(message)s')
        
        # Obtener el objeto logger
        self.logger = logging.getLogger()

    def info(self, message):
        # Escribir un mensaje de nivel INFO en el archivo de registro
        self.logger.info(message)

    def error(self, message):
        # Escribir un mensaje de nivel ERROR en el archivo de registro
        self.logger.error(message)

