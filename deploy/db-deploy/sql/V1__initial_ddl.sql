-- TABLES
CREATE TABLE IF NOT EXISTS aserv.hello_world (
	col1 varchar null,
	col2 int4 null
);

CREATE TABLE IF NOT EXISTS  raw.hello_api_job (
	source_word     text,
	source_time     text,
    sys_source_hash BYTEA NOT NULL CHECK (octet_length(sys_source_hash) = 32),
    sys_job_id      text NOT NULL,
    sys_job_ts      timestamp with time zone NOT NULL DEFAULT (now() at time zone 'utc')
);


CREATE TABLE IF NOT EXISTS  raw.hello_test_controller (
	source_word     text,
	source_time     text,
    sys_source_hash BYTEA NOT NULL CHECK (octet_length(sys_source_hash) = 32),
    sys_job_id      text NOT NULL,
    sys_job_ts      timestamp with time zone NOT NULL DEFAULT (now() at time zone 'utc')
);


CREATE TABLE IF NOT EXISTS  raw.hello_test_api (
	source_word     text,
	source_time     text,
    sys_source_hash BYTEA NOT NULL CHECK (octet_length(sys_source_hash) = 32),
    sys_job_id      text NOT NULL,
    sys_job_ts      timestamp with time zone NOT NULL DEFAULT (now() at time zone 'utc')
);


CREATE TABLE IF NOT EXISTS  raw.hello_test_api_fail (
	source_word     text,
	source_time     text,
    sys_source_hash BYTEA NOT NULL CHECK (octet_length(sys_source_hash) = 32),
    sys_job_id      text NOT NULL,
    sys_job_ts      timestamp with time zone NOT NULL DEFAULT (now() at time zone 'utc')
);

CREATE TABLE IF NOT EXISTS  raw.hello_job (
	source_word     text,
	source_time     text,
    sys_source_hash BYTEA NOT NULL CHECK (octet_length(sys_source_hash) = 32),
    sys_job_id      text NOT NULL,
    sys_job_ts      timestamp with time zone NOT NULL DEFAULT (now() at time zone 'utc')
);

CREATE TABLE IF NOT EXISTS  raw.ops_ledger (
    job_type        text NOT NULL,
    job_id          int NOT NULL,
    job_name        text NOT NULL,
    action_type     text NOT NULL,
    source          text,
    source_type     text,
    job_target      text,
    target_type     text,
    cmd             text,
    startup         bool NOT NULL,
    run_once        bool NOT NULL,
    run_next        text,
    job_try         int NOT NULL,
    run_id          text NOT NULL,
    enqueue_time    timestamptz NOT NULL,
    start_time      timestamptz NOT NULL,
    finish_time     timestamptz NOT NULL,  
    job_status      bool NOT NULL,
    job_message     text NOT NULL,
    CONSTRAINT house_uk1 UNIQUE (run_id)
);

CREATE TABLE IF NOT EXISTS raw.iso_country (
    code            TEXT,
    name            TEXT,
    sys_source_hash BYTEA NOT NULL CHECK (octet_length(sys_source_hash) = 32),
    sys_job_id      text NOT NULL,
    sys_job_ts      timestamp with time zone NOT NULL DEFAULT (now() at time zone 'utc')
);

create table raw.admin1 (
    code                text not null,
    name                text not null,
    asciiname           text not null,
    geonameid           text not null,
    sys_source_hash     BYTEA NOT NULL CHECK (octet_length(sys_source_hash) = 32),
    sys_job_id          text NOT NULL,
    sys_job_ts          timestamp with time zone NOT NULL DEFAULT (now() at time zone 'utc')
);

create table raw.admin2 (
    code                text not null,
    name                text not null,
    asciiname           text not null,
    geonameid           text not null,
    sys_source_hash     BYTEA NOT NULL CHECK (octet_length(sys_source_hash) = 32),
    sys_job_id          text NOT NULL,
    sys_job_ts          timestamp with time zone NOT NULL DEFAULT (now() at time zone 'utc')
);

CREATE TABLE IF NOT EXISTS raw.iso_subdivision (
    country_code    TEXT,
    code            TEXT,
    name            TEXT,
    sys_source_hash BYTEA NOT NULL CHECK (octet_length(sys_source_hash) = 32),
    sys_job_id      text NOT NULL,
    sys_job_ts      timestamp with time zone NOT NULL DEFAULT (now() at time zone 'utc')
);

