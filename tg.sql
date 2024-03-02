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
(10,	'🟡 Тинькофф                                                                                                                                                                                                                                                     ',	'Tinkoff                                                                                                                                                                                                                                                        '),
(2,	'🟣 СБП                                                                                                                                                                                                                                                          ',	'SBP - Fast Bank Transfer                                                                                                                                                                                                                                       '),
(3,	'🟠 Райффайзенбанк                                                                                                                                                                                                                                               ',	'Raiffeisenbank                                                                                                                                                                                                                                                 '),
(4,	'🔴 Альфа банк                                                                                                                                                                                                                                                   ',	'Alfa-bank                                                                                                                                                                                                                                                      '),
(7,	'⚪️ Другие банки                                                                                                                                                                                                                                                ',	'another                                                                                                                                                                                                                                                        '),
(6,	'🟩 USDT                                                                                                                                                                                                                                                         ',	'USDT                                                                                                                                                                                                                                                           '),
(5,	'💵 Наличные                                                                                                                                                                                                                                                     ',	'cash                                                                                                                                                                                                                                                           ');

DROP TABLE IF EXISTS "orders";
DROP SEQUENCE IF EXISTS orders_id_seq1;
CREATE SEQUENCE orders_id_seq1 INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."orders" (
    "id" integer DEFAULT nextval('orders_id_seq1') NOT NULL,
    "num" text NOT NULL,
    "course" numeric NOT NULL,
    "need_bat" numeric NOT NULL,
    "need_rub" numeric NOT NULL,
    CONSTRAINT "orders_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


DROP TABLE IF EXISTS "state_data";
DROP SEQUENCE IF EXISTS state_data_id_seq;
CREATE SEQUENCE state_data_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."state_data" (
    "id" integer DEFAULT nextval('state_data_id_seq') NOT NULL,
    "text" text NOT NULL,
    "type" character(255) NOT NULL,
    "admin" boolean DEFAULT false NOT NULL,
    CONSTRAINT "state_data_pkey" PRIMARY KEY ("id")
) WITH (oids = false);

INSERT INTO "state_data" ("id", "text", "type", "admin") VALUES
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
А также ознакомиться с нашими отзывами ⤵️',	'logo                                                                                                                                                                                                                                                           ',	'f'),
(2,	'https://t.me/channel4exchange_thai/20',	'review_link                                                                                                                                                                                                                                                    ',	'f'),
(3,	'🤖 **Наш бот помогает подобрать для Вас наилучший курс в зависимости от объема, способа платежа и курса на бирже, в режиме реального времени, который автоматически обновляется ежеминутно** ⏳
*помните, что курс является приблизительным и согласовывается с оператором*

Если у Вас есть особые пожелания по сделке, времени и месту, а также по другим вопросам, Вы всегда можете обратиться к нашему оператору @operator4exchange

При заказе доставки наличных в Паттайя Вам необходимо сделать всего **4️⃣ шага** !

1️⃣ Разместить заказ внутри бота
2️⃣ Утвердить курс, время и место с оператором
3️⃣ Совершить обмен, перечислив оплату при личной встрече, и сразу забрать баты
4️⃣ Помочь нам в дальнейшем сотрудничестве, поставив отзыв


При желании оформления банковских счетов/оплаты зарубежных сервисов, недвижимости/оплаты сделки наличными рублями и доллорами, уточняйте актуальную информацию у опертора 🔔


А также, представляем Вам уникальное предложение: получайте наличные по всему Таиланду в банкоматах, даже не имея банковской карты!
🏧 Этот сервис предлагает возможность вывести деньги практически из любой точки страны, будь то аэропорт или отдаленный остров. Вот инструкция по использованию каждого из банкоматов:

🟦 [Bangkok Bank ATM - Синий банкомат](https://t.me/channel4exchange_thai/21)

🟨 [Krungsri Bank ATM - Желтый банкомат](https://t.me/channel4exchange_thai/22)

🟩 [Kasikorn Bank ATM - Зеленый банкомат](https://t.me/channel4exchange_thai/23)

🔹 [KrungThai Bank - Голубой банкомат](https://t.me/channel4exchange_thai/24)


Чтобы быстрее найти ближайший банкомат или сообщить курьеру свое местоположение, поделитесь с ботом геолокацией (не переживайте, мы не храним данную информацию, и о ней узнает только оператор-курьер) 📍

Это не сложно, на всех этапах оператор будет с Вами !

С уважением, команда 4EXCHANGE 🙌',	'info                                                                                                                                                                                                                                                           ',	'f'),
(4,	'Введите сумму, которая необходима для обмена в батах или выберите при помощи кнопок ⏬',	'hello_message                                                                                                                                                                                                                                                  ',	'f'),
(5,	'Привет, админ!',	'hello_message                                                                                                                                                                                                                                                  ',	't'),
(9,	'Ожидайте ответа оператора ⏱',	'send_geo                                                                                                                                                                                                                                                       ',	'f'),
(7,	'🏷️
Курс THB = {course_thb_rub} RUB 🇷🇺
Курс USDT = {course_thb_value} THB 🇹🇭

Чтобы точнее узнать курс выберите cумму, способ оплаты и нажмите разместить заказ, чтобы связаться с оператором',	'course                                                                                                                                                                                                                                                         ',	'f'),
(8,	'😄Введите предпочтительную Вам сумму в батах, например, 15756 ⬇️',	'my_sum                                                                                                                                                                                                                                                         ',	'f'),
(10,	'Теперь вы можете выбрать сумму',	'take_sum                                                                                                                                                                                                                                                       ',	'f'),
(11,	'💬 Ваш заказ взят в работу\nДалее диалог ведет оператор @operator4exchange \nВаш ID заказа: {order_id}\nЕсли вы закрыли сообщения для других пользователей или у вас нет username (@username), то напишите нашему оператору сами',	'take_order                                                                                                                                                                                                                                                     ',	'f'),
(12,	'✅ Ваш заказ размещен \n🧑‍💻 Оператор @operator4exchange скоро свяжется с вами \nА пока можете посмотреть, где ближайшие банкомат или просто сообщить курьеру где вы находитесь, отправив свое текущее местоположение 🌎\n\nЕсли вы закрыли сообщения для других пользователей или у вас нет username (@username), то напишите нашему оператору сами',	'request_user                                                                                                                                                                                                                                                   ',	'f');

DROP TABLE IF EXISTS "user_marje";
DROP SEQUENCE IF EXISTS user_marje_id_seq;
CREATE SEQUENCE user_marje_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."user_marje" (
    "id" integer DEFAULT nextval('user_marje_id_seq') NOT NULL,
    "count" integer NOT NULL,
    "marje" integer NOT NULL,
    CONSTRAINT "user_marje_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


DROP TABLE IF EXISTS "user_state";
DROP SEQUENCE IF EXISTS state_id_seq;
CREATE SEQUENCE state_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."user_state" (
    "id" integer DEFAULT nextval('state_id_seq') NOT NULL,
    "chat_id" character(255) NOT NULL,
    "state" character(255),
    "bat" character(255),
    "complete" character(255),
    CONSTRAINT "chat_id_unique_idx" UNIQUE ("chat_id"),
    CONSTRAINT "state_pkey" PRIMARY KEY ("id")
) WITH (oids = false);

INSERT INTO "user_state" ("id", "chat_id", "state", "bat", "complete") VALUES
(1,	'1194700554                                                                                                                                                                                                                                                     ',	'0                                                                                                                                                                                                                                                              ',	'0                                                                                                                                                                                                                                                              ',	NULL),
(10,	'6908096537                                                                                                                                                                                                                                                     ',	'ожидание_выбора_способа_оплаты                                                                                                                                                                                                                                 ',	'0                                                                                                                                                                                                                                                              ',	NULL);

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
(4,	'ssk1722                                                                                                                                                                                                                                                        ',	'747612773                                                                                                                                                                                                                                                      ',	't'),
(3,	'Summer_Death                                                                                                                                                                                                                                                   ',	'1194700554                                                                                                                                                                                                                                                     ',	'f'),
(5,	'operator4exchange                                                                                                                                                                                                                                              ',	'6920037183                                                                                                                                                                                                                                                     ',	'f'),
(6,	'OxranaTrudaOnline                                                                                                                                                                                                                                              ',	'5480919609                                                                                                                                                                                                                                                     ',	't'),
(8,	'Xd                                                                                                                                                                                                                                                             ',	'6908096537                                                                                                                                                                                                                                                     ',	't'),
(7,	'NEVINOVEN700                                                                                                                                                                                                                                                   ',	'5794240411                                                                                                                                                                                                                                                     ',	't');

-- 2024-03-02 04:04:48.647175+00
