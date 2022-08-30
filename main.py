"""
Before Starting the Program Please create the database required using the bank.sql file
"""

import functions

if __name__ == '__main__':
    print("******************************Welcome to ATMOS BANK******************************")
    create_or_use = input("\nEnter 1 if you have an existing account\nEnter 2 If You want to create New account\n:")
    
    if create_or_use == '1':
        account_no = input("\nPlease enter your 4 digit account number :")
        account = functions.AccountFunctions(account_no)
        
        if account.account_checker(account_no):
            if account.pin_checker():
                while True:
                    # Main menu
                    print("\nWelcome to your account\nOptions:\n1.Check Balance\n2.Withdraw Amount\n3.Deposit Amount\n4.Transfer Amount\n5.Change Pin\n6.Show Passbook\n0.exit\n:")
                    func = input("\nPlease enter the corresponding number :")
                    
                    if func == '1':
                        account.check_balance()
                    elif func == '2':
                        account.withdraw_transaction()
                    elif func == '3':
                        account.deposit_transaction()
                    elif func == '4':
                        account.transfer_amount()
                    elif func == '5':
                        account.change_pin()
                    elif func == '6':
                        account.show_passbook()
                    elif func == '0':
                        print("\nHope you have a wonderful day")
                        break
                    else:
                        print("\nPlease enter a valid input ")
        else:
            print("\nThe entered account number does not match out database")

    elif create_or_use == '2':
        account = functions.NoAccount()
        func = input("\nEnter 1 to confirm\nEnter any other key to exit\n:")
        
        if func == '1':
            account.create_account()
        else:
            print("\nHave a good day!")

    else:
        print("\nPlease enter a valid input")
        print("\n\n")
