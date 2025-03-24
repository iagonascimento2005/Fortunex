from database import create_connection, insert_transaction, fetch_transactions, update_transaction, delete_transaction, create_table
import pandas as pd

class FinancialController:
    """Controlador para gerenciar transações financeiras."""

    def __init__(self, db_file):
        """Inicializa o controlador com uma conexão ao banco de dados.

        Args:
            db_file (str): Caminho para o arquivo do banco de dados.
        """
        self.conn = create_connection(db_file)
        if self.conn is not None:
            create_table(self.conn)
        else:
            print("Erro ao conectar ao banco de dados.")

    def add_transaction(self, date, description, amount, type):
        """Adiciona uma nova transação.

        Args:
            date (str): Data da transação.
            description (str): Descrição da transação.
            amount (float): Valor da transação.
            type (str): Tipo da transação (Receita/Despesa).

        Returns:
            int: ID da transação inserida.
        """
        try:
            amount = float(amount)
            if amount < 0:
                raise ValueError("O valor da transação não pode ser negativo.")
            transaction = (date, description, amount, type)
            return insert_transaction(self.conn, transaction)
        except ValueError as e:
            print(f"Erro ao adicionar transação: {e}")
            return None

    def get_transactions(self):
        """Recupera todas as transações.

        Returns:
            list: Lista de transações.
        """
        return fetch_transactions(self.conn)

    def update_transaction(self, transaction_id, date, description, amount, type):
        """Atualiza uma transação existente.

        Args:
            transaction_id (int): ID da transação a ser atualizada.
            date (str): Nova data da transação.
            description (str): Nova descrição da transação.
            amount (float): Novo valor da transação.
            type (str): Novo tipo da transação (Receita/Despesa).
        """
        try:
            amount = float(amount)
            if amount < 0:
                raise ValueError("O valor da transação não pode ser negativo.")
            update_transaction(self.conn, transaction_id, date, description, amount, type)
        except ValueError as e:
            print(f"Erro ao atualizar transação: {e}")

    def delete_transaction(self, transaction_id):
        """Remove uma transação.

        Args:
            transaction_id (int): ID da transação a ser removida.
        """
        delete_transaction(self.conn, transaction_id)

    def get_transactions_dataframe(self):
        """Retorna as transações como um DataFrame do Pandas.

        Returns:
            pd.DataFrame: DataFrame contendo as transações.
        """
        transactions = self.get_transactions()
        df = pd.DataFrame(transactions, columns=["id", "date", "description", "amount", "type"])
        return df

    def get_balance(self):
        """Calcula o saldo total.

        Returns:
            float: Saldo total.
        """
        df = self.get_transactions_dataframe()
        if not df.empty:
            receitas = df[df['type'] == 'Receita']['amount'].sum()
            despesas = df[df['type'] == 'Despesa']['amount'].sum()
            return receitas - despesas
        return 0.0

    def get_total_income(self):
        """Calcula o total de receitas.

        Returns:
            float: Total de receitas.
        """
        df = self.get_transactions_dataframe()
        if not df.empty:
            return df[df['type'] == 'Receita']['amount'].sum()
        return 0.0

    def get_total_expenses(self):
        """Calcula o total de despesas.

        Returns:
            float: Total de despesas.
        """
        df = self.get_transactions_dataframe()
        if not df.empty:
            return df[df['type'] == 'Despesa']['amount'].sum()
        return 0.0