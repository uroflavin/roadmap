## Milestones
{% for milestone in project.milestones %}
{% if "id" in milestone  -%}
{% set milestone_id = milestone.id -%}
{% else -%}
{% set milestone_id = "M" + loop.index | string -%}
{% endif -%}
### #{{ milestone_id }} | {{ milestone.title}}{{ ' | ' if "state" in milestone }}{{ milestone.state}}
{{ milestone.description -}}
{% if "reference" in milestone %}
- [{{ milestone.reference.name if milestone.reference.name != "" else milestone.reference.link }}]({{ milestone.reference.link -}}){% endif -%}
{% if "todos" in milestone %}
{% set todos = milestone.todos %}
{% include "roadmap.todos.md" -%}
{% endif -%}
{% include 'roadmap.milestone.deliverable.template.md' -%}
{% endfor -%}
