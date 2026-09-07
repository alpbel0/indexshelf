CREATE ROLE indexshelf_product_owner NOLOGIN;
CREATE ROLE indexshelf_product_migrator LOGIN PASSWORD 'indexshelf_product_migrator_dummy';
CREATE ROLE indexshelf_backend_runtime LOGIN PASSWORD 'indexshelf_backend_runtime_dummy';
CREATE ROLE indexshelf_data_owner NOLOGIN;
CREATE ROLE indexshelf_data_migrator LOGIN PASSWORD 'indexshelf_data_migrator_dummy';
CREATE ROLE indexshelf_data_runtime LOGIN PASSWORD 'indexshelf_data_runtime_dummy';

ALTER DATABASE indexshelf OWNER TO indexshelf_product_owner;
ALTER DATABASE indexshelf_data OWNER TO indexshelf_data_owner;

REVOKE CONNECT ON DATABASE indexshelf FROM PUBLIC;
REVOKE CONNECT ON DATABASE indexshelf_data FROM PUBLIC;
GRANT CONNECT ON DATABASE indexshelf TO indexshelf_product_migrator, indexshelf_backend_runtime;
GRANT CONNECT ON DATABASE indexshelf_data TO indexshelf_data_migrator, indexshelf_data_runtime;
GRANT CREATE ON DATABASE indexshelf TO indexshelf_product_migrator;
GRANT CREATE ON DATABASE indexshelf_data TO indexshelf_data_migrator;
