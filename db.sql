BEGIN;

CREATE DATABASE scraper_pf;
CREATE USER scraper_pf WITH PASSWORD 'scraper_pf';
GRANT ALL PRIVILEGES ON DATABASE scraper_pf to scraper_pf;
COMMIT;


BEGIN;
CREATE TABLE agentes (
  id INTEGER primary key NOT NULL,
  orden INTEGER NOT NULL,
  name varchar(120) NOT NULL
);

CREATE TABLE sipres (
  id serial primary key,
  institution varchar(512) NOT NULL,
  collected_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE fp_sancionados (
  id serial primary key,
  name varchar(255) NOT NULL,
  url varchar(255) NOT NULL,
  collected_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE council_sancionados (
  id serial primary key,
  description TEXT NOT NULL,
  type varchar(15) NOT NULL,
  url varchar(512) NULL,
  collected_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE logs (
  id serial primary key,
  execution_date timestamptz NOT NULL,
  new_records INTEGER NOT NULL,
  execution_time DECIMAL NOT NULL,
  execution_code INTEGER NOT NULL,
  agent_id INTEGER NOT NULL
);

CREATE TABLE scraper (
  id serial primary key,
  header varchar(255) NULL,
  url varchar(512) NOT NULL,
  body varchar(512) NULL,
  visible BOOLEAN NOT NULL DEFAULT true,
  alerta BOOLEAN NOT NULL DEFAULT false,
  created timestamptz NOT NULL DEFAULT now(),
  fuente_id INTEGER NOT NULL,
  persona_fisica_id INTEGER NULL,
  persona_moral_id INTEGER NULL,
  report_id INTEGER NULL
);


INSERT INTO agentes(id, orden, name) VALUES (1, 1, 'Banco Interamericano de Desarrollo');
INSERT INTO agentes(id, orden, name) VALUES (2, 2, 'Sanctions List - OFAC');
INSERT INTO agentes(id, orden, name) VALUES (3, 3, 'Secretaría de la Función Pública');
INSERT INTO agentes(id, orden, name) VALUES (4, 6, 'Buho Legal');
INSERT INTO agentes(id, orden, name) VALUES (5, 7, 'Profeco');
INSERT INTO agentes(id, orden, name) VALUES (6, 8, 'Secretaría de Economía');
INSERT INTO agentes(id, orden, name) VALUES (7, 9, 'Diario Oficial de la Federación');
INSERT INTO agentes(id, orden, name) VALUES (8, 10, 'IMPI');
INSERT INTO agentes(id, orden, name) VALUES (9, 11, 'Registro de Prestadores de Servicios Financieros');
INSERT INTO agentes(id, orden, name) VALUES (10, 12, 'INAI - Portal de Obligaciones de Transparencia');
INSERT INTO agentes(id, orden, name) VALUES (11, 13, 'Registro Único de Garantías Inmobiliarias');
INSERT INTO agentes(id, orden, name) VALUES (12, 14, 'Búsqueda de Funcionarios Públicos Federales');
INSERT INTO agentes(id, orden, name) VALUES (13, 16, 'United Nations List');
INSERT INTO agentes(id, orden, name) VALUES (14, 17, 'European Sanction List');
INSERT INTO agentes(id, orden, name) VALUES (15, 18, 'Consolidated Screening List');
INSERT INTO agentes(id, orden, name) VALUES (16, 19, 'Google');

COMMIT;