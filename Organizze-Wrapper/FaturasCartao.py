from .API import API


class FaturaCartao:
    def __init__(self,
                 amount_cents: int,
                 balance_cents: int,
                 closing_date: str,  # DATE YYYY-MM-DD
                 credit_card_id: int,
                 date: str,  # DATE YYYY-MM-DD
                 id: int,
                 payment_amount_cents: int,
                 previous_balance_cents: int,
                 starting_date: str,  # DATE YYYY-MM-DD
                 ):
        self.amount_cents = amount_cents
        self.balance_cents = balance_cents
        self.closing_date = closing_date
        self.credit_card_id = credit_card_id
        self.date = date
        self.id = id
        self.payment_amount_cents = payment_amount_cents
        self.previous_balance_cents = previous_balance_cents
        self.starting_date = starting_date

    def __str__(self):
        return (
            f"FaturaCartao(id={self.id}, "
            f"credit_card_id='{self.credit_card_id}', "
            f"date='{self.date}', "
            f"amount_cents='{self.amount_cents}', "
            f"balance_cents='{self.balance_cents}', "
            f"payment_amount_cents='{self.payment_amount_cents}', "
            f"previous_balance_cents='{self.previous_balance_cents}', "
            f"closing_date='{self.closing_date}', "
            f"starting_date='{self.starting_date}', "
        )


def getFaturasCartao(sessao: API, idCartao: int) -> list[FaturaCartao]:
    #####
    # TODO("Contém Bug grave não resolvido: Não traz corretamente as faturas de qualquer cartão")
    #####
    results = []
    response = sessao._get(f'/credit_cards/{idCartao}/invoices')
    for i in response:
        results.append(FaturaCartao(amount_cents=i['amount_cents'],
                                    balance_cents=i['balance_cents'],
                                    closing_date=i['closing_date'],
                                    credit_card_id=i['credit_card_id'],
                                    date=i['date'],
                                    id=i['id'],
                                    payment_amount_cents=i['payment_amount_cents'],
                                    previous_balance_cents=i['previous_balance_cents'],
                                    starting_date=i['starting_date']
                                    ))
    return results


def getFaturaCartao(sessao: API, idCartao: int, idFatura: int) -> FaturaCartao:
    #####
    # TODO("Contém Bug grave não resolvido: Não traz corretamente pagamentos de faturas")
    #####
    response = sessao._get(f'/credit_cards/{idCartao}/invoices/{idFatura}')
    return FaturaCartao(amount_cents=response['amount_cents'],
                        balance_cents=response['balance_cents'],
                        closing_date=response['closing_date'],
                        credit_card_id=response['credit_card_id'],
                        date=response['date'],
                        id=response['id'],
                        payment_amount_cents=response['payment_amount_cents'],
                        previous_balance_cents=response['previous_balance_cents'],
                        starting_date=response['starting_date'])


def getPagamentosFatura(sessao: API, idCartao: int, idFatura: int):
    return sessao._get(f'/credit_cards/{idCartao}/invoices/{idFatura}/payments')
