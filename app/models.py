import pymysql
from werkzeug.security import generate_password_hash, check_password_hash

class User:
    def __init__(self, id, username, email, password_hash):
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = password_hash

    @staticmethod
    def get_by_id(user_id):
        conn = get_db_connection()
        with conn.cursor() as cursor:
            sql = "SELECT * FROM users WHERE id = %s"
            cursor.execute(sql, (user_id,))
            user = cursor.fetchone()
        conn.close()
        if user:
            return User(user['id'], user['username'], user['email'], user['password_hash'])
        return None

    @staticmethod
    def get_by_email(email):
        conn = get_db_connection()
        with conn.cursor() as cursor:
            sql = "SELECT * FROM users WHERE email = %s"
            cursor.execute(sql, (email,))
            user = cursor.fetchone()
        conn.close()
        if user:
            return User(user['id'], user['username'], user['email'], user['password_hash'])
        return None

    @staticmethod
    def create(username, email, password):
        conn = get_db_connection()
        with conn.cursor() as cursor:
            sql = "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)"
            cursor.execute(sql, (username, email, generate_password_hash(password)))
        conn.commit()
        conn.close()

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

def get_db_connection():
    return pymysql.connect(
        host=app.config['DB_HOST'],
        user=app.config['DB_USER'],
        password=app.config['DB_PASSWORD'],
        db='eventos',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )