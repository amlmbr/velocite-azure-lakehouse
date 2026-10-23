-- Requêtes SELECT statiques extraites des activités Lookup ADF.
-- Lecture seule ; nécessite les objets SQL préexistants.

SELECT MAX(CASE WHEN source_table='locations' THEN CONVERT(varchar(33),last_watermark,126) END) AS locations, MAX(CASE WHEN source_table='abonnes' THEN CONVERT(varchar(33),last_watermark,126) END) AS abonnes FROM dbo.pipeline_state;

SELECT (SELECT COUNT_BIG(*) FROM dbo.abonnes) AS abonnes,(SELECT COUNT_BIG(*) FROM dbo.stations) AS stations,(SELECT COUNT_BIG(*) FROM dbo.locations) AS locations,HAS_PERMS_BY_NAME('dbo.locations','OBJECT','UPDATE') AS can_update_locations,HAS_PERMS_BY_NAME('dbo.sp_commit_watermark','OBJECT','EXECUTE') AS can_commit,IS_MEMBER('db_owner') AS is_db_owner,(SELECT TYPE_NAME(user_type_id) FROM sys.parameters WHERE object_id=OBJECT_ID('dbo.sp_commit_watermark') AND name='@new_watermark') AS watermark_parameter_type,(SELECT scale FROM sys.parameters WHERE object_id=OBJECT_ID('dbo.sp_commit_watermark') AND name='@new_watermark') AS watermark_parameter_scale;

SELECT CONVERT(varchar(33),COALESCE(MAX(modifie_le),CONVERT(datetime2,'19000101')),126) AS wm FROM dbo.locations;

SELECT CONVERT(varchar(33),COALESCE(MAX(modifie_le),CONVERT(datetime2,'19000101')),126) AS wm FROM dbo.abonnes;

SELECT CONVERT(varchar(33),MAX(modifie_le),126) AS upper_locations, (SELECT CONVERT(varchar(33),MAX(modifie_le),126) FROM dbo.abonnes) AS upper_abonnes FROM dbo.locations;

SELECT CONVERT(varchar(33),last_watermark,126) AS wm FROM dbo.pipeline_state WHERE source_table='locations';

SELECT CONVERT(varchar(33),last_watermark,126) AS wm FROM dbo.pipeline_state WHERE source_table='abonnes';

