import pymysql
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import app
from datetime import datetime

class User(UserMixin):
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
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
            cursor.execute(sql, (username, email, hashed_password))
        conn.commit()
        conn.close()

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Reservation:
    def __init__(self, id, user_id, date, time, status):
        self.id = id
        self.user_id = user_id
        self.date = date
        self.time = time
        self.status = status

    @staticmethod
    def create(user_id, date, time):
        conn = get_db_connection()
        with conn.cursor() as cursor:
            sql = "INSERT INTO reservations (user_id, date, time, status) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (user_id, date, time, 'pending'))
        conn.commit()
        conn.close()

    @staticmethod
    def get_by_user(user_id):
        conn = get_db_connection()
        with conn.cursor() as cursor:
            sql = "SELECT * FROM reservations WHERE user_id = %s"
            cursor.execute(sql, (user_id,))
            reservations = cursor.fetchall()
        conn.close()
        return [Reservation(r['id'], r['user_id'], r['date'], r['time'], r['status']) for r in reservations]

    @staticmethod
    def get_available_slots(date):
        conn = get_db_connection()
        with conn.cursor() as cursor:
            sql = """
            SELECT time FROM 
            (SELECT TIME_FORMAT(MAKETIME(hour, 0, 0), '%H:%i') AS time 
             FROM (SELECT 0 AS hour UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9 UNION SELECT 10 UNION SELECT 11 UNION SELECT 12 UNION SELECT 13 UNION SELECT 14 UNION SELECT 15 UNION SELECT 16 UNION SELECT 17 UNION SELECT 18 UNION SELECT 19 UNION SELECT 20 UNION SELECT 21 UNION SELECT 22 UNION SELECT 23) hours) all_slots
            WHERE time NOT IN (SELECT time FROM reservations WHERE date = %s)
            """
            cursor.execute(sql, (date,))
            available_slots = cursor.fetchall()
        conn.close()
        return [slot['time'] for slot in available_slots]

    def cancel(self):
        conn = get_db_connection()
        with conn.cursor() as cursor:
            sql = "UPDATE reservations SET status = 'cancelled' WHERE id = %s"
            cursor.execute(sql, (self.id,))
        conn.commit()
        conn.close()
        self.status = 'cancelled'
    @staticmethod
    def get_by_id(id):
        conn = get_db_connection()
        with conn.cursor() as cursor:
            sql = "SELECT * FROM reservations WHERE id = %s"
            cursor.execute(sql, (id,))
            reservation = cursor.fetchone()
        conn.close()
        if reservation:
            return Reservation(reservation['id'], reservation['user_id'], reservation['date'], reservation['time'], reservation['status'])
        return None
    @staticmethod
    def get_by_user(user_id):
        conn = get_db_connection()
        with conn.cursor() as cursor:
            sql = "SELECT * FROM reservations WHERE user_id = %s"
            cursor.execute(sql, (user_id,))
            reservations = cursor.fetchall()
        conn.close()
        return [Reservation(r['id'], r['user_id'], r['date'], r['time'], r['status']) for r in reservations]

def get_db_connection():
    return pymysql.connect(
        host=app.config['DB_HOST'],
        user=app.config['DB_USER'],
        password=app.config['DB_PASSWORD'],
        db=app.config['DB_NAME'],
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
