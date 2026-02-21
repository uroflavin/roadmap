**_Quantifiers_**
{%- if 'weighted_shortest_job_first' in quantifiers and quantifiers.weighted_shortest_job_first != None %}
- **_Weighted Shortest Job First_: {{ '%.2f' % quantifiers.weighted_shortest_job_first }}**
{%- endif %}
{%- if 'jobsize' in quantifiers and quantifiers.jobsize != None %}
- _Jobsize_: {{ quantifiers.jobsize }}
{%- endif %}
{%- if 'cost_of_delay' in quantifiers and quantifiers.cost_of_delay != None %}
- _Cost of Delay_: {{ quantifiers.cost_of_delay }}
{%- endif %}
{%- if 'user_business_value' in quantifiers and quantifiers.user_business_value != None %}
- _User Value / Business Value_: {{ quantifiers.user_business_value }}
{%- endif %}
{%- if 'time_criticality' in quantifiers and quantifiers.time_criticality != None %}
- _Time Criticality_: {{ quantifiers.time_criticality }}
{%- endif %}
{%- if 'opportunity_enablement_or_risk_reduction' in quantifiers and quantifiers.opportunity_enablement_or_risk_reduction != None %}
- _Opportunity Enablement / Risk Reduction_: {{ quantifiers.opportunity_enablement_or_risk_reduction }}
{%- endif %}
