**_Quantifiers_**
{{  "- **_Weighted Shortest Job First_: " + '%.2f' % quantifiers.weighted_shortest_job_first + "**" if 'weighted_shortest_job_first' in quantifiers and quantifiers.weighted_shortest_job_first != None }}
{{  "- _Jobsize_: " + quantifiers.jobsize|string if 'jobsize' in quantifiers and quantifiers.jobsize != None }}
{{  "- _Cost of Delay_: " + quantifiers.cost_of_delay|string if 'cost_of_delay' in quantifiers and quantifiers.cost_of_delay != None }}
{{  "- _User Value / Business Value_: " + quantifiers.user_business_value|string if 'jobsize' in quantifiers and quantifiers.jobsize != None }}
{{  "- _Time Criticality_: " + quantifiers.time_criticality|string if 'time_criticality' in quantifiers and quantifiers.time_criticality != None }}
{{  "- _Opportunity Enablement / Risk Reduction_: " + quantifiers.opportunity_enablement_or_risk_reduction|string if 'opportunity_enablement_or_risk_reduction' in quantifiers and quantifiers.opportunity_enablement_or_risk_reduction != None }}