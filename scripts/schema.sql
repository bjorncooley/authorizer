pg_dump -U staging_admin -d main_staging -h main-staging.cmmrjsgb2ell.us-west-1.rds.amazonaws.com -s
--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.3
-- Dumped by pg_dump version 9.6.3

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: cohorts; Type: TABLE; Schema: public; Owner: staging_admin
--

CREATE TABLE cohorts (
    id bigint NOT NULL,
    title text NOT NULL,
    salesforce_id text,
    start_date timestamp with time zone,
    end_date timestamp with time zone,
    term_id text,
    location_id text
);


ALTER TABLE cohorts OWNER TO staging_admin;

--
-- Name: cohorts_id_seq; Type: SEQUENCE; Schema: public; Owner: staging_admin
--

CREATE SEQUENCE cohorts_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE cohorts_id_seq OWNER TO staging_admin;

--
-- Name: cohorts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: staging_admin
--

ALTER SEQUENCE cohorts_id_seq OWNED BY cohorts.id;


--
-- Name: comments; Type: TABLE; Schema: public; Owner: staging_admin
--

CREATE TABLE comments (
    id bigint NOT NULL,
    date_time timestamp with time zone,
    comment_text text,
    user_id bigint,
    video_id bigint
);


ALTER TABLE comments OWNER TO staging_admin;

--
-- Name: comments_id_seq; Type: SEQUENCE; Schema: public; Owner: staging_admin
--

CREATE SEQUENCE comments_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE comments_id_seq OWNER TO staging_admin;

--
-- Name: comments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: staging_admin
--

ALTER SEQUENCE comments_id_seq OWNED BY comments.id;


--
-- Name: courses; Type: TABLE; Schema: public; Owner: staging_admin
--

CREATE TABLE courses (
    id bigint NOT NULL,
    name text NOT NULL,
    salesforce_id text,
    course_code text,
    term_id text,
    start_date timestamp with time zone,
    end_date timestamp with time zone,
    description text
);


ALTER TABLE courses OWNER TO staging_admin;

--
-- Name: courses_id_seq; Type: SEQUENCE; Schema: public; Owner: staging_admin
--

CREATE SEQUENCE courses_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE courses_id_seq OWNER TO staging_admin;

--
-- Name: courses_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: staging_admin
--

ALTER SEQUENCE courses_id_seq OWNED BY courses.id;


--
-- Name: interviews; Type: TABLE; Schema: public; Owner: staging_admin
--

CREATE TABLE interviews (
    id integer NOT NULL,
    salesforce_id text,
    zoom_id text,
    zoom_url text,
    recording_name text,
    meeting_id text,
    video_url text,
    date_time text,
    saved_locally boolean DEFAULT false,
    size text,
    source_account text
);


ALTER TABLE interviews OWNER TO staging_admin;

--
-- Name: interviews_id_seq; Type: SEQUENCE; Schema: public; Owner: staging_admin
--

CREATE SEQUENCE interviews_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE interviews_id_seq OWNER TO staging_admin;

--
-- Name: interviews_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: staging_admin
--

ALTER SEQUENCE interviews_id_seq OWNED BY interviews.id;


--
-- Name: reset_tokens; Type: TABLE; Schema: public; Owner: staging_admin
--

