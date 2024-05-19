from abc import ABC, abstractmethod

class Account:
    def __init__(self,client, numberAc) -> None:
        self._blnc = 0
        self._numberAc = numberAc
        self._agency = "0001"
        self._client = client
        self._history = History()

    @property
    def history(self):
        return self._history 
 
    @property
    def blnc(self):
        return self._blnc

    @property
    def numberAc(self):
        return self._numberAc

    @property
    def agency(self):
        return self._agency
    
    @blnc.setter
    def blnc(self, value):
        self._blnc += value

    @classmethod
    def new_account(cls, client, numberAc):
        return cls(client, numberAc) 

    def withdraw(self, value):
        blnc = self._blnc

        exceeded_balance = value > blnc

        print("-----------------------")

        if exceeded_balance:
            print("you dont have enough balance")
        elif value > 0:
            self.blnc = -value
            print(f"Sucessful Withdrawl. Amount Drawn: {value}")
            print(f"Your balance: {self.blnc}")
            return True
        else:
            print("Invalid Value.")
        return False
    

    def deposit(self, value):

        if value > 0:
            self.blnc = value
            print(f"Sucessful Deposit. Amount deposited: {value}")
            print(f"Your balance: {self.blnc}")
            return True
        else:
            print("Invalid Value")
            return False
      
class CurrentAccount(Account):
    def __init__(self, client, numberAc, LIMIT = 500, withdrawal_limit = 3) -> None:
        super().__init__(client, numberAc)
        self.limit = LIMIT
        self.withdraw_limit = withdrawal_limit
        
    def withdraw(self, value):
        number_withdrawals = len([transaction for transaction in self._history.transactions if transaction["type"] == Withdrawal.__name__])

        exceeded_limit = value > self.limit
        exceeded_withdrawals = number_withdrawals > self.withdraw_limit

        if exceeded_limit:
            print("You can't withdraw. Exceeded Limit. Your limit: 500")
        elif exceeded_withdrawals:
            print("You can't withdraw. Exceeded Number of withdrawals. Your limit = 3 withdrawals")
        else:
            super().withdraw(value)
            return True
        return False
    
    def __str__(self) -> str:
        return f"""
            agencia:\t {self.agency}
            conta:\t {self.numberAc}
            titular:\t {self._client._name}
"""
    
class Transaction(ABC):
    @property
    @abstractmethod
    def value(self):
        pass

    @abstractmethod
    def register_transaction(self, account):
        pass

class Withdrawal(Transaction):
    def __init__(self, value) -> None:
        self._value = value

    @property
    def value(self):
        return self._value


    def register_transaction(self, account):
        sucess = account.withdraw(self.value)
        if sucess:
            account.history.add_transaction(self)
        
class Deposit(Transaction):
    def __init__(self, value) -> None:
        self._value = value

    @property
    def value(self):
        return self._value


    def register_transaction(self, account):
        sucess = account.deposit(self.value)
        if sucess:
            account.history.add_transaction(self)
        
class History:
    def __init__(self) -> None:
        self._transactions = []
    
    @property
    def transactions(self):
        return self._transactions
    
    def add_transaction(self, transaction):
        self._transactions.append(
            {
                "type": transaction.__class__.__name__,
                "value": transaction.value
            }
        ) 

class Client:
    def __init__(self, address) -> None:
        self.accounts = []
        self.address = address


    def do_transaction(self, account, transaction):
        transaction.register_transaction(account)

    def add_account(self,account):
        self.accounts.append(account)

class NaturalPerson(Client):
    def __init__(self,address, cpf, name, date_birth) -> None:
        super().__init__(address)
        self.cpf = cpf
        self.name = name
        self.date_birth = date_birth


#part 2

def menu():
    print('''

[d] Deposit
[w] withdraw
[s] Bank Statement
[na] New Account
[nc] New client
[q] Quit

>: ''')
    op = input()
    return op


def filter_client(cpf, clients):
    clients_filtered = [client for client in clients if client.cpf == cpf]
    return clients_filtered[0] if clients_filtered else None

def recovery_client_account(client):
    if not client.accounts:
        print("Client dont have account.")
        return
    return client.accounts[0]

def deposit(clients):
    cpf = input("CPF: ")
    client = filter_client(cpf, clients)

    if not client:
        print("Client not found.")
        return
    
    value = float(input("Deposit amount: "))
    transaction = Deposit(value)

    account = recovery_client_account(client)
    if not account: 
        return
    
    client.do_transaction(account, transaction)


def withdrawal(clients):
    cpf = input("CPF: ")
    client = filter_client(cpf, clients)

    if not client:
        print("Client not found.")
        return
    
    value = float(input("Withdraw amount: "))
    transaction = Withdrawal(value)

    account = recovery_client_account(client)
    if not account: 
        return
    client.do_transaction(account, transaction)


def show_statememt(clients):
    cpf = input("CPF: ")
    client = filter_client(cpf, clients)

    if not client:
        print("Client not found.")
        return
    
    account = recovery_client_account(client)
    if not account: 
        return
    
    print("BANK STATEMENT")
    transactions = account.history.transactions
    statement = ""

    if not transactions:
        print("No bank transactions were carried out")
    else:
        for transaction in transactions:
            statement += f"\n{transaction['type']} \n{transaction['value']}"
    print(f"{statement}\nBalance: {account.blnc}")

def create_client(clients):
    cpf = input("CPF: ")
    client = filter_client(cpf, clients)

    if client:
        print("Client already exists.")
        return
    
    name = input("Name: ")
    date_birth = input("Date of birth: ")
    address = input("address: ")

    client = NaturalPerson(name=name, date_birth=date_birth, cpf=cpf, address= address)

    clients.append(client)

    print("Client created sucessfully")
    

def create_account(numberAc, clients, accounts):
    cpf = input("CPF: ")
    client = filter_client(cpf, clients)
    
    if not client:
        print("client not found. ")
        return
    
    account = CurrentAccount.new_account(client=client, numberAc=numberAc)

    accounts.append(account)
    client.accounts.append(account)
    print("Account created sucessfully")





def main():
    clients = []
    accounts = []

    while True:
        op = menu()

        if op == "d":
            deposit(clients)

        elif op == "w":
            withdrawal(clients)
    
        elif op == "s":
            show_statememt(clients)

        elif op == "na":
            numberAc= len(accounts)
            create_account(numberAc,clients, accounts)

        elif op == "nc":
            create_client(clients)

        elif op == "q":
            break
        
        else:
            print("Invalid Operation.")

main()