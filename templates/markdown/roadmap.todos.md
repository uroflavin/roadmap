##### TODO

{% for todo in todos %}
- [{{ 'X' if todo.state == 'CLOSED' else ' ' }}] {{ todo.title }}
{{ todo.description -}}
{% endfor -%}