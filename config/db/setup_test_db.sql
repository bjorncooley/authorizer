CREATE DATABASE authorizer_test;
CREATE ROLE authorizer_admin WITH LOGIN PASSWORD 'default';
CREATE SCHEMA IF NOT EXISTS authorizer_schema AUTHORIZATION authorizer_admin;
GRANT ALL PRIVILEGES ON SCHEMA authorizer_schema to authorizer_admin;