CREATE TABLE IF NOT EXISTS raw.cities (
    geonameid           TEXT,
    asciiname           TEXT,
    country_code        TEXT,
    admin1_code         TEXT,
    admin2_code         TEXT,    
    timezone            TEXT,
    latitude            TEXT,
    longitude           TEXT,
    modification_date   TEXT,
    sys_source_hash     BYTEA NOT NULL CHECK (octet_length(sys_source_hash) = 32),
    sys_job_id          text NOT NULL,
    sys_job_ts          timestamp with time zone NOT NULL DEFAULT (now() at time zone 'utc')  
);

CREATE TABLE IF NOT EXISTS aserv.location
(
    location_pk uuid NOT NULL DEFAULT gen_random_uuid(),
    source_id bigint NOT NULL,
    country text NOT NULL,
    state text not null,
    county text not null,
    city text NOT NULL,
    timezone text NOT NULL,
    latitude double precision NOT NULL CHECK (latitude BETWEEN -90 AND 90),
    longitude double precision NOT NULL CHECK (longitude BETWEEN -180 AND 180),
    sys_crt timestamp with time zone NOT NULL DEFAULT (now() at time zone 'utc'),
    sys_updt timestamp with time zone,
    CONSTRAINT location_pk1 PRIMARY KEY (location_pk),
    CONSTRAINT location_uk1 UNIQUE (source_id),
    CONSTRAINT location_uk2 UNIQUE (country, state, county, city)
);

CREATE TABLE IF NOT EXISTS aserv.profile
(
    profile_pk uuid NOT NULL DEFAULT gen_random_uuid(),
    name text NOT NULL,
    location_fk uuid NOT NULL,
    display text NOT NULL,
    birth_ts timestamp with time zone NOT NULL,
    sys_crt timestamp with time zone NOT NULL DEFAULT (now() at time zone 'utc'),
    sys_updt timestamp with time zone,
    CONSTRAINT profile_pk1 PRIMARY KEY (profile_pk),
    CONSTRAINT profile_uk1 UNIQUE (name)
);

CREATE TABLE IF NOT EXISTS aserv.body
(
    body_pk uuid NOT NULL DEFAULT gen_random_uuid(),
    name text NOT NULL,
    body_type_fk uuid,
    display text NOT NULL,
    sys_crt timestamp with time zone NOT NULL DEFAULT (now() at time zone 'utc'),
    sys_updt timestamp with time zone,
    CONSTRAINT body_pk1 PRIMARY KEY (body_pk),
    CONSTRAINT body_uk1 UNIQUE (name)
);

CREATE TABLE IF NOT EXISTS aserv.house
(
    house_pk uuid NOT NULL DEFAULT gen_random_uuid(),
    name text NOT NULL,
    display text NOT NULL,
    sys_crt timestamp with time zone NOT NULL DEFAULT (now() at time zone 'utc'),
    sys_updt timestamp with time zone,
    CONSTRAINT house_pk1 PRIMARY KEY (house_pk),
    CONSTRAINT house_uk1 UNIQUE (name)
);

CREATE TABLE IF NOT EXISTS aserv.natal
(
    natal_pk uuid NOT NULL DEFAULT gen_random_uuid(),
    profile_fk uuid NOT NULL,
    body_fk uuid NOT NULL,
    house_fk uuid NOT NULL,
    sign_fk uuid NOT NULL,
    longitude double precision NOT NULL CHECK (longitude >= 0 AND longitude < 360),
    degree smallint NOT NULL CHECK (degree BETWEEN 0 AND 29),
    minute smallint NOT NULL CHECK (minute BETWEEN 0 AND 59),
    second smallint NOT NULL CHECK (second BETWEEN 0 AND 59),
    retrograde boolean NOT NULL,
    speed double precision NOT NULL,
    sys_crt timestamp with time zone NOT NULL DEFAULT (now() at time zone 'utc'),
    sys_updt timestamp with time zone,
    CONSTRAINT natal_pk1 PRIMARY KEY (natal_pk),
    CONSTRAINT natal_uk1 UNIQUE (profile_fk, body_fk)
);

CREATE TABLE IF NOT EXISTS aserv.sign
(
    sign_pk uuid NOT NULL DEFAULT gen_random_uuid(),
    name text NOT NULL,
    display text NOT NULL,
    sys_crt timestamp with time zone NOT NULL DEFAULT (now() at time zone 'utc'),
    sys_updt timestamp with time zone,
    CONSTRAINT sign_pk1 PRIMARY KEY (sign_pk),
    CONSTRAINT sign_uk1 UNIQUE (name)
);

