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
{% for milestone in objective.milestones %}
#### ***▶ {{ milestone.title}}**
{{ milestone.description -}}
{% for deliverable in milestone.deliverables %}
##### 📦 **{{deliverable.requirement}}::{{ deliverable.state}}** | {{ deliverable.title}}
{{ deliverable.description -}}
{% endfor %}
{% endfor %}
{% endfor %}
{% if project.milestones %}
## Milestones
{% for milestone in project.milestones %}
### **▶ {{ milestone.title}}**
{{ milestone.description -}}
{% for deliverable in milestone.deliverables %}
#### {{ "~~" if deliverable.state == "DONE" }}📦 **{{deliverable.requirement}}::{{ deliverable.state}}** | {{ deliverable.title}}{{ "~~" if deliverable.state == "DONE" }}
{{ deliverable.description -}}
{% endfor %}
{% endfor %}
{% endif %}