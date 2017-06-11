CREATE DATABASE scraper_pf;
CREATE USER scraper_pf WITH PASSWORD 'scraper_pf';
GRANT ALL PRIVILEGES ON DATABASE scraper_pf to scraper_pf;


CREATE TABLE dof (
    id serial primary key,
    date varchar(15) NOT NULL,
    notice varchar(80) NOT NULL,
    link varchar(200) NOT NULL,
    person_name varchar(80) NOT NULL,
    collected_at timestamptz NOT NULL DEFAULT now()
);


CREATE TABLE se (
    id serial primary key,
    publication varchar(120) NOT NULL,
    date varchar(15) NOT NULL,
    link varchar(200) NOT NULL,
    person_name varchar(80) NOT NULL,
    business_name varchar(120) NOT NULL,
    collected_at timestamptz NOT NULL DEFAULT now()
);
