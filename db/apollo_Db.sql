--
-- PostgreSQL database dump
--

-- Dumped from database version 12.4 (Debian 12.4-1.pgdg100+1)
-- Dumped by pg_dump version 12.4

-- Started on 2020-10-07 12:04:18 UTC

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 12 (class 2615 OID 19129)
-- Name: tiger; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA IF NOT EXISTS tiger;


ALTER SCHEMA tiger OWNER TO postgres;

--
-- TOC entry 10 (class 2615 OID 19399)
-- Name: tiger_data; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA IF NOT EXISTS tiger_data;


ALTER SCHEMA tiger_data OWNER TO postgres;

--
-- TOC entry 11 (class 2615 OID 18974)
-- Name: topology; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA IF NOT EXISTS topology;


ALTER SCHEMA topology OWNER TO postgres;

--
-- TOC entry 4809 (class 0 OID 0)
-- Dependencies: 11
-- Name: SCHEMA topology; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON SCHEMA topology IS 'PostGIS Topology schema';


--
-- TOC entry 2 (class 3079 OID 19118)
-- Name: fuzzystrmatch; Type: EXTENSION; Schema: -; Owner: -
--

-- CREATE EXTENSION IF NOT EXISTS fuzzystrmatch WITH SCHEMA public;


--
-- TOC entry 4810 (class 0 OID 0)
-- Dependencies: 2
-- Name: EXTENSION fuzzystrmatch; Type: COMMENT; Schema: -; Owner: 
--

-- COMMENT ON EXTENSION fuzzystrmatch IS 'determine similarities and distance between strings';


--
-- TOC entry 3 (class 3079 OID 17972)
-- Name: postgis; Type: EXTENSION; Schema: -; Owner: -
--

-- CREATE EXTENSION IF NOT EXISTS postgis WITH SCHEMA public;


--
-- TOC entry 4811 (class 0 OID 0)
-- Dependencies: 3
-- Name: EXTENSION postgis; Type: COMMENT; Schema: -; Owner: 
--

-- COMMENT ON EXTENSION postgis IS 'PostGIS geometry, geography, and raster spatial types and functions';


--
-- TOC entry 5 (class 3079 OID 19130)
-- Name: postgis_tiger_geocoder; Type: EXTENSION; Schema: -; Owner: -
--

-- CREATE EXTENSION IF NOT EXISTS postgis_tiger_geocoder WITH SCHEMA tiger;


--
-- TOC entry 4812 (class 0 OID 0)
-- Dependencies: 5
-- Name: EXTENSION postgis_tiger_geocoder; Type: COMMENT; Schema: -; Owner: 
--

-- COMMENT ON EXTENSION postgis_tiger_geocoder IS 'PostGIS tiger geocoder and reverse geocoder';


--
-- TOC entry 4 (class 3079 OID 18975)
-- Name: postgis_topology; Type: EXTENSION; Schema: -; Owner: -
--

-- CREATE EXTENSION IF NOT EXISTS postgis_topology WITH SCHEMA topology;


--
-- TOC entry 4813 (class 0 OID 0)
-- Dependencies: 4
-- Name: EXTENSION postgis_topology; Type: COMMENT; Schema: -; Owner: 
--

-- COMMENT ON EXTENSION postgis_topology IS 'PostGIS topology spatial types and functions';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 270 (class 1259 OID 19558)
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO postgres;

--
-- TOC entry 329 (class 1259 OID 20339)
-- Name: contact_history; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.contact_history (
    id integer NOT NULL,
    participant_id integer NOT NULL,
    user_id integer NOT NULL,
    description character varying,
    created timestamp without time zone NOT NULL,
    uuid uuid NOT NULL
);


ALTER TABLE public.contact_history OWNER TO postgres;

--
-- TOC entry 328 (class 1259 OID 20337)
-- Name: contact_history_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.contact_history_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.contact_history_id_seq OWNER TO postgres;

--
-- TOC entry 4814 (class 0 OID 0)
-- Dependencies: 328
-- Name: contact_history_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.contact_history_id_seq OWNED BY public.contact_history.id;


--
-- TOC entry 272 (class 1259 OID 19565)
-- Name: deployment; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.deployment (
    id integer NOT NULL,
    name character varying NOT NULL,
    hostnames character varying[] NOT NULL,
    allow_observer_submission_edit boolean,
    logo character varying,
    include_rejected_in_votes boolean,
    is_initialized boolean,
    dashboard_full_locations boolean,
    uuid uuid NOT NULL,
    primary_locale character varying,
    other_locales character varying[],
    enable_partial_response_for_messages boolean
);


ALTER TABLE public.deployment OWNER TO postgres;

--
-- TOC entry 271 (class 1259 OID 19563)
-- Name: deployment_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.deployment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.deployment_id_seq OWNER TO postgres;

--
-- TOC entry 4815 (class 0 OID 0)
-- Dependencies: 271
-- Name: deployment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.deployment_id_seq OWNED BY public.deployment.id;


--
-- TOC entry 299 (class 1259 OID 19878)
-- Name: event; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.event (
    id integer NOT NULL,
    name character varying NOT NULL,
    start timestamp with time zone NOT NULL,
    "end" timestamp with time zone NOT NULL,
    resource_id integer,
    location_set_id integer,
    participant_set_id integer
);


ALTER TABLE public.event OWNER TO postgres;

--
-- TOC entry 298 (class 1259 OID 19876)
-- Name: event_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.event_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.event_id_seq OWNER TO postgres;

--
-- TOC entry 4816 (class 0 OID 0)
-- Dependencies: 298
-- Name: event_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.event_id_seq OWNED BY public.event.id;


--
-- TOC entry 325 (class 1259 OID 20305)
-- Name: events_forms; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.events_forms (
    event_id integer NOT NULL,
    form_id integer NOT NULL
);


ALTER TABLE public.events_forms OWNER TO postgres;

--
-- TOC entry 284 (class 1259 OID 19687)
-- Name: form; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.form (
    id integer NOT NULL,
    name character varying NOT NULL,
    prefix character varying NOT NULL,
    form_type character varying(255) NOT NULL,
    require_exclamation boolean,
    data jsonb,
    version_identifier character varying,
    resource_id integer,
    quality_checks jsonb,
    party_mappings jsonb,
    calculate_moe boolean,
    accredited_voters_tag character varying,
    quality_checks_enabled boolean,
    invalid_votes_tag character varying,
    registered_voters_tag character varying,
    blank_votes_tag character varying,
    vote_shares jsonb,
    untrack_data_conflicts boolean DEFAULT false NOT NULL,
    show_map boolean,
    show_moment boolean,
    show_progress boolean
);


ALTER TABLE public.form OWNER TO postgres;

--
-- TOC entry 283 (class 1259 OID 19685)
-- Name: form_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.form_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.form_id_seq OWNER TO postgres;

--
-- TOC entry 4817 (class 0 OID 0)
-- Dependencies: 283
-- Name: form_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.form_id_seq OWNED BY public.form.id;


--
-- TOC entry 301 (class 1259 OID 19909)
-- Name: location; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.location (
    id integer NOT NULL,
    code character varying NOT NULL,
    registered_voters integer,
    location_set_id integer NOT NULL,
    location_type_id integer NOT NULL,
    extra_data jsonb,
    uuid uuid NOT NULL,
    name_translations jsonb,
    geom public.geometry(Point,4326)
);


ALTER TABLE public.location OWNER TO postgres;

--
-- TOC entry 286 (class 1259 OID 19708)
-- Name: location_data_field; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.location_data_field (
    id integer NOT NULL,
    location_set_id integer NOT NULL,
    name character varying NOT NULL,
    label character varying NOT NULL,
    visible_in_lists boolean,
    resource_id integer
);


ALTER TABLE public.location_data_field OWNER TO postgres;

--
-- TOC entry 285 (class 1259 OID 19706)
-- Name: location_data_field_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.location_data_field_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.location_data_field_id_seq OWNER TO postgres;

--
-- TOC entry 4818 (class 0 OID 0)
-- Dependencies: 285
-- Name: location_data_field_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.location_data_field_id_seq OWNED BY public.location_data_field.id;


--
-- TOC entry 300 (class 1259 OID 19907)
-- Name: location_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.location_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.location_id_seq OWNER TO postgres;

--
-- TOC entry 4819 (class 0 OID 0)
-- Dependencies: 300
-- Name: location_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.location_id_seq OWNED BY public.location.id;


--
-- TOC entry 311 (class 1259 OID 20022)
-- Name: location_path; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.location_path (
    location_set_id integer NOT NULL,
    ancestor_id integer NOT NULL,
    descendant_id integer NOT NULL,
    depth integer
);


ALTER TABLE public.location_path OWNER TO postgres;

--
-- TOC entry 274 (class 1259 OID 19605)
-- Name: location_set; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.location_set (
    id integer NOT NULL,
    name character varying NOT NULL,
    slug character varying,
    deployment_id integer NOT NULL,
    uuid uuid NOT NULL,
    is_finalized boolean
);


ALTER TABLE public.location_set OWNER TO postgres;

--
-- TOC entry 273 (class 1259 OID 19603)
-- Name: location_set_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.location_set_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.location_set_id_seq OWNER TO postgres;

--
-- TOC entry 4820 (class 0 OID 0)
-- Dependencies: 273
-- Name: location_set_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.location_set_id_seq OWNED BY public.location_set.id;


--
-- TOC entry 288 (class 1259 OID 19729)
-- Name: location_type; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.location_type (
    id integer NOT NULL,
    is_administrative boolean,
    is_political boolean,
    has_registered_voters boolean,
    slug character varying,
    location_set_id integer NOT NULL,
    uuid uuid NOT NULL,
    name_translations jsonb,
    has_coordinates boolean DEFAULT false
);


ALTER TABLE public.location_type OWNER TO postgres;

--
-- TOC entry 287 (class 1259 OID 19727)
-- Name: location_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.location_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.location_type_id_seq OWNER TO postgres;

