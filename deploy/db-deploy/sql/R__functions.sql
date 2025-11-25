CREATE OR REPLACE FUNCTION raw.audit_dtl(p_target text)
RETURNS TABLE (sys_source_hash BYTEA, sys_job_id text)
LANGUAGE plpgsql
AS $$
DECLARE
	v_schema    text;
	v_table     text;
	v_reg_class regclass;
BEGIN
	IF position('.' IN p_target) = 0
 	then RAISE EXCEPTION 'input parameter must use {schema}.{table} format: %', p_target USING ERRCODE = '22023';
	END IF;
	v_schema := split_part(p_target, '.', 1);
	v_table  := split_part(p_target, '.', 2);
 	IF v_schema <> 'raw'
	THEN RAISE EXCEPTION 'only schema "raw" is allowed: %', p_target USING ERRCODE = '22023';
	END IF;
  	v_reg_class := to_regclass(format('%I.%I', v_schema, v_table));
  	IF v_reg_class IS NULL
  	then RAISE EXCEPTION 'table % does not exist', p_target USING ERRCODE = '42P01';
	END IF;
 	RETURN QUERY EXECUTE format(
		'SELECT sys_source_hash, sys_job_id FROM %s ORDER BY sys_job_ts DESC LIMIT 1', 
		v_reg_class::text
	);
END;
$$;

CREATE OR REPLACE FUNCTION aserv.merge_profile(
	p_location_pk	aserv.location.location_pk%type,
	p_display     	aserv.profile.display%type,
	p_birth_ts		timestamp
)
RETURNS TABLE (profile_pk aserv.profile.profile_pk%type, action text) 
LANGUAGE plpgsql
AS $$
DECLARE
	v_timezone		aserv.location.timezone%type;
	v_birth_ts		aserv.profile.birth_ts%type;
	v_name			aserv.profile.name%type;
BEGIN
	select a.timezone into v_timezone from aserv.location a where a.location_pk = p_location_pk;
	v_birth_ts 		:= p_birth_ts AT TIME ZONE v_timezone;
	v_name 			:= replace(lower(p_display), ' ', '_');
    RETURN QUERY
	with cte as (
		select v_name as name, p_location_pk as location_fk, p_display as display, v_birth_ts as birth_ts	
	)
	MERGE INTO aserv.profile a
	USING cte b ON a.name = b.name
	WHEN MATCHED then UPDATE set
		location_fk = b.location_fk,
	    display     = b.display,
	    birth_ts    = b.birth_ts,
		sys_updt    = (now() AT TIME ZONE 'utc')
	WHEN NOT MATCHED THEN
	    INSERT (name, location_fk, display, birth_ts)
	 	VALUES (b.name, b.location_fk, b.display, b.birth_ts)
    RETURNING a.profile_pk profile_pk, merge_action() AS action;
END;
$$;
