{% for deliverable in milestone.deliverables %}
{% set deliverable_id = loop.index %}
#### [{{ 'R' if 'date' not in deliverable  }}{{ deliverable.date if 'date' in deliverable else deliverable_id  }}] | {{ deliverable.title}} | {{deliverable.requirement}} {{ deliverable.state}}
{{ deliverable.description -}}
{% if "reference" in deliverable %}
- [{{ deliverable.reference.name if deliverable.reference.name != "" else deliverable.reference.link }}]({{ deliverable.reference.link -}})
{% endif -%}
{% if "todos" in deliverable %}
{% set todos = deliverable.todos %}
{% include "roadmap.todos.md" -%}
{% endif -%}
{% endfor -%}