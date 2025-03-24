import sqlite3

def create_connection(db_file):
    """Cria uma conexão com o banco de dados SQLite.

    Args:
        db_file (str): Caminho para o arquivo do banco de dados.

    Returns:
        sqlite3.Connection: Objeto de conexão com o banco de dados.
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Conectado ao banco de dados SQLite: {db_file}")
    except sqlite3.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
    return conn

def create_table(conn):
    """Cria a tabela de transações financeiras.

    Args:
        conn (sqlite3.Connection): Objeto de conexão com o banco de dados.
    """
    sql_create_transactions_table = """CREATE TABLE IF NOT EXISTS transactions (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        date TEXT NOT NULL,
                                        description TEXT NOT NULL,
                                        amount REAL NOT NULL,
                                        type TEXT NOT NULL
                                    );"""
    try:
        c = conn.cursor()
        c.execute(sql_create_transactions_table)
        conn.commit()
    except sqlite3.Error as e:
        print(f"Erro ao criar tabela: {e}")
        conn.rollback()

def insert_transaction(conn, transaction):
    """Insere uma nova transação no banco de dados.

    Args:
        conn (sqlite3.Connection): Objeto de conexão com o banco de dados.
        transaction (tuple): Tupla contendo (date, description, amount, type).

    Returns:
        int: ID da transação inserida.
    """
    sql = '''INSERT INTO transactions(date, description, amount, type)
             VALUES(?, ?, ?, ?)'''
    try:
        cur = conn.cursor()
        cur.execute(sql, transaction)
        conn.commit()
        return cur.lastrowid
    except sqlite3.Error as e:
        print(f"Erro ao inserir transação: {e}")
        conn.rollback()
        return None

def fetch_transactions(conn):
    """Recupera todas as transações do banco de dados.

    Args:
        conn (sqlite3.Connection): Objeto de conexão com o banco de dados.

    Returns:
        list: Lista de transações.
    """
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM transactions")
        return cur.fetchall()
    except sqlite3.Error as e:
        print(f"Erro ao recuperar transações: {e}")
        return []

def update_transaction(conn, transaction_id, date, description, amount, type):
    """Atualiza uma transação existente.

    Args:
        conn (sqlite3.Connection): Objeto de conexão com o banco de dados.
        transaction_id (int): ID da transação a ser atualizada.
        date (str): Nova data da transação.
        description (str): Nova descrição da transação.
        amount (float): Novo valor da transação.
        type (str): Novo tipo da transação (Receita/Despesa).
    """
    sql = '''UPDATE transactions
            SET date = ?, description = ?, amount = ?, type = ?
            WHERE id = ?'''
    try:
        cur = conn.cursor()
        cur.execute(sql, (date, description, amount, type, transaction_id))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Erro ao atualizar transação: {e}")
        conn.rollback()

def delete_transaction(conn, transaction_id):
    """Remove uma transação do banco de dados.

    Args:
        conn (sqlite3.Connection): Objeto de conexão com o banco de dados.
        transaction_id (int): ID da transação a ser removida.
    """
    sql = '''DELETE FROM transactions WHERE id = ?'''
    try:
        cur = conn.cursor()
        cur.execute(sql, (transaction_id,))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Erro ao remover transação: {e}")
        conn.rollback()