import datetime


class MainBill(object):
    def __init__(self, bill_type, amount, about, to):
        self._type = bill_type
        self._amount = amount
        self._about = about
        self._to = to

    def get_amount(self):
        return self._amount

    def get_share(self):
        return self._amount / len(self._to)

    def get_to_list(self):
        return self._to


class UserBill(object):
    def __init__(self, bill_type, telephone, name, bill, equip, services):
        self._bill_type = bill_type
        self._telephone = telephone
        self._name = name
        self._bill = bill
        self._equip = equip
        self._balance = bill + equip + services
        self._services = services
        self._other_users = []

    def update_balance(self, money):
        self._balance += money

    def get_balance(self):
        return self._balance

    def add_other_account(self, tel, amount):
        self._other_users.append( {'tel': tel, 'amount': amount} )

    def generate_bill(self):
        total = self._balance
        added_msg = ''
        for other in self._other_users:
            total += other['amount']
            added_msg += "{0} ==> ${1:.2f}\n".format(other['tel'], other['amount'])

        today = datetime.datetime.now()
        msg = "Bill for {} 15, {}\n".format(today.strftime('%B'), today.year)
        msg += str("-" * 17) + "\n"
        msg += "{0} ==> ${1:.2f}\n".format(self._telephone, self._balance)
        msg += added_msg
        msg += "\nTotal: ${:.2f}".format(total)
        return msg
