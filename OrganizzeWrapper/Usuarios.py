from API import API


class Usuario:
    def __init__(self,
                 email: str,
                 id: int,
                 name: str,
                 role: str):
        self.email = email
        self.id = id
        self.name = name
        self.role = role


def getUsuarios(sessao: API) -> list[Usuario]:
    results = []
    response = sessao.get("/users")
    for i in response:
        results.append(Usuario(email=i['email'],
                               id=i['id'],
                               name=i['name'],
                               role=i['role']
                               ))
    return results


def getUsuario(sessao: API, idUsuario: int) -> Usuario:
    response = sessao.get(f'/users/{idUsuario}')
    return Usuario(email=response['email'], id=response['id'], name=response['name'], role=response['role'])