--
-- TOC entry 4821 (class 0 OID 0)
-- Dependencies: 287
-- Name: location_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.location_type_id_seq OWNED BY public.location_type.id;


--
-- TOC entry 302 (class 1259 OID 19931)
-- Name: location_type_path; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.location_type_path (
    location_set_id integer NOT NULL,
    ancestor_id integer NOT NULL,
    descendant_id integer NOT NULL,
    depth integer
);


ALTER TABLE public.location_type_path OWNER TO postgres;

--
-- TOC entry 320 (class 1259 OID 20183)
-- Name: message; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.message (
    id integer NOT NULL,
    direction character varying(255) NOT NULL,
    recipient character varying,
    sender character varying,
    text character varying,
    received timestamp without time zone,
    delivered timestamp without time zone,
    deployment_id integer NOT NULL,
    event_id integer NOT NULL,
    submission_id integer,
    participant_id integer,
    uuid uuid NOT NULL,
    message_type character varying(255),
    originating_message_id integer
);


ALTER TABLE public.message OWNER TO postgres;

--
-- TOC entry 319 (class 1259 OID 20181)
-- Name: message_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.message_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.message_id_seq OWNER TO postgres;

--
-- TOC entry 4822 (class 0 OID 0)
-- Dependencies: 319
-- Name: message_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.message_id_seq OWNED BY public.message.id;


--
-- TOC entry 313 (class 1259 OID 20046)
-- Name: participant; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.participant (
    id integer NOT NULL,
    participant_id character varying,
    role_id integer,
    partner_id integer,
    supervisor_id integer,
    gender character varying(255),
    email character varying,
    location_id integer,
    participant_set_id integer NOT NULL,
    message_count integer,
    accurate_message_count integer,
    completion_rating double precision,
    device_id character varying,
    password character varying,
    extra_data jsonb,
    uuid uuid NOT NULL,
    full_name_translations jsonb,
    first_name_translations jsonb,
    last_name_translations jsonb,
    other_names_translations jsonb
);


ALTER TABLE public.participant OWNER TO postgres;

--
-- TOC entry 304 (class 1259 OID 19955)
-- Name: participant_data_field; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.participant_data_field (
    id integer NOT NULL,
    participant_set_id integer NOT NULL,
    name character varying NOT NULL,
    label character varying NOT NULL,
    visible_in_lists boolean,
    resource_id integer
);


ALTER TABLE public.participant_data_field OWNER TO postgres;

--
-- TOC entry 303 (class 1259 OID 19953)
-- Name: participant_data_field_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.participant_data_field_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.participant_data_field_id_seq OWNER TO postgres;

--
-- TOC entry 4823 (class 0 OID 0)
-- Dependencies: 303
-- Name: participant_data_field_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.participant_data_field_id_seq OWNED BY public.participant_data_field.id;


--
-- TOC entry 315 (class 1259 OID 20082)
-- Name: participant_group; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.participant_group (
    id integer NOT NULL,
    name character varying NOT NULL,
    group_type_id integer NOT NULL,
    participant_set_id integer NOT NULL,
    uuid uuid NOT NULL
);


ALTER TABLE public.participant_group OWNER TO postgres;

--
-- TOC entry 314 (class 1259 OID 20080)
-- Name: participant_group_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.participant_group_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.participant_group_id_seq OWNER TO postgres;

--
-- TOC entry 4824 (class 0 OID 0)
-- Dependencies: 314
-- Name: participant_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.participant_group_id_seq OWNED BY public.participant_group.id;


--
-- TOC entry 306 (class 1259 OID 19976)
-- Name: participant_group_type; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.participant_group_type (
    id integer NOT NULL,
    name character varying,
    participant_set_id integer NOT NULL,
    uuid uuid NOT NULL
);


ALTER TABLE public.participant_group_type OWNER TO postgres;

--
-- TOC entry 305 (class 1259 OID 19974)
-- Name: participant_group_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.participant_group_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.participant_group_type_id_seq OWNER TO postgres;

--
-- TOC entry 4825 (class 0 OID 0)
-- Dependencies: 305
-- Name: participant_group_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.participant_group_type_id_seq OWNED BY public.participant_group_type.id;


--
-- TOC entry 316 (class 1259 OID 20116)
-- Name: participant_groups_participants; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.participant_groups_participants (
    group_id integer NOT NULL,
    participant_id integer NOT NULL
);


ALTER TABLE public.participant_groups_participants OWNER TO postgres;

--
-- TOC entry 312 (class 1259 OID 20044)
-- Name: participant_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.participant_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.participant_id_seq OWNER TO postgres;

--
-- TOC entry 4826 (class 0 OID 0)
-- Dependencies: 312
-- Name: participant_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.participant_id_seq OWNED BY public.participant.id;


--
-- TOC entry 333 (class 1259 OID 20431)
-- Name: participant_other_locations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.participant_other_locations (
    id integer NOT NULL,
    participant_id integer NOT NULL,
    location_id integer NOT NULL,
    description character varying,
    created timestamp without time zone
);


ALTER TABLE public.participant_other_locations OWNER TO postgres;

--
-- TOC entry 308 (class 1259 OID 19992)
-- Name: participant_partner; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.participant_partner (
    id integer NOT NULL,
    name character varying NOT NULL,
    participant_set_id integer NOT NULL,
    uuid uuid NOT NULL
);


ALTER TABLE public.participant_partner OWNER TO postgres;

--
-- TOC entry 307 (class 1259 OID 19990)
-- Name: participant_partner_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.participant_partner_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.participant_partner_id_seq OWNER TO postgres;

--
-- TOC entry 4827 (class 0 OID 0)
-- Dependencies: 307
-- Name: participant_partner_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.participant_partner_id_seq OWNED BY public.participant_partner.id;


--
-- TOC entry 310 (class 1259 OID 20008)
-- Name: participant_role; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.participant_role (
    id integer NOT NULL,
    name character varying NOT NULL,
    participant_set_id integer NOT NULL,
    uuid uuid NOT NULL
);


ALTER TABLE public.participant_role OWNER TO postgres;

--
-- TOC entry 309 (class 1259 OID 20006)
-- Name: participant_role_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.participant_role_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.participant_role_id_seq OWNER TO postgres;

--
-- TOC entry 4828 (class 0 OID 0)
-- Dependencies: 309
-- Name: participant_role_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.participant_role_id_seq OWNED BY public.participant_role.id;


--
-- TOC entry 290 (class 1259 OID 19745)
-- Name: participant_set; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.participant_set (
    id integer NOT NULL,
    name character varying NOT NULL,
    slug character varying,
    location_set_id integer NOT NULL,
    deployment_id integer NOT NULL,
    uuid uuid NOT NULL,
    gender_hidden boolean,
    partner_hidden boolean,
    role_hidden boolean
);


ALTER TABLE public.participant_set OWNER TO postgres;

--
-- TOC entry 289 (class 1259 OID 19743)
-- Name: participant_set_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.participant_set_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.participant_set_id_seq OWNER TO postgres;

--
-- TOC entry 4829 (class 0 OID 0)
-- Dependencies: 289
-- Name: participant_set_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.participant_set_id_seq OWNED BY public.participant_set.id;


--
-- TOC entry 276 (class 1259 OID 19621)
-- Name: permission; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.permission (
    id integer NOT NULL,
    name character varying NOT NULL,
    description character varying,
    deployment_id integer NOT NULL,
    uuid uuid NOT NULL
);


ALTER TABLE public.permission OWNER TO postgres;

--
-- TOC entry 275 (class 1259 OID 19619)
-- Name: permission_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.permission_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.permission_id_seq OWNER TO postgres;

--
-- TOC entry 4830 (class 0 OID 0)
-- Dependencies: 275
-- Name: permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.permission_id_seq OWNED BY public.permission.id;


--
-- TOC entry 327 (class 1259 OID 20323)
-- Name: phone_contact; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.phone_contact (
    id integer NOT NULL,
    participant_id integer NOT NULL,
    number character varying NOT NULL,
    created timestamp without time zone NOT NULL,
    updated timestamp without time zone NOT NULL,
    verified boolean,
    uuid uuid NOT NULL
);


ALTER TABLE public.phone_contact OWNER TO postgres;

--
-- TOC entry 326 (class 1259 OID 20321)
-- Name: phone_contact_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.phone_contact_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.phone_contact_id_seq OWNER TO postgres;

--
-- TOC entry 4831 (class 0 OID 0)
-- Dependencies: 326
-- Name: phone_contact_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.phone_contact_id_seq OWNED BY public.phone_contact.id;


--
-- TOC entry 278 (class 1259 OID 19637)
-- Name: resource; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.resource (
    resource_id integer NOT NULL,
    resource_type character varying NOT NULL,
    deployment_id integer NOT NULL,
    uuid uuid NOT NULL
);


ALTER TABLE public.resource OWNER TO postgres;

--
-- TOC entry 277 (class 1259 OID 19635)
-- Name: resource_resource_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.resource_resource_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.resource_resource_id_seq OWNER TO postgres;

--
-- TOC entry 4832 (class 0 OID 0)
-- Dependencies: 277
-- Name: resource_resource_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.resource_resource_id_seq OWNED BY public.resource.resource_id;


--
-- TOC entry 280 (class 1259 OID 19653)
-- Name: role; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.role (
    id integer NOT NULL,
    deployment_id integer NOT NULL,
    name character varying,
    description character varying,
    uuid uuid NOT NULL
);


ALTER TABLE public.role OWNER TO postgres;

--
-- TOC entry 279 (class 1259 OID 19651)
-- Name: role_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.role_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.role_id_seq OWNER TO postgres;

--
-- TOC entry 4833 (class 0 OID 0)
-- Dependencies: 279
-- Name: role_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.role_id_seq OWNED BY public.role.id;


--
-- TOC entry 291 (class 1259 OID 19764)
-- Name: role_resource_permissions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.role_resource_permissions (
    role_id integer NOT NULL,
    resource_id integer NOT NULL
);


ALTER TABLE public.role_resource_permissions OWNER TO postgres;

