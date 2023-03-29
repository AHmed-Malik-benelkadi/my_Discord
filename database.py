import mysql.connector

class Database:
    def __init__(self, host, user, password, db_name):
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        self.cursor = self.conn.cursor()

    def create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                                    id INT AUTO_INCREMENT PRIMARY KEY,
                                    username VARCHAR(255),
                                    full_name VARCHAR(255),
                                    email VARCHAR(255) UNIQUE,
                                    password VARCHAR(255))''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS channels (
                                    id INT AUTO_INCREMENT PRIMARY KEY,
                                    name VARCHAR(255) UNIQUE)''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS messages (
                                    id INT AUTO_INCREMENT PRIMARY KEY,
                                    channel_id INT,
                                    user_id INT,
                                    content TEXT,
                                    timestamp DATETIME,
                                    FOREIGN KEY(channel_id) REFERENCES channels(id),
                                    FOREIGN KEY(user_id) REFERENCES users(id))''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS user_channels (
                                    user_id INT,
                                    channel_id INT,
                                    FOREIGN KEY(user_id) REFERENCES users(id),
                                    FOREIGN KEY(channel_id) REFERENCES channels(id),
                                    UNIQUE(user_id, channel_id))''')

        self.conn.commit()

    def close(self):
        self.conn.close()

if __name__ == "__main__":
    # Remplacez ces valeurs par vos propres informations de connexion à la base de données MySQL
    db = Database(host="localhost", user="root", password="Kiko2002=", db_name="my_discord")
    db.create_tables()
    db.close()
