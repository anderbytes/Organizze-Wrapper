from dataclasses import dataclass

from PyMultiHelper.Validation import validateDateFormat, matchesRegex
from PyMultiHelper.Dates import dateRanges
from .API import API

@dataclass
class Lancamento:
    """
    Representa um lançamento financeiro na plataforma Organizze.

    Attributes:
        id (int): Identificador único do lançamento.
        description (str): Descrição do lançamento.
        date (str): Data do lançamento no formato `YYYY-MM-DD`.
        paid (bool): Indica se o lançamento foi pago.
        amount_cents (int): Valor do lançamento em centavos.
        total_installments (int): Número total de parcelas do lançamento.
        installment (int): Número da parcela do lançamento.
        recurring (bool): Indica se o lançamento é recorrente.
        account_id (int): Identificador da conta relacionada ao lançamento.
        category_id (int): Identificador da categoria do lançamento.
        tags (list): Lista de tags associadas ao lançamento.
        notes (str): Notas adicionais sobre o lançamento.
        attachments_count (int): Quantidade de anexos relacionados ao lançamento.
        credit_card_id (int): Identificador do cartão de crédito associado ao lançamento.
        credit_card_invoice_id (int): Identificador da fatura do cartão de crédito associada ao lançamento.
        paid_credit_card_id (int): Identificador do cartão de crédito pago associado ao lançamento.
        paid_credit_card_invoice_id (int): Identificador da fatura do cartão de crédito paga associada ao lançamento.
        oposite_transaction_id (int): Identificador da transação oposta ao lançamento.
        oposite_account_id (int): Identificador da conta da transação oposta.
        created_at (str): Data de criação do lançamento no formato ISO (`YYYY-MM-DD`).
        updated_at (str): Data da última atualização do lançamento no formato ISO (`YYYY-MM-DD`).
    """

    id: int
    description: str
    date: str  # YYYY-MM-DD FORMAT
    paid: bool
    amount_cents: int
    total_installments: int
    installment: int
    recurring: bool
    account_id: int
    category_id: int
    tags: []
    notes: str
    attachments_count: int
    credit_card_id: int
    credit_card_invoice_id: int
    paid_credit_card_id: int
    paid_credit_card_invoice_id: int
    oposite_transaction_id: int
    oposite_account_id: int
    created_at: str  # DATE ISO FORMAT
    updated_at: str  # DATE ISO FORMAT

    def to_dict(self):
        """ Retorna uma representação em JSON de um Lançamento """
        return {"id": self.id,
                "description": self.description,
                "date": self.date,
                "paid": self.paid,
                "amount_cents": self.amount_cents,
                "total_installments": self.total_installments,
                "installment": self.installment,
                "recurring": self.recurring,
                "account_id": self.account_id,
                "category_id": self.category_id,
                "tags": self.tags,
                "notes": self.notes,
                "attachments_count": self.attachments_count,
                "credit_card_id": self.credit_card_id,
                "credit_card_invoice_id": self.credit_card_invoice_id,
                "paid_credit_card_id": self.paid_credit_card_id,
                "paid_credit_card_invoice_id": self.paid_credit_card_invoice_id,
                "oposite_transaction_id": self.oposite_transaction_id,
                "oposite_account_id": self.oposite_account_id,
                "created_at": self.created_at,
                "updated_at": self.updated_at}

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

# OPERAÇÕES BÁSICAS

def getLancamentos(sessao: API, dataInicio: str, dataFim: str) -> list[Lancamento]:
    """
    Obtém os lançamentos financeiros em um intervalo de datas da plataforma Organizze.

    Args:
        sessao (API): Sessão autenticada para realizar chamadas à API.
        dataInicio (str): Data de início do intervalo de busca no formato `YYYY-MM-DD`.
        dataFim (str): Data de fim do intervalo de busca no formato `YYYY-MM-DD`.

    Returns:
        list[Lancamento]: Lista de objetos `Lancamento` com os dados dos lançamentos encontrados.
    """

    validateDateFormat(dataInicio, "%Y-%m-%d")
    validateDateFormat(dataFim, "%Y-%m-%d")
    results: list[Lancamento] = []

    for inicio, fim in dateRanges(startDate=dataInicio, endDate=dataFim):

        parametros = "?"
        if dataInicio is not None:
            parametros = f'{parametros}start_date={inicio}&'
        if dataFim is not None:
            parametros = f'{parametros}end_date={fim}'

        response = sessao._get(comando=f'/transactions{parametros}')

        for i in response:
            results.append(Lancamento(id=i['id'],
                                      description=i['description'],
                                      date=i['date'],
                                      paid=i['paid'],
                                      amount_cents=i['amount_cents'],
                                      total_installments=i['total_installments'],
                                      installment=i['installment'],
                                      recurring=i['recurring'],
                                      account_id=i['account_id'],
                                      category_id=i['category_id'],
                                      tags=i['tags'],
                                      notes=i['notes'],
                                      attachments_count=i['attachments_count'],
                                      credit_card_id=i['credit_card_id'],
                                      credit_card_invoice_id=i['credit_card_invoice_id'],
                                      paid_credit_card_id=i['paid_credit_card_id'],
                                      paid_credit_card_invoice_id=i['paid_credit_card_invoice_id'],
                                      oposite_transaction_id=i['oposite_transaction_id'],
                                      oposite_account_id=i['oposite_account_id'],
                                      created_at=i['created_at'],
                                      updated_at=i['updated_at']))
    return results

