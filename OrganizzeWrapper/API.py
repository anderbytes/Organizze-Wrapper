import requests
from requests import HTTPError
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

    def _get(self, comando: str, params: dict = None):
        try:
            response = self.sessao.get(f'{API_URL}{comando}', params=params)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.HTTPError as erroHTTP:
            if response.status_code == 401:
                raise HTTPError("Erro HTTP 401: Não autorizado. Verifique as credenciais fornecidas do Organizze")
            else:
                raise HTTPError(f"Erro HTTP: {erroHTTP}")

        except requests.exceptions.RequestException as requestERROR:
            raise HTTPError(f"Ocorreu um erro durante a requisição: {requestERROR}")

    def _post(self, comando: str, params: dict = None):
        try:
            response = self.sessao.post(f'{API_URL}{comando}', params=params)
            response.raise_for_status()

        except requests.exceptions.HTTPError as erroHTTP:
            if response.status_code == 401:
                raise HTTPError("Erro HTTP 401: Não autorizado. Verifique as credenciais fornecidas do Organizze")
            else:
                raise HTTPError(f"Erro HTTP: {erroHTTP}")

        except requests.exceptions.RequestException as requestERROR:
            raise HTTPError(f"Ocorreu um erro durante a requisição: {requestERROR}")


    def _put(self, comando: str, params: dict = None):
        try:
            response = self.sessao.put(f'{API_URL}{comando}', params=params)
            response.raise_for_status()

        except requests.exceptions.HTTPError as erroHTTP:
            if response.status_code == 401:
                raise HTTPError("Erro HTTP 401: Não autorizado. Verifique as credenciais fornecidas do Organizze")
            else:
                raise HTTPError(f"Erro HTTP: {erroHTTP}")

        except requests.exceptions.RequestException as requestERROR:
            raise HTTPError(f"Ocorreu um erro durante a requisição: {requestERROR}")


    def _delete(self, comando: str, params: dict = None):
        try:
            response = self.sessao.delete(f'{API_URL}{comando}', params=params)
            response.raise_for_status()

        except requests.exceptions.HTTPError as erroHTTP:
            if response.status_code == 401:
                raise HTTPError("Erro HTTP 401: Não autorizado. Verifique as credenciais fornecidas do Organizze")
            else:
                raise HTTPError(f"Erro HTTP: {erroHTTP}")

        except requests.exceptions.RequestException as requestERROR:
            raise HTTPError(f"Ocorreu um erro durante a requisição: {requestERROR}")
