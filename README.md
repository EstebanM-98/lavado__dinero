# lavado_dinero

lavado_dinero es un proyecto destinado a la creación de una etl y un orquestador para la detección de patrones en lavado de dinero.

# Estructura del repositorio.

$$
project_nequi/
│
├── README.md          # Archivo con información sobre el proyecto
├── requirements.txt   # Archivo con las dependencias del proyecto
├── setup.py           # Archivo para instalar el proyecto como un paquete
├── .gitignore         # Archivo para especificar los archivos/directorios que no se deben rastrear en Git
│
├── scripts/           # Directorio para el código fuente del proyecto
│   ├── read/          # Directorio para carpetas con archivos de escritura y lectura
│   │   ├── excel/      # Directorio con archivos de excel con pruebas de datos
│   │   ├── logs/       # Directorio con archivo .log 
│   │   ├── sql         # Directorio con archivos .sql a ejecutar
│   │   └── params.json # Diccionario con instrucciones y credenciales de ejecucion.
│   ├── __init__.py    # Archivo que indica que este directorio es un paquete de Python
│   ├── etl.py     # Módulo que contiene la etl del proyecto
│   ├── lib_sql.py    # Módulo que contiene la clase para conectar con AWS RDS y ejecutar queries
│   ├── loggs.py     # Módulo para ejecutar logs
│   ├── main.py     # Módulo para correr el proyecto
│   └── run_everything.py  # Módulo para ejecutar solo lo establecido en params.json
│
├── imagenes/  # Imagenes de resultados y otras cosas del proyecto
│
├── docs/   # Directorio para documentacion y diccionario de datos
│   ├── diccionario_datos/   # Directorio del diccionario de datos
│   │   └── METADATA.xlsx   # Diccionario de datos
│   └── Material_estudio/  # Material de estudio para llevar a cabo el proyecto junto con certificados obtenidos
│
├── tests/             # Directorio para pruebas unitarias y de integración
│   ├── test_modulo1.py   # Pruebas para el módulo 1
│   └── test_modulo2.py   # Pruebas para el módulo 2
│
└── data/              # Directorio para documentación
    └── LI-Small_Trans.csv     # Datos insumo del proyecto. Fuente: kaggle
$$

# Ejecucion.

- Clone el proyecto.
- Cree un ambiente virtual.
- Instale las librerias con el requirements.txt
- Corra el script llamada main.py dentro de scripts



# Descripcion del paso a paso del desarrollo del proyecto:

# Alcance del proyecto y captura de datos

- Identificar y recopilar los datos que usaras para tu proyecto:
La base de datos utilizada se basa en una simulación propuesta por IBM en el cual se propone un ambiente transaccional “real” en el cual diferentes individuos por medio de diferentes bancos transfieren dinero entre sí. La simulación admite que diferentes personas puedan estar lavando dinero por medio de una banco, através de una canal de transacción. La base de datos tiene información sobre que transferencias que han sido catalogadas como lavado de dinero mediante una red neuronal (para conocer conocer en detalle los tipos de datos de esta base consulte en el repositorio docs/diccionario_datos/METADATA.xlsx la tabla llamada Dataorigin) 

Fuente de datos: https://www.kaggle.com/datasets/ealtman2019ibm-transactions-for-anti-money-laundering-aml/code

- Explicar para qué casos de uso final deseas preparar los datos, por ejemplo: tabla de análisis, aplicación de fondo, base de datos de fuentes de verdad, etc.): Este proyecto busca agrupar los datos marcados como lavado de activos en la referencia anteriormente enunciada en dos tablas de analisis. La primera con información detallada acerca de los casos que fueron detectados como lavado de activo, esta tabla contendra información acerca de el orirginario cuanto le transfirio a un destinario, qué cantidad de veces, a cuanto en porcentaje respecto al total de transferencias equivale eso. La segunda es un consolidado de la primera. (para conocer conocer en detalle los tipos de datos de estas dos tablas consulte en el repositorio docs/diccionario_datos/METADATA.xlsx las tablas info_transacciones_persona_fraude y info_transacciones_consolid_fraud)

# Explorar y evaluar los datos, el EDA.

