import customtkinter as ctk
from tkinter import ttk
import pandas as pd
from tkcalendar import DateEntry
from controllers import FinancialController
from tkinter import messagebox
from datetime import datetime

# Configuração da janela principal
ctk.set_appearance_mode("light")  # Tema claro
ctk.set_default_color_theme("blue")

class FinanceDashboard(ctk.CTk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("Dashboard Financeiro")
        self.geometry("800x500")
        
        # Frame superior - Resumo financeiro
        self.frame_resumo = ctk.CTkFrame(self)
        self.frame_resumo.pack(fill='x', padx=10, pady=5)
        
        # Ordem desejada: Saldo, Receita, Despesa
        self.lbl_saldo = ctk.CTkLabel(self.frame_resumo, text="Saldo: R$ 0,00", font=("Arial", 14, "bold"))
        self.lbl_saldo.pack(side='left', padx=20)
        
        self.lbl_receitas = ctk.CTkLabel(self.frame_resumo, text="Receitas: R$ 0,00", font=("Arial", 14, "bold"))
        self.lbl_receitas.pack(side='left', padx=20)
        
        self.lbl_despesas = ctk.CTkLabel(self.frame_resumo, text="Despesas: R$ 0,00", font=("Arial", 14, "bold"))
        self.lbl_despesas.pack(side='left', padx=20)
        
        # Frame de filtros
        self.frame_filtros = ctk.CTkFrame(self)
        self.frame_filtros.pack(fill='x', padx=10, pady=5)
        
        self.lbl_filtro = ctk.CTkLabel(self.frame_filtros, text="Filtrar por data:")
        self.lbl_filtro.pack(side='left', padx=5)
        
        self.entry_data = DateEntry(self.frame_filtros, date_pattern='dd/mm/yyyy')
        self.entry_data.pack(side='left', padx=5)
        
        self.btn_filtrar = ctk.CTkButton(self.frame_filtros, text="Filtrar", command=self.filtrar_transacoes)
        self.btn_filtrar.pack(side='left', padx=5)
        
        # Botão para limpar o filtro
        self.btn_limpar_filtro = ctk.CTkButton(self.frame_filtros, text="Limpar Filtro", command=self.limpar_filtro)
        self.btn_limpar_filtro.pack(side='left', padx=5)
        
        # Frame principal - Tabela de transações
        self.frame_tabela = ctk.CTkFrame(self)
        self.frame_tabela.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Definindo as colunas na ordem desejada: Tipo, Data, Descrição, Valor, ID
        self.tree = ttk.Treeview(self.frame_tabela, columns=("Tipo", "Data", "Descrição", "Valor", "ID"), show='headings')
        self.tree.heading("Tipo", text="Tipo")
        self.tree.heading("Data", text="Data")
        self.tree.heading("Descrição", text="Descrição")
        self.tree.heading("Valor", text="Valor")
        self.tree.heading("ID", text="ID")
        
        self.tree.pack(fill='both', expand=True)
        
        # Frame inferior - Botões de ação
        self.frame_botoes = ctk.CTkFrame(self)
        self.frame_botoes.pack(fill='x', padx=10, pady=5)
        
        self.btn_adicionar = ctk.CTkButton(self.frame_botoes, text="Adicionar", command=self.adicionar_transacao)
        self.btn_adicionar.pack(side='left', padx=5)
        
        self.btn_editar = ctk.CTkButton(self.frame_botoes, text="Editar", command=self.editar_transacao)
        self.btn_editar.pack(side='left', padx=5)
        
        self.btn_remover = ctk.CTkButton(self.frame_botoes, text="Remover", command=self.remover_transacao)
        self.btn_remover.pack(side='left', padx=5)
        
        # Atualiza a tabela e o resumo financeiro ao iniciar
        self.update_transactions_list()
        self.update_resumo()

    def update_transactions_list(self, transactions=None):
        """Atualiza a lista de transações na tabela."""
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        # Se nenhuma lista de transações for passada, busca todas as transações
        if transactions is None:
            transactions = self.controller.get_transactions()
        
        for transaction in transactions:
            # Inserindo os valores na ordem correta: Tipo, Data, Descrição, Valor, ID
            self.tree.insert("", "end", values=(transaction[4], transaction[1], transaction[2], f"R$ {transaction[3]:.2f}", transaction[0]))

    def update_resumo(self, transactions=None):
        """Atualiza o resumo financeiro (saldo, receitas e despesas)."""
        if transactions is None:
            df = self.controller.get_transactions_dataframe()
        else:
            df = pd.DataFrame(transactions, columns=["id", "date", "description", "amount", "type"])
        
        if not df.empty:
            receitas = df[df['type'] == 'Receita']['amount'].sum()
            despesas = df[df['type'] == 'Despesa']['amount'].sum()
            saldo = receitas - despesas
            
            # Atualiza os labels na ordem desejada: Saldo, Receitas, Despesas
            self.lbl_saldo.configure(text=f"Saldo: R$ {saldo:.2f}")
            self.lbl_receitas.configure(text=f"Receitas: R$ {receitas:.2f}")
            self.lbl_despesas.configure(text=f"Despesas: R$ {despesas:.2f}")
        else:
            self.lbl_saldo.configure(text="Saldo: R$ 0,00")
            self.lbl_receitas.configure(text="Receitas: R$ 0,00")
            self.lbl_despesas.configure(text="Despesas: R$ 0,00")

    def filtrar_transacoes(self):
        """Filtra as transações por data."""
        data_filtro = self.entry_data.get()
        try:
            # Converte a data do filtro para o formato YYYY-MM-DD
            data_filtro_formatada = datetime.strptime(data_filtro, "%d/%m/%Y").strftime("%Y-%m-%d")
            
            # Recupera todas as transações
            transactions = self.controller.get_transactions()
            
            # Filtra as transações pela data selecionada
            transacoes_filtradas = [t for t in transactions if t[1] == data_filtro_formatada]
            
            # Atualiza a tabela e o resumo com as transações filtradas
            self.update_transactions_list(transacoes_filtradas)
            self.update_resumo(transacoes_filtradas)
        except ValueError:
            messagebox.showerror("Erro", "Data inválida! Use o formato DD/MM/AAAA.")

    def limpar_filtro(self):
        """Limpa o filtro e exibe todas as transações."""
        self.update_transactions_list()
        self.update_resumo()

    def adicionar_transacao(self):
        """Abre uma janela para adicionar uma nova transação."""
        add_window = ctk.CTkToplevel(self)
        add_window.title("Adicionar Transação")
        add_window.geometry("400x300")
        
        # Data
        ctk.CTkLabel(add_window, text="Data:").grid(row=0, column=0, padx=5, pady=5)
        date_entry = DateEntry(add_window, date_pattern='dd/mm/yyyy')
        date_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Descrição
        ctk.CTkLabel(add_window, text="Descrição:").grid(row=1, column=0, padx=5, pady=5)
        description_entry = ctk.CTkEntry(add_window)
        description_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Valor
        ctk.CTkLabel(add_window, text="Valor:").grid(row=2, column=0, padx=5, pady=5)
        amount_entry = ctk.CTkEntry(add_window)
        amount_entry.grid(row=2, column=1, padx=5, pady=5)
        
        # Tipo (Receita/Despesa)
        type_var = ctk.StringVar(value="Receita")
        ctk.CTkRadioButton(add_window, text="Receita", variable=type_var, value="Receita").grid(row=3, column=0, padx=5, pady=5)
        ctk.CTkRadioButton(add_window, text="Despesa", variable=type_var, value="Despesa").grid(row=3, column=1, padx=5, pady=5)
        
        # Botão para salvar a transação
        ctk.CTkButton(add_window, text="Salvar", command=lambda: self.salvar_transacao(
            date_entry.get(),
            description_entry.get(),
            amount_entry.get(),
            type_var.get(),
            add_window
        )).grid(row=4, column=0, columnspan=2, padx=5, pady=5)

    def salvar_transacao(self, date, description, amount, type, window):
        """Salva a nova transação."""
        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("Erro", "Digite um valor válido!")
            return
        
        self.controller.add_transaction(date, description, amount, type)
        self.update_transactions_list()
        self.update_resumo()
        window.destroy()

    def editar_transacao(self):
        """Abre uma janela para editar a transação selecionada."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Erro", "Selecione uma transação para editar!")
            return
        
        # Obtém o ID da transação selecionada diretamente da tabela
        transaction_id = self.tree.item(selected_item, "values")[4]  # ID está na última coluna
        
        # Recupera a transação correspondente ao ID
        transactions = self.controller.get_transactions()
        transaction = next((t for t in transactions if t[0] == int(transaction_id)), None)
        
        if not transaction:
            messagebox.showerror("Erro", "Transação não encontrada!")
            return
        
        # Janela de edição
        edit_window = ctk.CTkToplevel(self)
        edit_window.title("Editar Transação")
        edit_window.geometry("400x300")
        
        # Preenche os campos com os dados atuais
        ctk.CTkLabel(edit_window, text="Data:").grid(row=0, column=0, padx=5, pady=5)
        date_entry = DateEntry(edit_window, date_pattern='dd/mm/yyyy')
        date_entry.set_date(transaction[1])
        date_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ctk.CTkLabel(edit_window, text="Descrição:").grid(row=1, column=0, padx=5, pady=5)
        description_entry = ctk.CTkEntry(edit_window)
        description_entry.insert(0, transaction[2])
        description_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ctk.CTkLabel(edit_window, text="Valor:").grid(row=2, column=0, padx=5, pady=5)
        amount_entry = ctk.CTkEntry(edit_window)
        amount_entry.insert(0, str(transaction[3]))
        amount_entry.grid(row=2, column=1, padx=5, pady=5)
        
        type_var = ctk.StringVar(value=transaction[4])
        ctk.CTkRadioButton(edit_window, text="Receita", variable=type_var, value="Receita").grid(row=3, column=0, padx=5, pady=5)
        ctk.CTkRadioButton(edit_window, text="Despesa", variable=type_var, value="Despesa").grid(row=3, column=1, padx=5, pady=5)
        
        # Botão para salvar as alterações
        ctk.CTkButton(edit_window, text="Salvar", command=lambda: self.salvar_edicao(
            transaction_id,
            date_entry.get(),
            description_entry.get(),
            amount_entry.get(),
            type_var.get(),
            edit_window
        )).grid(row=4, column=0, columnspan=2, padx=5, pady=5)

    def salvar_edicao(self, transaction_id, date, description, amount, type, window):
        """Salva as alterações da transação editada."""
        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("Erro", "Digite um valor válido!")
            return
        
        self.controller.update_transaction(transaction_id, date, description, amount, type)
        self.update_transactions_list()
        self.update_resumo()
        window.destroy()

    def remover_transacao(self):
        """Remove a transação selecionada."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Erro", "Selecione uma transação para remover!")
            return
        
        # Obtém o ID da transação selecionada diretamente da tabela
        transaction_id = self.tree.item(selected_item, "values")[4]  # ID está na última coluna
        
        self.controller.delete_transaction(transaction_id)
        self.update_transactions_list()
        self.update_resumo()