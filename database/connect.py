import psycopg2
import datetime

conn = None
cur = None

conn = psycopg2.connect(
host="localhost",
port=5432,
database="tg",
user="admin",
password="admin")

cur = conn.cursor()