CREATE TABLE reset_tokens (
    id bigint NOT NULL,
    email text NOT NULL,
    token text NOT NULL,
    time_created timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE reset_tokens OWNER TO staging_admin;

--
-- Name: reset_tokens_id_seq; Type: SEQUENCE; Schema: public; Owner: staging_admin
--

CREATE SEQUENCE reset_tokens_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE reset_tokens_id_seq OWNER TO staging_admin;

--
-- Name: reset_tokens_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: staging_admin
--

ALTER SEQUENCE reset_tokens_id_seq OWNED BY reset_tokens.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: staging_admin
--

CREATE TABLE users (
    id bigint NOT NULL,
    email text NOT NULL,
    password text,
    salt text,
    first_name text,
    last_name text,
    salesforce_id text,
    user_type text,
    cohort bigint
);


ALTER TABLE users OWNER TO staging_admin;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: staging_admin
--

CREATE SEQUENCE users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE users_id_seq OWNER TO staging_admin;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: staging_admin
--

ALTER SEQUENCE users_id_seq OWNED BY users.id;


--
-- Name: validation_tokens; Type: TABLE; Schema: public; Owner: staging_admin
--

CREATE TABLE validation_tokens (
    id bigint NOT NULL,
    email text NOT NULL,
    token text,
    time_created timestamp with time zone DEFAULT now()
);


ALTER TABLE validation_tokens OWNER TO staging_admin;

--
-- Name: validation_tokens_id_seq; Type: SEQUENCE; Schema: public; Owner: staging_admin
--

CREATE SEQUENCE validation_tokens_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE validation_tokens_id_seq OWNER TO staging_admin;

--
-- Name: validation_tokens_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: staging_admin
--

ALTER SEQUENCE validation_tokens_id_seq OWNED BY validation_tokens.id;


--
-- Name: video_users; Type: TABLE; Schema: public; Owner: staging_admin
--

CREATE TABLE video_users (
    id bigint NOT NULL,
    video_id bigint,
    user_id bigint
);


ALTER TABLE video_users OWNER TO staging_admin;

--
-- Name: video_users_id_seq; Type: SEQUENCE; Schema: public; Owner: staging_admin
--

CREATE SEQUENCE video_users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE video_users_id_seq OWNER TO staging_admin;

--
-- Name: video_users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: staging_admin
--

ALTER SEQUENCE video_users_id_seq OWNED BY video_users.id;


--
-- Name: videos; Type: TABLE; Schema: public; Owner: staging_admin
--

CREATE TABLE videos (
    id bigint NOT NULL,
    salesforce_id text,
    zoom_id text,
    zoom_url text,
    title text,
    zoom_meeting_id text,
    video_url text,
    start_time text,
    saved_locally boolean DEFAULT false,
    size bigint,
    source_account text,
    host_id bigint,
    course_id bigint,
    end_time text,
    subject text,
    tags json,
    video_type text,
    votes integer,
    facilitator text,
    chat_log text,
    participants text[]
);


ALTER TABLE videos OWNER TO staging_admin;

--
-- Name: videos_id_seq; Type: SEQUENCE; Schema: public; Owner: staging_admin
--

CREATE SEQUENCE videos_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE videos_id_seq OWNER TO staging_admin;

--
-- Name: videos_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: staging_admin
--

ALTER SEQUENCE videos_id_seq OWNED BY videos.id;


--
-- Name: cohorts id; Type: DEFAULT; Schema: public; Owner: staging_admin
--

ALTER TABLE ONLY cohorts ALTER COLUMN id SET DEFAULT nextval('cohorts_id_seq'::regclass);


--
-- Name: comments id; Type: DEFAULT; Schema: public; Owner: staging_admin
--

ALTER TABLE ONLY comments ALTER COLUMN id SET DEFAULT nextval('comments_id_seq'::regclass);


--
-- Name: courses id; Type: DEFAULT; Schema: public; Owner: staging_admin
--

ALTER TABLE ONLY courses ALTER COLUMN id SET DEFAULT nextval('courses_id_seq'::regclass);


--
-- Name: interviews id; Type: DEFAULT; Schema: public; Owner: staging_admin
--

ALTER TABLE ONLY interviews ALTER COLUMN id SET DEFAULT nextval('interviews_id_seq'::regclass);


--
-- Name: reset_tokens id; Type: DEFAULT; Schema: public; Owner: staging_admin
--

ALTER TABLE ONLY reset_tokens ALTER COLUMN id SET DEFAULT nextval('reset_tokens_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: staging_admin
--

ALTER TABLE ONLY users ALTER COLUMN id SET DEFAULT nextval('users_id_seq'::regclass);


--
-- Name: validation_tokens id; Type: DEFAULT; Schema: public; Owner: staging_admin
--

ALTER TABLE ONLY validation_tokens ALTER COLUMN id SET DEFAULT nextval('validation_tokens_id_seq'::regclass);


--
-- Name: video_users id; Type: DEFAULT; Schema: public; Owner: staging_admin
--

ALTER TABLE ONLY video_users ALTER COLUMN id SET DEFAULT nextval('video_users_id_seq'::regclass);


--
-- Name: videos id; Type: DEFAULT; Schema: public; Owner: staging_admin
--

ALTER TABLE ONLY videos ALTER COLUMN id SET DEFAULT nextval('videos_id_seq'::regclass);


--
-- Name: cohorts cohorts_pkey; Type: CONSTRAINT; Schema: public; Owner: staging_admin
--

ALTER TABLE ONLY cohorts
    ADD CONSTRAINT cohorts_pkey PRIMARY KEY (id);


--
-- Name: cohorts cohorts_title_key; Type: CONSTRAINT; Schema: public; Owner: staging_admin
--

ALTER TABLE ONLY cohorts
    ADD CONSTRAINT cohorts_title_key UNIQUE (title);


--
-- Name: comments comments_pkey; Type: CONSTRAINT; Schema: public; Owner: staging_admin
--

ALTER TABLE ONLY comments
    ADD CONSTRAINT comments_pkey PRIMARY KEY (id);


--
-- Name: courses courses_pkey; Type: CONSTRAINT; Schema: public; Owner: staging_admin
--

ALTER TABLE ONLY courses
    ADD CONSTRAINT courses_pkey PRIMARY KEY (id);


--
-- Name: interviews interviews_pkey; Type: CONSTRAINT; Schema: public; Owner: staging_admin
--

ALTER TABLE ONLY interviews
    ADD CONSTRAINT interviews_pkey PRIMARY KEY (id);


--
-- Name: interviews interviews_salesforce_id_key; Type: CONSTRAINT; Schema: public; Owner: staging_admin
--

ALTER TABLE ONLY interviews
    ADD CONSTRAINT interviews_salesforce_id_key UNIQUE (salesforce_id);


--
-- Name: interviews interviews_zoom_id_key; Type: CONSTRAINT; Schema: public; Owner: staging_admin
--

ALTER TABLE ONLY interviews
    ADD CONSTRAINT interviews_zoom_id_key UNIQUE (zoom_id);


--
-- Name: reset_tokens reset_tokens_pkey; Type: CONSTRAINT; Schema: public; Owner: staging_admin
--

ALTER TABLE ONLY reset_tokens
    ADD CONSTRAINT reset_tokens_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: staging_admin
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: staging_admin
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_username_key UNIQUE (email);


--
-- Name: validation_tokens validation_tokens_pkey; Type: CONSTRAINT; Schema: public; Owner: staging_admin
--

ALTER TABLE ONLY validation_tokens
    ADD CONSTRAINT validation_tokens_pkey PRIMARY KEY (id);


--
-- Name: validation_tokens validation_tokens_token_key; Type: CONSTRAINT; Schema: public; Owner: staging_admin
--

ALTER TABLE ONLY validation_tokens
    ADD CONSTRAINT validation_tokens_token_key UNIQUE (token);


--
-- Name: video_users video_users_pkey; Type: CONSTRAINT; Schema: public; Owner: staging_admin
--

ALTER TABLE ONLY video_users
    ADD CONSTRAINT video_users_pkey PRIMARY KEY (id);


--
-- Name: videos videos_pkey; Type: CONSTRAINT; Schema: public; Owner: staging_admin
--

ALTER TABLE ONLY videos
    ADD CONSTRAINT videos_pkey PRIMARY KEY (id);


--
-- Name: videos videos_salesforce_id_key; Type: CONSTRAINT; Schema: public; Owner: staging_admin
--

ALTER TABLE ONLY videos
    ADD CONSTRAINT videos_salesforce_id_key UNIQUE (salesforce_id);


--
-- Name: videos videos_zoom_id_key; Type: CONSTRAINT; Schema: public; Owner: staging_admin
--

ALTER TABLE ONLY videos
    ADD CONSTRAINT videos_zoom_id_key UNIQUE (zoom_id);


--
-- Name: comments comments_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: staging_admin
--

ALTER TABLE ONLY comments
    ADD CONSTRAINT comments_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(id);


--
-- Name: comments comments_video_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: staging_admin
--

ALTER TABLE ONLY comments
    ADD CONSTRAINT comments_video_id_fkey FOREIGN KEY (video_id) REFERENCES videos(id);


--
-- Name: users users_cohort_fkey; Type: FK CONSTRAINT; Schema: public; Owner: staging_admin
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_cohort_fkey FOREIGN KEY (cohort) REFERENCES cohorts(id);


--
-- Name: video_users video_users_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: staging_admin
--

ALTER TABLE ONLY video_users
    ADD CONSTRAINT video_users_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;


--
-- Name: video_users video_users_video_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: staging_admin
--

ALTER TABLE ONLY video_users
    ADD CONSTRAINT video_users_video_id_fkey FOREIGN KEY (video_id) REFERENCES videos(id) ON DELETE CASCADE;


--
-- Name: videos videos_course_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: staging_admin
--

ALTER TABLE ONLY videos
    ADD CONSTRAINT videos_course_id_fkey FOREIGN KEY (course_id) REFERENCES courses(id);


--
-- Name: videos videos_host_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: staging_admin
--

ALTER TABLE ONLY videos
    ADD CONSTRAINT videos_host_id_fkey FOREIGN KEY (host_id) REFERENCES users(id);


--
-- Name: public; Type: ACL; Schema: -; Owner: staging_admin
--

REVOKE ALL ON SCHEMA public FROM rdsadmin;
REVOKE ALL ON SCHEMA public FROM PUBLIC;
GRANT ALL ON SCHEMA public TO staging_admin;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

