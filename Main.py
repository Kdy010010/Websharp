import os
import mysql.connector
from bs4 import BeautifulSoup

# 초기 데이터베이스 설정
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'webpp_board'
}

variables = {}

def execute_webpp(filename):
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith('set'):
                var_name, var_value = line.split(' ')[1].split('=')
                set_variable(var_name, var_value)
            elif line.startswith('get'):
                var_name = line.split(' ')[1]
                print(get_variable(var_name))
            elif line.startswith('set_db_config'):
                set_db_config(line)
            elif line.startswith('makehtml'):
                params = line.split('(')[1].rstrip(')').split(')(')
                makehtml(params[0], params[1])
            elif line.startswith('makedir'):
                dirname = line.split('(')[1].rstrip(')')
                makedir(dirname)
            elif line.startswith('createfile'):
                params = line.split('(')[1].rstrip(')').split(')(')
                createfile(params[0], params[1])
            elif line.startswith('create_table'):
                create_table()
            elif line.startswith('insert_post'):
                params = line.split('(')[1].rstrip(')').split(',')
                insert_post(params[0].strip(), params[1].strip())
            elif line.startswith('list_posts'):
                list_posts()
            elif line.startswith('view_post'):
                post_id = line.split('(')[1].rstrip(')')
                view_post(post_id)

def set_variable(name, value):
    variables[name] = value

def get_variable(name):
    return variables.get(name, 'Variable not found')

def set_db_config(config_line):
    global db_config
    params = config_line.split(' ')[1].split(',')
    for param in params:
        key, value = param.split('=')
        db_config[key] = value
    print(f"Database configuration set: {db_config}")

def makehtml(filename, content):
    with open(filename, 'w') as file:
        file.write(content)
    print(f"Created HTML file: {filename}")

def makedir(dirname):
    if not os.path.exists(dirname):
        os.makedirs(dirname)
        print(f"Created directory: {dirname}")

def createfile(filepath, content):
    with open(filepath, 'w') as file:
        file.write(content)
    print(f"Created file: {filepath}")

def create_table():
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS posts (
                      id INT AUTO_INCREMENT PRIMARY KEY,
                      title VARCHAR(255),
                      content TEXT)''')
    db.commit()
    cursor.close()
    db.close()
    print("Table created successfully")

def insert_post(title, content):
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    cursor.execute("INSERT INTO posts (title, content) VALUES (%s, %s)", (title, content))
    db.commit()
    cursor.close()
    db.close()
    print("Post inserted successfully")

def list_posts():
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    cursor.execute("SELECT id, title FROM posts")
    for (post_id, title) in cursor:
        print(f"ID: {post_id}, Title: {title}")
    cursor.close()
    db.close()

def view_post(post_id):
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    cursor.execute("SELECT id, title, content FROM posts WHERE id = %s", (post_id,))
    for (id, title, content) in cursor:
        print(f"ID: {id}, Title: {title}, Content: {content}")
    cursor.close()
    db.close()

# Web++ 코드 파일 실행 예시
execute_webpp('example.webpp')
