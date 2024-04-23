import mysql.connector
# Kết nối đến MySQL
db = mysql.connector.connect(user='root', password='123456', host='localhost')

# Tạo một đối tượng cursor
mycursor = db.cursor()
database_name = 'TEST1'
code = f"drop SCHEMA {database_name};"  
mycursor.execute(code)
# Commit thay đổi
db.commit()
# Đóng kết nối
db.close()
