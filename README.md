# Organizze Wrapper

Esta biblioteca servirá de apoio para utilização da API do Organizze (www.organizze.com.br).

## Instalação

Use o gerenciador 'pip' para instalação do pacote.

```bash
pip install organizze-wrapper
```

## Uso

Para utilização da API, primeiramente você deve gerar uma chave de API em sua conta no Organizze, neste [link](https://app.organizze.com.br/configuracoes/api-keys).

Para seu código, seguem alguns exemplos de comandos: 

```python
from OrganizzeWrapper.API import API

# Inicializar a sessão
conn = API(email="seu_email_do_Organizze", token="token gerado no Organizze", autor="Seu_primeiro_nome")

# Listar as categorias existentes
from OrganizzeWrapper.Categorias import getCategorias

for cat in getCategorias(conn):
    print(cat)
    
# Listar os lançamentos de Junho de 2024
from OrganizzeWrapper.Lancamentos import getLancamentos

for lanc in getLancamentos(conn, dataInicio="2024-06-01", dataFim="2024-06-30"):
    print(lanc)

# Atualizar o lançamento de 'id' 7353025510 para o valor de R$ 445,99 (como despesa)
from OrganizzeWrapper.Lancamentos import updLancamento

updLancamento(conn, idLancamento=7353025510, JSON_params={'amount_cents': -44599})


```

A documentação de referência da API oficial da Organizze se encontra em:
https://github.com/organizze/api-doc

## Contribuindo

Pull requests são bem-vindos, principalmente para correção de bugs ou sugestão de melhoria na documentação.

Para grandes mudanças, sugiro abrir um 'issue' previamente para discussão.

Quer ajudar?
- Precisamos melhorar a documentação (mais detalhamentos e exemplos)
- Precisamos de métodos mais granulares para atualizar campos específicos (e não depender apenas de JSON_Params)

Sou um desenvolvedor 'solo' nas horas vagas, então sejam pacientes 😉

## Publicação

Este projeto está publicado em:
- GitHub: https://github.com/anderbytes/Organizze-Wrapper
- PyPi: https://pypi.org/project/Organizze-Wrapper/

## Licença

[GPLv3](https://gplv3.fsf.org/)