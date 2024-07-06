from .API import API
from .auxiliar import validaData, rangesIntervalo


class Lancamento:
    def __init__(self,
                 amount_cents: int,
                 attachments_count: int,
                 category_id: int,
                 created_at: str,  # DATE ISO FORMAT
                 credit_card_id: int,
                 credit_card_invoice_id: int,
                 date: str,  # YYYY-MM-DD FORMAT
                 description: str,
                 id: int,
                 installment: int,
                 notes: str,
                 oposite_account_id: int,
                 oposite_transaction_id: int,
                 paid: bool,
                 paid_credit_card_id: int,
                 paid_credit_card_invoice_id: int,
                 recurring: bool,
                 tags: [],
                 total_installments: int,
                 updated_at: str  # DATE ISO FORMAT
                 ):
        self.amount_cents = amount_cents
        self.attachments_count = attachments_count
        self.category_id = category_id
        self.created_at = created_at
        self.credit_card_id = credit_card_id
        self.credit_card_invoice_id = credit_card_invoice_id
        self.date = date
        self.description = description
        self.id = id
        self.installment = installment
        self.notes = notes
        self.oposite_account_id = oposite_account_id
        self.oposite_transaction_id = oposite_transaction_id
        self.paid = paid
        self.paid_credit_card_id = paid_credit_card_id
        self.paid_credit_card_invoice_id = paid_credit_card_invoice_id
        self.recurring = recurring
        self.tags = tags
        self.total_installments = total_installments
        self.updated_at = updated_at

    def __str__(self):
        return (
            f"Lancamento(id={self.id}, "
            f"date='{self.date}', "
            f"description='{self.description}', "
            f"amount_cents='{self.amount_cents}', "
            f"category_id='{self.category_id}', "
            f"attachments_count={self.attachments_count}, "
            f"installment={self.installment}, "
            f"total_installments={self.total_installments}, "
            f"recurring={self.recurring}, "
            f"paid={self.paid}, "
            f"notes={self.notes}, "
            f"oposite_account_id={self.oposite_account_id}, "
            f"oposite_transaction_id={self.oposite_transaction_id}, "
            f"credit_card_id={self.credit_card_id}, "
            f"credit_card_invoice_id={self.credit_card_invoice_id}, "
            f"paid_credit_card_id={self.paid_credit_card_id}, "
            f"paid_credit_card_invoice_id={self.paid_credit_card_invoice_id}, "
            f"created_at='{self.created_at}', "
            f"updated_at='{self.updated_at}')"
        )


def getLancamentos(sessao: API, dataInicio: str, dataFim: str) -> list[Lancamento]:
    validaData(dataInicio)
    validaData(dataFim)
    results: list[Lancamento] = []

    for inicio, fim in rangesIntervalo(dataInicio, dataFim):

        parametros = "?"
        if dataInicio is not None:
            parametros = f'{parametros}start_date={inicio}&'
        if dataFim is not None:
            parametros = f'{parametros}end_date={fim}'

        response = sessao.get(comando=f'/transactions{parametros}')

        for i in response:
            results.append(Lancamento(amount_cents=i['amount_cents'],
                                      attachments_count=i['attachments_count'],
                                      category_id=i['category_id'],
                                      created_at=i['created_at'],
                                      credit_card_id=i['credit_card_id'],
                                      credit_card_invoice_id=i['credit_card_invoice_id'],
                                      date=i['date'],
                                      description=i['description'],
                                      id=i['id'],
                                      installment=i['installment'],
                                      notes=i['notes'],
                                      oposite_account_id=i['oposite_account_id'],
                                      oposite_transaction_id=i['oposite_transaction_id'],
                                      paid=i['paid'],
                                      paid_credit_card_id=i['paid_credit_card_id'],
                                      paid_credit_card_invoice_id=i['paid_credit_card_invoice_id'],
                                      recurring=i['recurring'],
                                      tags=i['tags'],
                                      total_installments=i['total_installments'],
                                      updated_at=i['updated_at']))
    return results


def getLancamento(sessao: API, idLancamento: int) -> Lancamento:
    response = sessao.get(f'/transactions/{idLancamento}')
    return Lancamento(amount_cents=response['amount_cents'],
                      attachments_count=response['attachments_count'],
                      category_id=response['category_id'],
                      created_at=response['created_at'],
                      credit_card_id=response['credit_card_id'],
                      credit_card_invoice_id=response['credit_card_invoice_id'],
                      date=response['date'],
                      description=response['description'],
                      id=response['id'],
                      installment=response['installment'],
                      notes=response['notes'],
                      oposite_account_id=response['oposite_account_id'],
                      oposite_transaction_id=response['oposite_transaction_id'],
                      paid=response['paid'],
                      paid_credit_card_id=response['paid_credit_card_id'],
                      paid_credit_card_invoice_id=response['paid_credit_card_invoice_id'],
                      recurring=response['recurring'],
                      tags=response['tags'],
                      total_installments=response['total_installments'],
                      updated_at=response['updated_at'])


def addLancamento(sessao: API, JSON_params: dict):
    sessao.post("/transactions", params=JSON_params)


def addLancamentoFixo(sessao: API, JSON_params: dict, periodicidade: str):
    # OPÇÕES DE PERIODICIDADE: ["weekly", "biweekly", "monthly",  "bimonthly", "trimonthly", "yearly"]
    # Cadê DAILY e SEMESTRAL (or SEMESTRIAL)
    periodos = {'diário': 'daily', 'semanal': 'weekly', 'bissemanal': 'biweekly', 'mensal': 'monthly',
                'bimestral': 'bimonthly', 'trimestral': 'trimonthly', 'semestral': 'semesterly', 'anual': 'yearly'}

    JSON_params.update({"recurrence_attributes": {"periodicity": periodos[periodicidade]}})
    sessao.post("/transactions", params=JSON_params)


def addLancamentoRecorrente(sessao: API, JSON_params: dict, periodicidade: str, parcelas: int):
    # OPÇÕES DE PERIODICIDADE: ["weekly", "biweekly", "monthly",  "bimonthly", "trimonthly", "yearly"]
    # Cadê DAILY e SEMESTRAL (or SEMESTRIAL)
    periodos = {'diário': 'daily', 'semanal': 'weekly', 'bissemanal': 'biweekly', 'mensal': 'monthly',
                'bimestral': 'bimonthly', 'trimestral': 'trimonthly', 'semestral': 'semesterly', 'anual': 'yearly'}
    periodicidade = periodos[periodicidade]

    if not (2 <= parcelas <= 480):
        raise ValueError("O número de parcelas é inválido (utilize um Nº entre 2 a 480)")
    JSON_params.update({"installments_attributes": {"periodicity": periodicidade, "total": parcelas}})
    sessao.post("/transactions", params=JSON_params)


def updLancamento(sessao: API, idLancamento: int, JSON_params: dict, atualizaFuturos: bool = False, atualizaTodos: bool = False):
    if atualizaFuturos is True:
        JSON_params.update({"update_future": True})
    elif atualizaTodos is True:
        JSON_params.update({"update_all": True})
    sessao.put(f'/transactions/{idLancamento}', params=JSON_params)


def delLancamento(sessao: API, idLancamento: int, apagaFuturos: bool = False, apagaTodos: bool = False):
    parametros = None
    if apagaFuturos is True:
        parametros = {"update_future": True}
    elif apagaTodos is True:
        parametros = {"update_all": True}
    sessao.delete(f'/transactions/{idLancamento}', params=parametros)
