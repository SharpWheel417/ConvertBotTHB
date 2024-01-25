-- Adminer 4.8.1 PostgreSQL 16.1 (Debian 16.1-1.pgdg120+1) dump

\connect "tg";

DROP TABLE IF EXISTS "banks";
DROP SEQUENCE IF EXISTS banks_id_seq;
CREATE SEQUENCE banks_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."banks" (
    "id" integer DEFAULT nextval('banks_id_seq') NOT NULL,
    "rus" character(255) NOT NULL,
    "eng" character(255) NOT NULL,
    CONSTRAINT "banks_pkey" PRIMARY KEY ("id")
) WITH (oids = false);

INSERT INTO "banks" ("id", "rus", "eng") VALUES
(0,	'🟢Сбербанк                                                                                                                                                                                                                                                      ',	'Sberbank                                                                                                                                                                                                                                                       '),
(2,	'🟢СБП                                                                                                                                                                                                                                                           ',	'SBP - Fast Bank Transfer                                                                                                                                                                                                                                       '),
(4,	'🔴Альфа-Банк                                                                                                                                                                                                                                                    ',	'Alfa-bank                                                                                                                                                                                                                                                      '),
(1,	'🟡Тинькофф                                                                                                                                                                                                                                                      ',	'Tinkoff                                                                                                                                                                                                                                                        '),
(3,	'🟡Райфайзен                                                                                                                                                                                                                                                     ',	'Raiffeisenbank                                                                                                                                                                                                                                                 '),
(5,	'💶Наличные                                                                                                                                                                                                                                                      ',	'cash                                                                                                                                                                                                                                                           '),
(6,	'🏧USDT                                                                                                                                                                                                                                                          ',	'USDT                                                                                                                                                                                                                                                           '),
(7,	'💵Другие банки                                                                                                                                                                                                                                                  ',	'another                                                                                                                                                                                                                                                        ');

DROP TABLE IF EXISTS "orders";
DROP SEQUENCE IF EXISTS orders_id_seq;
CREATE SEQUENCE orders_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."orders" (
    "id" integer DEFAULT nextval('orders_id_seq') NOT NULL,
    "username" character(255) NOT NULL,
    "admin_pay" real NOT NULL,
    "user_pay" real NOT NULL,
    "course_rub" real NOT NULL,
    "course_thb" real NOT NULL,
    "marje" real NOT NULL,
    "trade_method" character(255) NOT NULL,
    "gain" real NOT NULL,
    "review" text,
    "mark" integer,
    "completed" character(255) NOT NULL,
    "date" timestamp,
    "ids" character(255),
    "user_bat" real NOT NULL,
    "user_usdt" real NOT NULL,
    CONSTRAINT "orders_pkey" PRIMARY KEY ("id")
) WITH (oids = false);

