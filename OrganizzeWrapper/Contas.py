from .API import API


class Conta:
    def __init__(self,
                 archived: bool,
                 created_at: str,  # DATE ISO FORMAT
                 default: bool,
                 description: str,
                 id: int,
                 name: str,
                 type: str,
                 updated_at: str  # DATE ISO FORMAT
                 ):
        self.archived = archived,
        self.created_at = created_at,
        self.default = default,
        self.description = description,
        self.id = id,
        self.name = name,
        self.type = type,
        self.updated_at = updated_at

    def __str__(self):
        return (
            f"Conta(id={self.id}, "
            f"name='{self.name}', "
            f"description='{self.description}', "
            f"type='{self.type}', "
            f"archived={self.archived}, "
            f"default={self.default}, "
            f"created_at='{self.created_at}', "
            f"updated_at='{self.updated_at}')"
        )


def getContas(sessao: API) -> list[Conta]:
    results = []
    response = sessao.get("/accounts")
    for i in response:
        results.append(Conta(archived=i['archived'],
                             created_at=i['created_at'],
                             default=i['default'],
                             description=i['description'],
                             id=i['id'],
                             name=i['name'],
                             type=i['type'],
                             updated_at=i['updated_at']
                             ))
    return results


def addConta(sessao: API, nome: str, descricao: str, default: bool, tipo: str = "checking"):
    JSON_Params = dict({
        "name": nome,
        "type": tipo,
        "description": descricao,
        "default": default
    })
    sessao.post("/accounts", params=JSON_Params)


def updConta(sessao: API, idConta: int, nome: str):
    JSON_Params = dict({
        "name": nome
    })
    sessao.put(f'/accounts/{idConta}', params=JSON_Params)


def delConta(sessao: API, idConta: int):
    sessao.delete(f'/accounts/{idConta}')


def getConta(sessao: API, idConta: int) -> Conta:
    response = sessao.get(f'/accounts/{idConta}')
    return Conta(archived=response['archived'],
                 created_at=response['created_at'],
                 default=response['default'],
                 description=response['description'],
                 id=response['id'],
                 name=response['name'],
                 type=response['type'],
                 updated_at=response['updated_at'])