--
-- TOC entry 292 (class 1259 OID 19779)
-- Name: roles_permissions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.roles_permissions (
    role_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.roles_permissions OWNER TO postgres;

--
-- TOC entry 293 (class 1259 OID 19794)
-- Name: roles_users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.roles_users (
    user_id integer NOT NULL,
    role_id integer NOT NULL
);


ALTER TABLE public.roles_users OWNER TO postgres;

--
-- TOC entry 331 (class 1259 OID 20367)
-- Name: sample; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.sample (
    id integer NOT NULL,
    name character varying NOT NULL,
    participant_set_id integer NOT NULL,
    uuid uuid NOT NULL
);


ALTER TABLE public.sample OWNER TO postgres;

--
-- TOC entry 330 (class 1259 OID 20365)
-- Name: sample_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.sample_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.sample_id_seq OWNER TO postgres;

--
-- TOC entry 4834 (class 0 OID 0)
-- Dependencies: 330
-- Name: sample_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.sample_id_seq OWNED BY public.sample.id;


--
-- TOC entry 332 (class 1259 OID 20381)
-- Name: samples_participants; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.samples_participants (
    sample_id integer NOT NULL,
    participant_id integer NOT NULL
);


ALTER TABLE public.samples_participants OWNER TO postgres;

--
-- TOC entry 318 (class 1259 OID 20146)
-- Name: submission; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.submission (
    id integer NOT NULL,
    deployment_id integer NOT NULL,
    event_id integer NOT NULL,
    form_id integer NOT NULL,
    participant_id integer,
    location_id integer NOT NULL,
    data jsonb,
    extra_data jsonb,
    submission_type character varying(255),
    created timestamp without time zone,
    updated timestamp without time zone,
    sender_verified boolean,
    quarantine_status character varying(255),
    verification_status character varying(255),
    incident_description character varying,
    incident_status character varying(255),
    overridden_fields character varying[],
    conflicts jsonb,
    uuid uuid NOT NULL,
    unreachable boolean NOT NULL,
    last_phone_number character varying,
    geom public.geometry(Point,4326),
    verified_fields jsonb,
    participant_updated timestamp without time zone,
    serial_no character varying
);


ALTER TABLE public.submission OWNER TO postgres;

--
-- TOC entry 322 (class 1259 OID 20215)
-- Name: submission_comment; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.submission_comment (
    id integer NOT NULL,
    submission_id integer NOT NULL,
    user_id integer,
    comment character varying,
    submit_date timestamp without time zone,
    deployment_id integer NOT NULL,
    uuid uuid NOT NULL
);


ALTER TABLE public.submission_comment OWNER TO postgres;

--
-- TOC entry 321 (class 1259 OID 20213)
-- Name: submission_comment_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.submission_comment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.submission_comment_id_seq OWNER TO postgres;

--
-- TOC entry 4835 (class 0 OID 0)
-- Dependencies: 321
-- Name: submission_comment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.submission_comment_id_seq OWNED BY public.submission_comment.id;


--
-- TOC entry 317 (class 1259 OID 20144)
-- Name: submission_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.submission_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.submission_id_seq OWNER TO postgres;

--
-- TOC entry 4836 (class 0 OID 0)
-- Dependencies: 317
-- Name: submission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.submission_id_seq OWNED BY public.submission.id;


--
-- TOC entry 324 (class 1259 OID 20241)
-- Name: submission_version; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.submission_version (
    id integer NOT NULL,
    submission_id integer NOT NULL,
    data jsonb,
    "timestamp" timestamp without time zone,
    channel character varying(255),
    deployment_id integer NOT NULL,
    identity character varying NOT NULL,
    uuid uuid NOT NULL
);


ALTER TABLE public.submission_version OWNER TO postgres;

--
-- TOC entry 323 (class 1259 OID 20239)
-- Name: submission_version_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.submission_version_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.submission_version_id_seq OWNER TO postgres;

--
-- TOC entry 4837 (class 0 OID 0)
-- Dependencies: 323
-- Name: submission_version_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.submission_version_id_seq OWNED BY public.submission_version.id;


--
-- TOC entry 282 (class 1259 OID 19671)
-- Name: user; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."user" (
    id integer NOT NULL,
    deployment_id integer NOT NULL,
    email character varying NOT NULL,
    username character varying NOT NULL,
    password character varying NOT NULL,
    last_name character varying,
    first_name character varying,
    active boolean,
    confirmed_at timestamp without time zone,
    current_login_at timestamp without time zone,
    last_login_at timestamp without time zone,
    current_login_ip character varying,
    last_login_ip character varying,
    login_count integer,
    uuid uuid NOT NULL,
    locale character varying
);


ALTER TABLE public."user" OWNER TO postgres;

--
-- TOC entry 281 (class 1259 OID 19669)
-- Name: user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.user_id_seq OWNER TO postgres;

--
-- TOC entry 4838 (class 0 OID 0)
-- Dependencies: 281
-- Name: user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.user_id_seq OWNED BY public."user".id;


--
-- TOC entry 294 (class 1259 OID 19825)
-- Name: user_resource_permissions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_resource_permissions (
    user_id integer NOT NULL,
    resource_id integer NOT NULL
);


ALTER TABLE public.user_resource_permissions OWNER TO postgres;

--
-- TOC entry 296 (class 1259 OID 19842)
-- Name: user_upload; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_upload (
    id integer NOT NULL,
    deployment_id integer NOT NULL,
    user_id integer NOT NULL,
    created timestamp without time zone,
    upload_filename character varying,
    uuid uuid NOT NULL
);


ALTER TABLE public.user_upload OWNER TO postgres;

--
-- TOC entry 295 (class 1259 OID 19840)
-- Name: user_upload_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.user_upload_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.user_upload_id_seq OWNER TO postgres;

--
-- TOC entry 4839 (class 0 OID 0)
-- Dependencies: 295
-- Name: user_upload_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.user_upload_id_seq OWNED BY public.user_upload.id;


--
-- TOC entry 297 (class 1259 OID 19861)
-- Name: users_permissions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users_permissions (
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.users_permissions OWNER TO postgres;

--
-- TOC entry 4322 (class 2604 OID 20342)
-- Name: contact_history id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.contact_history ALTER COLUMN id SET DEFAULT nextval('public.contact_history_id_seq'::regclass);


--
-- TOC entry 4296 (class 2604 OID 19568)
-- Name: deployment id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.deployment ALTER COLUMN id SET DEFAULT nextval('public.deployment_id_seq'::regclass);


--
-- TOC entry 4309 (class 2604 OID 19881)
-- Name: event id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.event ALTER COLUMN id SET DEFAULT nextval('public.event_id_seq'::regclass);


--
-- TOC entry 4302 (class 2604 OID 19690)
-- Name: form id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.form ALTER COLUMN id SET DEFAULT nextval('public.form_id_seq'::regclass);


--
-- TOC entry 4310 (class 2604 OID 19912)
-- Name: location id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.location ALTER COLUMN id SET DEFAULT nextval('public.location_id_seq'::regclass);


--
-- TOC entry 4304 (class 2604 OID 19711)
-- Name: location_data_field id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.location_data_field ALTER COLUMN id SET DEFAULT nextval('public.location_data_field_id_seq'::regclass);


--
-- TOC entry 4297 (class 2604 OID 19608)
-- Name: location_set id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.location_set ALTER COLUMN id SET DEFAULT nextval('public.location_set_id_seq'::regclass);


--
-- TOC entry 4305 (class 2604 OID 19732)
-- Name: location_type id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.location_type ALTER COLUMN id SET DEFAULT nextval('public.location_type_id_seq'::regclass);


--
-- TOC entry 4318 (class 2604 OID 20186)
-- Name: message id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.message ALTER COLUMN id SET DEFAULT nextval('public.message_id_seq'::regclass);


--
-- TOC entry 4315 (class 2604 OID 20049)
-- Name: participant id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.participant ALTER COLUMN id SET DEFAULT nextval('public.participant_id_seq'::regclass);


--
-- TOC entry 4311 (class 2604 OID 19958)
-- Name: participant_data_field id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.participant_data_field ALTER COLUMN id SET DEFAULT nextval('public.participant_data_field_id_seq'::regclass);


--
-- TOC entry 4316 (class 2604 OID 20085)
-- Name: participant_group id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.participant_group ALTER COLUMN id SET DEFAULT nextval('public.participant_group_id_seq'::regclass);


--
-- TOC entry 4312 (class 2604 OID 19979)
-- Name: participant_group_type id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.participant_group_type ALTER COLUMN id SET DEFAULT nextval('public.participant_group_type_id_seq'::regclass);


--
-- TOC entry 4313 (class 2604 OID 19995)
-- Name: participant_partner id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.participant_partner ALTER COLUMN id SET DEFAULT nextval('public.participant_partner_id_seq'::regclass);


--
-- TOC entry 4314 (class 2604 OID 20011)
-- Name: participant_role id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.participant_role ALTER COLUMN id SET DEFAULT nextval('public.participant_role_id_seq'::regclass);


--
-- TOC entry 4307 (class 2604 OID 19748)
-- Name: participant_set id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.participant_set ALTER COLUMN id SET DEFAULT nextval('public.participant_set_id_seq'::regclass);


--
-- TOC entry 4298 (class 2604 OID 19624)
-- Name: permission id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.permission ALTER COLUMN id SET DEFAULT nextval('public.permission_id_seq'::regclass);


--
-- TOC entry 4321 (class 2604 OID 20326)
-- Name: phone_contact id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.phone_contact ALTER COLUMN id SET DEFAULT nextval('public.phone_contact_id_seq'::regclass);


--
-- TOC entry 4299 (class 2604 OID 19640)
-- Name: resource resource_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.resource ALTER COLUMN resource_id SET DEFAULT nextval('public.resource_resource_id_seq'::regclass);


--
-- TOC entry 4300 (class 2604 OID 19656)
-- Name: role id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.role ALTER COLUMN id SET DEFAULT nextval('public.role_id_seq'::regclass);


--
-- TOC entry 4323 (class 2604 OID 20370)
-- Name: sample id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sample ALTER COLUMN id SET DEFAULT nextval('public.sample_id_seq'::regclass);


--
-- TOC entry 4317 (class 2604 OID 20149)
-- Name: submission id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.submission ALTER COLUMN id SET DEFAULT nextval('public.submission_id_seq'::regclass);


--
-- TOC entry 4319 (class 2604 OID 20218)
-- Name: submission_comment id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.submission_comment ALTER COLUMN id SET DEFAULT nextval('public.submission_comment_id_seq'::regclass);


--
-- TOC entry 4320 (class 2604 OID 20244)
-- Name: submission_version id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.submission_version ALTER COLUMN id SET DEFAULT nextval('public.submission_version_id_seq'::regclass);


--
-- TOC entry 4301 (class 2604 OID 19674)
-- Name: user id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user" ALTER COLUMN id SET DEFAULT nextval('public.user_id_seq'::regclass);


--
-- TOC entry 4308 (class 2604 OID 19845)
-- Name: user_upload id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_upload ALTER COLUMN id SET DEFAULT nextval('public.user_upload_id_seq'::regclass);


--
-- TOC entry 4740 (class 0 OID 19558)
-- Dependencies: 270
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.alembic_version (version_num) FROM stdin;
32263b7ab47e
\.


--
-- TOC entry 4799 (class 0 OID 20339)
-- Dependencies: 329
-- Data for Name: contact_history; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.contact_history (id, participant_id, user_id, description, created, uuid) FROM stdin;
\.


--
-- TOC entry 4742 (class 0 OID 19565)
-- Dependencies: 272
-- Data for Name: deployment; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.deployment (id, name, hostnames, allow_observer_submission_edit, logo, include_rejected_in_votes, is_initialized, dashboard_full_locations, uuid, primary_locale, other_locales, enable_partial_response_for_messages) FROM stdin;
1	Default	{localhost}	t	\N	f	f	t	a0ef7ef7-5596-4c4a-aae4-22378451b33a	\N	\N	\N
\.


--
-- TOC entry 4769 (class 0 OID 19878)
-- Dependencies: 299
-- Data for Name: event; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.event (id, name, start, "end", resource_id, location_set_id, participant_set_id) FROM stdin;
1	Default	1970-01-01 00:00:00+00	1970-01-01 00:00:00+00	1	\N	\N
\.


--
-- TOC entry 4795 (class 0 OID 20305)
-- Dependencies: 325
-- Data for Name: events_forms; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.events_forms (event_id, form_id) FROM stdin;
\.


--
-- TOC entry 4754 (class 0 OID 19687)
-- Dependencies: 284
-- Data for Name: form; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.form (id, name, prefix, form_type, require_exclamation, data, version_identifier, resource_id, quality_checks, party_mappings, calculate_moe, accredited_voters_tag, quality_checks_enabled, invalid_votes_tag, registered_voters_tag, blank_votes_tag, vote_shares, untrack_data_conflicts, show_map, show_moment, show_progress) FROM stdin;
\.


--
-- TOC entry 4771 (class 0 OID 19909)
-- Dependencies: 301
-- Data for Name: location; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.location (id, code, registered_voters, location_set_id, location_type_id, extra_data, uuid, name_translations, geom) FROM stdin;
\.


--
-- TOC entry 4756 (class 0 OID 19708)
-- Dependencies: 286
-- Data for Name: location_data_field; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.location_data_field (id, location_set_id, name, label, visible_in_lists, resource_id) FROM stdin;
\.


--
-- TOC entry 4781 (class 0 OID 20022)
-- Dependencies: 311
-- Data for Name: location_path; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.location_path (location_set_id, ancestor_id, descendant_id, depth) FROM stdin;
\.


--
-- TOC entry 4744 (class 0 OID 19605)
-- Dependencies: 274
-- Data for Name: location_set; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.location_set (id, name, slug, deployment_id, uuid, is_finalized) FROM stdin;
\.


--
-- TOC entry 4758 (class 0 OID 19729)
-- Dependencies: 288
-- Data for Name: location_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.location_type (id, is_administrative, is_political, has_registered_voters, slug, location_set_id, uuid, name_translations, has_coordinates) FROM stdin;
\.


--
-- TOC entry 4772 (class 0 OID 19931)
-- Dependencies: 302
-- Data for Name: location_type_path; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.location_type_path (location_set_id, ancestor_id, descendant_id, depth) FROM stdin;
\.


--
-- TOC entry 4790 (class 0 OID 20183)
-- Dependencies: 320
-- Data for Name: message; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.message (id, direction, recipient, sender, text, received, delivered, deployment_id, event_id, submission_id, participant_id, uuid, message_type, originating_message_id) FROM stdin;
\.


--
-- TOC entry 4783 (class 0 OID 20046)
-- Dependencies: 313
-- Data for Name: participant; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.participant (id, participant_id, role_id, partner_id, supervisor_id, gender, email, location_id, participant_set_id, message_count, accurate_message_count, completion_rating, device_id, password, extra_data, uuid, full_name_translations, first_name_translations, last_name_translations, other_names_translations) FROM stdin;
\.


--
-- TOC entry 4774 (class 0 OID 19955)
-- Dependencies: 304
-- Data for Name: participant_data_field; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.participant_data_field (id, participant_set_id, name, label, visible_in_lists, resource_id) FROM stdin;
\.


--
-- TOC entry 4785 (class 0 OID 20082)
-- Dependencies: 315
-- Data for Name: participant_group; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.participant_group (id, name, group_type_id, participant_set_id, uuid) FROM stdin;
\.


--
-- TOC entry 4776 (class 0 OID 19976)
-- Dependencies: 306
-- Data for Name: participant_group_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.participant_group_type (id, name, participant_set_id, uuid) FROM stdin;
\.


--
-- TOC entry 4786 (class 0 OID 20116)
-- Dependencies: 316
-- Data for Name: participant_groups_participants; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.participant_groups_participants (group_id, participant_id) FROM stdin;
\.


--
-- TOC entry 4803 (class 0 OID 20431)
-- Dependencies: 333
-- Data for Name: participant_other_locations; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.participant_other_locations (id, participant_id, location_id, description, created) FROM stdin;
\.


--
-- TOC entry 4778 (class 0 OID 19992)
-- Dependencies: 308
-- Data for Name: participant_partner; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.participant_partner (id, name, participant_set_id, uuid) FROM stdin;
\.


--
-- TOC entry 4780 (class 0 OID 20008)
-- Dependencies: 310
-- Data for Name: participant_role; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.participant_role (id, name, participant_set_id, uuid) FROM stdin;
\.


--
-- TOC entry 4760 (class 0 OID 19745)
-- Dependencies: 290
-- Data for Name: participant_set; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.participant_set (id, name, slug, location_set_id, deployment_id, uuid, gender_hidden, partner_hidden, role_hidden) FROM stdin;
\.


--
-- TOC entry 4746 (class 0 OID 19621)
-- Dependencies: 276
-- Data for Name: permission; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.permission (id, name, description, deployment_id, uuid) FROM stdin;
1	add_submission	\N	1	899949fb-e63f-482d-83af-cc54616db794
2	edit_both_submissions	\N	1	ec335d62-af1c-44a9-b57c-a5133ec5ac21
3	edit_forms	\N	1	b715b42e-d69c-416e-a4a4-4eb318fea8c0
4	edit_locations	\N	1	9182eda4-c417-4f25-8445-8b7a8a993b7e
5	edit_participant	\N	1	9fac0713-a229-4eec-8d17-2f1d2021e0cd
6	edit_submission	\N	1	5b2ac08c-2828-43bb-9044-7cfb58a1b4d4
7	edit_submission_quarantine_status	\N	1	3903e06c-136e-4cfa-a300-28972f56fc61
8	edit_submission_verification_status	\N	1	484521ca-d61b-40bb-9901-1a00b6058a09
9	export_locations	\N	1	8d3a5ef1-7668-49f8-ac2f-6b8d37d393af
10	export_messages	\N	1	5342373a-f734-4cd8-9405-b522c6143a26
11	export_participants	\N	1	14b7ec7e-20c4-4ddd-9d39-cf68f9126118
12	export_submissions	\N	1	c91ef152-7014-4366-9d6f-131b93ef2838
13	import_locations	\N	1	6a5c6a5f-9d55-4894-9ed2-22c42f2c3a09
14	import_participants	\N	1	0b1e5f54-6907-4c80-9fc1-cb14402fda5e
15	send_messages	\N	1	2d8f9978-5a25-490f-84fa-2d788d528669
16	view_events	\N	1	824f08dd-c138-4dac-ac48-a030ecbaf38d
17	view_messages	\N	1	ad9d634e-ee76-46b5-b17d-2b7ae574cc9b
18	view_participants	\N	1	1ccc892f-0bc2-490f-9f87-2f59aff6c91f
19	view_process_analysis	\N	1	7446d08b-16f6-4da0-a303-c65d2a967f85
20	view_quality_assurance	\N	1	2e3acfdc-976c-470b-928e-2b4b1a931bf1
21	view_result_analysis	\N	1	6c410206-80b8-4f69-98e9-2a8cd2640391
\.


--
-- TOC entry 4797 (class 0 OID 20323)
-- Dependencies: 327
-- Data for Name: phone_contact; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.phone_contact (id, participant_id, number, created, updated, verified, uuid) FROM stdin;
\.


--
-- TOC entry 4748 (class 0 OID 19637)
-- Dependencies: 278
-- Data for Name: resource; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.resource (resource_id, resource_type, deployment_id, uuid) FROM stdin;
1	event	1	35e3dc8c-9797-4919-8f28-1901ab097b07
\.


--
-- TOC entry 4750 (class 0 OID 19653)
-- Dependencies: 280
-- Data for Name: role; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.role (id, deployment_id, name, description, uuid) FROM stdin;
1	1	admin	\N	ee411837-135a-4bbd-9189-a96e4abeb0cb
2	1	analyst	\N	3087d171-7cee-4b08-b2be-e0eb79724d12
3	1	manager	\N	a0458aae-ab1b-449c-a69e-b861d2b49d86
4	1	clerk	\N	df26f465-f545-49df-99cf-8f6ec221e7c9
5	1	field-coordinator	\N	34777acb-f831-48eb-b7a8-ec71e3cd1eb2
\.


--
-- TOC entry 4761 (class 0 OID 19764)
-- Dependencies: 291
-- Data for Name: role_resource_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.role_resource_permissions (role_id, resource_id) FROM stdin;
\.


--
-- TOC entry 4762 (class 0 OID 19779)
-- Dependencies: 292
-- Data for Name: roles_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.roles_permissions (role_id, permission_id) FROM stdin;
4	1
4	2
4	6
4	17
4	18
4	16
3	1
3	2
3	6
3	7
3	8
3	15
3	16
3	17
3	18
3	20
2	1
2	2
2	5
2	6
2	7
2	8
2	10
2	11
2	12
2	15
2	16
2	17
2	18
2	20
2	19
2	21
\.


--
-- TOC entry 4763 (class 0 OID 19794)
-- Dependencies: 293
-- Data for Name: roles_users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.roles_users (user_id, role_id) FROM stdin;
1	1
\.


--
-- TOC entry 4801 (class 0 OID 20367)
-- Dependencies: 331
-- Data for Name: sample; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.sample (id, name, participant_set_id, uuid) FROM stdin;
\.


--
-- TOC entry 4802 (class 0 OID 20381)
-- Dependencies: 332
-- Data for Name: samples_participants; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.samples_participants (sample_id, participant_id) FROM stdin;
\.


--
-- TOC entry 4224 (class 0 OID 18277)
-- Dependencies: 210
-- Data for Name: spatial_ref_sys; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.spatial_ref_sys (srid, auth_name, auth_srid, srtext, proj4text) FROM stdin;
\.


--
-- TOC entry 4788 (class 0 OID 20146)
-- Dependencies: 318
-- Data for Name: submission; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.submission (id, deployment_id, event_id, form_id, participant_id, location_id, data, extra_data, submission_type, created, updated, sender_verified, quarantine_status, verification_status, incident_description, incident_status, overridden_fields, conflicts, uuid, unreachable, last_phone_number, geom, verified_fields, participant_updated, serial_no) FROM stdin;
\.


--
-- TOC entry 4792 (class 0 OID 20215)
-- Dependencies: 322
-- Data for Name: submission_comment; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.submission_comment (id, submission_id, user_id, comment, submit_date, deployment_id, uuid) FROM stdin;
\.


--
-- TOC entry 4794 (class 0 OID 20241)
-- Dependencies: 324
-- Data for Name: submission_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.submission_version (id, submission_id, data, "timestamp", channel, deployment_id, identity, uuid) FROM stdin;
\.


--
-- TOC entry 4752 (class 0 OID 19671)
-- Dependencies: 282
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."user" (id, deployment_id, email, username, password, last_name, first_name, active, confirmed_at, current_login_at, last_login_at, current_login_ip, last_login_ip, login_count, uuid, locale) FROM stdin;
1	1	admin@example.com	admin	$pbkdf2-sha256$29000$kVIKAQAgpDSmdM55D2EMQQ$58zooDKavogzL6Tg1kPQSqk68Wm.rWA1D4UAImQTxK8	\N	\N	t	\N	\N	\N	\N	\N	\N	97af5f4f-02aa-4ec7-a034-4bfa434e0824	\N
\.


--
-- TOC entry 4764 (class 0 OID 19825)
-- Dependencies: 294
-- Data for Name: user_resource_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.user_resource_permissions (user_id, resource_id) FROM stdin;
\.


--
-- TOC entry 4766 (class 0 OID 19842)
-- Dependencies: 296
-- Data for Name: user_upload; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.user_upload (id, deployment_id, user_id, created, upload_filename, uuid) FROM stdin;
\.


--
-- TOC entry 4767 (class 0 OID 19861)
-- Dependencies: 297
-- Data for Name: users_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users_permissions (user_id, permission_id) FROM stdin;
\.


--
-- TOC entry 4227 (class 0 OID 19136)
-- Dependencies: 221
-- Data for Name: geocode_settings; Type: TABLE DATA; Schema: tiger; Owner: postgres
--

COPY tiger.geocode_settings (name, setting, unit, category, short_desc) FROM stdin;
\.


--
-- TOC entry 4228 (class 0 OID 19491)
-- Dependencies: 265
-- Data for Name: pagc_gaz; Type: TABLE DATA; Schema: tiger; Owner: postgres
--

COPY tiger.pagc_gaz (id, seq, word, stdword, token, is_custom) FROM stdin;
\.


--
-- TOC entry 4229 (class 0 OID 19503)
-- Dependencies: 267
-- Data for Name: pagc_lex; Type: TABLE DATA; Schema: tiger; Owner: postgres
--

COPY tiger.pagc_lex (id, seq, word, stdword, token, is_custom) FROM stdin;
\.


--
-- TOC entry 4230 (class 0 OID 19515)
-- Dependencies: 269
-- Data for Name: pagc_rules; Type: TABLE DATA; Schema: tiger; Owner: postgres
--

COPY tiger.pagc_rules (id, rule, is_custom) FROM stdin;
\.


--
-- TOC entry 4225 (class 0 OID 18978)
-- Dependencies: 215
-- Data for Name: topology; Type: TABLE DATA; Schema: topology; Owner: postgres
--

COPY topology.topology (id, name, srid, "precision", hasz) FROM stdin;
\.


--
-- TOC entry 4226 (class 0 OID 18991)
-- Dependencies: 216
-- Data for Name: layer; Type: TABLE DATA; Schema: topology; Owner: postgres
--

COPY topology.layer (topology_id, layer_id, schema_name, table_name, feature_column, feature_type, level, child_id) FROM stdin;
\.


--
-- TOC entry 4840 (class 0 OID 0)
-- Dependencies: 328
-- Name: contact_history_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.contact_history_id_seq', 1, false);


--
-- TOC entry 4841 (class 0 OID 0)
-- Dependencies: 271
-- Name: deployment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.deployment_id_seq', 1, true);


--
-- TOC entry 4842 (class 0 OID 0)
-- Dependencies: 298
-- Name: event_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.event_id_seq', 1, true);


--
-- TOC entry 4843 (class 0 OID 0)
-- Dependencies: 283
-- Name: form_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.form_id_seq', 1, false);


--
-- TOC entry 4844 (class 0 OID 0)
-- Dependencies: 285
-- Name: location_data_field_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.location_data_field_id_seq', 1, false);


--
-- TOC entry 4845 (class 0 OID 0)
-- Dependencies: 300
-- Name: location_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.location_id_seq', 1, false);


--
-- TOC entry 4846 (class 0 OID 0)
-- Dependencies: 273
-- Name: location_set_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.location_set_id_seq', 1, false);


--
-- TOC entry 4847 (class 0 OID 0)
-- Dependencies: 287
-- Name: location_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.location_type_id_seq', 1, false);


--
-- TOC entry 4848 (class 0 OID 0)
-- Dependencies: 319
-- Name: message_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.message_id_seq', 1, false);


--
-- TOC entry 4849 (class 0 OID 0)
-- Dependencies: 303
-- Name: participant_data_field_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.participant_data_field_id_seq', 1, false);


--
-- TOC entry 4850 (class 0 OID 0)
-- Dependencies: 314
-- Name: participant_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.participant_group_id_seq', 1, false);


--
-- TOC entry 4851 (class 0 OID 0)
-- Dependencies: 305
-- Name: participant_group_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.participant_group_type_id_seq', 1, false);


--
-- TOC entry 4852 (class 0 OID 0)
-- Dependencies: 312
-- Name: participant_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.participant_id_seq', 1, false);


--
-- TOC entry 4853 (class 0 OID 0)
-- Dependencies: 307
-- Name: participant_partner_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.participant_partner_id_seq', 1, false);


--
-- TOC entry 4854 (class 0 OID 0)
-- Dependencies: 309
-- Name: participant_role_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.participant_role_id_seq', 1, false);


--
-- TOC entry 4855 (class 0 OID 0)
-- Dependencies: 289
-- Name: participant_set_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.participant_set_id_seq', 1, false);


--
-- TOC entry 4856 (class 0 OID 0)
-- Dependencies: 275
-- Name: permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.permission_id_seq', 21, true);


--
-- TOC entry 4857 (class 0 OID 0)
-- Dependencies: 326
-- Name: phone_contact_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.phone_contact_id_seq', 1, false);


--
-- TOC entry 4858 (class 0 OID 0)
-- Dependencies: 277
-- Name: resource_resource_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.resource_resource_id_seq', 1, true);


--
-- TOC entry 4859 (class 0 OID 0)
-- Dependencies: 279
-- Name: role_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.role_id_seq', 5, true);


--
-- TOC entry 4860 (class 0 OID 0)
-- Dependencies: 330
-- Name: sample_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.sample_id_seq', 1, false);


--
-- TOC entry 4861 (class 0 OID 0)
-- Dependencies: 321
-- Name: submission_comment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.submission_comment_id_seq', 1, false);


--
-- TOC entry 4862 (class 0 OID 0)
-- Dependencies: 317
-- Name: submission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.submission_id_seq', 1, false);


--
-- TOC entry 4863 (class 0 OID 0)
-- Dependencies: 323
-- Name: submission_version_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.submission_version_id_seq', 1, false);


--
-- TOC entry 4864 (class 0 OID 0)
-- Dependencies: 281
-- Name: user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.user_id_seq', 1, true);


--
-- TOC entry 4865 (class 0 OID 0)
-- Dependencies: 295
-- Name: user_upload_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.user_upload_id_seq', 1, false);


--
-- TOC entry 4445 (class 2606 OID 19562)
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- TOC entry 4527 (class 2606 OID 20347)
-- Name: contact_history contact_history_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.contact_history
    ADD CONSTRAINT contact_history_pkey PRIMARY KEY (id);


--
-- TOC entry 4447 (class 2606 OID 19573)
-- Name: deployment deployment_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.deployment
    ADD CONSTRAINT deployment_pkey PRIMARY KEY (id);


--
-- TOC entry 4481 (class 2606 OID 19886)
-- Name: event event_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.event
    ADD CONSTRAINT event_pkey PRIMARY KEY (id);


--
-- TOC entry 4523 (class 2606 OID 20309)
-- Name: events_forms events_forms_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.events_forms
    ADD CONSTRAINT events_forms_pkey PRIMARY KEY (event_id, form_id);


--
-- TOC entry 4461 (class 2606 OID 19695)
-- Name: form form_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.form
    ADD CONSTRAINT form_pkey PRIMARY KEY (id);


--
-- TOC entry 4463 (class 2606 OID 19716)
-- Name: location_data_field location_data_field_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.location_data_field
    ADD CONSTRAINT location_data_field_pkey PRIMARY KEY (id);


--
-- TOC entry 4484 (class 2606 OID 19919)
-- Name: location location_location_set_id_code_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.location
    ADD CONSTRAINT location_location_set_id_code_key UNIQUE (location_set_id, code);


--
-- TOC entry 4500 (class 2606 OID 20026)
-- Name: location_path location_path_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.location_path
    ADD CONSTRAINT location_path_pkey PRIMARY KEY (ancestor_id, descendant_id);


--
-- TOC entry 4486 (class 2606 OID 19917)
-- Name: location location_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.location
    ADD CONSTRAINT location_pkey PRIMARY KEY (id);


--
-- TOC entry 4449 (class 2606 OID 19613)
-- Name: location_set location_set_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.location_set
    ADD CONSTRAINT location_set_pkey PRIMARY KEY (id);


--
-- TOC entry 4488 (class 2606 OID 19935)
-- Name: location_type_path location_type_path_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.location_type_path
    ADD CONSTRAINT location_type_path_pkey PRIMARY KEY (ancestor_id, descendant_id);


--
-- TOC entry 4465 (class 2606 OID 19737)
-- Name: location_type location_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.location_type
    ADD CONSTRAINT location_type_pkey PRIMARY KEY (id);


--
-- TOC entry 4517 (class 2606 OID 20191)
-- Name: message message_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.message
    ADD CONSTRAINT message_pkey PRIMARY KEY (id);


--
-- TOC entry 4492 (class 2606 OID 19963)
-- Name: participant_data_field participant_data_field_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.participant_data_field
    ADD CONSTRAINT participant_data_field_pkey PRIMARY KEY (id);


--
-- TOC entry 4506 (class 2606 OID 20090)
-- Name: participant_group participant_group_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.participant_group
    ADD CONSTRAINT participant_group_pkey PRIMARY KEY (id);


--
-- TOC entry 4494 (class 2606 OID 19984)
-- Name: participant_group_type participant_group_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.participant_group_type
    ADD CONSTRAINT participant_group_type_pkey PRIMARY KEY (id);


--
-- TOC entry 4535 (class 2606 OID 20435)
-- Name: participant_other_locations participant_other_locations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.participant_other_locations
    ADD CONSTRAINT participant_other_locations_pkey PRIMARY KEY (id);


--
-- TOC entry 4496 (class 2606 OID 20000)
-- Name: participant_partner participant_partner_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.participant_partner
    ADD CONSTRAINT participant_partner_pkey PRIMARY KEY (id);


--
-- TOC entry 4504 (class 2606 OID 20054)
-- Name: participant participant_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.participant
    ADD CONSTRAINT participant_pkey PRIMARY KEY (id);


--
-- TOC entry 4498 (class 2606 OID 20016)
-- Name: participant_role participant_role_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.participant_role
    ADD CONSTRAINT participant_role_pkey PRIMARY KEY (id);


--
-- TOC entry 4467 (class 2606 OID 19753)
-- Name: participant_set participant_set_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.participant_set
    ADD CONSTRAINT participant_set_pkey PRIMARY KEY (id);


--
-- TOC entry 4451 (class 2606 OID 19629)
-- Name: permission permission_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.permission
    ADD CONSTRAINT permission_pkey PRIMARY KEY (id);


--
-- TOC entry 4525 (class 2606 OID 20331)
-- Name: phone_contact phone_contact_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.phone_contact
    ADD CONSTRAINT phone_contact_pkey PRIMARY KEY (id);


--
-- TOC entry 4453 (class 2606 OID 19645)
-- Name: resource resource_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.resource
    ADD CONSTRAINT resource_pkey PRIMARY KEY (resource_id);


--
-- TOC entry 4455 (class 2606 OID 19663)
-- Name: role role_deployment_id_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.role
    ADD CONSTRAINT role_deployment_id_name_key UNIQUE (deployment_id, name);


--
-- TOC entry 4457 (class 2606 OID 19661)
-- Name: role role_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.role
    ADD CONSTRAINT role_pkey PRIMARY KEY (id);


--
-- TOC entry 4469 (class 2606 OID 19768)
-- Name: role_resource_permissions role_resource_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.role_resource_permissions
    ADD CONSTRAINT role_resource_permissions_pkey PRIMARY KEY (role_id, resource_id);


--
-- TOC entry 4471 (class 2606 OID 19783)
-- Name: roles_permissions roles_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roles_permissions
    ADD CONSTRAINT roles_permissions_pkey PRIMARY KEY (role_id, permission_id);


--
-- TOC entry 4473 (class 2606 OID 19798)
-- Name: roles_users roles_users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roles_users
    ADD CONSTRAINT roles_users_pkey PRIMARY KEY (user_id, role_id);


--
-- TOC entry 4529 (class 2606 OID 20375)
-- Name: sample sample_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sample
    ADD CONSTRAINT sample_pkey PRIMARY KEY (id);


--
-- TOC entry 4531 (class 2606 OID 20385)
-- Name: samples_participants samples_participants_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.samples_participants
    ADD CONSTRAINT samples_participants_pkey PRIMARY KEY (sample_id, participant_id);


--
-- TOC entry 4519 (class 2606 OID 20223)
-- Name: submission_comment submission_comment_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.submission_comment
    ADD CONSTRAINT submission_comment_pkey PRIMARY KEY (id);


--
-- TOC entry 4513 (class 2606 OID 20154)
-- Name: submission submission_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.submission
    ADD CONSTRAINT submission_pkey PRIMARY KEY (id);


--
-- TOC entry 4521 (class 2606 OID 20249)
-- Name: submission_version submission_version_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.submission_version
    ADD CONSTRAINT submission_version_pkey PRIMARY KEY (id);


--
-- TOC entry 4459 (class 2606 OID 19679)
-- Name: user user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);


--
-- TOC entry 4475 (class 2606 OID 19829)
-- Name: user_resource_permissions user_resource_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_resource_permissions
    ADD CONSTRAINT user_resource_permissions_pkey PRIMARY KEY (user_id, resource_id);


--
-- TOC entry 4477 (class 2606 OID 19850)
-- Name: user_upload user_upload_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_upload
    ADD CONSTRAINT user_upload_pkey PRIMARY KEY (id);


--
-- TOC entry 4479 (class 2606 OID 19865)
-- Name: users_permissions users_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users_permissions
    ADD CONSTRAINT users_permissions_pkey PRIMARY KEY (user_id, permission_id);


--
-- TOC entry 4532 (class 1259 OID 20444)
-- Name: fki_participant_id_fkey; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX fki_participant_id_fkey ON public.participant_other_locations USING btree (participant_id);


--
-- TOC entry 4533 (class 1259 OID 20455)
-- Name: fki_participant_other_locations_location_id_fkey; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX fki_participant_other_locations_location_id_fkey ON public.participant_other_locations USING btree (location_id);


--
-- TOC entry 4482 (class 1259 OID 19930)
-- Name: ix_location_code; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_location_code ON public.location USING btree (code);


--
-- TOC entry 4514 (class 1259 OID 20212)
-- Name: ix_message_received; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_message_received ON public.message USING btree (received);


--
-- TOC entry 4507 (class 1259 OID 20360)
-- Name: ix_submission_participant_updated; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_submission_participant_updated ON public.submission USING btree (participant_updated);


--
-- TOC entry 4508 (class 1259 OID 20361)
-- Name: ix_submission_serial_no; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_submission_serial_no ON public.submission USING btree (serial_no);


--
-- TOC entry 4509 (class 1259 OID 20362)
-- Name: ix_submission_submission_type; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_submission_submission_type ON public.submission USING btree (submission_type);


--
-- TOC entry 4510 (class 1259 OID 20363)
-- Name: ix_submission_updated; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_submission_updated ON public.submission USING btree (updated);


--
-- TOC entry 4515 (class 1259 OID 20358)
-- Name: ix_text_tsv; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_text_tsv ON public.message USING gin (to_tsvector('english'::regconfig, (text)::text));


--
-- TOC entry 4501 (class 1259 OID 20042)
-- Name: location_paths_ancestor_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX location_paths_ancestor_idx ON public.location_path USING btree (ancestor_id);


--
-- TOC entry 4502 (class 1259 OID 20043)
-- Name: location_paths_descendant_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX location_paths_descendant_idx ON public.location_path USING btree (descendant_id);


--
-- TOC entry 4489 (class 1259 OID 19951)
-- Name: location_type_paths_ancestor_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX location_type_paths_ancestor_idx ON public.location_type_path USING btree (ancestor_id);


--
-- TOC entry 4490 (class 1259 OID 19952)
-- Name: location_type_paths_descendant_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX location_type_paths_descendant_idx ON public.location_type_path USING btree (descendant_id);


--
-- TOC entry 4511 (class 1259 OID 20180)
-- Name: submission_data_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX submission_data_idx ON public.submission USING gin (data);


--
-- TOC entry 4602 (class 2606 OID 20348)
-- Name: contact_history contact_history_participant_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.contact_history
    ADD CONSTRAINT contact_history_participant_id_fkey FOREIGN KEY (participant_id) REFERENCES public.participant(id) ON DELETE CASCADE;


--
-- TOC entry 4603 (class 2606 OID 20353)
-- Name: contact_history contact_history_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.contact_history
    ADD CONSTRAINT contact_history_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id) ON DELETE CASCADE;