CREATE TABLE IF NOT EXISTS aserv.body_type
(
    body_type_pk uuid NOT NULL DEFAULT gen_random_uuid(),
    name text NOT NULL,
    display text NOT NULL,
    sys_crt timestamp with time zone NOT NULL DEFAULT (now() at time zone 'utc'),
    sys_updt timestamp with time zone,
    CONSTRAINT body_type_pk PRIMARY KEY (body_type_pk),
    CONSTRAINT body_type_uk1 UNIQUE (name)
);

CREATE TABLE IF NOT EXISTS aserv.house_angle
(
    house_angle_pk uuid NOT NULL DEFAULT gen_random_uuid(),
    house_fk uuid NOT NULL,
    profile_fk uuid NOT NULL,
    display text NOT NULL CHECK (display IN ('ascendant', 'descendant', 'midheaven', 'imum coeli')),
    longitude double precision NOT NULL CHECK (longitude >= 0 AND longitude < 360),
    degree smallint NOT NULL CHECK (degree BETWEEN 0 AND 29),
    minute smallint NOT NULL CHECK (minute BETWEEN 0 AND 59),
    second smallint NOT NULL CHECK (second BETWEEN 0 AND 59),
    sys_crt timestamp with time zone NOT NULL DEFAULT (now() at time zone 'utc'),
    sys_updt timestamp with time zone,
    CONSTRAINT house_angle_pk1 PRIMARY KEY (house_angle_pk),
    CONSTRAINT house_angle_uk1 UNIQUE (house_fk, profile_fk)
);

CREATE TABLE IF NOT EXISTS aserv.point
(
    point_pk uuid NOT NULL DEFAULT gen_random_uuid(),
    point_type_fk uuid NOT NULL,
    body_fk uuid,
    house_angle_fk uuid,
    sys_crt timestamp with time zone NOT NULL DEFAULT (now() at time zone 'utc'),
    sys_updt timestamp with time zone,
    CONSTRAINT point_pk1 PRIMARY KEY (point_pk),
    -- uk not managed by erd see indexes below 
    -- table check constraints not managed by erd
    CONSTRAINT point_body_xor_angle_chk CHECK (
        (body_fk IS NOT NULL AND house_angle_fk IS NULL) OR
        (body_fk IS NULL AND house_angle_fk IS NOT NULL)
    )
);
-- not manged by erd
CREATE UNIQUE INDEX IF NOT EXISTS point_uk1 ON aserv.point (point_type_fk, body_fk) WHERE body_fk IS NOT NULL;
CREATE UNIQUE INDEX IF NOT EXISTS point_uk2 ON aserv.point (point_type_fk, house_angle_fk) WHERE house_angle_fk IS NOT NULL;

CREATE TABLE IF NOT EXISTS aserv.point_type
(
    point_type_pk uuid NOT NULL DEFAULT gen_random_uuid(),
    name text NOT NULL,
    display text NOT NULL,
    sys_crt timestamp with time zone NOT NULL DEFAULT (now() at time zone 'utc'),
    sys_updt timestamp with time zone,
    CONSTRAINT point_type_pk1 PRIMARY KEY (point_type_pk),
    CONSTRAINT point_type_uk1 UNIQUE (name)
);

CREATE TABLE IF NOT EXISTS aserv.midpoint
(
    midpoint_pk uuid NOT NULL DEFAULT gen_random_uuid(),
    profile_fk uuid NOT NULL,
    lo_point_fk uuid NOT NULL,
    hi_point_fk uuid NOT NULL,
    degree_0_to_180 double precision NOT NULL CHECK (degree_0_to_180 >= 0 AND degree_0_to_180 < 180),
    degree_0_to_360 double precision NOT NULL CHECK (degree_0_to_360 >= 0 AND degree_0_to_360 < 360),
    sys_crt timestamp with time zone NOT NULL DEFAULT (now() at time zone 'utc'),
    sys_updt timestamp with time zone,
    CONSTRAINT midpoint_pk1 PRIMARY KEY (midpoint_pk),
    CONSTRAINT midpoint_uk1 UNIQUE (profile_fk, lo_point_fk, hi_point_fk),
    -- table check constraints not managed by erd
    CONSTRAINT midpoint_lo_ne_hi CHECK (lo_point_fk <> hi_point_fk),
    CONSTRAINT midpoint_lo_lt_hi CHECK (lo_point_fk < hi_point_fk)
);

-- alter

