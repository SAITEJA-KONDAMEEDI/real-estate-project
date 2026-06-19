import pymysql

conn = pymysql.connect(
    host='dbserversai.mysql.database.azure.com',
    user='azsqladmin',
    password='Saiteja@2002',
    database='real_estate',
    ssl={'ssl': True}
)

cursor = conn.cursor()

data = [
    ('Andhra Pradesh', 'Tirupati', 'Tirupati Urban', 15000, 13.6288, 79.4192),
    ('Andhra Pradesh', 'Tirupati', 'Chandragiri', 8000, 13.5833, 79.3167),
    ('Andhra Pradesh', 'Tirupati', 'Srikalahasti', 6000, 13.7500, 79.6989),
    ('Andhra Pradesh', 'Krishna', 'Vijayawada Urban', 18000, 16.5062, 80.6480),
    ('Andhra Pradesh', 'Guntur', 'Guntur Urban', 12000, 16.3067, 80.4365),
    ('Telangana', 'Hyderabad', 'Secunderabad', 25000, 17.4399, 78.4983),
    ('Telangana', 'Hyderabad', 'Kukatpally', 22000, 17.4849, 78.3953),
    ('Telangana', 'Rangareddy', 'Shamshabad', 12000, 17.2543, 78.4017),
]

cursor.executemany('''
    INSERT INTO land_rates (state, district, mandal, rate, latitude, longitude)
    VALUES (%s, %s, %s, %s, %s, %s)
''', data)

conn.commit()
print(f"Inserted {cursor.rowcount} records successfully!")
cursor.close()
conn.close()
