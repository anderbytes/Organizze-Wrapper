from dataclasses import dataclass

from .API import API

@dataclass
class Usuario:
    """
    Representa um usuário da plataforma Organizze.

    Attributes:
        id (int): Identificador único do usuário.
        name (str): Nome do usuário.
        email (str): Endereço de e-mail do usuário.
        role (str): Papel ou função do usuário na plataforma.
    """

    id: int
    name: str
    email: str
    role: str

    def to_dict(self):
        """ Retorna uma representação em JSON de um Usuário """
        return {"id": self.id,
                "name": self.name,
                "email": self.email,
                "role": self.role}

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


def getUsuarios(sessao: API) -> list[Usuario]:
    """
    Obtém a lista de usuários da plataforma Organizze.

    Args:
        sessao (API): Sessão autenticada para realizar chamadas à API.

    Returns:
        list[Usuario]: Uma lista de objetos `Usuario` contendo os usuários obtidos.
    """

    results = []
    response = sessao._get("/users")
    for i in response:
        results.append(Usuario(id=i['id'],
                               name=i['name'],
                               email=i['email'],
                               role=i['role']))
    return results

def getUsuario(sessao: API, idUsuario: int) -> Usuario:
    """
    Obtém as informações de um usuário específico da plataforma Organizze.

    Args:
        sessao (API): Sessão autenticada para realizar chamadas à API.
        idUsuario (int): Identificador único do usuário a ser buscado.

    Returns:
        Usuario: Um objeto `Usuario` contendo os dados do usuário obtido.
    """

    response = sessao._get(f'/users/{idUsuario}')
    return Usuario(id=response['id'],
                   name=response['name'],
                   email=response['email'],
                   role=response['role'])