ALTER TABLE IF EXISTS aserv.profile
    ADD CONSTRAINT location_fk1 FOREIGN KEY (location_fk)
    REFERENCES aserv.location (location_pk) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;
CREATE INDEX IF NOT EXISTS fki_location_fk1
    ON aserv.profile(location_fk);


ALTER TABLE IF EXISTS aserv.body
    ADD CONSTRAINT body_type_fk1 FOREIGN KEY (body_type_fk)
    REFERENCES aserv.body_type (body_type_pk) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;
CREATE INDEX IF NOT EXISTS fki_body_type_fk1
    ON aserv.body(body_type_fk);


ALTER TABLE IF EXISTS aserv.natal
    ADD CONSTRAINT profile_fk1 FOREIGN KEY (profile_fk)
    REFERENCES aserv.profile (profile_pk) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;
CREATE INDEX IF NOT EXISTS fki_profile_fk1
    ON aserv.natal(profile_fk);


ALTER TABLE IF EXISTS aserv.natal
    ADD CONSTRAINT house_fk1 FOREIGN KEY (house_fk)
    REFERENCES aserv.house (house_pk) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;
CREATE INDEX IF NOT EXISTS fki_house_fk1
    ON aserv.natal(house_fk);


ALTER TABLE IF EXISTS aserv.natal
    ADD CONSTRAINT sign_fk1 FOREIGN KEY (sign_fk)
    REFERENCES aserv.sign (sign_pk) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;
CREATE INDEX IF NOT EXISTS fki_sign_fk1
    ON aserv.natal(sign_fk);


ALTER TABLE IF EXISTS aserv.natal
    ADD CONSTRAINT body_fk1 FOREIGN KEY (body_fk)
    REFERENCES aserv.body (body_pk) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;
CREATE INDEX IF NOT EXISTS fki_body_fk1
    ON aserv.natal(body_fk);


ALTER TABLE IF EXISTS aserv.house_angle
    ADD CONSTRAINT house_fk2 FOREIGN KEY (house_fk)
    REFERENCES aserv.house (house_pk) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;
CREATE INDEX IF NOT EXISTS fki_house_fk2
    ON aserv.house_angle(house_fk);


ALTER TABLE IF EXISTS aserv.house_angle
    ADD CONSTRAINT profile_fk2 FOREIGN KEY (profile_fk)
    REFERENCES aserv.profile (profile_pk) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;
CREATE INDEX IF NOT EXISTS fki_profile_fk2
    ON aserv.house_angle(profile_fk);

ALTER TABLE IF EXISTS aserv.point
    ADD CONSTRAINT body_fk2 FOREIGN KEY (body_fk)
    REFERENCES aserv.body (body_pk) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;
CREATE INDEX IF NOT EXISTS fki_body_fk2
    ON aserv.point(body_fk);


ALTER TABLE IF EXISTS aserv.point
    ADD CONSTRAINT house_angle_fk1 FOREIGN KEY (house_angle_fk)
    REFERENCES aserv.house_angle (house_angle_pk) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;
CREATE INDEX IF NOT EXISTS fki_house_angle_fk1
    ON aserv.point(house_angle_fk);


ALTER TABLE IF EXISTS aserv.point
    ADD CONSTRAINT point_type_fk1 FOREIGN KEY (point_type_fk)
    REFERENCES aserv.point_type (point_type_pk) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;
CREATE INDEX IF NOT EXISTS fki_point_type_fk1
    ON aserv.point(point_type_fk);


ALTER TABLE IF EXISTS aserv.midpoint
    ADD CONSTRAINT lo_point_fk1 FOREIGN KEY (lo_point_fk)
    REFERENCES aserv.point (point_pk) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;
CREATE INDEX IF NOT EXISTS fki_lo_point_fk1
    ON aserv.midpoint(lo_point_fk);


ALTER TABLE IF EXISTS aserv.midpoint
    ADD CONSTRAINT hi_point_fk1 FOREIGN KEY (hi_point_fk)
    REFERENCES aserv.point (point_pk) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;
CREATE INDEX IF NOT EXISTS fki_hi_point_fk1
    ON aserv.midpoint(hi_point_fk);


ALTER TABLE IF EXISTS aserv.midpoint
    ADD CONSTRAINT profile_fk3 FOREIGN KEY (profile_fk)
    REFERENCES aserv.profile (profile_pk) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;
CREATE INDEX IF NOT EXISTS fki_profile_fk3
    ON aserv.midpoint(profile_fk);

GRANT INSERT, update ON aserv.profile TO aserv_app;
