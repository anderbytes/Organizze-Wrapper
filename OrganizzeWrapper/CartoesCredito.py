from API import API


class CartaoCredito:
    def __init__(self,
                 archived: bool,
                 card_network: str,
                 closing_day: int,
                 created_at: str,  # DATE ISO FORMAT
                 default: bool,
                 description: str,
                 due_day: int,
                 id: int,
                 limit_cents: int,
                 name: str,
                 type: str,
                 updated_at: str  # DATE ISO FORMAT
                 ):
        self.archived = archived
        self.card_network = card_network
        self.closing_day = closing_day
        self.created_at = created_at
        self.default = default
        self.description = description
        self.due_day = due_day
        self.id = id
        self.limit_cents = limit_cents
        self.name = name
        self.type = type
        self.updated_at = updated_at

    def __str__(self):
        return (
            f"Cartao(id={self.id}, "
            f"name='{self.name}', "
            f"description='{self.description}', "
            f"type='{self.type}', "
            f"card_network='{self.card_network}', "
            f"archived={self.archived}, "
            f"default={self.default}, "
            f"limit_cents={self.limit_cents}, "
            f"closing_day={self.closing_day}, "
            f"created_at='{self.created_at}', "
            f"due_day={self.due_day}, "
            f"updated_at='{self.updated_at}')"
        )


def addCartaoCredito(sessao: API, nome: str, bandeira: str, diaVencimento: int, diaFechamento: int, limite: int):
    JSON_Params = dict({
        "name": nome,
        "card_network": bandeira,
        "due_day": diaVencimento,
        "closing_day": diaFechamento,
        "limit_cents": limite
    })
    sessao.post("/credit_cards", params=JSON_Params)


def updCartaoCredito(sessao: API, idCartao: int, nome: str, diaVencimento: int, diaFechamento: int,
                     atualizarFaturasDesde: str):
    JSON_Params = dict({
        "name": nome,
        "due_day": diaVencimento,
        "closing_day": diaFechamento,
        "update_invoices_since": atualizarFaturasDesde  # DATE YYYY-MM-DD
    })
    sessao.put(f'/credit_cards/{idCartao}', params=JSON_Params)


def delCartaoCredito(sessao: API, idCartao: int):
    sessao.delete(f'/credit_cards/{idCartao}')


def getCartoesCredito(sessao: API) -> list[CartaoCredito]:
    results = []
    response = sessao.get("/credit_cards")
    for i in response:
        results.append(CartaoCredito(archived=i['archived'],
                                     card_network=i['card_network'],
                                     closing_day=i['closing_day'],
                                     created_at=i['created_at'],
                                     default=i['default'],
                                     description=i['description'],
                                     due_day=i['due_day'],
                                     id=i['id'],
                                     limit_cents=i['limit_cents'],
                                     name=i['name'],
                                     type=i['type'],
                                     updated_at=i['updated_at']
                                     ))
    return results


def getCartaoCredito(sessao: API, idCartao: int) -> CartaoCredito:
    response = sessao.get(f'/credit_cards/{idCartao}')
    return CartaoCredito(archived=response['archived'],
                         card_network=response['card_network'],
                         closing_day=response['closing_day'],
                         created_at=response['created_at'],
                         default=response['default'],
                         description=response['description'],
                         due_day=response['due_day'],
                         id=response['id'],
                         limit_cents=response['limit_cents'],
                         name=response['name'],
                         type=response['type'],
                         updated_at=response['updated_at'])
