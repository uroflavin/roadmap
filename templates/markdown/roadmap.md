# {{ project.title }}

{{ project.description }}

{% if "visionstatement" in project %}
## Visionstatement
{{ project.visionstatement -}}
{% endif -%}
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
### 🚀 {{ objective.state}} | {{ objective.title}}
{{ objective.description -}}
{% if "reference" in objective %}
- [{{ objective.reference.name if objective.reference.name != "" else objective.reference.link }}]({{ objective.reference.link -}}){% endif -%}
{% if "keyresults" in objective %}
{% set objective_id = loop.index %} 
{% for keyresult in objective.keyresults %}
{% set keyresult_id = loop.index %}
#### {{ "~~" if keyresult.state == "DONE" }}[{{ 'R' if 'date' not in keyresult  }}{{ keyresult.date if 'date' in keyresult else keyresult_id  }}] **{{keyresult.requirement}}::{{ keyresult.state}}** | {{ keyresult.title}}{{ "~~" if keyresult.state == "DONE" }}
{{ keyresult.description -}}
{% if "reference" in keyresult %}
- [{{ keyresult.reference.name if keyresult.reference.name != "" else keyresult.reference.link }}]({{ keyresult.reference.link -}}){% endif -%}
{% endfor -%}
{% endif -%}
{% endfor -%}
 {% if "milestones" in project %}
{% include "roadmap.milestone.template.md" -%}
{% endif -%}