--
-- TOC entry 4559 (class 2606 OID 19892)
-- Name: event event_location_set_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.event
    ADD CONSTRAINT event_location_set_id_fkey FOREIGN KEY (location_set_id) REFERENCES public.location_set(id) ON DELETE SET NULL;


--
-- TOC entry 4560 (class 2606 OID 19897)
-- Name: event event_participant_set_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.event
    ADD CONSTRAINT event_participant_set_id_fkey FOREIGN KEY (participant_set_id) REFERENCES public.participant_set(id) ON DELETE SET NULL;


--
-- TOC entry 4561 (class 2606 OID 19902)
-- Name: event event_resource_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.event
    ADD CONSTRAINT event_resource_id_fkey FOREIGN KEY (resource_id) REFERENCES public.resource(resource_id) ON DELETE CASCADE;


--
-- TOC entry 4599 (class 2606 OID 20310)
-- Name: events_forms events_forms_event_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.events_forms
    ADD CONSTRAINT events_forms_event_id_fkey FOREIGN KEY (event_id) REFERENCES public.event(id) ON DELETE CASCADE;


--
-- TOC entry 4600 (class 2606 OID 20315)
-- Name: events_forms events_forms_form_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.events_forms
    ADD CONSTRAINT events_forms_form_id_fkey FOREIGN KEY (form_id) REFERENCES public.form(id) ON DELETE CASCADE;


