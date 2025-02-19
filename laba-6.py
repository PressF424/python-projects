class BankAccount:
    def __init__(self, accountNumber: str, balance: float = 0.0):
        if balance < 0:
            raise ValueError("баланс не может быть отрицательным.")
        self.accountNumber = accountNumber
        self.balance = balance

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("сумма пополнения должна быть больше нуля.")
        self.balance += amount

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("сумма вывода должна быть больше нуля.")
        if amount > self.balance:
            raise ValueError("недостаточно средств.")
        self.balance -= amount

    def getBalance(self) -> float:
        return self.balance

# юнит тесты классы
import unittest

class TestBankAccount(unittest.TestCase):
    def test_create_account_with_valid_balance(self):
        account = BankAccount("123456", 100.0)
        self.assertEqual(account.getBalance(), 100.0)

    def test_create_account_with_negative_balance(self):
        with self.assertRaises(ValueError) as context:
            BankAccount("123456", -50.0)
        self.assertEqual(str(context.exception), "баланс не может быть отрицательным.")

    def test_deposit_valid_amount(self):
        account = BankAccount("123456", 100.0)
        account.deposit(50.0)
        self.assertEqual(account.getBalance(), 150.0)

    def test_deposit_zero_or_negative_amount(self):
        account = BankAccount("123456", 100.0)
        with self.assertRaises(ValueError) as context:
            account.deposit(0)
        self.assertEqual(str(context.exception), "сумма пополнения должна быть больше нуля.")

        with self.assertRaises(ValueError) as context:
            account.deposit(-10.0)
        self.assertEqual(str(context.exception), "сумма пополнения должна быть больше нуля.")

    def test_withdraw_valid_amount(self):
        account = BankAccount("123456", 100.0)
        account.withdraw(50.0)
        self.assertEqual(account.getBalance(), 50.0)

    def test_withdraw_more_than_balance(self):
        account = BankAccount("123456", 100.0)
        with self.assertRaises(ValueError) as context:
            account.withdraw(150.0)
        self.assertEqual(str(context.exception), "недостаточно средств.")

    def test_withdraw_zero_or_negative_amount(self):
        account = BankAccount("123456", 100.0)
        with self.assertRaises(ValueError) as context:
            account.withdraw(0)
        self.assertEqual(str(context.exception), "сумма вывода должна быть больше нуля.")

        with self.assertRaises(ValueError) as context:
            account.withdraw(-10.0)
        self.assertEqual(str(context.exception), "сумма вывода должна быть больше нуля.")

    def test_balance_after_operations(self):
        account = BankAccount("123456", 200.0)
        account.deposit(100.0)
        account.withdraw(50.0)
        self.assertEqual(account.getBalance(), 250.0)

if __name__ == '__main__':
    unittest.main()

# ============================= ПРИМЕР ВЫВОДА ПРОГРАММЫ =============================
# collecting ... collected 8 items
#
# laba-6.py::TestBankAccount::test_balance_after_operations PASSED         [ 12%]
# laba-6.py::TestBankAccount::test_create_account_with_negative_balance PASSED [ 25%]
# laba-6.py::TestBankAccount::test_create_account_with_valid_balance PASSED [ 37%]
# laba-6.py::TestBankAccount::test_deposit_valid_amount PASSED             [ 50%]
# laba-6.py::TestBankAccount::test_deposit_zero_or_negative_amount PASSED  [ 62%]
# laba-6.py::TestBankAccount::test_withdraw_more_than_balance PASSED       [ 75%]
# laba-6.py::TestBankAccount::test_withdraw_valid_amount PASSED            [ 87%]
# laba-6.py::TestBankAccount::test_withdraw_zero_or_negative_amount PASSED [100%]
#
# ============================== ПРИМЕРНОЕ ВРЕМЯ 8 ТЕСТОВ ЗА 0.03с ==============================