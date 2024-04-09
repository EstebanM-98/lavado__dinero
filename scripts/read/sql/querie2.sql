DROP TABLE IF exists info_transacciones_consolid_fraud;
CREATE TABLE IF NOT exists info_transacciones_consolid_fraud
(
WITH t1 as(
select 
anio,
mes,
dia,
originario,
SUM(dinero_enviado_orig_dest) as dinero_total_env,
SUM(numero_envios_orig_dest) as cantidad_total_env
from info_transacciones_persona_fraude
GROUP BY originario, anio, mes, dia
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
    t1.dinero_total_env AS dinero_total_env,
    CASE WHEN t2.dinero_enviado_canales = 0 THEN 1
    ELSE t1.dinero_total_env/t2.dinero_enviado_canales END as ptge_enviado_orig,
    t1.cantidad_total_env as numero_envios_orig_dest,
    CASE WHEN t2.cantidad_envios_totales = 0 THEN 1
    ELSE t1.cantidad_total_env/t2.cantidad_envios_totales END as ptge_envios_orig
FROM t1 
INNER JOIN t2 ON t1.mes = t2.mes
AND t1.dia = t1.dia AND t1.originario = t2.originario
);