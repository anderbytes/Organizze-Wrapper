from datetime import datetime

from PyMultiHelper.Validation import validateYear
from .API import API


class Meta:
    def __init__(self,
                 activity_type: int,
                 amount_in_cents: int,
                 category_id: int,
                 date: str,  # DATE YYYY-MM-DD
                 id: int,
                 percentage: str,  # DECIMAL - XXX.XXX
                 predicted_total: int,
                 total: int):
        self.activity_type = activity_type
        self.amount_in_cents = amount_in_cents
        self.category_id = category_id
        self.date = date
        self.id = id
        self.percentage = percentage
        self.predicted_total = predicted_total
        self.total = total

    def __str__(self):
        return (
            f"Meta(id={self.id}, "
            f"date='{self.date}', "
            f"category_id='{self.category_id}', "
            f"activity_type='{self.activity_type}', "
            f"amount_in_cents='{self.amount_in_cents}', "
            f"percentage='{self.percentage}', "
            f"predicted_total='{self.predicted_total}', "
            f"total='{self.total}', "
        )


def getMetas(sessao: API, ano: int = 0, mes: int = 0) -> list[Meta]:
    parametros = ""
    if ano > 0:
        validateYear(ano, minYear=1900, maxYear=datetime.today().year)
        parametros = f'{ano}'
        if 1 <= mes <= 12:
            parametros = f'{parametros}/{mes}'

    results = []
    response = sessao._get(f'/budgets/{parametros}')
    for i in response:
        results.append(Meta(activity_type=i['activity_type'],
                            amount_in_cents=i['amount_in_cents'],
                            category_id=i['category_id'],
                            date=i['date'],
                            id=i['id'],
                            percentage=i['percentage'],
                            predicted_total=i['predicted_total'],
                            total=i['total']
                            ))
    return results
