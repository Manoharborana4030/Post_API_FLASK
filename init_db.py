import os
import psycopg2

conn = psycopg2.connect(
        host="localhost",
        database="flask_redis_database",
        user=os.environ['DB_USERNAME'],
        password=os.environ['DB_PASSWORD'])

# Open a cursor to perform database operations
cur = conn.cursor()

# Execute a command: this creates a new table

# cur.execute('DROP TABLE IF EXISTS users;')
# cur.execute('CREATE TABLE users (id serial PRIMARY KEY,'
#                                  'username varchar (30) NOT NULL,'
#                                  'email varchar (30) NOT NULL,'
#                                  'password varchar (100) NOT NULL,' 
#                                  'fname varchar (25) NOT NULL,'
#                                  'lname varchar (25) NOT NULL,'
#                                  'OTP numeric,'
#                                  'address varchar (250) NOT NULL,'
#                                  'date_added date DEFAULT CURRENT_TIMESTAMP);'
#                                  )



cur.execute('DROP TABLE IF EXISTS Access_token;')
cur.execute('CREATE TABLE Access_token (id serial PRIMARY KEY,'
                                 'username varchar (30) NOT NULL,'
                                 'token varchar (300) NOT NULL,'
                                 'date_added date DEFAULT CURRENT_TIMESTAMP);'
                                 )

# Insert data into the table

# cur.execute('INSERT INTO users (username, email, password, fname, lname, address)'
#             'VALUES (%s, %s, %s, %s, %s, %s)',
#             ('manoharborana',
#              'manohar.borana@yudiz.com',
#              'Manohar@123',
#              'Manohar',
#              'Borana',
#              '4922/Vikashnagar,Gota, Ahmedabad, Gujarat')
#             )

conn.commit()

cur.close()
conn.close()