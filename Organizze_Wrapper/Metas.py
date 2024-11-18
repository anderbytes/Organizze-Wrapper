from dataclasses import dataclass
from datetime import datetime

from PyMultiHelper.Validation import validateYear
from .API import API

@dataclass
class Meta:
    """
    Representa os dados de uma meta no sistema Organizze.

    Attributes:
        amount_in_cents (int): Valor da meta em centavos.
        category_id (int): Identificador único da categoria associada à meta.
        date (str): Data associada à meta no formato `YYYY-MM-DD`.
        activity_type (int): Tipo de atividade vinculada à meta.
        total (int): Total acumulado em centavos para a meta até o momento.
        predicted_total (int): Total previsto para a meta em centavos.
        percentage (str): Percentual de progresso da meta, representado como número decimal no formato `XXX.XXX`.
    """

    amount_in_cents: int
    category_id: int
    date: str  # DATE YYYY-MM-DD
    activity_type: int
    total: int
    predicted_total: int
    percentage: str  # DECIMAL - XXX.XXX

    def to_dict(self):
        """ Retorna uma representação em JSON de uma Meta """
        return {"amount_in_cents": self.amount_in_cents,
                "category_id": self.category_id,
                "date": self.date,
                "activity_type": self.activity_type,
                "total": self.total,
                "predicted_total": self.predicted_total,
                "percentage": self.percentage}

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


def getMetas(sessao: API, ano: int, mes: int = None) -> list[Meta]:
    """
    Obtém a lista de metas da plataforma Organizze para um determinado ano e, opcionalmente, mês.

    Args:
        sessao (API): Sessão autenticada para realizar chamadas à API.
        ano (int): Ano para o qual as metas serão buscadas. Deve estar no intervalo entre 1900 e o ano atual.
        mes (int, optional): Mês específico para o qual as metas serão buscadas. Deve estar no intervalo de 1 a 12. Padrão é `None`.

    Returns:
        list[Meta]: Uma lista de objetos `Meta` contendo as metas obtidas.

    Raises:
        ValueError: Se o ano informado estiver fora do intervalo permitido ou se o mês não for válido.
    """

    validateYear(ano, minYear=1900, maxYear=datetime.today().year)

    if mes and 1 <= mes <= 12:
        parametros = f"{ano}/{mes}"
    else:
        parametros = ano

    results = []
    response = sessao._get(f'/budgets/{parametros}')
    for i in response:
        results.append(Meta(amount_in_cents=i['amount_in_cents'],
                            category_id=i['category_id'],
                            date=i['date'],
                            activity_type=i['activity_type'],
                            total=i['total'],
                            predicted_total = i['predicted_total'],
                            percentage = i['percentage']))
    return results
