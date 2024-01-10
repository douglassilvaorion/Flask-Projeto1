import psycopg2

DB_NAME = "flask_db"
DB_USER = "postgres"
DB_PASS = "123456"
DB_HOST = "localhost"
DB_PORT = "5432"
 
conn = psycopg2.connect(database=DB_NAME,
                        user=DB_USER,
                        password=DB_PASS,
                        host=DB_HOST,
                        port=DB_PORT)
print("Database connected successfully")
 
cur = conn.cursor()  # creating a cursor
 
# executing queries to create table
cur.execute("""
CREATE TABLE Employee
(
    ID INT   PRIMARY KEY NOT NULL,
    NAME TEXT NOT NULL,
    EMAI TEXT NOT NULL
)
""")
 
# commit the changes
conn.commit()
print("Table Created successfully")