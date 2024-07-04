from datetime import datetime, timedelta


def validaData(texto: str):
    try:
        from datetime import datetime
        datetime.strptime(texto, "%Y-%m-%d")
    except ValueError:
        raise ValueError("O formato da data é inválida. Formato esperado: AAAA-MM-DD")


def validaAno(numero: int, minimo: int = 1900, maximo: int = 2199):
    if not (minimo <= numero <= maximo):
        raise ValueError(f'O ano informado ({numero}) não é considerado válido (Entre {minimo} e {maximo}).')


def rangesIntervalo(data_inicio, data_fim, tamanho_intervalo=80):
    """
        Retorna uma série de ranges de 'tamanho_intervalo' dias entre as datas Início e Fim, útil para trabalhar iterativamente com métodos que tem limite de dias.

        Args:
            tamanho_intervalo (int): A quantidade máxima de dias de cada intervalo
            data_inicio (str): A data inicial real.
            data_fim (str): A data final real.

        Returns:
            list(str, str): Lista de 1+ intervalos de tamanho 'tamanho_intervalo' entre as datas inicial e final.

        Examples:
            >>> rangesIntervalo("2020-02-25", "2020-08-24", 90)
        """

    # Converte as strings de data em objetos datetime
    inicio = datetime.strptime(data_inicio, '%Y-%m-%d')
    fim = datetime.strptime(data_fim, '%Y-%m-%d')

    # Define um intervalo
    um_mes = timedelta(days=tamanho_intervalo)

    # Define a data atual como a data de início
    data_atual = inicio

    # Inicializa a lista de ranges
    ranges = []

    # Loop enquanto a data atual for menor ou igual à data final
    while data_atual <= fim:
        # Define a data de início e fim do intervalo atual
        inicio_intervalo = data_atual
        fim_intervalo = min(data_atual + um_mes - timedelta(days=1), fim)

        # Adiciona o intervalo à lista de ranges
        ranges.append((inicio_intervalo.strftime('%Y-%m-%d'), fim_intervalo.strftime('%Y-%m-%d')))

        # Adiciona um mês à data atual
        data_atual += um_mes

    # Retorna a lista de ranges
    return ranges