def getLancamento(sessao: API, idLancamento: int) -> Lancamento:
    """
    Obtém os detalhes de um lançamento financeiro específico da plataforma Organizze.

    Args:
        sessao (API): Sessão autenticada para realizar chamadas à API.
        idLancamento (int): Identificador único do lançamento a ser obtido.

    Returns:
        Lancamento: Objeto `Lancamento` com os dados do lançamento encontrado.
    """

    response = sessao._get(f'/transactions/{idLancamento}')
    return Lancamento(id=response['id'],
                      description=response['description'],
                      date=response['date'],
                      paid=response['paid'],
                      amount_cents=response['amount_cents'],
                      total_installments=response['total_installments'],
                      installment=response['installment'],
                      recurring=response['recurring'],
                      account_id=response['account_id'],
                      category_id=response['category_id'],
                      tags=response['tags'],
                      notes=response['notes'],
                      attachments_count=response['attachments_count'],
                      credit_card_id=response['credit_card_id'],
                      credit_card_invoice_id=response['credit_card_invoice_id'],
                      paid_credit_card_id=response['paid_credit_card_id'],
                      paid_credit_card_invoice_id=response['paid_credit_card_invoice_id'],
                      oposite_transaction_id=response['oposite_transaction_id'],
                      oposite_account_id=response['oposite_account_id'],
                      created_at=response['created_at'],
                      updated_at=response['updated_at'])

def delLancamento(sessao: API, idLancamento: int, apagaFuturos: bool = False, apagaTodos: bool = False):
    """
    Deleta um lançamento financeiro da plataforma Organizze.

    Args:
        sessao (API): Sessão autenticada para realizar chamadas à API.
        idLancamento (int): Identificador único do lançamento a ser deletado.
        apagaFuturos (bool, optional): Se `True`, deleta o lançamento e as ocorrências futuras. Default é `False`.
        apagaTodos (bool, optional): Se `True`, deleta o lançamento e todos os lançamentos relacionados. Default é `False`.
    """

    parametros = None
    if apagaFuturos is True:
        parametros = {"update_future": True}
    elif apagaTodos is True:
        parametros = {"update_all": True}
    sessao._delete(f'/transactions/{idLancamento}', params=parametros)

def addLancamento(sessao: API, JSON_params: dict):
    """
    Adiciona um novo lançamento financeiro na plataforma Organizze.

    Args:
        sessao (API): Sessão autenticada para realizar chamadas à API.
        JSON_params (dict): Parâmetros do lançamento no formato JSON a ser adicionado.
    """

    # TODO: "Requer validação de parâmetros JSON"

    sessao._post("/transactions", params=JSON_params)

def addLancamentoFixo(sessao: API, JSON_params: dict, periodicidade: str):
    """
    Adiciona um novo lançamento fixo com periodicidade na plataforma Organizze.

    Args:
        sessao (API): Sessão autenticada para realizar chamadas à API.
        JSON_params (dict): Parâmetros do lançamento fixo no formato JSON a ser adicionado.
        periodicidade (str): Periodicidade do lançamento. Deve ser um dos seguintes valores:
                             ["diário", "semanal", "bissemanal", "mensal", "bimestral", "trimestral", "semestral", "anual"].
    """

    # TODO: "Incompleta. Mais testes"

    # OPÇÕES DE PERIODICIDADE: ["weekly", "biweekly", "monthly",  "bimonthly", "trimonthly", "yearly"]
    # Cadê DAILY e SEMESTRAL (or SEMESTRIAL)
    periodos = {'diário': 'daily', 'semanal': 'weekly', 'bissemanal': 'biweekly', 'mensal': 'monthly',
                'bimestral': 'bimonthly', 'trimestral': 'trimonthly', 'semestral': 'semesterly', 'anual': 'yearly'}

    JSON_params.update({"recurrence_attributes": {"periodicity": periodos[periodicidade]}})
    sessao._post("/transactions", params=JSON_params)