--
-- TOC entry 4541 (class 2606 OID 19701)
-- Name: form form_resource_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.form
    ADD CONSTRAINT form_resource_id_fkey FOREIGN KEY (resource_id) REFERENCES public.resource(resource_id) ON DELETE CASCADE;


--
-- TOC entry 4542 (class 2606 OID 19717)
-- Name: location_data_field location_data_field_location_set_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.location_data_field
    ADD CONSTRAINT location_data_field_location_set_id_fkey FOREIGN KEY (location_set_id) REFERENCES public.location_set(id) ON DELETE CASCADE;


--
-- TOC entry 4543 (class 2606 OID 19722)
-- Name: location_data_field location_data_field_resource_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.location_data_field
    ADD CONSTRAINT location_data_field_resource_id_fkey FOREIGN KEY (resource_id) REFERENCES public.resource(resource_id) ON DELETE CASCADE;


--
-- TOC entry 4562 (class 2606 OID 19920)
-- Name: location location_location_set_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.location
    ADD CONSTRAINT location_location_set_id_fkey FOREIGN KEY (location_set_id) REFERENCES public.location_set(id) ON DELETE CASCADE;


--
-- TOC entry 4563 (class 2606 OID 19925)
-- Name: location location_location_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.location
    ADD CONSTRAINT location_location_type_id_fkey FOREIGN KEY (location_type_id) REFERENCES public.location_type(id) ON DELETE CASCADE;