INSERT INTO "orders" ("id", "username", "admin_pay", "user_pay", "course_rub", "course_thb", "marje", "trade_method", "gain", "review", "mark", "completed", "date", "ids", "user_bat", "user_usdt") VALUES
(4,	'OxranaTrudaOnline                                                                                                                                                                                                                                              ',	12794.94,	13212.03,	2.56,	143.47,	1.01,	'🟢Сбербанк                                                                                                                                                                                                                                                      ',	417.09,	NULL,	NULL,	'cancle                                                                                                                                                                                                                                                         ',	'2024-01-24 15:33:51.035664',	'aa641803-00d5-468f-9c35-fbc3855d78ab                                                                                                                                                                                                                           ',	5000,	10),
(1,	'OxranaTrudaOnline                                                                                                                                                                                                                                              ',	51179.78,	52709.03,	2.56,	573.86,	1.01,	'🟢Сбербанк                                                                                                                                                                                                                                                      ',	1529.25,	'Круто',	5,	'complete                                                                                                                                                                                                                                                       ',	'2024-01-24 11:35:03.757179',	'8dbb53aa-21c0-4a43-ac3f-507c24c84da9                                                                                                                                                                                                                           ',	20000,	10),
(3,	'ssk1722                                                                                                                                                                                                                                                        ',	38384.83,	42738.06,	2.56,	464.49,	1.01,	'💶Наличные                                                                                                                                                                                                                                                      ',	4353.23,	NULL,	NULL,	'complete                                                                                                                                                                                                                                                       ',	'2024-01-24 15:22:22.590515',	'c30dae1b-1546-4e61-bb11-6029022d397c                                                                                                                                                                                                                           ',	15000,	10),
(2,	'OxranaTrudaOnline                                                                                                                                                                                                                                              ',	51179.78,	52732.21,	2.56,	573.86,	1.01,	'🟢СБП                                                                                                                                                                                                                                                           ',	1552.43,	NULL,	5,	'complete                                                                                                                                                                                                                                                       ',	'2024-01-24 11:35:41.894301',	'97ed311c-b7fb-4a72-9f34-62db71290961                                                                                                                                                                                                                           ',	20000,	10),
(5,	'OxranaTrudaOnline                                                                                                                                                                                                                                              ',	12794.94,	13212.03,	2.56,	143.47,	1.01,	'🟢Сбербанк                                                                                                                                                                                                                                                      ',	417.09,	NULL,	5,	'complete                                                                                                                                                                                                                                                       ',	'2024-01-24 15:34:18.604554',	'64f371af-ba3d-4cb4-9e14-845b33282484                                                                                                                                                                                                                           ',	5000,	10),
(7,	'ssk1722                                                                                                                                                                                                                                                        ',	25589.17,	26900,	2.69,	288.1,	1.025,	'🟢Сбербанк 93.32                                                                                                                                                                                                                                                ',	1310.83,	NULL,	5,	'complete                                                                                                                                                                                                                                                       ',	'2024-01-24 21:19:49.398943',	'13924b54-5df5-45df-a250-774e5ae9aec5                                                                                                                                                                                                                           ',	10000,	10),
(8,	'ssk1722                                                                                                                                                                                                                                                        ',	25561.88,	26800,	2.68,	287.77,	1.025,	'🟢Сбербанк 93.17                                                                                                                                                                                                                                                ',	1238.12,	NULL,	NULL,	'request                                                                                                                                                                                                                                                        ',	'2024-01-24 21:56:23.761058',	'184e2ae8-8535-4c69-b971-7394761892d0                                                                                                                                                                                                                           ',	10000,	10),
(9,	'ssk1722                                                                                                                                                                                                                                                        ',	25548.98,	26800,	2.68,	287.6,	1.025,	'🟢Сбербанк 93.34                                                                                                                                                                                                                                                ',	1251.02,	NULL,	NULL,	'request                                                                                                                                                                                                                                                        ',	'2024-01-24 22:18:08.332819',	'620875a8-fa33-4895-99b2-c674f2c35f78                                                                                                                                                                                                                           ',	10000,	10),
(10,	'ssk1722                                                                                                                                                                                                                                                        ',	25548.98,	28200,	2.82,	295.25,	1.025,	'💶Наличные 95.66                                                                                                                                                                                                                                                ',	2651.02,	NULL,	NULL,	'complete                                                                                                                                                                                                                                                       ',	'2024-01-24 22:18:44.10409',	'4eb7b653-7b9a-489b-bab0-0182216ad64b                                                                                                                                                                                                                           ',	10000,	10),
(6,	'ssk1722                                                                                                                                                                                                                                                        ',	25588.45,	26871.59,	2.56,	288.09,	1.025,	'🟢Сбербанк 91.0                                                                                                                                                                                                                                                 ',	1283.14,	NULL,	NULL,	'complete                                                                                                                                                                                                                                                       ',	'2024-01-24 20:50:14.518564',	'159fb84f-3a40-47a6-8a26-1353d3396846                                                                                                                                                                                                                           ',	10000,	10);

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
(1,	'Вас приветствует обменник 4exchange 💸

Честный, быстрый, надёжный партнер в сфере конвертации и обмена любой популярной валюты и криптовалюты 🔐

Совершите обмен в 4 шага: 
1️⃣ Автоматический расчет курса внутри бота 
2️⃣ Утверждение сделки с оператором 
3️⃣ Доставка курьера 
4️⃣ Честный обмен 

Вы можете оплатить любым удобным Вам способом и получить тайские баты:

🛵 Курьерской доставкой в Паттайя
💳 На тайскую карту 
🏧 В любом ближайшем банкомате 
💰 Оплатить недвижимость, транспорт, оформить документы и банковские счета 

PS: Курс рассчитывается автоматически и зависит от способа оплаты и объема обмена, а также биржевого курса, поэтому можете мониторить курс в течении дня. Не стесняйтесь пользоваться ботом, менять способы оплаты и размещать заказы, ведь обмен можно отменить на любом этапе, до утверждения сделки с оператором. Подробнее о процессе вы можете узнать на кнопке информации ⤵️ 
А также ознакомиться с нашими отзывами ⤵️

Введите сумму, которая необходима для обмена в батах или выберите при помощи кнопок ⏬',	'logo                                                                                                                                                                                                                                                           '),
(2,	'https://t.me/channel4exchange_thai/20',	'review_link                                                                                                                                                                                                                                                    ');

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
(1,	'Summer_Death                                                                                                                                                                                                                                                   ',	'1194700554                                                                                                                                                                                                                                                     ',	'f'),
(2,	'OxranaTrudaOnline                                                                                                                                                                                                                                              ',	'5480919609                                                                                                                                                                                                                                                     ',	't'),
(4,	'operator4exchange                                                                                                                                                                                                                                              ',	'6920037183                                                                                                                                                                                                                                                     ',	'f'),
(5,	'NEVINOVEN700                                                                                                                                                                                                                                                   ',	'5794240411                                                                                                                                                                                                                                                     ',	'f'),
(3,	'ssk1722                                                                                                                                                                                                                                                        ',	'747612773                                                                                                                                                                                                                                                      ',	't');

-- 2024-01-25 08:28:46.027885+00
