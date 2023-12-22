import yookassa

import tokeni
def create_oplata(value):
    yookassa.Configuration.account_id = tokeni.Api_id
    yookassa.Configuration.secret_key = tokeni.Api_key

    payment = yookassa.Payment.create({
        "amount" : {
            "value": value,
            "currency": "RUB"

        },
        "confirmation":{
            "type": "redirect",
            "return_url": "https://github.com/treezyyy"
        },
        "description": "Покупка чего либо",
        "capture": True
    })

    url = payment.confirmation.confirmation_url
    return url, payment


def oplata_check(id):
    payment = yookassa.Payment.find_one(id)
    if payment.status == 'succeeded':
        value = payment.amount.value
        return True, value
    else:
        return False