--
-- TOC entry 4572 (class 2606 OID 20027)
-- Name: location_path location_path_ancestor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.location_path
    ADD CONSTRAINT location_path_ancestor_id_fkey FOREIGN KEY (ancestor_id) REFERENCES public.location(id) ON DELETE CASCADE;


--
-- TOC entry 4573 (class 2606 OID 20032)
-- Name: location_path location_path_descendant_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.location_path
    ADD CONSTRAINT location_path_descendant_id_fkey FOREIGN KEY (descendant_id) REFERENCES public.location(id) ON DELETE CASCADE;


--
-- TOC entry 4574 (class 2606 OID 20037)
-- Name: location_path location_path_location_set_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.location_path
    ADD CONSTRAINT location_path_location_set_id_fkey FOREIGN KEY (location_set_id) REFERENCES public.location_set(id) ON DELETE CASCADE;


--
-- TOC entry 4536 (class 2606 OID 19614)
-- Name: location_set location_set_deployment_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.location_set
    ADD CONSTRAINT location_set_deployment_id_fkey FOREIGN KEY (deployment_id) REFERENCES public.deployment(id) ON DELETE CASCADE;


--
-- TOC entry 4544 (class 2606 OID 19738)
-- Name: location_type location_type_location_set_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.location_type
    ADD CONSTRAINT location_type_location_set_id_fkey FOREIGN KEY (location_set_id) REFERENCES public.location_set(id) ON DELETE CASCADE;


