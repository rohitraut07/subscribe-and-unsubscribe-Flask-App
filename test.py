import psycopg2
conn = psycopg2.connect(host="localhost", database="postgres", user="postgres",password="3366")
print(conn)