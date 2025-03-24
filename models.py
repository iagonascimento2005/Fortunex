class Transaction:
    """Representa uma transação financeira."""

    def __init__(self, date, description, amount, type):
        """Inicializa uma transação.

        Args:
            date (str): Data da transação.
            description (str): Descrição da transação.
            amount (float): Valor da transação.
            type (str): Tipo da transação (Receita/Despesa).

        Raises:
            ValueError: Se o valor for negativo ou o tipo for inválido.
        """
        if amount < 0:
            raise ValueError("O valor da transação não pode ser negativo.")
        if type not in ["Receita", "Despesa"]:
            raise ValueError("Tipo de transação inválido. Deve ser 'Receita' ou 'Despesa'.")

        self.date = date
        self.description = description
        self.amount = amount
        self.type = type