--
-- TOC entry 4564 (class 2606 OID 19936)
-- Name: location_type_path location_type_path_ancestor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.location_type_path
    ADD CONSTRAINT location_type_path_ancestor_id_fkey FOREIGN KEY (ancestor_id) REFERENCES public.location_type(id) ON DELETE CASCADE;


--
-- TOC entry 4565 (class 2606 OID 19941)
-- Name: location_type_path location_type_path_descendant_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.location_type_path
    ADD CONSTRAINT location_type_path_descendant_id_fkey FOREIGN KEY (descendant_id) REFERENCES public.location_type(id) ON DELETE CASCADE;


--
-- TOC entry 4566 (class 2606 OID 20260)
-- Name: location_type_path location_type_path_location_set_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.location_type_path
    ADD CONSTRAINT location_type_path_location_set_id_fkey FOREIGN KEY (location_set_id) REFERENCES public.location_set(id) ON DELETE CASCADE;


--
-- TOC entry 4589 (class 2606 OID 20192)
-- Name: message message_deployment_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.message
    ADD CONSTRAINT message_deployment_id_fkey FOREIGN KEY (deployment_id) REFERENCES public.deployment(id) ON DELETE CASCADE;


--
-- TOC entry 4590 (class 2606 OID 20197)
-- Name: message message_event_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.message
    ADD CONSTRAINT message_event_id_fkey FOREIGN KEY (event_id) REFERENCES public.event(id) ON DELETE CASCADE;


--
-- TOC entry 4593 (class 2606 OID 20265)
-- Name: message message_originating_message_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.message
    ADD CONSTRAINT message_originating_message_id_fkey FOREIGN KEY (originating_message_id) REFERENCES public.message(id) ON DELETE SET NULL;


--
-- TOC entry 4591 (class 2606 OID 20202)
-- Name: message message_participant_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.message
    ADD CONSTRAINT message_participant_id_fkey FOREIGN KEY (participant_id) REFERENCES public.participant(id) ON DELETE CASCADE;


--
-- TOC entry 4592 (class 2606 OID 20207)
-- Name: message message_submission_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.message
    ADD CONSTRAINT message_submission_id_fkey FOREIGN KEY (submission_id) REFERENCES public.submission(id) ON DELETE CASCADE;


--
-- TOC entry 4567 (class 2606 OID 19964)
-- Name: participant_data_field participant_data_field_participant_set_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.participant_data_field
    ADD CONSTRAINT participant_data_field_participant_set_id_fkey FOREIGN KEY (participant_set_id) REFERENCES public.participant_set(id) ON DELETE CASCADE;


--
-- TOC entry 4568 (class 2606 OID 19969)
-- Name: participant_data_field participant_data_field_resource_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.participant_data_field
    ADD CONSTRAINT participant_data_field_resource_id_fkey FOREIGN KEY (resource_id) REFERENCES public.resource(resource_id) ON DELETE CASCADE;


--
-- TOC entry 4580 (class 2606 OID 20091)
-- Name: participant_group participant_group_group_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.participant_group
    ADD CONSTRAINT participant_group_group_type_id_fkey FOREIGN KEY (group_type_id) REFERENCES public.participant_group_type(id) ON DELETE CASCADE;


--
-- TOC entry 4581 (class 2606 OID 20096)
-- Name: participant_group participant_group_participant_set_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.participant_group
    ADD CONSTRAINT participant_group_participant_set_id_fkey FOREIGN KEY (participant_set_id) REFERENCES public.participant_set(id) ON DELETE CASCADE;


--
-- TOC entry 4569 (class 2606 OID 19985)
-- Name: participant_group_type participant_group_type_participant_set_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.participant_group_type
    ADD CONSTRAINT participant_group_type_participant_set_id_fkey FOREIGN KEY (participant_set_id) REFERENCES public.participant_set(id) ON DELETE CASCADE;


--
-- TOC entry 4582 (class 2606 OID 20119)
-- Name: participant_groups_participants participant_groups_participants_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.participant_groups_participants
    ADD CONSTRAINT participant_groups_participants_group_id_fkey FOREIGN KEY (group_id) REFERENCES public.participant_group(id) ON DELETE CASCADE;


--
-- TOC entry 4583 (class 2606 OID 20124)
-- Name: participant_groups_participants participant_groups_participants_participant_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.participant_groups_participants
    ADD CONSTRAINT participant_groups_participants_participant_id_fkey FOREIGN KEY (participant_id) REFERENCES public.participant(id) ON DELETE CASCADE;


--
-- TOC entry 4575 (class 2606 OID 20055)
-- Name: participant participant_location_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.participant
    ADD CONSTRAINT participant_location_id_fkey FOREIGN KEY (location_id) REFERENCES public.location(id) ON DELETE CASCADE;


--
-- TOC entry 4607 (class 2606 OID 20450)
-- Name: participant_other_locations participant_other_locations_location_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.participant_other_locations
    ADD CONSTRAINT participant_other_locations_location_id_fkey FOREIGN KEY (location_id) REFERENCES public.location(id);


--
-- TOC entry 4608 (class 2606 OID 20445)
-- Name: participant_other_locations participant_other_locations_participant_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.participant_other_locations
    ADD CONSTRAINT participant_other_locations_participant_id_fkey FOREIGN KEY (participant_id) REFERENCES public.participant(id);


--
-- TOC entry 4576 (class 2606 OID 20060)
-- Name: participant participant_participant_set_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.participant
    ADD CONSTRAINT participant_participant_set_id_fkey FOREIGN KEY (participant_set_id) REFERENCES public.participant_set(id) ON DELETE CASCADE;


