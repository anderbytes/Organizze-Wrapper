from dataclasses import dataclass

from .API import API

@dataclass
class CartaoCredito:
    """
    Representa os dados de um cartão de crédito na plataforma Organizze.

    Attributes:
        id (int): Identificador único do cartão de crédito.
        name (str): Nome do cartão de crédito.
        description (str): Descrição do cartão de crédito.
        card_network (str): Rede do cartão (ex: Visa, MasterCard).
        closing_day (int): Dia de fechamento da fatura do cartão.
        due_day (int): Dia de vencimento da fatura do cartão.
        limit_cents (int): Limite do cartão de crédito em centavos.
        type (str): Tipo do cartão (ex: crédito, débito).
        archived (bool): Indica se o cartão está arquivado.
        default (bool): Indica se o cartão é o padrão para pagamento.
        created_at (str): Data de criação do cartão no formato ISO 8601.
        updated_at (str): Data da última atualização do cartão no formato ISO 8601.
    """

    id: int
    name: str
    description: str
    card_network: str
    closing_day: int
    due_day: int
    limit_cents: int
    type: str
    archived: bool
    default: bool
    created_at: str  # DATE ISO FORMAT
    updated_at: str  # DATE ISO FORMAT

    def to_dict(self):
        """ Retorna uma representação em JSON de um Cartão de Crédito """
        return {"id": self.id,
                "name": self.name,
                "description": self.description,
                "card_network": self.card_network,
                "closing_day": self.closing_day,
                "due_day": self.due_day,
                "limit_cents": self.limit_cents,
                "type": self.type,
                "archived": self.archived,
                "default": self.default,
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


def getCartoesCredito(sessao: API) -> list[CartaoCredito]:
    """
    Obtém a lista de cartões de crédito da plataforma Organizze.

    Args:
        sessao (API): Sessão autenticada para realizar chamadas à API.

    Returns:
        list[CartaoCredito]: Uma lista de objetos `CartaoCredito` contendo os cartões de crédito obtidos.
    """

    results = []
    response = sessao._get("/credit_cards")
    for i in response:
        results.append(CartaoCredito(id=i['id'],
                                     name=i['name'],
                                     description=i['description'],
                                     card_network=i['card_network'],
                                     closing_day=i['closing_day'],
                                     due_day=i['due_day'],
                                     limit_cents=i['limit_cents'],
                                     type=i['type'],
                                     archived=i['archived'],
                                     default=i['default'],
                                     created_at=i['created_at'],
                                     updated_at=i['updated_at']
                                     ))
    return results

def getCartaoCredito(sessao: API, idCartao: int) -> CartaoCredito:
    """
    Obtém as informações detalhadas de um cartão de crédito específico da plataforma Organizze.

    Args:
        sessao (API): Sessão autenticada para realizar chamadas à API.
        idCartao (int): Identificador único do cartão de crédito a ser buscado.

    Returns:
        CartaoCredito: Um objeto `CartaoCredito` contendo os dados do cartão de crédito obtido.
    """

    response = sessao._get(f'/credit_cards/{idCartao}')
    return CartaoCredito(id=response['id'],
                         name=response['name'],
                         description=response['description'],
                         card_network=response['card_network'],
                         closing_day=response['closing_day'],
                         due_day=response['due_day'],
                         limit_cents=response['limit_cents'],
                         type=response['type'],
                         archived=response['archived'],
                         default=response['default'],
                         created_at=response['created_at'],
                         updated_at=response['updated_at'])

def delCartaoCredito(sessao: API, idCartao: int):
    """
    Deleta um cartão de crédito específico da plataforma Organizze.

    Args:
        sessao (API): Sessão autenticada para realizar chamadas à API.
        idCartao (int): Identificador único do cartão de crédito a ser deletado.
    """

    sessao._delete(f'/credit_cards/{idCartao}')

def addCartaoCredito(sessao: API, nome: str, bandeira: str, diaVencimento: int, diaFechamento: int, limite: int):
    """
    Adiciona um novo cartão de crédito na plataforma Organizze.

    Args:
        sessao (API): Sessão autenticada para realizar chamadas à API.
        nome (str): Nome do cartão de crédito.
        bandeira (str): Rede do cartão de crédito (ex: Visa, MasterCard).
        diaVencimento (int): Dia de vencimento da fatura do cartão.
        diaFechamento (int): Dia de fechamento da fatura do cartão.
        limite (int): Limite do cartão de crédito em centavos.
    """

    JSON_Params: dict = {
        "name": nome,
        "card_network": bandeira.value,
        "due_day": diaVencimento,
        "closing_day": diaFechamento,
        "limit_cents": limite
    }
    sessao._post("/credit_cards", params=JSON_Params)

def updCartaoCredito(sessao: API, idCartao: int, nome: str = None, diaVencimento: int = None, diaFechamento: int = None,
                     atualizarFaturasDesde: str = None, bandeira: str = None, limite: int = None):
    """
    Atualiza as informações de um cartão de crédito específico na plataforma Organizze.

    Args:
        sessao (API): Sessão autenticada para realizar chamadas à API.
        idCartao (int): Identificador único do cartão de crédito a ser atualizado.
        nome (str): Novo nome do cartão de crédito.
        limite (int): Novo limite do cartão de crédito, em centavos
        bandeira (str): Bandeira do cartão, aceita os inputs VISA ou MASTERCARD
        diaVencimento (int): Novo dia de vencimento da fatura do cartão.
        diaFechamento (int): Novo dia de fechamento da fatura do cartão.
        atualizarFaturasDesde (str): Data a partir da qual as faturas do cartão devem ser atualizadas (formato: `YYYY-MM-DD`).
    Warnings:
        (Alguns campos foram retirados porque atualizações em campo 'Descrição' e 'Default' não funcionam)
    """

    # TODO: Validação de parâmetros JSON

    JSON_Params: dict = {}
    if nome is not None: JSON_Params['name'] = nome
    if diaVencimento is not None: JSON_Params['due_day'] = diaVencimento
    if diaFechamento is not None: JSON_Params['closing_day'] = diaFechamento
    if bandeira is not None: JSON_Params['card_network'] = bandeira.value
    if limite is not None: JSON_Params['limit_cents'] = limite

    if JSON_Params != {}:
        if atualizarFaturasDesde is not None: JSON_Params['update_invoices_since'] = atualizarFaturasDesde
        sessao._put(f'/credit_cards/{idCartao}', params=JSON_Params)

def arquivaCartaoCredito(sessao: API, idCartao: int):
    """

    Args:
        sessao (API): Sessão autenticada para realizar chamadas à API.
        idCartao (int): Identificador único do cartão de crédito a ser arquivado.

    Warnings:
        (Desarquivamentos devem ocorrer atualmente apenas na interface web ou app)
    """
    sessao._put(f'/credit_cards/{idCartao}', params={'archived': True})
