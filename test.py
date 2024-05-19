class Transaction():
    def __init__(self, description, type, amount):
        self.type = type
        self.description = description
        self.amount = amount
    
    def __str__(self):
        output = f"TRANSACTION\n  {self.description}\n  {self.amount}\n  {self.type}"
        return output

class Account():
    def __init__(self, name, cpf):
        self.name = name
        self.cpf = cpf
        self.balance = 0.0
        self.transactions = []
    
    def deposit(self, transaction):
        self.balance += transaction.amount
        self.transactions.append(transaction)
    
    def withdraw(self, transaction):
        self.balance -= transaction.amount
        self.transactions.append(transaction)

    def __str__(self):
        output = f"{self.name}\n{self.balance}\n{self.transactions}"
        return output


accounts = {}

while True:
    choice = input("> ")
    if choice == "create":
        name = input("Name: ")
        cpf = input("CPF: ")
        accounts[cpf] = Account(name, cpf)
    if choice == "deposit":
        cpf = input("CPF: ")
        account = accounts[cpf]
        account.deposit(Transaction("X", "income", 10))
    if choice == "withdraw":
        cpf = input("CPF: ")
        account = accounts[cpf]
        account.withdraw(Transaction("Y", "expense", 10))
    if choice == "show":
        cpf = input("CPF: ")
        account = accounts[cpf]
        for t in account.transactions:
            print(t)
        