--
-- TOC entry 4577 (class 2606 OID 20065)
-- Name: participant participant_partner_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.participant
    ADD CONSTRAINT participant_partner_id_fkey FOREIGN KEY (partner_id) REFERENCES public.participant_partner(id) ON DELETE SET NULL;


--
-- TOC entry 4570 (class 2606 OID 20001)
-- Name: participant_partner participant_partner_participant_set_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.participant_partner
    ADD CONSTRAINT participant_partner_participant_set_id_fkey FOREIGN KEY (participant_set_id) REFERENCES public.participant_set(id) ON DELETE CASCADE;


--
-- TOC entry 4578 (class 2606 OID 20070)
-- Name: participant participant_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.participant
    ADD CONSTRAINT participant_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.participant_role(id) ON DELETE SET NULL;


--
-- TOC entry 4571 (class 2606 OID 20017)
-- Name: participant_role participant_role_participant_set_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.participant_role
    ADD CONSTRAINT participant_role_participant_set_id_fkey FOREIGN KEY (participant_set_id) REFERENCES public.participant_set(id) ON DELETE CASCADE;


--
-- TOC entry 4545 (class 2606 OID 19754)
-- Name: participant_set participant_set_deployment_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.participant_set
    ADD CONSTRAINT participant_set_deployment_id_fkey FOREIGN KEY (deployment_id) REFERENCES public.deployment(id) ON DELETE CASCADE;


--
-- TOC entry 4546 (class 2606 OID 19759)
-- Name: participant_set participant_set_location_set_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.participant_set
    ADD CONSTRAINT participant_set_location_set_id_fkey FOREIGN KEY (location_set_id) REFERENCES public.location_set(id) ON DELETE CASCADE;


--
-- TOC entry 4579 (class 2606 OID 20075)
-- Name: participant participant_supervisor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.participant
    ADD CONSTRAINT participant_supervisor_id_fkey FOREIGN KEY (supervisor_id) REFERENCES public.participant(id) ON DELETE SET NULL;


--
-- TOC entry 4537 (class 2606 OID 19630)
-- Name: permission permission_deployment_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.permission
    ADD CONSTRAINT permission_deployment_id_fkey FOREIGN KEY (deployment_id) REFERENCES public.deployment(id) ON DELETE CASCADE;


--
-- TOC entry 4601 (class 2606 OID 20332)
-- Name: phone_contact phone_contact_participant_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.phone_contact
    ADD CONSTRAINT phone_contact_participant_id_fkey FOREIGN KEY (participant_id) REFERENCES public.participant(id) ON DELETE CASCADE;


--
-- TOC entry 4538 (class 2606 OID 19646)
-- Name: resource resource_deployment_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.resource
    ADD CONSTRAINT resource_deployment_id_fkey FOREIGN KEY (deployment_id) REFERENCES public.deployment(id) ON DELETE CASCADE;


--
-- TOC entry 4539 (class 2606 OID 19664)
-- Name: role role_deployment_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.role
    ADD CONSTRAINT role_deployment_id_fkey FOREIGN KEY (deployment_id) REFERENCES public.deployment(id) ON DELETE CASCADE;


--
-- TOC entry 4547 (class 2606 OID 19769)
-- Name: role_resource_permissions role_resource_permissions_resource_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.role_resource_permissions
    ADD CONSTRAINT role_resource_permissions_resource_id_fkey FOREIGN KEY (resource_id) REFERENCES public.resource(resource_id) ON DELETE CASCADE;


--
-- TOC entry 4548 (class 2606 OID 19774)
-- Name: role_resource_permissions role_resource_permissions_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.role_resource_permissions
    ADD CONSTRAINT role_resource_permissions_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.role(id) ON DELETE CASCADE;


--
-- TOC entry 4549 (class 2606 OID 19784)
-- Name: roles_permissions roles_permissions_permission_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roles_permissions
    ADD CONSTRAINT roles_permissions_permission_id_fkey FOREIGN KEY (permission_id) REFERENCES public.permission(id) ON DELETE CASCADE;


--
-- TOC entry 4550 (class 2606 OID 19789)
-- Name: roles_permissions roles_permissions_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roles_permissions
    ADD CONSTRAINT roles_permissions_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.role(id) ON DELETE CASCADE;


--
-- TOC entry 4551 (class 2606 OID 19799)
-- Name: roles_users roles_users_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roles_users
    ADD CONSTRAINT roles_users_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.role(id) ON DELETE CASCADE;


--
-- TOC entry 4552 (class 2606 OID 19804)
-- Name: roles_users roles_users_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roles_users
    ADD CONSTRAINT roles_users_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id) ON DELETE CASCADE;


--
-- TOC entry 4604 (class 2606 OID 20376)
-- Name: sample sample_participant_set_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sample
    ADD CONSTRAINT sample_participant_set_id_fkey FOREIGN KEY (participant_set_id) REFERENCES public.participant_set(id) ON DELETE CASCADE;


--
-- TOC entry 4605 (class 2606 OID 20386)
-- Name: samples_participants samples_participants_participant_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.samples_participants
    ADD CONSTRAINT samples_participants_participant_id_fkey FOREIGN KEY (participant_id) REFERENCES public.participant(id) ON DELETE CASCADE;


--
-- TOC entry 4606 (class 2606 OID 20391)
-- Name: samples_participants samples_participants_sample_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.samples_participants
    ADD CONSTRAINT samples_participants_sample_id_fkey FOREIGN KEY (sample_id) REFERENCES public.sample(id) ON DELETE CASCADE;


--
-- TOC entry 4594 (class 2606 OID 20224)
-- Name: submission_comment submission_comment_deployment_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.submission_comment
    ADD CONSTRAINT submission_comment_deployment_id_fkey FOREIGN KEY (deployment_id) REFERENCES public.deployment(id) ON DELETE CASCADE;


--
-- TOC entry 4595 (class 2606 OID 20229)
-- Name: submission_comment submission_comment_submission_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.submission_comment
    ADD CONSTRAINT submission_comment_submission_id_fkey FOREIGN KEY (submission_id) REFERENCES public.submission(id) ON DELETE CASCADE;


--
-- TOC entry 4596 (class 2606 OID 20234)
-- Name: submission_comment submission_comment_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.submission_comment
    ADD CONSTRAINT submission_comment_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id);


--
-- TOC entry 4584 (class 2606 OID 20155)
-- Name: submission submission_deployment_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.submission
    ADD CONSTRAINT submission_deployment_id_fkey FOREIGN KEY (deployment_id) REFERENCES public.deployment(id) ON DELETE CASCADE;


--
-- TOC entry 4585 (class 2606 OID 20160)
-- Name: submission submission_event_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.submission
    ADD CONSTRAINT submission_event_id_fkey FOREIGN KEY (event_id) REFERENCES public.event(id) ON DELETE CASCADE;


--
-- TOC entry 4586 (class 2606 OID 20165)
-- Name: submission submission_form_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.submission
    ADD CONSTRAINT submission_form_id_fkey FOREIGN KEY (form_id) REFERENCES public.form(id) ON DELETE CASCADE;


--
-- TOC entry 4587 (class 2606 OID 20170)
-- Name: submission submission_location_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.submission
    ADD CONSTRAINT submission_location_id_fkey FOREIGN KEY (location_id) REFERENCES public.location(id) ON DELETE CASCADE;


--
-- TOC entry 4588 (class 2606 OID 20175)
-- Name: submission submission_participant_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.submission
    ADD CONSTRAINT submission_participant_id_fkey FOREIGN KEY (participant_id) REFERENCES public.participant(id) ON DELETE CASCADE;


--
-- TOC entry 4597 (class 2606 OID 20250)
-- Name: submission_version submission_version_deployment_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.submission_version
    ADD CONSTRAINT submission_version_deployment_id_fkey FOREIGN KEY (deployment_id) REFERENCES public.deployment(id) ON DELETE CASCADE;


--
-- TOC entry 4598 (class 2606 OID 20255)
-- Name: submission_version submission_version_submission_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.submission_version
    ADD CONSTRAINT submission_version_submission_id_fkey FOREIGN KEY (submission_id) REFERENCES public.submission(id) ON DELETE CASCADE;


--
-- TOC entry 4540 (class 2606 OID 19680)
-- Name: user user_deployment_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_deployment_id_fkey FOREIGN KEY (deployment_id) REFERENCES public.deployment(id) ON DELETE CASCADE;


--
-- TOC entry 4553 (class 2606 OID 19830)
-- Name: user_resource_permissions user_resource_permissions_resource_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_resource_permissions
    ADD CONSTRAINT user_resource_permissions_resource_id_fkey FOREIGN KEY (resource_id) REFERENCES public.resource(resource_id) ON DELETE CASCADE;


--
-- TOC entry 4554 (class 2606 OID 19835)
-- Name: user_resource_permissions user_resource_permissions_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_resource_permissions
    ADD CONSTRAINT user_resource_permissions_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id) ON DELETE CASCADE;


--
-- TOC entry 4555 (class 2606 OID 19851)
-- Name: user_upload user_upload_deployment_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_upload
    ADD CONSTRAINT user_upload_deployment_id_fkey FOREIGN KEY (deployment_id) REFERENCES public.deployment(id) ON DELETE CASCADE;


--
-- TOC entry 4556 (class 2606 OID 19856)
-- Name: user_upload user_upload_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_upload
    ADD CONSTRAINT user_upload_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id) ON DELETE CASCADE;


--
-- TOC entry 4557 (class 2606 OID 19866)
-- Name: users_permissions users_permissions_permission_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users_permissions
    ADD CONSTRAINT users_permissions_permission_id_fkey FOREIGN KEY (permission_id) REFERENCES public.permission(id) ON DELETE CASCADE;


--
-- TOC entry 4558 (class 2606 OID 19871)
-- Name: users_permissions users_permissions_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users_permissions
    ADD CONSTRAINT users_permissions_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id) ON DELETE CASCADE;


-- Completed on 2020-10-07 12:04:20 UTC

--
-- PostgreSQL database dump complete
--

