from datetime import datetime
import csv
import mysql.connector as sqltor
try:
    my_con = sqltor.connect(host='localhost', user='root', passwd='psswd', database='atm')
    if my_con.is_connected():
        cursor = my_con.cursor()
except:
    print("Could not connect to the server")
    exit()


class AccountNo:
    def __init__(self, account_no):
        self.account_no = account_no

    def account_checker(self, account_no=None):
        if len(account_no) != 4:
            return False
        else:
            # checks if account is there in database
            cursor.execute(f"SELECT EXISTS(SELECT account_no from accountinfo WHERE account_no={account_no})") 
            account_isthere = bool(cursor.fetchone()[0])
        
        return account_isthere

    def pin_checker(self):
        #gets pin from the database
        cursor.execute(f'SELECT pin from accountinfo WHERE account_no = {self.account_no}') 
        oringinal_pin = cursor.fetchone()[0]

        while True:
            entered_pin = input("Please enter your pin:")

            if entered_pin == '0':  # if one wants to exit to main menu
                print("\nHope you have a wonderful day")
                
                return False
            # if pin is correct
            elif entered_pin == oringinal_pin:  
                print("Pin is correct")
                
                return True
            else:
                # if pin is incorrect
                print("The pin entered is incorrect please try again(enter 0 to exit)")



class AccountFunctions(AccountNo):
    # commands for transferring funds between accounts
    def transfer_amount(self):
        to_account_no = input("Enter the account where you want to transfer:")
        amount = int(input("Enter the amount which you want to transfer:"))
        
        #checks if account exists
        if self.account_checker(to_account_no): 
            cursor.execute(f'SELECT balance FROM accountinfo WHERE account_no= {self.account_no}')

            og_balance = cursor.fetchone()[0]
            # changes balance of the owner's account
            og_new_balance = og_balance - amount 

            cursor.execute(f'SELECT balance FROM accountinfo WHERE account_no= {to_account_no}')

            to_balance = cursor.fetchone()[0]
            #adds balance to the reciever
            to_new_balance = to_balance + amount 

            # checks if there are enough funds in owner's account
            if og_new_balance >= 0: 
                self.transaction_logger(to_account_no, amount, og_new_balance, to_new_balance, 'transfer') #updates the logs

                cursor.execute(f"UPDATE accountinfo SET balance = {og_new_balance} WHERE account_no = {self.account_no}")
                cursor.execute(f"UPDATE accountinfo SET balance = {to_new_balance} WHERE account_no = {to_account_no}")
                my_con.commit()

                print("Transaction Completed")
            else:
                print("You do not have sufficient funds for this operation")
        
        else:
            print("The account to transfer is not in the database")
    
    #commands for withdrawing transaction
    def withdraw_transaction(self): 
        amount = int(input("Enter the amount which you want to withdraw:"))

        cursor.execute(f"SELECT balance FROM accountinfo WHERE account_no= {self.account_no}")

        og_balance = cursor.fetchone()[0]
        og_new_balance = og_balance - amount

        if og_new_balance >= 0:

            self.transaction_logger(self.account_no, amount, og_new_balance, og_new_balance, 'withdraw')

            cursor.execute(f"UPDATE accountinfo SET balance = {og_new_balance} WHERE account_no = {self.account_no}")
            my_con.commit()
            
            print("\nAmount has been withdrawn")
        else:
            print("You do not have sufficient funds for this operation")
    
    # commands for depositing transaction
    def deposit_transaction(self):
        amount = int(input("Enter the amount which you want to deposit:"))

        cursor.execute(f"SELECT balance FROM accountinfo WHERE account_no= {self.account_no}")

        og_balance = cursor.fetchone()[0]
        og_new_balance = og_balance + amount

        self.transaction_logger(self.account_no, amount, og_new_balance, og_new_balance, 'deposit')

        cursor.execute(f"UPDATE accountinfo SET balance = {og_new_balance} WHERE account_no = {self.account_no}")
        my_con.commit()
        
        print("\nThe amount has been deposited")

    #function to change pin
    def change_pin(self):
        #re-checks to see if he is the same owner
        if self.pin_checker(): 
            while True:
                changed_pin = input("Please enter the new pin(4 digit only) :")
                
                # checks if pin is of 4 digits
                if len(changed_pin) != 4: 
                    print("enter pin with 4 digits")
                else:
                    reenter_pin = input("Please re-enter the new pin(4 digit only):")

                #checks if the re-entered pin is the same
                if reenter_pin == changed_pin: 
                    cursor.execute(f"UPDATE accountinfo SET pin = {changed_pin} WHERE account_no = {self.account_no}")
                    my_con.commit()

                    print("\nThe PIN has succesfully been changed")
                    break
                else:
                    print("The pins do not match please try again:")
        else:
            print("We could not change your pin")
    
    #fetches last 10 transactions
    def show_passbook(self): 
        cursor.execute(f"SELECT * from transactions WHERE account_no = {self.account_no} ORDER BY transaction_time desc")
        passbook = cursor.fetchall()

        with open(f"passbookof{self.account_no}.csv","w",newline="") as csvfile:
            csvwriter = csv.writer(csvfile)
            fields = ['transaction_time', 'account_no', 'to/from_account', 'deposit', 'withdrawal', 'balance',' transaction_type']
            csvwriter.writerow(fields)

            for i in range(len(passbook)-1,-1,-1):
                l = passbook[i]
                csvwriter.writerow([l[0], l[1], l[2], l[3], l[4], l[5], l[6]])
            
        print("Your Passbook has been saved in csv file with your account number")
    
    #checks the balance of the account
    def check_balance(self):
        cursor.execute(f"SELECT balance FROM accountinfo WHERE account_no= {self.account_no}")
        
        balance = cursor.fetchone()[0]
        print("\nYour balance is", balance)
    
    #logs the transaction in database
    def transaction_logger(self, to_account_no, amount, og_new_balance, to_new_balance, funds):
        sql = f"INSERT INTO transactions VALUES (%s, %s, %s, %s, %s, %s, %s)"
        
        if funds == 'transfer': 
            # scheme if its a transfer transaction
            val = [(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), self.account_no, to_account_no, None, -amount, og_new_balance, funds),
                   (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), to_account_no, self.account_no, amount, None, to_new_balance, funds)]
        
        elif funds == 'deposit': 
            # scheme if its a depositing transaction
            val = [(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), self.account_no, to_account_no, amount, None, og_new_balance, funds)]
        
        elif funds == 'withdraw': 
            #scheme if its a withdraw transaction
            val = [(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), self.account_no, to_account_no, None, -amount, og_new_balance, funds)]
        cursor.executemany(sql, val)
        my_con.commit()



class NoAccount():
    #creates new account in database
    def create_account(self):
        
        name = input("Please enter your name:")
        cursor.execute(f"SELECT account_no FROM accountinfo ORDER BY account_no DESC LIMIT 1")
        try:
            last_no = int(cursor.fetchone()[0])
        except:
            last_no = 1000    
        cursor.execute(f"INSERT INTO accountinfo (account_no,name) VALUES ({last_no + 1},'{name}')")
        my_con.commit()
        
        print(f"\nYour account is created,Your account details are:\naccount number = {last_no + 1}\nname = {name}\npin = 1234\nPlease change your pin for security purposes first")
