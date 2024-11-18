from dataclasses import dataclass

from .API import API
from PyMultiHelper.Validation import matchesRegex

@dataclass
class Categoria:
    """
    Representa uma categoria no Organizze.

    Attributes:
        id (int): O identificador único da categoria.
        name (str): O nome da categoria.
        color (str): A cor associada à categoria.
        parent_id (int): O identificador da categoria pai, se houver.
    """

    id: int
    name: str
    color: str
    parent_id: int

    def to_dict(self):
        """ Retorna uma representação em JSON de uma Categoria """
        return {"id": self.id,
                "name": self.name,
                "color": self.color,
                "parent_id": self.parent_id}

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

def getCategorias(sessao: API) -> list[Categoria]:
    """
    Obtém todas as categorias do Organizze.

    Args:
        sessao (API): Uma instância da sessão API para permitir requisições.

    Returns:
        list[Categoria]: Uma lista de objetos Categoria em sua conta Organizze.
    """

    results = []
    response = sessao._get("/categories")
    for i in response:
        results.append(Categoria(id=i['id'],
                                 name=i['name'],
                                 color=i['color'],
                                 parent_id=i['parent_id']))
    return results

def getCategoria(sessao: API, idCategoria: int) -> Categoria:
    """
    Obtém uma categoria específica pelo seu ID.

    Args:
        sessao (API): Uma instância da sessão API para permitir requisições.
        idCategoria (int): O ID da categoria a ser obtida.

    Returns:
        Categoria: Um objeto Categoria representando a categoria encontrada.
    """

    response = sessao._get(f'/categories/{idCategoria}')
    return Categoria(id=response['id'],
                     name=response['name'],
                     color=response['color'],
                     parent_id=response['parent_id'])

def addCategoria(sessao: API, nome: str, categoriaPai: int = None) -> None:
    """
    Adiciona uma nova categoria ao Organizze.

    Args:
        sessao (API): Uma instância da sessão API para permitir requisições.
        nome (str): O nome da nova categoria a ser adicionada.
        categoriaPai (int, optional): id da categoria Pai desta. Não especificar implicará em ser um categoria raiz.
    """

    JSON_Params: dict = {
        "name": nome,
        "parent_id": categoriaPai
    }
    sessao._post("/categories", params=JSON_Params)

def updCategoria(sessao: API, idCategoria: int, nome: str = None, categoriaPai: int = None) -> None:
    """
    Atualizar os dados de um categoria no Organizze.

    Args:
        sessao (API): Uma instância da sessão API para permitir requisições.
        idCategoria (int): o id da Categoria a ser editada.
        nome (str, optional): o novo nome da categoria.
        categoriaPai (int, optional): a categoria pai, caso seja necessário.
    """

    JSON_Params: dict = {
        "name": nome,
        "parent_id": categoriaPai
    }

    sessao._put(f'/categories/{idCategoria}', params=JSON_Params)

def delCategoria(sessao: API, idCategoria: int, idNovaCategoria: int = None) -> None:
    """
    Deleta uma categoria no Organizze.

    Args:
        sessao (API): Uma instância da sessão API para permitir requisições.
        idCategoria (int): O id da categoria a ser excluída.
        idNovaCategoria (int, optional): o id da categoria Pai para onde os lançamentos da excluída serão movidos.

    Raises:
        HTTPError 404: A categoria citada não foi encontrada
        HTTPError 500: Erro interno de processamento

    Warnings:
        Bug Conhecido: A API atual possui um bug onde caso o replacement_id não seja especificado, pode ocorrer erro HTTP 500 na API.
    """

    if idNovaCategoria is not None:
        sessao._delete(f'/categories/{idCategoria}', params={'replacement_id': idNovaCategoria})
    else:
        sessao._delete(f'/categories/{idCategoria}')

# OPERAÇÕES CUSTOMIZADAS

def filtraCategorias(categorias: list[Categoria], nomeBuscado: str, usaRegex: bool = False) -> list[Categoria]:
    """
    Filtra uma lista de categorias com base em uma string de busca ou padrão regex.

    Args:
        categorias (list[Categoria]): A lista de objetos `Categoria` a ser filtrada.
        nomeBuscado (str): A string ou padrão regex para comparar com os nomes das categorias.
        usaRegex (bool, optional): Se `True`, utiliza correspondência com regex. Se `False`, realiza uma busca por substring, ignorando diferenças de maiúsculas e minúsculas. Padrão é `False`.

    Returns:
        list[Categoria]:
            Uma lista de objetos `Categoria` que atendem aos critérios de busca.
    """

    results: list[Categoria] = []

    for c in categorias:
        considera = False
        if usaRegex:
            if matchesRegex(c.name, nomeBuscado):
                considera = True
        else:
            if nomeBuscado.upper() in c.name.upper():
                considera = True

        if considera:
            results.append(c)

    return results