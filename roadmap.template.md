# {{ project.title }}

{{ project.description }}
## Authors
{% for author in project.authors %}
- {{ author.name}} *{{ author.contact}}*{% endfor %}

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
{% for milestone in objective.milestones %}
#### ***▶ {{ milestone.title}}**
{{ milestone.description -}}
{% if "reference" in milestone %}
- [{{ milestone.reference.name if milestone.reference.name != "" else milestone.reference.link }}]({{ milestone.reference.link -}}){% endif -%}
{% for deliverable in milestone.deliverables %}
##### 📦 **{{deliverable.requirement}}::{{ deliverable.state}}** | {{ deliverable.title}}
{{ deliverable.description -}}
{% endfor -%}
{% endfor -%}
{% endfor -%}
{% if project.milestones %}
## Milestones
{% for milestone in project.milestones %}
### **▶ {{ milestone.title}}**
{{ milestone.description -}}
{% if "reference" in milestone %}
- [{{ milestone.reference.name if milestone.reference.name != "" else milestone.reference.link }}]({{ milestone.reference.link -}}){% endif -%}
{% for deliverable in milestone.deliverables %}
#### {{ "~~" if deliverable.state == "DONE" }}📦 **{{deliverable.requirement}}::{{ deliverable.state}}** | {{ deliverable.title}}{{ "~~" if deliverable.state == "DONE" }}
{{ deliverable.description -}}
{% if "reference" in deliverable %}
- [{{ deliverable.reference.name if deliverable.reference.name != "" else deliverable.reference.link }}]({{ deliverable.reference.link -}}){% endif -%}
{% endfor -%}
{% endfor -%}
{% endif %}