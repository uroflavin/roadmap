{% for milestone in objective.milestones %}
#### **▶ {{ milestone.title}}**
{{ milestone.description -}}
{% if "reference" in milestone %}
- [{{ milestone.reference.name if milestone.reference.name != "" else milestone.reference.link }}]({{ milestone.reference.link -}}){% endif -%}
{% include 'markdown.roadmap.objective.milestone.deliverable.template.md' -%}
{% endfor -%}