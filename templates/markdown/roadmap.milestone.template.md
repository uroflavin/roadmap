{% if "milestones" in project %}
## Milestones
{% for milestone in project.milestones %}

### {{ milestone.title}}{{ ' | ' if "state" in milestone }}{{ milestone.state}}
{{ milestone.description -}}
{% if "reference" in milestone %}
- [{{ milestone.reference.name if milestone.reference.name != "" else milestone.reference.link }}]({{ milestone.reference.link -}}){% endif -%}
{% include 'roadmap.milestone.deliverable.template.md' -%}
{% endfor -%}
{% endif -%}