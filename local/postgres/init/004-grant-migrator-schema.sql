\connect indexshelf

GRANT USAGE, CREATE ON SCHEMA public TO indexshelf_product_migrator;
GRANT USAGE ON SCHEMA public TO indexshelf_backend_runtime;

\connect indexshelf_data

GRANT USAGE, CREATE ON SCHEMA public TO indexshelf_data_migrator;
GRANT USAGE ON SCHEMA public TO indexshelf_data_runtime;
