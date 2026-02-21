# What is WSJF

WSJF is a prioritization method that helps to identify the greatest possible value of a planned result in relation to its effort.

In addition to pure prioritization, WSJF is also useful to gain further insight into customer benefits, existing risks or simply to understand the work involved in implementing the roadmap.

The formula for WSJF is relatively simple:

WSJF = CoD(Cost of Delay) / Job Size

The higher the WSJF, the higher the priority - the sooner something should be ready...

## Cost Of Delay (CoD)

In simple terms, CoD provides information on how much value is lost if a job is delayed or not performed at all at a certain time. 
A well-known agile framework defines CoD as a measure of the economic value of a job over time.

Cost of Delay is determined by 3 values which, when added together, give the CoD:

### User Value and Business Value

A statement on how much the customer (user value) or the company (business value) benefits from the result.

### Time Criticality

Are there fixed deadlines for certain results, e.g. because there are assurances to partners or customers, contractual agreements or legal deadlines? Is there a risk that the value can no longer be achieved if the deadline is not met?
Will a possible completion in a few months still have the same value as today?

### Opportunity enablement or risk reduction

By achieving the result, are we building up certain technical or specialist skills from which we will benefit later in the implementation or which will allow us to achieve certain later results more easily or at all?
Are there risks that are minimized by achieving a certain result?

## Jobsize

The job size is an approximation of the expected effort or a statement about how long it takes to deliver the value for a delivery object, result or milestone.
In the original formulation of the WSJF method, it is assumed that a permanent team is working permanently on the implementation. Ideally, the job size is estimated with the teams concerned.

Under these conditions, the time required to implement a project is a valid approximation of the effort involved.

The job size can be estimated in various dimensions:
- Effort of the teams
- Complexity of the implementation
- other, e.g. external costs if results are provided externally. These can also be dependencies that are taken into account in the jobsize.

# Clarifying the meaning of WSJF for roadmap.py

It is important to understand that roadmap.py is not a real tool for the implementation of WSJF, but provides a place where the information is kept and displayed together consistently.

The implementation of WSJF usually requires several moderated meetings with stakeholders and the teams, whereby the relevant information regarding the results to be achieved is included in the roadmap and the results of the workshops are also recorded in the roadmap.

For the implementation, you can either start with an easily estimable average result or first commit to the extreme (lowest effort, highest effort or similar).

The relevant support for WSJF that roadmap.py offers, is to provide the necessary parameters for CoD and WSJF and to calculate them on the basis of the information in roadmap.yml and to aggregate them to the higher-level objects - if they are not stored there.

The roadmap.yml structure derived from the schema is supplemented by the following optional elements (under quantifiers)

```
quantifiers:
- <...>
- weighted_shortest_job_first: range from 0 to 30 as floating point number
- cost_of_delay: range from 0 to 30 as whole number
- user_business_value: range from 0 to 10 as whole number
- time_criticality: range from 0 to 10 as whole number
- opportunity_enablement_or_risk_reduction: range from 0 to 10 as whole number
- jobsize: minimum 1 (no upper limit) as whole number
```

The default value from schema/roadmap.json is NULL for all dimensions and **all given ranges are inclusive!**

**Keep in mind:** 
If you realy need a Jobsize of 0, think twice if you really have to present this in your roadmap. To make your life easier, it is simply not allowed from schema and validation will fail if you use it.
Technically: division by zero will cause errors, so we can't support this.

This also means that no matter in which dimension you look at the job size with the teams, there is only one value that is kept in roadmap.yml. 
It does not matter for the calculation whether you estimate in relative or absolute terms - what is relevant is that your estimate result can be sorted on a scale from 0 to 10.

None of the values are required from schema/roadmap.json Just leave them empty until you know.
Normally you find out the parameters with different people in different meetings.

## Calculating WSJF and using in templates

*weighted_shortest_job_first* and *cost_of_delay* are both calculated during rendering, under the following condtions:

**cost_of_delay**, is only calculated if cost_of_delay is empty AND if user_business_value,time_criticality, opportunity_enablement_or_risk_reduction are not empty

**weighted_shortest_job_first**, is only calculated if weighted_shortest_job_first is empty AND if both jobsize AND cost_of_delay are not empty

The order of calculating is *cost_of_delay*  -> *weighted_shortest_job_first*.

This means you can either enter weightet shortet job first and cost_of_delay yourself into your roadmap.yml or left the calculation to roadmap.py.
In addition, you can set cost_of_delay in roadmap.yml according to your needs and let roadmap.py calculate weighted_shortest_job_first using your given value and your given jobsize.

But every calculation requires validity!

The ```quantifier.*``` are available in the templates ```project.*``` structure.

The output takes place in the csv, markdown and HTML templates

# A few more personal things

From my own experience, WSJF is not suitable for building a roadmap based on this criterion alone. 

There are 3 key lessons that I would like to share:
- Jobsize becomes less meaningful the further a task is in the future.
- Stakeholders are usually overoptimistic when assigning business value the further in the future a result is or the more it serves their own interests.
- Stakeholders push for more "resources" if something has a higher value for them. However, this behavior is at odds with what jobsize requires: stable teams.

WSJF offers helpful insights and the method is certainly suitable for prioritizing the delivery objects of an individual milestone. 

However, the greater the abstraction or the further into the future a task lies, the less reliable the significance of the WSJF becomes.

As a rule, risks are weighted more heavily in the job size by the teams the further into the future something is or the larger the scope of something appears to be. 

This behavior can naturally be explained by the fact that a view into the future is only ever possible on the basis of current knowledge and only for the period of time that is somehow tangible for the teams. 
But: for many things, the code base for the next step is simply not even available in the teams during the process of drawing up a roadmap. Nevertheless, WSJF can be used as one of many indicators for planning and prioritization.

On the other hand, stakeholders tend to estimate the value of certain things much higher than they actually will be - and to the same extent, the further away something is in the future.

My personal opinion is that teams are reluctant to take risks that could fall on their feet over time (i.e. they tend to overestimate the job size). 

Stakeholders, especially from the business, are also usually overoptimistic when it comes to assigning business value.
Stakeholders are also much more willing to put more "resources" into something they believe in - in order to move forward "faster". However, this behavior is at odds with what Jobsize requires: stable teams.

In my opinion, the way out of this dilemma lies in the following premises:
- **Focus on small delivery objects**, these are easier for the teams to grasp and provide greater validity.
- **Validate your assumptions retrospectively**: Retrospective look at the WSJF dimensions after achieving deliverables: Were the assumptions correct? What can we learn for future estimates? 
- **Regular repetition**: Use the experience gained during the processing of the roadmap: regular repetition of WSJF, ideally after each milestone or delivery object has been reached
- **Risk disclosure**: Transparent stakeholder communication: make it clear to those involved what WSJF can/can't achieve. Explain the risks inherent in the method and the significance of WSJF 

Ideally, you should refrain from making any commitments to stakeholders from the WSJF for anything that lies within an unmanageable time horizon for the teams. But the world is complex...

It is better to commit with your stakeholders to certain objectives that are manageable in terms of time and leave the setting up of milestones and delivery objects to the teams.