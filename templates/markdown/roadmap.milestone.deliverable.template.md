{% for deliverable in milestone.deliverables %}
#### [{{ deliverable.date if 'date' in deliverable else deliverable.id  }}] | {{ deliverable.title}} | {{deliverable.requirement}} {{ deliverable.state}}
{{ deliverable.description -}}
{% if "reference" in deliverable %}
- [{{ deliverable.reference.name if deliverable.reference.name != "" else deliverable.reference.link }}]({{ deliverable.reference.link -}})
{% endif -%}
{% if "todos" in deliverable %}
{% set todos = deliverable.todos %}
{% include "roadmap.todos.md" -%}
{% endif -%}
{% endfor -%}