Наши тарифы:
{% for sbp in subscriptions %}
id тарифа: {{sbp.id}}
Описание: {{sbp.description}}
Количество запросов: {{sbp.count_request}}
Стоимость: {{sbp.amount}}
Количество месяцев: {{sbp.count_month}}
Количество недель: {{sbp.count_week}}
Количество дней: {{sbp.count_day}}

{%endfor%}
