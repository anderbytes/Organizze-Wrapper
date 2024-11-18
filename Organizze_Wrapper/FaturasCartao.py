from dataclasses import dataclass

from .API import API

@dataclass
class FaturaCartao:
    """
    Representa os dados de uma fatura de cartão de crédito na plataforma Organizze.

    Attributes:
        id (int): Identificador único da fatura.
        date (str): Data da fatura no formato `YYYY-MM-DD`.
        starting_date (str): Data de início do período da fatura no formato `YYYY-MM-DD`.
        closing_date (str): Data de fechamento do período da fatura no formato `YYYY-MM-DD`.
        amount_cents (int): Valor total da fatura em centavos.
        payment_amount_cents (int): Valor total dos pagamentos realizados na fatura em centavos.
        balance_cents (int): Saldo atual da fatura em centavos.
        previous_balance_cents (int): Saldo anterior da fatura em centavos.
        credit_card_id (int): Identificador único do cartão de crédito associado à fatura.
    """

    id: int
    date: str  # DATE YYYY-MM-DD
    starting_date: str  # DATE YYYY-MM-DD
    closing_date: str  # DATE YYYY-MM-DD
    amount_cents: int
    payment_amount_cents: int
    balance_cents: int
    previous_balance_cents: int
    credit_card_id: int

    def to_dict(self):
        """ Retorna uma representação em JSON de uma Fatura de Cartão """
        return {"id": self.id,
                "date": self.date,
                "starting_date": self.starting_date,
                "closing_date": self.closing_date,
                "amount_cents": self.amount_cents,
                "payment_amount_cents": self.payment_amount_cents,
                "balance_cents": self.balance_cents,
                "previous_balance_cents": self.previous_balance_cents,
                "credit_card_id": self.credit_card_id}

    @classmethod
    def load_dict(cls, dct):
        """Reconstrói o(s) objeto(s) a partir de um dicionário"""
        if isinstance(dct, list):
            return [cls(**item) for item in dct]
        else:
            return cls(**dct)

    @classmethod
    def json(cls, obj):
        """ Útil para chamadas excepcionais. Ex: json.dumps(default=Classe.json)"""
        return obj.to_dict()


def getFaturasCartao(sessao: API, idCartao: int) -> list[FaturaCartao]:
    """
    Obtém a lista de faturas de um cartão de crédito específico da plataforma Organizze.

    Args:
        sessao (API): Sessão autenticada para realizar chamadas à API.
        idCartao (int): Identificador único do cartão de crédito para o qual as faturas serão buscadas.

    Returns:
        list[FaturaCartao]: Uma lista de objetos `FaturaCartao` contendo as faturas obtidas.
    """

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
    """
    Obtém as informações detalhadas de uma fatura de cartão de crédito específica da plataforma Organizze.

    Args:
        sessao (API): Sessão autenticada para realizar chamadas à API.
        idCartao (int): Identificador único do cartão de crédito.
        idFatura (int): Identificador único da fatura do cartão a ser buscada.

    Returns:
        FaturaCartao: Um objeto `FaturaCartao` contendo os dados da fatura.
    """

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
    """
    Obtém a lista de pagamentos realizados para uma fatura específica de um cartão de crédito.

    Args:
        sessao (API): Sessão autenticada para realizar chamadas à API.
        idCartao (int): Identificador único do cartão de crédito.
        idFatura (int): Identificador único da fatura do cartão.

    Returns:
        list: Lista de pagamentos realizados para a fatura.
    """

    return sessao._get(f'/credit_cards/{idCartao}/invoices/{idFatura}/payments')