import requests
from requests import Session, HTTPError
from requests.auth import HTTPBasicAuth

from OrganizzeWrapper.auxiliar import validaEmail

API_URL = "https://api.organizze.com.br/rest/v2"


class API:

    def __init__(self, email: str, token: str, autor: str = "SemNome"):
        """
        Args:
            email (str): Seu email da conta do Organizze, utilizado para gerar o user-agent e autenticação.
            token (str): Seu token gerado em https://app.organizze.com.br/configuracoes/api-keys
            autor (str): Seu primeiro nome, utilizado para gerar o user-agent da consulta

        Returns:
            API: Objeto API com a conexão estabelecida e utilizável.

        Raises:
            TypeError: Se o argumento 'email' fornecido não for uma string.
            ValueError: Se o argumento 'email' fornecido for uma string vazia ou no formato incorreto.
            SyntaxError: Erro se os parâmetros de email e token não forem válidos dentro do Organizze.com.br
        """

        """
        Validações
        """
        validaEmail(email)

        """
        Execução
        """
        self.email = email
        self.token = token
        self.autor = autor
        self.sessao = requests.Session()

        self.sessao.auth = HTTPBasicAuth(self.email, self.token)
        self.sessao.headers.update({'User-Agent': f'{self.autor} ({self.email})',
                                    'Content-Type': 'application/json; charset=utf-8'})

    def get(self, comando: str, params: dict = None):
        response = self.sessao.get(f'{API_URL}{comando}', params=params)
        if response.status_code == 401:
            raise HTTPError("Erro 401: Não autorizado. Verifique suas credenciais fornecidas do Organizze")
        else:
            return response.json()


    def post(self, comando: str, params: dict = None):
        self.sessao.post(f'{API_URL}{comando}', params=params)

    def put(self, comando: str, params: dict = None):
        self.sessao.put(f'{API_URL}{comando}', params=params)

    def delete(self, comando: str, params: dict = None):
        self.sessao.delete(f'{API_URL}{comando}', params=params)
