class Bank:
    def __init__(self) -> None:
        self.account = int(input("Enter the Account Number: "))
        self.name = input("Enter the name: ")
        self.balance = 0

    def show_info(self):
        print(f"Account Number is {self.account}")
        print(f"Name is {self.name}")
        print(f"Balance is {self.balance}\n")

    def show_balance(self) -> None:
        print(f" Current Balance={self.balance}")

    def withdraw(self) -> None:
        amount = int(input("Enter the withdraw amount: "))
        if amount > self.balance:
            print("Insufficient Balance")
        else:
            self.balance -= amount
            print("Withdrawal successful")

    def deposit(self) -> None:
        amount = int(input("Enter the deposit amount: "))
        self.balance += amount
        print("Deposit successful")


banks = []


def check_account_exists(acc_no: int):
    global banks
    for obj in banks:
        if obj.account == acc_no:
            return obj
        return None


while True:
    print("1. Create Account")
    print("2. Show account detail")
    print("3. Deposit amount to the Bank")
    print("4. Withdraw Amount")
    print("5. Transfer Amount")
    print("6. Exit")
    choice = int(input("Enter the choice: "))

    if choice == 1:
        obj = Bank()
        banks.append(obj)
        print("Account created successfully")
    elif choice == 2:
        if len(banks) == 0:
            print("No account created")
        else:
            for account in banks:
                account.show_info()
    elif choice == 3:
        if len(banks) == 0:
            print("No account created")
        else:
            acc_no = int(input("Enter the Account Number: "))
            obj = check_account_exists(acc_no)
            if obj:
                obj.deposit()
                obj.show_balance()
            else:
                print("Account does not exist")
    elif choice == 4:
        if len(banks) == 0:
            print("No account created")
        else:
            acc_no = int(input("Enter the Account Number: "))
            obj = check_account_exists(acc_no)
            if obj:
                obj.withdraw()
                obj.show_balance()
            else:
                print("Account does not exist")
    elif choice == 5:
        from_acc_no = int(input("Enter the FROM account number: "))
        to_acc_no = int(input("Enter the TO account number: "))

        from_acc_obj = check_account_exists(from_acc_no)
        to_acc_obj = check_account_exists(to_acc_no)

        if from_acc_obj is None:
            print("FROM account does not exist")
        elif to_acc_obj is None:
            print("TO account does not exist")
        elif from_acc_obj.account == to_acc_obj.account:
            print("Cannot transfer to same account")
        else:
            transfer_amount = int(input("Enter the transfer amount: "))
            if transfer_amount > from_acc_obj.balance:
                print("Insufficient balance")
            else:
                from_acc_obj.balance -= transfer_amount
                to_acc_obj.balance += transfer_amount
                # print(
                #     f"Transfer successful: {transfer_amount} from {from_acc_no} to {to_acc_no}"
                # )
                # from_acc_obj.show_balance()
                # to_acc_obj.show_balance()
    elif choice == 6:
        print("Thank you for using the banking system!")
        break
    else:
        print("Invalid choice")
