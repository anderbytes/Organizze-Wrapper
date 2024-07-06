from .API import API


class Categoria:
    def __init__(self,
                 color: str,
                 id: int,
                 name: str,
                 parent_id: int
                 ):
        self.color = color
        self.id = id
        self.name = name
        self.parent_id = parent_id


def getCategorias(sessao: API) -> list[Categoria]:
    results = []
    response = sessao.get("/categories")
    for i in response:
        results.append(Categoria(color=i['color'],
                                 id=i['id'],
                                 name=i['name'],
                                 parent_id=i['parent_id']
                                 ))
    return results


def getCategoria(sessao: API, idCategoria: int) -> Categoria:
    response = sessao.get(f'/categories/{idCategoria}')
    return Categoria(color=response['color'],
                     id=response['id'],
                     name=response['name'],
                     parent_id=response['parent_id'])


def addCategoria(sessao: API, nome: str):
    JSON_Params = dict({
        "name": nome
    })
    sessao.post("/categories", params=JSON_Params)


def updCategoria(sessao: API, idCategoria: int, nome: str):
    JSON_Params = dict({
        "name": nome
    })
    sessao.put(f'/categories/{idCategoria}', params=JSON_Params)


def delCategoria(sessao: API, idCategoria: int, idNovaCategoria: int = None):
    if idNovaCategoria is not None:
        sessao.delete(f'/categories/{idCategoria}', params={'replacement_id': idNovaCategoria})
    else:
        sessao.delete(f'/categories/{idCategoria}')
