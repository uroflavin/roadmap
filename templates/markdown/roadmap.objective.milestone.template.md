#### Milestones
{% for milestone in objective.milestones %}
##### {{ milestone.title}}{{ ' | ' if "state" in milestone }}{{ milestone.state}}
{{ milestone.description -}}
{% if "reference" in milestone %}
- [{{ milestone.reference.name if milestone.reference.name != "" else milestone.reference.link }}]({{ milestone.reference.link -}}){% endif -%}
{% if "todos" in milestone %}
{% set todos = milestone.todos %}
{% include "roadmap.todos.md" -%}
{% endif -%}
{% include 'roadmap.objective.milestone.deliverable.template.md' -%}
{% endfor -%}