DROP TABLE IF EXISTS info_transacciones_persona_fraude;
CREATE TABLE IF NOT exists info_transacciones_persona_fraude
(
WITH t1 as (
SELECT
Month(Time) as mes,
day(Time) as dia,
Account as originario,
Account2 as destinario,
SUM(Amount_Received) as dinero_enviado,
count(*) as cantidad_envios
FROM Dataorigin
WHERE Is_Laundering = 1 
GROUP BY Account, Account2, Month(Time), day(Time)
),
t2 as (
SELECT
Month(Time) as mes,
day(Time) as dia,
Account as originario,
SUM(Amount_Paid) as dinero_enviado_canales,
count(*) as cantidad_envios_totales
FROM Dataorigin
GROUP BY Account, Month(Time), day(Time)
)
SELECT 
	DISTINCT
	year(now()) as anio,
	t1.mes, 
	t1.dia, 
    t1.originario, 
    t1.destinario, 
    t1.dinero_enviado AS dinero_enviado_orig_dest,    
	CASE WHEN t2.dinero_enviado_canales = 0 THEN 1
	ELSE t1.dinero_enviado/t2.dinero_enviado_canales END AS ptge_enviado_orig_dest,
    t1.cantidad_envios as numero_envios_orig_dest,
    CASE WHEN t2.cantidad_envios_totales = 0 THEN 1
    ELSE t1.cantidad_envios/t2.cantidad_envios_totales END AS ptge_envios_orig_dest
FROM t1 
INNER JOIN t2 ON t1.mes = t2.mes
AND t1.dia = t1.dia AND t1.originario = t2.originario
);