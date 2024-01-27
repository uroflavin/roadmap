# {{ project.title }}
{% if "logo" in project %}
<img src="{{ project.logo.filename }}" alt="{{ project.logo.copyright_notice }}"/>
{% endif %}

{{ project.description }}

{% if "visionstatement" in project %}
## Visionstatement
{{ project.visionstatement -}}
{% endif -%}
## Authors
{% for author in project.authors %}
- {{ author.name}} *{{ author.contact}}*
{% endfor %}
{% if "timeline" in project %}
## Important Dates
{% for timelineentry in project.timeline %}
- **{{ timelineentry.date }}** | {{ timelineentry.title }}
{{ timelineentry.description -}}
{% endfor %}{% endif -%}
## Objectives
{% for objective in project.objectives %}
### {{ objective.title}}{{ ' | ' if "state" in objective }}{{ objective.state if "state" in objective }}
{{ objective.description -}}
{% if "reference" in objective %}
- [{{ objective.reference.name if objective.reference.name != "" else objective.reference.link }}]({{ objective.reference.link -}}){% endif -%}
{% if "keyresults" in objective %}
#### Keyresults
{%- set objective_id = loop.index -%} 
{%- for keyresult in objective.keyresults -%}
{% set keyresult_id = loop.index %}
##### [{{ 'R' if 'date' not in keyresult  }}{{ keyresult.date if 'date' in keyresult else keyresult_id  }}] | {{ keyresult.title}} | {{keyresult.requirement}} {{ keyresult.state}}
{{ keyresult.description -}}
{% if "reference" in keyresult %}
- [{{ keyresult.reference.name if keyresult.reference.name != "" else keyresult.reference.link }}]({{ keyresult.reference.link -}}){% endif -%}
{% endfor -%}
{% endif %}
{% if "milestones" in objective %}
{% include "roadmap.objective.milestone.template.md" %}{% endif %}
{% endfor %}
{% if "milestones" in project %}
{% include "roadmap.milestone.template.md" -%}
{% endif -%}