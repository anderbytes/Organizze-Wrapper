import requests
from requests.auth import HTTPBasicAuth

API_URL = "https://api.organizze.com.br/rest/v2"


class API:

    def __init__(self, email: str, token: str, autor: str = "SemNome"):
        self.email = email
        self.token = token
        self.autor = autor
        self.sessao = requests.Session()
        self.sessao.auth = HTTPBasicAuth(self.email, self.token)
        self.sessao.headers.update({'User-Agent': f'{self.autor} ({self.email})',
                                    'Content-Type': 'application/json; charset=utf-8'})

    def get(self, comando: str, params: dict = None):
        return self.sessao.get(f'{API_URL}{comando}', params=params).json()

    def post(self, comando: str, params: dict = None):
        self.sessao.post(f'{API_URL}{comando}', params=params)

    def put(self, comando: str, params: dict = None):
        self.sessao.put(f'{API_URL}{comando}', params=params)

    def delete(self, comando: str, params: dict = None):
        self.sessao.delete(f'{API_URL}{comando}', params=params)
