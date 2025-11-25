{% macro grant_select_on_schemas(schemas, role) %}
  {% for schema in schemas %}
    grant usage on schema {{ schema }} to {{ role }};
    grant select on all tables in schema {{ schema }} to {{ role }};
    alter default privileges for role {{ role }}
      grant select on tables to {{ role }};
  {% endfor %}
{% endmacro %}
