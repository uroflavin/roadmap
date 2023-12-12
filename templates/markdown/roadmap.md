# {{ project.title }}

{{ project.description }}
## Authors
{% for author in project.authors %}
- {{ author.name}} *{{ author.contact}}*
{% endfor %}
## Important Dates
{% for timelineentry in project.timeline %}
- **{{ timelineentry.date }}** | {{ timelineentry.title }}
{{ timelineentry.description -}}
{% endfor %}
## Objectives
{% for objective in project.objectives %}
### 🚀 {{ objective.title}}
{{ objective.description -}}
{% if "reference" in objective %}
- [{{ objective.reference.name if objective.reference.name != "" else objective.reference.link }}]({{ objective.reference.link -}}){% endif -%}
{% endfor -%}
{% include "roadmap.milestone.template.md" -%}

