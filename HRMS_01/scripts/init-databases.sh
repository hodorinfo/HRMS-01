#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE identity_db;
    CREATE DATABASE core_db;
    CREATE DATABASE attendance_db;
    CREATE DATABASE payroll_db;
    CREATE DATABASE permission_db;
    CREATE DATABASE talent_db;
    CREATE DATABASE platform_db;
EOSQL