- Explorar los datos para identificar problemas de calidad de los datos, como valores perdidos, datos duplicados, problemas de formato etc: La tabla de insumos elegida por defecto no presenta problemas problemas como valores perdidos, sin embargo, puede tener valores duplicados además de problemas de formato en el timestamp (para conocer conocer en detalle los tipos de datos de esta base consulte en el repositorio docs/diccionario_datos/METADATA.xlsx la tabla llamada Dataorigin) 
- Documentar los pasos necesarios para limpiar los datos, indicar que tipo de pasos se sugieren para la limpieza. Tip se puede usar un diagrama, mapa mental o adición en la arquitectura del paso siguiente con el fin de dejar claro este paso: El siguiente diagrama muestra los pasos necesarios para limpiar de manera efectiva los insumos utilizados.

![defect](https://github.com/EstebanM-98/lavado_dinero/blob/main/images/diagram1.png)

#  Definir el modelo de datos

- Trazar el modelo de datos conceptual y explicar por qué se eligió ese modelo: dado que la base de datos elegida consiste en un conjunto de transacciones marcadas con la etiqueta correspondiente a lavado de activo (0 o 1) nuestro modelo busca ir un paso paso allá de esto y es la construcción de una tabla que tenga información acerca de por qué (en caso de ser posbile) el modelo presentado en la referencia lo marco de esta manera. Esto es identificar patrones transaccionales ya sea por dinero o por número de veces transferidas a ciertas personas.

![defect0](https://github.com/EstebanM-98/lavado_dinero/blob/main/images/diagram3.png)
  
- Diseñar la arquitectura y los recursos utilizados. Indique claramente los motivos de la elección de las herramientas y tecnologías para el proyecto.

![defect2](https://github.com/EstebanM-98/lavado_dinero/blob/main/images/diagram2.png)

tecnologias: python, AWS RDS con motor de base de datos Mysql. La elección se basa en que los queries no son muy muy pesados y que se esta consumiendo en general poco espacio. Python en general tiene gran versatilidad y bastante documentación para la implementación de la ETL.

# Ejecutar la ETL

- Crear las tuberías de datos y el modelo de datos: La tuberia de datos no se logro completar usando una tecnologia de AWS por cuestiones de tiempo, sin embargo, se programi algo que es casi equivalente usando python.
  Dentro de la carpeta scripts existen dos modulos llamados run_everything.py y etl.py. El primero orquesta las funcionalidades de la etl, y la etl corre el modelo de datos implementado.
- Ejecutar controles de calidad de los datos para asegurar que la tubería funcionó como se esperaba: Los controles de calidad se ejecutan
- Control de calidad en los datos con la integridad en la base de datos relacional (por ejemplo, clave única, tipo de datos, etc.): En la etl se han creado prueba para la verificacion de campos nulos, testear duplicados, entre otras cosas.
- Pruebas de unidad para los “Script” para asegurar que están haciendo lo correcto: no se logro hacer por cuestiones de tiempo, sin embargo usando unittest y con ayuda de chatgpt se podría hacer facilmente.
- Comprobaciones de fuente/conteo para asegurar la integridad de los datos: Se ha creado una funcion en la ETL que deja un registro de los datos correspondientes a las tablas finales. Este deja un registro de cuanto y en función de un threshold dispara una alerta.
- Incluir un diccionario de datos: el diccionario de datos se ha agregado en docs/diccionario_datos/METADATA.xlsx
- Criterio de reproducibilidad: La reprodubilidad no se ha garantizado estrictamente hablando, sin embargo, se ha desarrollado sobre un entorno virtual y con la version de python 3.11.5. En caso de que se busque un criterio de reproducibilidad estricto, se sugiere usar docker. Este no se hizo por cuestiones de tiempo.

# Preguntas por resolver en este proyecto.

- ¿Cuál es el objetivo del proyecto?
La base de datos utilizada simula un ambiente transaccional “real” en el cual diferentes individuos por medio de diferentes bancos transfieren dinero entre sí.  La base de datos tiene información de que transferencias han sido catalogadas como lavado de dinero mediante una red neuronal. El objetivo del proyecto es identificar patrones aquellas transacciones marcadas como fraude.
- ¿Qué preguntas quieres hacer?
 Las preguntas por responder en base al objetivo planteado es identificar patrones transaccionales, ¿cuánto suele ser la cantidad de dinero que se transfiere en un fraude? ¿cuánto es la cantidad de veces que se envía? ¿por cuál canal de transferencia se suele lavar más dinero? ¿equivalente en porcentaje del dinero enviado para considerarse como fraude respecto al total?





