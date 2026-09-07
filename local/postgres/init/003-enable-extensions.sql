\connect indexshelf
CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE EXTENSION IF NOT EXISTS citext;
CREATE EXTENSION IF NOT EXISTS vector;
REVOKE CREATE ON SCHEMA public FROM PUBLIC;
GRANT USAGE ON SCHEMA public TO indexshelf_backend_runtime;
GRANT USAGE, CREATE ON SCHEMA public TO indexshelf_product_migrator;
ALTER DEFAULT PRIVILEGES FOR ROLE indexshelf_product_owner IN SCHEMA public
  GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO indexshelf_backend_runtime;
ALTER DEFAULT PRIVILEGES FOR ROLE indexshelf_product_migrator
  GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO indexshelf_backend_runtime;
ALTER DEFAULT PRIVILEGES FOR ROLE indexshelf_product_migrator
  GRANT USAGE, SELECT ON SEQUENCES TO indexshelf_backend_runtime;

\connect indexshelf_data
REVOKE CREATE ON SCHEMA public FROM PUBLIC;
GRANT USAGE ON SCHEMA public TO indexshelf_data_runtime;
GRANT USAGE, CREATE ON SCHEMA public TO indexshelf_data_migrator;
ALTER DEFAULT PRIVILEGES FOR ROLE indexshelf_data_owner IN SCHEMA public
  GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO indexshelf_data_runtime;
ALTER DEFAULT PRIVILEGES FOR ROLE indexshelf_data_migrator
  GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO indexshelf_data_runtime;
ALTER DEFAULT PRIVILEGES FOR ROLE indexshelf_data_migrator
  GRANT USAGE, SELECT ON SEQUENCES TO indexshelf_data_runtime;
