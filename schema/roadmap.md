# JSON Schema

*A roadmap represents a high-level plan for your project or team.*

## Properties

- <a id="properties/title"></a>**`title`** *(string, required)*: A brief title which describes this roadmap.
- <a id="properties/description"></a>**`description`** *(string)*: A markdown formatted description of what this roadmap represents and any additional context which may be useful to a reader.
- <a id="properties/logo"></a>**`logo`** *(object)*: A path to your project logo. This might be a good brand for your roadmap.Best fit would be some small-icon.
  - <a id="properties/logo/properties/filename"></a>**`filename`** *(string, required)*: Your logo MUST placed where your roadmap.yml lives.
  - <a id="properties/logo/properties/copyright_notice"></a>**`copyright_notice`** *(string)*: If there is any copyright-notice, this would be rendered as alt-text.
- <a id="properties/visionstatement"></a>**`visionstatement`** *(string)*: A markdown formatted project pr product visionstatement. A product vision describes the ideal product from the customer's perspective. The leitmotif of a product vision is therefore the question of how the product can optimally address and solve the customer's problem or needs.
- <a id="properties/authors"></a>**`authors`** *(array, required)*: A list of authors who were/are involved in the creation of the roadmap.
  - <a id="properties/authors/items"></a>**Items**: Refer to *[#/definitions/Author](#definitions/Author)*.
- <a id="properties/releases"></a>**`releases`** *(array)*: A list of releases which provide enhancements in the form of deliverables to the stakeholders.
  - <a id="properties/releases/items"></a>**Items**: Refer to *[#/definitions/Release](#definitions/Release)*.
- <a id="properties/timeline"></a>**`timeline`** *(array)*: The list of important dates which relate to this roadmap.
  - <a id="properties/timeline/items"></a>**Items**: Refer to *[#/definitions/TimelineMarker](#definitions/TimelineMarker)*.
- <a id="properties/objectives"></a>**`objectives`** *(array, required)*: The list of objectives which the team is working towards over the course of this roadmap.
  - <a id="properties/objectives/items"></a>**Items**: Refer to *[#/definitions/Objective](#definitions/Objective)*.
- <a id="properties/milestones"></a>**`milestones`** *(array)*: The list of milestones which act as indicators of progress for this roadmap.
  - <a id="properties/milestones/items"></a>**Items**: Refer to *[#/definitions/Milestone](#definitions/Milestone)*.
## Definitions

- <a id="definitions/Author"></a>**`Author`** *(object)*: The details of an author responsible for this roadmap, in case a reader has questions.
  - <a id="definitions/Author/properties/name"></a>**`name`** *(string, required)*: The full name of the author.
  - <a id="definitions/Author/properties/contact"></a>**`contact`** *(string, required)*: The contact address for the author - usually their email, but may also be an IM handle or otherwise.

  Examples:
  ```yaml
  name: John Doe
  contact: john.doe@example.com
  ```

- <a id="definitions/TimelineMarker"></a>**`TimelineMarker`** *(object)*: An important date which relates to this roadmap.
  - <a id="definitions/TimelineMarker/properties/date"></a>**`date`** *(string, format: date, required)*: The date that this timeline marker is associated with.
  - <a id="definitions/TimelineMarker/properties/title"></a>**`title`** *(string, required)*: A brief name associated with this timeline marker to describe it.
  - <a id="definitions/TimelineMarker/properties/description"></a>**`description`** *(string)*: A markdown formatted description of what this timeline marker represents, or additional context associated with it.

  Examples:
  ```yaml
  date: '2023-01-15'
  title: Something really important happens
  description: Something really important happens on this date and we will all become
      lucky people
  ```

- <a id="definitions/Objective"></a>**`Objective`** *(object)*: An objective describes a high level goal for the team. It is usually something that will be worked towards over several milestones and might not have a clear definition of done.
  - <a id="definitions/Objective/properties/title"></a>**`title`** *(string, required)*: A brief name associated with this objective which describes the intended outcome.
  - <a id="definitions/Objective/properties/description"></a>**`description`** *(string)*: A markdown formatted description of what this objective represents and how it influences the direction that the team is moving in.
  - <a id="definitions/Objective/properties/date"></a>**`date`** *(string, format: date)*: The date that this objective should or is reached.
  - <a id="definitions/Objective/properties/state"></a>**`state`**: Refer to *[#/definitions/ObjectiveState](#definitions/ObjectiveState)*.
  - <a id="definitions/Objective/properties/reference"></a>**`reference`**: Refer to *[#/definitions/Reference](#definitions/Reference)*.
  - <a id="definitions/Objective/properties/milestones"></a>**`milestones`** *(array)*: The list of milestones which act as indicators of progress for this objective.
    - <a id="definitions/Objective/properties/milestones/items"></a>**Items**: Refer to *[#/definitions/Milestone](#definitions/Milestone)*.
  - <a id="definitions/Objective/properties/keyresults"></a>**`keyresults`** *(array)*: The list of key-results which make up this Objective. Key-Results usually map to specific pieces of work which may be delegated to a member of your team.
    - <a id="definitions/Objective/properties/keyresults/items"></a>**Items**: Refer to *[#/definitions/Keyresult](#definitions/Keyresult)*.
  - <a id="definitions/Objective/properties/todos"></a>**`todos`** *(array)*: A List of Todos, which are necessary to clarify the objective, e.g. a open point. The intend of the todos is something around the roadmap creation, not to do something to achieve an roadmap objective.
    - <a id="definitions/Objective/properties/todos/items"></a>**Items**: Refer to *[#/definitions/Todo](#definitions/Todo)*.

  Examples:
  ```yaml
  title: Our users love the documentation we provide
  description: Great documentation is critical to the adoption of our project and is
      an integral part of everything we introduce.
  state: IDEA
  reference:
      name: example.com
      link: https://example.com
  ```

  ```yaml
  title: We provide a single, universal, schema for high-level planning
  description: "The goal of this project is, primarily, to provide a single schema that\
      \ can be used by different teams to describe the work they are doing and their\
      \ future intentions. \n      The usefulness and applicability of this schema to\
      \ real-world problem domains will determine whether anything else we do here is\
      \ of value."
  state: IDEA
  reference:
      name: example.com
      link: https://example.com
  keyresults:
  -   title: Provide a schema defintion
      description: Develop a schema that fulfills the main requirements of the objective
      state: DONE
      requirement: MUST
      reference:
          name: example.com
          link: https://example.com
  ```

- <a id="definitions/Milestone"></a>**`Milestone`** *(object)*: An indicator of progress for this roadmap. Usually milestones are collections of deliverables which, when considered together, represent a shift in the value delivered by a team or project.
  - <a id="definitions/Milestone/properties/id"></a>**`id`** *(string)*: A human-readable unique identifier for this milestone.
  - <a id="definitions/Milestone/properties/_id"></a>**`_id`** *(string)*: unique identifier for this milestone, derived from milestone.id - if unset calculated based on milestone order.
  - <a id="definitions/Milestone/properties/title"></a>**`title`** *(string, required)*: A brief name associated with this milestone to describe the value shift.
  - <a id="definitions/Milestone/properties/description"></a>**`description`** *(string)*: A markdown formatted description of what this milestone represents and, if appropriate, the justification for its presence and prioritization.
  - <a id="definitions/Milestone/properties/date"></a>**`date`** *(string, format: date)*: The date that this milestone should or is reached.
  - <a id="definitions/Milestone/properties/state"></a>**`state`**: Refer to *[#/definitions/MilestoneState](#definitions/MilestoneState)*.
  - <a id="definitions/Milestone/properties/reference"></a>**`reference`**: Refer to *[#/definitions/Reference](#definitions/Reference)*.
  - <a id="definitions/Milestone/properties/deliverables"></a>**`deliverables`** *(array)*: The list of deliverables which make up this milestone. Deliverables usually map to specific pieces of work which may be delegated to a member of your team.
    - <a id="definitions/Milestone/properties/deliverables/items"></a>**Items**: Refer to *[#/definitions/Deliverable](#definitions/Deliverable)*.
  - <a id="definitions/Milestone/properties/todos"></a>**`todos`** *(array)*: A List of Todos, which are necessary to clarify the milestone, e.g. a open point. The intend of the todos is something around the roadmap creation, not to do something to achieve an roadmap objective.
    - <a id="definitions/Milestone/properties/todos/items"></a>**Items**: Refer to *[#/definitions/Todo](#definitions/Todo)*.

  Examples:
  ```yaml
  title: Documentation Website
  description: Publish a documentation website for the project, with information that
      customers can use to understand how to use it.
  deliverables:
  -   title: Setup Docs Repo
      description: Create a documentation repository and configure the build tooling
          to generate and publish a website.
      requirement: MUST
      state: DOING
  -   title: Getting Started Guide
      description: Put together a getting started guide for new customers.
      requirement: SHOULD
      state: TODO
  ```

- <a id="definitions/Deliverable"></a>**`Deliverable`** *(object)*: A specific piece of work which may be delegated to a member of the team.
  - <a id="definitions/Deliverable/properties/title"></a>**`title`** *(string, required)*: A brief name describing this deliverable.
  - <a id="definitions/Deliverable/properties/description"></a>**`description`** *(string)*: A markdown formatted description of what this deliverable entails and why it is necessary for this milestone.
  - <a id="definitions/Deliverable/properties/date"></a>**`date`** *(string)*: the date (quarter, month, day,...) where the keyresult should be achieved.
  - <a id="definitions/Deliverable/properties/reference"></a>**`reference`**: Refer to *[#/definitions/Reference](#definitions/Reference)*.
  - <a id="definitions/Deliverable/properties/state"></a>**`state`**: Refer to *[#/definitions/DeliverableState](#definitions/DeliverableState)*.
  - <a id="definitions/Deliverable/properties/requirement"></a>**`requirement`**: Refer to *[#/definitions/Requirement](#definitions/Requirement)*.
  - <a id="definitions/Deliverable/properties/todos"></a>**`todos`** *(array)*: A List of Todos, which are necessary to clarify the deliverable, e.g. a open point. The intend of the todos is something around the roadmap creation, not to do something to achieve an roadmap objective.
    - <a id="definitions/Deliverable/properties/todos/items"></a>**Items**: Refer to *[#/definitions/Todo](#definitions/Todo)*.
  - <a id="definitions/Deliverable/properties/quantifiers"></a>**`quantifiers`**: Refer to *[#/definitions/Quantifiers](#definitions/Quantifiers)*.
- <a id="definitions/Keyresult"></a>**`Keyresult`** *(object)*: A specific piece of work which may be delegated to a member of the team.
  - <a id="definitions/Keyresult/properties/title"></a>**`title`** *(string, required)*: A brief name describing this result.
  - <a id="definitions/Keyresult/properties/description"></a>**`description`** *(string)*: A markdown formatted description of what this result entails and why it is necessary for this objective.
  - <a id="definitions/Keyresult/properties/date"></a>**`date`** *(string)*: the date (quarter, month, day,...) where the keyresult should be achieved.
  - <a id="definitions/Keyresult/properties/reference"></a>**`reference`**: Refer to *[#/definitions/Reference](#definitions/Reference)*.
  - <a id="definitions/Keyresult/properties/state"></a>**`state`**: Refer to *[#/definitions/DeliverableState](#definitions/DeliverableState)*.
  - <a id="definitions/Keyresult/properties/requirement"></a>**`requirement`**: Refer to *[#/definitions/Requirement](#definitions/Requirement)*.
  - <a id="definitions/Keyresult/properties/todos"></a>**`todos`** *(array)*: A List of Todos, which are necessary to clarify the keyresult, e.g. a open point. The intend of the todos is something around the roadmap creation, not to do something to achieve an roadmap objective.
    - <a id="definitions/Keyresult/properties/todos/items"></a>**Items**: Refer to *[#/definitions/Todo](#definitions/Todo)*.
  - <a id="definitions/Keyresult/properties/quantifiers"></a>**`quantifiers`**: Refer to *[#/definitions/Quantifiers](#definitions/Quantifiers)*.
- <a id="definitions/Todo"></a>**`Todo`** *(object)*: A Todo which is necessary to clarify a roadmap item, e.g. a open point to clarify a milestone. The intend of the todo is something around the roadmap creation, not to do something to achieve an roadmap item.
  - <a id="definitions/Todo/properties/title"></a>**`title`** *(string, required)*: A brief title describing the todo.
  - <a id="definitions/Todo/properties/description"></a>**`description`** *(string)*: A markdown formatted description of what this todo entails and what to do.
  - <a id="definitions/Todo/properties/state"></a>**`state`** *(required)*: Refer to *[#/definitions/TodoState](#definitions/TodoState)*.
- <a id="definitions/Quantifiers"></a>**`Quantifiers`** *(object)*: Quantifiers attempt to convert or describe particular properties and aspects of certain roadmap elements into mathematically measurable values.
This involves reformulating properties and assumptions of key results or deliverables into numerical values.
Not all aspects of roadmap are currently supported.
  - <a id="definitions/Quantifiers/properties/weighted_shortest_job_first"></a>**`weighted_shortest_job_first`** *(number or null)*: A value between 0 (lowest) and 30 (highest), describing, the weighet shortest job first size (according to docs/wsjf.md).
If weighted_shortest_job_first is NULL weighted_shortest_job_first is calculated during processing, if all criteria of calculation are meet.
WSJF is a prioritization method that helps to identify the greatest possible value of a planned result in relation to its effort.
All Dimension are normally given independently
WSJF = CoD(Cost of Delay) / Job Size
CoD is: (user_business_value + time_criticality +  opportunity_or_risk)
In Order to calculate, we need all of them. Minimum: `0`. Maximum: `30`. Default: `null`.
  - <a id="definitions/Quantifiers/properties/cost_of_delay"></a>**`cost_of_delay`** *(integer or null)*: A value between 0 (lowest) and 30 (highest), describing a measurement of the economic value of a job over time.
According to docs/wsjf.md CoD is calculated using user_business_value + time_criticality + opportunity_enablement_or_risk_reduction
If cost_of_delay is NULL cost_of_delay is calculated during processing, if all criteria are given and have values >= 0. Minimum: `0`. Maximum: `30`. Default: `null`.
  - <a id="definitions/Quantifiers/properties/user_business_value"></a>**`user_business_value`** *(integer or null)*: A value between 0 (lowest) and 10 (highest), describing, how much the customer (user value) or the company (business value) benefits from the result. Minimum: `0`. Maximum: `10`. Default: `null`.
  - <a id="definitions/Quantifiers/properties/time_criticality"></a>**`time_criticality`** *(integer or null)*: A value between 0 (lowest) and 10 (highest), describing, how time critical the item ist. E.g. are there fixed deadlines for certain results, e.g. because there are assurances to partners or customers, contractual agreements or legal deadlines? Is there a risk that the value can no longer be achieved if the deadline is not met? Will a possible completion in a few months still have the same value as today? Minimum: `0`. Maximum: `10`. Default: `null`.
  - <a id="definitions/Quantifiers/properties/opportunity_enablement_or_risk_reduction"></a>**`opportunity_enablement_or_risk_reduction`** *(integer or null)*: A value between 0 (lowest) and 10 (highest), describing if there is any opportunity enablement or risk reduction by achiving this item. E.g. By achieving the result, are we building up certain technical or specialist skills from which we will benefit later in the implementation or which will allow us to achieve certain later results more easily or at all? Are there risks that are minimized by achieving a certain result? Minimum: `0`. Maximum: `10`. Default: `null`.
  - <a id="definitions/Quantifiers/properties/jobsize"></a>**`jobsize`** *(integer or null)*: A value between 1 (shortest) and 10 (longest), describing, the approximation of the expected effort or statement about how long it takes to deliver the value for a delivery or result.
If you really need a Jobsize of 0, something went wrong.. Minimum: `1`. Default: `null`.

  Examples:
  ```yaml
  $comment: 'Item with a wsjf of 3: ((1 + 1+ 1) / 1) - mid ranked'
  weighted_shortest_job_first: 3.0
  cost_of_delay: 3
  user_business_value: 1
  time_criticality: 1
  opportunity_enablement_or_risk_reduction: 1
  jobsize: 1
  ```

  ```yaml
  $comment: 'Item with a wsjf of 12: ((10 + 1+ 1) / 1) - ranked high'
  weighted_shortest_job_first: 12
  cost_of_delay: 12
  user_business_value: 10
  time_criticality: 1
  opportunity_enablement_or_risk_reduction: 1
  jobsize: 1
  ```

  ```yaml
  $comment: 'Item with a wsjf of 1.2: ((10 + 1+ 1) / 10) -> ranked low'
  weighted_shortest_job_first: 1.2
  cost_of_delay: 12
  user_business_value: 10
  time_criticality: 1
  opportunity_enablement_or_risk_reduction: 1
  jobsize: 10
  ```

- <a id="definitions/Reference"></a>**`Reference`** *(object)*: A reference to a file or url with additional context which may be useful to a reader.
  - <a id="definitions/Reference/properties/name"></a>**`name`** *(string)*: a short-name for the uri.
  - <a id="definitions/Reference/properties/description"></a>**`description`** *(string)*: a describtion in natural words, what someone could expect by using the link of this reference.
  - <a id="definitions/Reference/properties/link"></a>**`link`** *(string, format: uri, required)*: A URI at which additional information about this deliverable may be found (whether that be documentation or a tracking ticket).
- <a id="definitions/Release"></a>**`Release`** *(object)*: releases which provide enhancements in the form of deliverables to the stakeholders.
  - <a id="definitions/Release/properties/tag"></a>**`tag`** *(string, required)*: a short-name for the release.
  - <a id="definitions/Release/properties/description"></a>**`description`** *(string)*: a describtion in natural words,what should or must be part of this release.
  - <a id="definitions/Release/properties/reference"></a>**`reference`**: Refer to *[#/definitions/Reference](#definitions/Reference)*.
- <a id="definitions/DeliverableState"></a>**`DeliverableState`** *(string)*: The state of an item on the roadmap. Must be one of: "TODO", "DOING", "DONE", or "SKIP". Default: `"TODO"`.
- <a id="definitions/ObjectiveState"></a>**`ObjectiveState`** *(string)*: The state of an objective-item. Must be one of: "IDEA", "PLANNED", "COMMITTED", "ACHIEVED", or "SKIP". Default: `"IDEA"`.
- <a id="definitions/MilestoneState"></a>**`MilestoneState`** *(string)*: The state of an milestone-item. Must be one of: "IDEA", "PLANNED", "COMMITTED", "REACHED", or "SKIP". Default: `"IDEA"`.
- <a id="definitions/Requirement"></a>**`Requirement`** *(string)*: An RFC2119 verb which describes how a specific requirement should be treated. Must be one of: "MUST", "SHOULD", or "MAY". Default: `"SHOULD"`.
- <a id="definitions/TodoState"></a>**`TodoState`** *(string)*: The state of an item on a todo-list. Must be one of: "OPEN", "DOING", or "CLOSED". Default: `"OPEN"`.