def addLancamentoRecorrente(sessao: API, JSON_params: dict, periodicidade: str, parcelas: int):
    """
    Adiciona um novo lançamento recorrente com periodicidade e número de parcelas na plataforma Organizze.

    Args:
        sessao (API): Sessão autenticada para realizar chamadas à API.
        JSON_params (dict): Parâmetros do lançamento recorrente no formato JSON a ser adicionado.
        periodicidade (str): Periodicidade do lançamento recorrente. Deve ser um dos seguintes valores:
                             ["diário", "semanal", "bissemanal", "mensal", "bimestral", "trimestral", "semestral", "anual"].
        parcelas (int): Número de parcelas do lançamento recorrente (deve ser entre 2 e 480).

    Raises:
        ValueError: Se o número de parcelas for menor que 2 ou maior que 480.
    """

    # TODO: "Incompleta. Mais testes"

    # OPÇÕES DE PERIODICIDADE: ["weekly", "biweekly", "monthly",  "bimonthly", "trimonthly", "yearly"]
    # Cadê DAILY e SEMESTRAL (or SEMESTRIAL)
    periodos = {'diário': 'daily', 'semanal': 'weekly', 'bissemanal': 'biweekly', 'mensal': 'monthly',
                'bimestral': 'bimonthly', 'trimestral': 'trimonthly', 'semestral': 'semesterly', 'anual': 'yearly'}
    periodicidade = periodos[periodicidade]

    if not (2 <= parcelas <= 480):
        raise ValueError("O número de parcelas é inválido (utilize um Nº entre 2 a 480)")
    JSON_params.update({"installments_attributes": {"periodicity": periodicidade, "total": parcelas}})
    sessao._post("/transactions", params=JSON_params)

def updLancamento(sessao: API, idLancamento: int, JSON_params: dict, atualizaFuturos: bool = False, atualizaTodos: bool = False):
    """
    Atualiza um lançamento existente na plataforma Organizze, com a opção de atualizar lançamentos futuros ou todos.

    Args:
        sessao (API): Sessão autenticada para realizar chamadas à API.
        idLancamento (int): ID do lançamento a ser atualizado.
        JSON_params (dict): Parâmetros JSON a serem atualizados no lançamento.
        atualizaFuturos (bool): Se True, atualiza apenas os lançamentos futuros.
        atualizaTodos (bool): Se True, atualiza todos os lançamentos relacionados.

    Raises:
        ValueError: Se nenhum dos parâmetros de atualização (atualizaFuturos ou atualizaTodos) for fornecido.
    """

    # TODO: "Requer validação de parâmetros JSON"

    if atualizaFuturos is True:
        JSON_params.update({"update_future": True})
    elif atualizaTodos is True:
        JSON_params.update({"update_all": True})
    sessao._put(f'/transactions/{idLancamento}', params=JSON_params)

# OPERAÇÕES CUSTOMIZADAS

def filtraLancamentos(lancamentos: list[Lancamento], contaBuscada: int = None, tituloBuscado: str = None, usaRegex: bool = False):
    """
    Filtra a lista de lançamentos com base no título fornecido, utilizando correspondência simples ou expressão regular.

    Args:
        lancamentos (list[Lancamento]): Lista de objetos Lancamento a ser filtrada.
        contaBuscada (int, opcional): ID da conta para ser filtrada, se desejado. O padrão é None.
        tituloBuscado (str, opcional): Título ou expressão regular para buscar nas descrições dos lançamentos. O padrão é None.
        usaRegex (bool, opcional): Se True, utiliza expressão regular para a correspondência, caso contrário, realiza uma correspondência simples. O padrão é False.

    Returns:
        list[Lancamento]: Lista de lançamentos filtrados que correspondem ao título fornecido.
    """

    results: list[Lancamento] = []

    for l in lancamentos:
        # Considera até 2ª ordem
        considera = True

        # Busca por Conta
        if contaBuscada:
            if l.account_id != contaBuscada:
                considera = False

        # Busca pelo Título
        if tituloBuscado:
            if usaRegex:
                if not matchesRegex(l.description, tituloBuscado):
                    considera = False
            else:
                if not tituloBuscado.upper() in l.description.upper():
                    considera = False

        if considera:
            results.append(l)

    return results
