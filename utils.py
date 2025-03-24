import pandas as pd
import matplotlib.pyplot as plt

def generate_report(transactions):
    """Gera um relatório financeiro com base nas transações.

    Args:
        transactions (list): Lista de transações.
    """
    df = pd.DataFrame(transactions, columns=["ID", "Date", "Description", "Amount", "Type"])
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)

    # Relatório de resumo
    summary = df.groupby('Type')['Amount'].sum()
    print("Resumo Financeiro:")
    print(summary)

    # Gráfico de evolução ao longo do tempo
    df.resample('M')['Amount'].sum().plot(kind='line', title="Evolução Financeira Mensal")
    plt.xlabel("Data")
    plt.ylabel("Valor")
    plt.show()

    # Gráfico de pizza de receitas vs despesas
    df.groupby('Type')['Amount'].sum().plot(kind='pie', autopct='%1.1f%%', title="Distribuição de Receitas e Despesas")
    plt.show()