#!/bin/bash

function init_database {
    # Create schemas
    PGPASSWORD=$DB_ADMIN_PWD psql -U $DB_ADMIN_USER -h $DB_HOST -d $DB_NAME -p $DB_CONTAINER_PORT \
    -c "DROP SCHEMA IF EXISTS public;" \
    -c "CREATE SCHEMA IF NOT EXISTS $APP_SCHEMA;"
    
    # Create USERS
    PGPASSWORD=$DB_ADMIN_PWD psql -U $DB_ADMIN_USER -h $DB_HOST -d $DB_NAME -p $DB_CONTAINER_PORT \
    -c "CREATE USER $DB_DATA_USER PASSWORD '$DB_DATA_PWD';" \
    -c "CREATE USER $DB_APP_USER PASSWORD '$DB_APP_PWD';"

    # Grants / PRIVILEGES
    PGPASSWORD=$DB_ADMIN_PWD psql -U $DB_ADMIN_USER -h $DB_HOST -d $DB_NAME -p $DB_CONTAINER_PORT \
    -c "GRANT USAGE ON SCHEMA $APP_SCHEMA TO $DB_DATA_USER;" \
    -c "GRANT SELECT, INSERT, UPDATE, DELETE, TRUNCATE ON ALL TABLES IN SCHEMA $APP_SCHEMA TO $DB_DATA_USER;" \
    -c "GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA $APP_SCHEMA TO $DB_DATA_USER;" \
    -c "GRANT EXECUTE ON ALL PROCEDURES IN SCHEMA $APP_SCHEMA TO $DB_DATA_USER;" \
    -c "ALTER DEFAULT PRIVILEGES IN SCHEMA $APP_SCHEMA GRANT SELECT, INSERT, UPDATE, DELETE, TRUNCATE ON TABLES TO $DB_DATA_USER;" \
    -c "ALTER DEFAULT PRIVILEGES IN SCHEMA $APP_SCHEMA GRANT EXECUTE ON FUNCTIONS TO $DB_DATA_USER;" \
    -c "GRANT USAGE ON SCHEMA $APP_SCHEMA TO $DB_APP_USER;" \
    -c "ALTER DEFAULT PRIVILEGES IN SCHEMA $APP_SCHEMA GRANT SELECT ON TABLES TO $DB_APP_USER;" \
    -c "ALTER DEFAULT PRIVILEGES IN SCHEMA $APP_SCHEMA GRANT EXECUTE ON FUNCTIONS TO $DB_APP_USER;"
}


function migrate_database {
    flyway \
    -url=jdbc:postgresql://${DB_HOST}:${DB_CONTAINER_PORT}/${DB_NAME} \
    -user=${DB_ADMIN_USER} \
    -password=${DB_ADMIN_PWD} \
    -locations="filesystem:/ops/sql" \
    -createSchemas=false \
    -schemas=${APP_CODE} \
    migrate
}


function clean_database {
    flyway \
    -url=jdbc:postgresql://${DB_HOST}:${DB_CONTAINER_PORT}/${DB_NAME} \
    -user=${DB_ADMIN_USER} \
    -password=${DB_ADMIN_PWD} \
    -locations="filesystem:/ops/sql" \
    -createSchemas=false \
    -schemas=${APP_CODE} \
    clean -outputType=json
}


function repair_database {
    flyway \
    -url=jdbc:postgresql://${DB_HOST}:${DB_CONTAINER_PORT}/${DB_NAME} \
    -user=${DB_ADMIN_USER} \
    -password=${DB_ADMIN_PWD} \
    -locations="filesystem:/ops/sql" \
    -createSchemas=false \
    -schemas=${APP_CODE} \
    repair -outputType=json
}

echo "db deploy start"
echo "- sleep 3 seconds for db to start"
sleep 3

APP_SCHEMA=${APP_CODE}
DB_ADMIN_USER="${APP_CODE}_admin"
DB_DATA_USER="${APP_CODE}_data"
DB_APP_USER="${APP_CODE}_app"
DB_HOST="${APP_CODE}-postgres"
DB_NAME="db_${APP_CODE}"

# use clean_database during development to reset flyway
echo "- Init DB"
init_database
# clean_database
# repair_database
echo "- Migrate DB"
migrate_database
echo "db deploy complete"
