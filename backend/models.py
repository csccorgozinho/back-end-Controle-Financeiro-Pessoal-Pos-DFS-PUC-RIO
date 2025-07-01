import sqlite3

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Tabela de usuários
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL
        )
    ''')

    # Tabela de gastos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS gastos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_usuario INTEGER,
            categoria TEXT NOT NULL,
            valor REAL NOT NULL,
            data TEXT NOT NULL,
            FOREIGN KEY(id_usuario) REFERENCES usuarios(id)
        )
    ''')

    conn.commit()
    conn.close()

def get_connection():
    return sqlite3.connect('database.db')
