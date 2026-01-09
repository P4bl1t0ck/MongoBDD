--Scripts que se usaron para hacer la migracion de los archivos
--de SQL Server a MongoDB atlas se creo y guardo a los archivos en 
--formato .json/
--Parroquia
SELECT
    p.ID_Parroquin AS _id,
    p.Nombre AS nombre,
    p.Vicaria AS nombre_vicaria,
    p.Direccion AS direccion,
    p.Telefono AS telefono,
    200 AS capacidad_catequesis,
    1 AS activo,
    GETDATE() AS fecha_creacion,
    GETDATE() AS fecha_actualizacion
FROM Parroquía p
FOR JSON PATH;
--Catequistas.json
SELECT
    c.ID_Catequista AS _id,
    c.Nombres AS nombre,
    c.Apellidos AS apellido,
    CONCAT(c.Nombres, ' ', c.Apellidos) AS nombre_completo,
    c.Correo AS correo,
    c.Telefono AS telefono,
    c.Parroquía_ID_Parroquin AS parroquia_id,
    c.Rol AS especialidad,
    1 AS activo,
    GETDATE() AS fecha_creacion,
    GETDATE() AS fecha_actualizacion
FROM Catequista c
FOR JSON PATH;
--grupos.json
SELECT 
    g.ID_Grupo,
    g.Ano,
    g.Horario,
    g.ID_Nivel,
    g.ID_Catequista,
    g.Parroquía_ID_Parroquin
FROM GrupoCatequesis g
FOR JSON PATH;
--catequizandos.json
SELECT 
    c.ID_Catequizando,
    c.Nombre,
    c.Apellido,
    c.Cedula,
    c.Fecha_Nacimiento,
    c.Telefono,
    c.Fecha_Registro,
    c.Observaciones,
    c.FeBautismo_ID_Bautismo
FROM Catequizando c
FOR JSON PATH;