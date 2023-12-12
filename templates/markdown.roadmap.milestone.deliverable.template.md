{% for deliverable in milestone.deliverables %}
#### {{ "~~" if deliverable.state == "DONE" }}📦 **{{deliverable.requirement}}::{{ deliverable.state}}** | {{ deliverable.title}}{{ "~~" if deliverable.state == "DONE" }}
{{ deliverable.description -}}
{% if "reference" in deliverable %}
- [{{ deliverable.reference.name if deliverable.reference.name != "" else deliverable.reference.link }}]({{ deliverable.reference.link -}})
{% endif -%}
{% endfor -%}