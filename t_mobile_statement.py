#!/usr/bin/env python3

import json
from Bills import *
from twilio.rest import Client
from Config import Config
import datetime

from phones import Phones
from settings import *

# Make table of all users
users = {}


def broadcast_msg():
    client = Client(TWILIO_SID, TWILIO_TOKEN)

    print("Sending SMS ...")
    phones = Phones()
    for k, v in phones.get_numbers():
        user = users[k]
        for phone in v:
            message = client.messages.create(
                to=phone,
                from_=TWILIO_NUMBER,
                body=user.generate_bill()
            )
            print('<To {}: SID:{}>'.format(message.to, message.sid))
    print("SMS sent\n")


def read_statement():
    path = "statement.json"
    lines = ""
    with open(path, 'r') as readfile:
        for line in readfile:
            lines += line
    return lines


def main():
    # Read in statement
    data = read_statement()

    # Parse statement to JSON
    parsed = json.loads(data)

    main_bill = parsed["main"]
    bills = parsed["bills"]
    additional = parsed['additional']

    for bill in bills:
        user = UserBill(bill["type"], bill["tel"], bill["name"], bill["bill"], bill["equip"], bill["services"])
        users[user._telephone] = user

    # Get main bill and add fees to respective accounts
    main_bills = {}
    for main in main_bill:
        bill = MainBill(main["type"], main["amount"], main["about"], main["to"])
        main_bills[bill._type] = bill

    for user in main_bills["main_bill"].get_to_list():
        main_bill = main_bills["main_bill"].get_share()
        users[user].update_balance(main_bill)

    # Add north america plan to respective account
    for user in main_bills["main_extra"].get_to_list():
        main_bill = main_bills["main_extra"].get_amount()
        users[user].update_balance(main_bill)

    # Add iPhone fee to account
    for user in main_bills["equip"].get_to_list():
        main_bill = main_bills["equip"].get_amount()
        users[user].update_balance(main_bill)

    # Add extra
    for add_json in additional:
        add_account = users[add_json["add"]]
        to_account = users[add_json["to"]]

        to_account.add_other_account(add_json["add"], add_account.get_balance())

    # Send Txt msgs
    if not Config.PREVIEW_ONLY:
        broadcast_msg()

    # Statement total
    total = 0.00

    # Display to console
    today = datetime.datetime.now()
    month = today.strftime('%B'),
    msg = "Late Bill for {} 15, {}\n".format(month[0], today.year)
    msg += str("-" * 17) + "\n"

    for tel, user in users.items():
        amount = user.get_balance()
        total += amount
        msg += "{0} ==> ${1:.2f} {2}\n".format(user._telephone, user.get_balance(), user._name)

    msg += "\nTotal: ${:.2f}".format(total)
    print(msg)


if __name__ == "__main__":
    main()
