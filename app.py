import tkinter as tk
from tkinter import messagebox
import sqlite3

# Conectar ao banco de dados
conn = sqlite3.connect("finance.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        description TEXT,
        amount REAL
    )
""")
conn.commit()

# Função para adicionar receita ou despesa
def add_transaction():
    description = description_entry.get()
    amount = amount_entry.get()
    
    if description == "" or amount == "":
        messagebox.showwarning("Erro", "Preencha todos os campos!")
        return
    
    try:
        amount = float(amount)
    except ValueError:
        messagebox.showwarning("Erro", "Digite um valor numérico válido!")
        return
    
    cursor.execute("INSERT INTO transactions (description, amount) VALUES (?, ?)", (description, amount))
    conn.commit()
    update_balance()
    description_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)

# Função para calcular e atualizar o saldo
def update_balance():
    cursor.execute("SELECT SUM(amount) FROM transactions")
    balance = cursor.fetchone()[0]
    balance = balance if balance is not None else 0
    balance_label.config(text=f"Saldo Atual: R$ {balance:.2f}")
    update_transaction_list()

# Função para exibir a lista de transações
def update_transaction_list():
    transaction_list.delete(0, tk.END)
    cursor.execute("SELECT description, amount FROM transactions")
    for desc, amount in cursor.fetchall():
        transaction_list.insert(tk.END, f"{desc}: R$ {amount:.2f}")

# Criando a interface gráfica
root = tk.Tk()
root.title("Gerenciador Financeiro")
root.geometry("400x400")

# Rótulos e campos de entrada
tk.Label(root, text="Descrição:").pack()
description_entry = tk.Entry(root)
description_entry.pack()

tk.Label(root, text="Valor (use negativo para despesas):").pack()
amount_entry = tk.Entry(root)
amount_entry.pack()

# Botão para adicionar transação
tk.Button(root, text="Adicionar", command=add_transaction).pack()

# Exibição do saldo
balance_label = tk.Label(root, text="Saldo Atual: R$ 0.00", font=("Arial", 12, "bold"))
balance_label.pack()

# Lista de transações
transaction_list = tk.Listbox(root)
transaction_list.pack(expand=True, fill=tk.BOTH)

# Atualizar saldo inicial
update_balance()

# Executando a aplicação
root.mainloop()

# Fechar conexão ao encerrar
conn.close()
