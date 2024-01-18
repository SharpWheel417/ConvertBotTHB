
-- Adminer 4.8.1 PostgreSQL 15.3 (Debian 15.3-1.pgdg120+1) dump

\connect "tg";

DROP TABLE IF EXISTS "state_data";
DROP SEQUENCE IF EXISTS state_data_id_seq;
CREATE SEQUENCE state_data_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."state_data" (
    "id" integer DEFAULT nextval('state_data_id_seq') NOT NULL,
    "text" text NOT NULL,
    "type" character(255) NOT NULL,
    CONSTRAINT "state_data_pkey" PRIMARY KEY ("id")
) WITH (oids = false);

INSERT INTO "state_data" ("id", "text", "type") VALUES
(1,	' Тест нового текста',	'logo                                                                                                                                                                                                                                                           ');

DROP TABLE IF EXISTS "users";
DROP SEQUENCE IF EXISTS users_id_seq;
CREATE SEQUENCE users_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."users" (
    "id" integer DEFAULT nextval('users_id_seq') NOT NULL,
    "name" character(255) NOT NULL,
    "chat_id" character(255) NOT NULL,
    "request" boolean DEFAULT false NOT NULL,
    CONSTRAINT "users_pkey" PRIMARY KEY ("id")
) WITH (oids = false);

INSERT INTO "users" ("id", "name", "chat_id", "request") VALUES
(9,	'Summer_Death                                                                                                                                                                                                                                                   ',	'1194700554                                                                                                                                                                                                                                                     ',	'f'),
(8,	'OxranaTrudaOnline                                                                                                                                                                                                                                              ',	'5480919609                                                                                                                                                                                                                                                     ',	't');

-- 2024-01-18 05:35:12.606239+00
