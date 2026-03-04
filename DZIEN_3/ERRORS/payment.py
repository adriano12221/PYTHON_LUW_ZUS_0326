import datetime

class PaymentError(Exception):

    def __init__(self, message, amount, balance, account_id):
        super().__init__(message)
        self.amount = amount
        self.balance = balance
        self.account_id = account_id
        self.timestamp = datetime.datetime.now()

    def diagnostic_report(self):
        return (
            f"\n--- PAYMENT ERROR REPORT ---\n"
            f"Account ID: {self.account_id}\n"
            f"Attempted Amount: {self.amount}\n"
            f"Avaliable Balance: {self.balance}\n"
            f"Time: {self.timestamp}\n"
            f"Message: {self.args[0]}"
        )

class BankAccount:

    def __init__(self, account_id, balance):
        self.account_id = account_id
        self.balance = balance

    def pay(self,amount):
        if amount <= 0:
            raise PaymentError(
                "Invalid amount",
                amount,
                self.balance,
                self.account_id
            )
        if amount > self.balance:
            raise PaymentError(
                "Insufficient funds",
                amount,
                self.balance,
                self.account_id
            )

        self.balance -= amount
        print(f"Payment of {amount} successful")

acc = BankAccount("ACC-6435", 10000)

try:
    acc.pay(-112300)
except PaymentError as e:
    print(e.diagnostic_report())
