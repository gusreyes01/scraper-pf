CREATE DATABASE scraper_pf;
CREATE USER scraper_pf WITH PASSWORD 'scraper_pf';
GRANT ALL PRIVILEGES ON DATABASE scraper_pf to scraper_pf;


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
