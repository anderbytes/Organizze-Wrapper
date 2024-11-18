from dataclasses import dataclass

from .API import API


@dataclass
class Conta:
    """
    Representa uma conta no sistema.

    Attributes:
        id (int): Identificador único da conta.
        name (str): Nome da conta.
        description (str): Descrição da conta.
        type (str): Tipo da conta.
        default (bool): Indica se a conta é a padrão.
        archived (bool): Indica se a conta está arquivada.
        created_at (str): Data de criação da conta, no formato ISO (YYYY-MM-DD).
        updated_at (str): Data da última atualização da conta, no formato ISO (YYYY-MM-DD).
    """

    id: int
    name: str
    description: str
    type: str
    default: bool
    archived: bool
    created_at: str  # DATE ISO FORMAT
    updated_at: str  # DATE ISO FORMAT

    def to_dict(self):
        """ Retorna uma representação em JSON de uma Conta """
        return {"id": self.id,
                "name": self.name,
                "description": self.description,
                "type": self.type.value,
                "default": self.default,
                "archived": self.archived,
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

def getContas(sessao: API) -> list[Conta]:
    """
    Recupera a lista de todas as contas.

    Args:
        sessao (API): A instância da sessão da API usada para a requisição.

    Returns:
        list[Conta]: Uma lista de instâncias da classe `Conta` com os detalhes de todas as contas.
    """

    results = []
    response = sessao._get("/accounts")
    for i in response:
        # Contas sem 'type' provavelmente são inconsistências e devem ser ignoradas
        if "type" not in i: continue

        results.append(Conta(id=i['id'],
                             name=i['name'],
                             description=i['description'],
                             type=i['type'],
                             default=i['default'],
                             archived=i['archived'],
                             created_at=i['created_at'],
                             updated_at=i['updated_at']))
    return results

def getConta(sessao: API, idConta: int) -> Conta:
    """
    Recupera os detalhes de uma conta pelo seu ID.

    Args:
        sessao (API): A instância da sessão da API usada para a requisição.
        idConta (int): O identificador único da conta.

    Returns:
        Conta: Uma instância da classe `Conta` contendo os detalhes da conta.
    """

    response = sessao._get(f'/accounts/{idConta}')
    return Conta(id=response['id'],
                 name=response['name'],
                 description=response['description'],
                 type=response['type'],
                 default=response['default'],
                 archived=response['archived'],
                 created_at=response['created_at'],
                 updated_at=response['updated_at'])

def delConta(sessao: API, idConta: int):
    """
    Exclui uma conta específica.

    Args:
        sessao (API): A instância da sessão da API usada para a requisição.
        idConta (int): O ID da conta a ser excluída.
    """

    sessao._delete(f'/accounts/{idConta}')

def addConta(sessao: API, nome: str, descricao: str, default: bool, tipo: str):
    """
    Adiciona uma nova conta bancária ou de poupanças.

    Args:
        sessao (API): A instância da sessão da API usada para a requisição.
        nome (str): O nome da conta.
        descricao (str): A descrição da conta.
        default (bool): Indica se a conta é a conta padrão.
        tipo (str): O tipo da conta, deve ser 'checking', 'savings' ou 'other'.
    """

    # TODO: "Parâmetro tipo precisa de validação: checking ou outro"

    JSON_Params: dict = {
        "name": nome,
        "type": tipo,
        "description": descricao,
        "default": default
    }
    sessao._post("/accounts", params=JSON_Params)

def updConta(sessao: API, idConta: int, nome: str):
    """
    Atualiza uma conta existente.

    Args:
        sessao (API): A instância da sessão da API usada para a requisição.
        idConta (int): O identificador único da conta a ser atualizada.
        nome (str): O novo nome para a conta.
    """

    # TODO: "Incompleta. Mais testes"

    JSON_Params: dict = {
        "name": nome
    }
    sessao._put(f'/accounts/{idConta}', params=JSON_Params)