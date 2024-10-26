import datetime
import mysql.connector as mysql
from flask import Flask, request

app = Flask(__name__)

def get_db_connection():
    try:
        return mysql.connect(
            host="db",
            user="USER",
            passwd="PWD",
            database="TEST_DB"
        )
    except mysql.Error as err:
        print(f"Ошибка при подключении к базе данных: {err}")
        return None

def create_table():
    db = get_db_connection()
    if db:
        mycursor = db.cursor()
        drop_query = "DROP TABLE IF EXISTS TEST_TABLE"
        mycursor.execute(drop_query)
        create_query = f'''
            CREATE TABLE TEST_TABLE (
                id INT AUTO_INCREMENT PRIMARY KEY,
                datetime DATETIME,
                client_info TEXT
            );
        '''
        mycursor.execute(create_query)
        db.commit()
        mycursor.close()
        db.close()

@app.route('/')
def hello():
    user_agent = request.headers.get('User-Agent')
    current_datetime = datetime.datetime.now()
    db = get_db_connection()
    if db:
        mycursor = db.cursor()

        insertQuery = f'''
        INSERT INTO TEST_TABLE (datetime, client_info)
        VALUES (%s, %s)
        '''
        mycursor.execute(insertQuery, (current_datetime, user_agent))
        db.commit()  

        last_id = mycursor.lastrowid  # Получаем ID последней вставленной строки

        mycursor.close()
        db.close()

        data = [
            {'id': last_id, 'datetime': current_datetime.strftime("%Y-%m-%d %H:%M:%S"), 'user-agent': user_agent}
        ]

        html = '<table border="1">'
        html += '<thead><tr><th>ID</th><th>Время</th><th>User-Agent</th></tr></thead>'
        html += '<tbody>'
        for row in data:
            html += f'<tr><td>{row["id"]}</td><td>{row["datetime"]}</td><td>{row["user-agent"]}</td></tr>'
        html += '</tbody>'
        html += '</table>'
        return html
    else:
        return "Ошибка подключения к базе данных."

if __name__ == '__main__':
    create_table() # Создаем таблицу при запуске
    app.run(host='0.0.0.0', port = 5001)