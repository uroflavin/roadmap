# {{ project.title }}
{% if "logo" in project %}
<img src="{{ project.logo.filename }}" alt="{{ project.logo.copyright_notice }}"/>
{% endif -%}
{% if "description" in project %}
{{ project.description }}
{% endif -%}
{% if "visionstatement" in project %}
## Visionstatement
{{ project.visionstatement -}}
{% endif -%}
{% if "authors" in project %}
## Authors
{% for author in project.authors %}
- {{ author.name}} *{{ author.contact}}*
{% endfor %}
{% endif -%}
{%- if "timeline" in project -%}
## Importand Dates
{% for date, timelineentries in project.group.timeline_by.date.items() %}
- **{{ date }}**{% for timelineentry in timelineentries %}
    - <u>{{ timelineentry.title }}</u>
      {{ timelineentry.description -}}
{% endfor -%}
{% endfor -%}{% endif -%}
{%- if "objectives" in project -%}
## Objectives
{% for date, objectives in project.group.objectives_by.date.items() %}
{% if date != "None" %}
### {{ date }}
{% for objective in objectives %}
#### {{ objective.title}}{{ ' | ' if "state" in objective }}{{ objective.state if "state" in objective }}
{{ objective.description -}}
{% if "reference" in objective %}
- [{{ objective.reference.name if objective.reference.name != "" else objective.reference.link }}]({{ objective.reference.link -}})
{% endif -%}
{% if "todos" in objective %}
{% set todos = objective.todos %}
{% include "roadmap.todos.md" -%}
{% endif -%}
{% if "keyresults" in objective %}
##### Keyresults
{%- for keyresult in objective.keyresults -%}
###### [{{ keyresult.date if 'date' in keyresult else keyresult.id  }}] | {{ keyresult.title}} | {{keyresult.requirement}} {{ keyresult.state}}
{{ keyresult.description -}}
{% if "reference" in keyresult %}
- [{{ keyresult.reference.name if keyresult.reference.name != "" else keyresult.reference.link }}]({{ keyresult.reference.link -}})
{% endif -%}
{% if "todos" in keyresult %}
{% set todos = keyresult.todos %}
{% include "roadmap.todos.md" -%}
{% endif -%}
{% endfor -%}
{% endif %}
{% if "milestones" in objective %}
{% include "roadmap.objective.milestone.template.md" %}
{% endif %}
{% endfor %}
{% endif -%}
{% endfor %}
{% for date, objectives in project.group.objectives_by.date.items() %}
{% if date == "None" %}
{% for objective in objectives %}
### {{ objective.title}}{{ ' | ' if "state" in objective }}{{ objective.state if "state" in objective }}
{{ objective.description -}}
{% if "reference" in objective %}
- [{{ objective.reference.name if objective.reference.name != "" else objective.reference.link }}]({{ objective.reference.link -}})
{% endif -%}
{% if "todos" in objective %}
{% set todos = objective.todos %}
{% include "roadmap.todos.md" -%}
{% endif -%}
{% if "keyresults" in objective %}
#### Keyresults
{%- for keyresult in objective.keyresults -%}
##### [{{ keyresult.date if 'date' in keyresult else keyresult.id  }}] | {{ keyresult.title}} | {{keyresult.requirement}} {{ keyresult.state}}
{{ keyresult.description -}}
{% if "reference" in keyresult %}
- [{{ keyresult.reference.name if keyresult.reference.name != "" else keyresult.reference.link }}]({{ keyresult.reference.link -}})
{% endif -%}
{% if "todos" in keyresult %}
{% set todos = keyresult.todos %}
{% include "roadmap.todos.md" -%}
{% endif -%}
{% endfor -%}
{% endif %}
{% if "milestones" in objective %}
{% include "roadmap.objective.milestone.template.md" %}
{% endif %}
{% endfor %}
{% endif -%}
{% endfor %}
{% endif -%}
{% if "milestones" in project %}
{% include "roadmap.milestone.template.md" -%}
{% endif -%}