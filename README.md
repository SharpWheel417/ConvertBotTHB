


# Fast Start

### CONFIG

Не забудьте создать файл config.py и в переменную положить api ключ от вашего бота
----

###  Устанавливаете все нужные библиотеки

``` pip install python-telegram-bot ```

``` pip install schedule ```

``` pip install selenium ```

```pip install web-driver ```

```pip install psycopg2-binary ```

-------------

### Гайд по установке web-driver для ubuntu

https://tecadmin.net/setup-selenium-with-python-on-ubuntu-debian/

Ниже три команды, которые нужны для установки веб-драйвера

```wget -nc https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb```

```sudo apt update```

```sudo apt install -f ./google-chrome-stable_current_amd64.deb```

------

### Запускаете бота

``` python bot.py```

# ВАЖНО

Чтобы после отключения от сервера процесс продолжар работать запустите бота вот таким способом

``` nohup python bot.py & ```

nohup так же создаст файл в директории запуска ```nohup.out```
Там будут лежать логи вашего процесса

Чтобы отключить процесс

``` ps aux | grep bot.py ```

```kill 12345```
