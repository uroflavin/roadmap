# JSON Schema

*A roadmap represents a high-level plan for your project or team.*

## Properties

- **`title`** *(string)*: A brief title which describes this roadmap.
- **`description`** *(string)*: A markdown formatted description of what this roadmap represents and any additional context which may be useful to a reader.
- **`logo`** *(object)*: A path to your project logo. This might be a good brand for your roadmap.Best fit would be some small-icon.
  - **`filename`** *(string, required)*: Your logo MUST placed where your roadmap.yml lives.
  - **`copyright_notice`** *(string)*: If there is any copyright-notice, this would be rendered as alt-text.
- **`visionstatement`** *(string)*: A markdown formatted project pr product visionstatement. A product vision describes the ideal product from the customer's perspective. The leitmotif of a product vision is therefore the question of how the product can optimally address and solve the customer's problem or needs.
- **`authors`** *(array)*: A list of authors who were/are involved in the creation of the roadmap.
  - **Items**: Refer to *[#/definitions/Author](#definitions/Author)*.
- **`releases`** *(array)*: A list of releases which provide enhancements in the form of deliverables to the stakeholders.
  - **Items**: Refer to *[#/definitions/Release](#definitions/Release)*.
- **`timeline`** *(array)*: The list of important dates which relate to this roadmap.
  - **Items**: Refer to *[#/definitions/TimelineMarker](#definitions/TimelineMarker)*.
- **`objectives`** *(array)*: The list of objectives which the team is working towards over the course of this roadmap.
  - **Items**: Refer to *[#/definitions/Objective](#definitions/Objective)*.
- **`milestones`** *(array)*: The list of milestones which act as indicators of progress for this roadmap.
  - **Items**: Refer to *[#/definitions/Milestone](#definitions/Milestone)*.
## Definitions

- <a id="definitions/Author"></a>**`Author`** *(object)*: The details of an author responsible for this roadmap, in case a reader has questions.
  - **`name`** *(string, required)*: The full name of the author.
  - **`contact`** *(string, required)*: The contact address for the author - usually their email, but may also be an IM handle or otherwise.

  Examples:
  ```yaml
  contact: john.doe@example.com
  name: John Doe
  ```

- <a id="definitions/TimelineMarker"></a>**`TimelineMarker`** *(object)*: An important date which relates to this roadmap.
  - **`date`** *(string, format: date, required)*: The date that this timeline marker is associated with.
  - **`title`** *(string, required)*: A brief name associated with this timeline marker to describe it.
  - **`description`** *(string)*: A markdown formatted description of what this timeline marker represents, or additional context associated with it.

  Examples:
  ```yaml
  date: '2023-01-15'
  description: Something really important happens on this date and we will all become
      lucky people
  title: Something really important happens
  ```

- <a id="definitions/Objective"></a>**`Objective`** *(object)*: An objective describes a high level goal for the team. It is usually something that will be worked towards over several milestones and might not have a clear definition of done.
  - **`title`** *(string, required)*: A brief name associated with this objective which describes the intended outcome.
  - **`description`** *(string)*: A markdown formatted description of what this objective represents and how it influences the direction that the team is moving in.
  - **`date`** *(string, format: date)*: The date that this objective should or is reached.
  - **`state`**: Refer to *[#/definitions/ObjectiveState](#definitions/ObjectiveState)*.
  - **`reference`**: Refer to *[#/definitions/Reference](#definitions/Reference)*.
  - **`milestones`** *(array)*: The list of milestones which act as indicators of progress for this objective.
    - **Items**: Refer to *[#/definitions/Milestone](#definitions/Milestone)*.
  - **`keyresults`** *(array)*: The list of key-results which make up this Objective. Key-Results usually map to specific pieces of work which may be delegated to a member of your team.
    - **Items**: Refer to *[#/definitions/Keyresult](#definitions/Keyresult)*.
  - **`todos`** *(array)*: A List of Todos, which are necessary to clarify the objective, e.g. a open point. The intend of the todos is something around the roadmap creation, not to do something to achieve an roadmap objective.
    - **Items**: Refer to *[#/definitions/Todo](#definitions/Todo)*.

  Examples:
  ```yaml
  description: Great documentation is critical to the adoption of our project and is
      an integral part of everything we introduce.
  reference:
      link: https://example.com
      name: example.com
  state: IDEA
  title: Our users love the documentation we provide
  ```

  ```yaml
  description: "The goal of this project is, primarily, to provide a single schema that\
      \ can be used by different teams to describe the work they are doing and their\
      \ future intentions. \n      The usefulness and applicability of this schema to\
      \ real-world problem domains will determine whether anything else we do here is\
      \ of value."
  keyresults:
  -   description: Develop a schema that fulfills the main requirements of the objective
      reference:
          link: https://example.com
          name: example.com
      requirement: MUST
      state: DONE
      title: Provide a schema defintion
  reference:
      link: https://example.com
      name: example.com
  state: IDEA
  title: We provide a single, universal, schema for high-level planning
  ```

- <a id="definitions/Milestone"></a>**`Milestone`** *(object)*: An indicator of progress for this roadmap. Usually milestones are collections of deliverables which, when considered together, represent a shift in the value delivered by a team or project.
  - **`id`** *(string)*: A human-readable unique identifier for this milestone.
  - **`_id`** *(string)*: unique identifier for this milestone, derived from milestone.id - if unset calculated based on milestone order.
  - **`title`** *(string, required)*: A brief name associated with this milestone to describe the value shift.
  - **`description`** *(string)*: A markdown formatted description of what this milestone represents and, if appropriate, the justification for its presence and prioritization.
  - **`date`** *(string, format: date)*: The date that this milestone should or is reached.
  - **`state`**: Refer to *[#/definitions/MilestoneState](#definitions/MilestoneState)*.
  - **`reference`**: Refer to *[#/definitions/Reference](#definitions/Reference)*.
  - **`deliverables`** *(array)*: The list of deliverables which make up this milestone. Deliverables usually map to specific pieces of work which may be delegated to a member of your team.
    - **Items**: Refer to *[#/definitions/Deliverable](#definitions/Deliverable)*.
  - **`todos`** *(array)*: A List of Todos, which are necessary to clarify the milestone, e.g. a open point. The intend of the todos is something around the roadmap creation, not to do something to achieve an roadmap objective.
    - **Items**: Refer to *[#/definitions/Todo](#definitions/Todo)*.

  Examples:
  ```yaml
  deliverables:
  -   description: Create a documentation repository and configure the build tooling
          to generate and publish a website.
      requirement: MUST
      state: DOING
      title: Setup Docs Repo
  -   description: Put together a getting started guide for new customers.
      requirement: SHOULD
      state: TODO
      title: Getting Started Guide
  description: Publish a documentation website for the project, with information that
      customers can use to understand how to use it.
  title: Documentation Website
  ```

- <a id="definitions/Deliverable"></a>**`Deliverable`** *(object)*: A specific piece of work which may be delegated to a member of the team.
  - **`title`** *(string, required)*: A brief name describing this deliverable.
  - **`description`** *(string)*: A markdown formatted description of what this deliverable entails and why it is necessary for this milestone.
  - **`date`** *(string)*: the date (quarter, month, day,...) where the keyresult should be achieved.
  - **`reference`**: Refer to *[#/definitions/Reference](#definitions/Reference)*.
  - **`state`**: Refer to *[#/definitions/DeliverableState](#definitions/DeliverableState)*.
  - **`requirement`**: Refer to *[#/definitions/Requirement](#definitions/Requirement)*.
  - **`todos`** *(array)*: A List of Todos, which are necessary to clarify the deliverable, e.g. a open point. The intend of the todos is something around the roadmap creation, not to do something to achieve an roadmap objective.
    - **Items**: Refer to *[#/definitions/Todo](#definitions/Todo)*.
  - **`wsjf`**: Refer to *[#/definitions/WSJF](#definitions/WSJF)*.
- <a id="definitions/Keyresult"></a>**`Keyresult`** *(object)*: A specific piece of work which may be delegated to a member of the team.
  - **`title`** *(string, required)*: A brief name describing this result.
  - **`description`** *(string)*: A markdown formatted description of what this result entails and why it is necessary for this objective.
  - **`date`** *(string)*: the date (quarter, month, day,...) where the keyresult should be achieved.
  - **`reference`**: Refer to *[#/definitions/Reference](#definitions/Reference)*.
  - **`state`**: Refer to *[#/definitions/DeliverableState](#definitions/DeliverableState)*.
  - **`requirement`**: Refer to *[#/definitions/Requirement](#definitions/Requirement)*.
  - **`todos`** *(array)*: A List of Todos, which are necessary to clarify the keyresult, e.g. a open point. The intend of the todos is something around the roadmap creation, not to do something to achieve an roadmap objective.
    - **Items**: Refer to *[#/definitions/Todo](#definitions/Todo)*.
  - **`wsjf`**: Refer to *[#/definitions/WSJF](#definitions/WSJF)*.
- <a id="definitions/Todo"></a>**`Todo`** *(object)*: A Todo which is necessary to clarify a roadmap item, e.g. a open point to clarify a milestone. The intend of the todo is something around the roadmap creation, not to do something to achieve an roadmap item.
  - **`title`** *(string, required)*: A brief title describing the todo.
  - **`description`** *(string)*: A markdown formatted description of what this todo entails and what to do.
  - **`state`**: Refer to *[#/definitions/TodoState](#definitions/TodoState)*.
- <a id="definitions/WSJF"></a>**`WSJF`** *(object)*: WSJF is a prioritization method that helps to identify the greatest possible value of a planned result in relation to its effort.
All Dimension are normally given independently
WSJF = CoD(Cost of Delay) / Job Size
CoD is: (user_business_value + time_criticality +  opportunity_or_risk)
In Order to calculate, we need .
  - **`user_business_value`** *(integer)*: A value between 0 (lowest) and 10 (highest), describing, how much the customer (user value) or the company (business value) benefits from the result. Minimum: `0`. Maximum: `10`. Default: `0`.
  - **`time_criticality`** *(integer)*: A value between 0 (lowest) and 10 (highest), describing, how time critical the item ist. E.g. are there fixed deadlines for certain results, e.g. because there are assurances to partners or customers, contractual agreements or legal deadlines? Is there a risk that the value can no longer be achieved if the deadline is not met? Will a possible completion in a few months still have the same value as today? Minimum: `0`. Maximum: `10`. Default: `0`.
  - **`opportunity_enablement_or_risk_reduction`** *(integer)*: A value between 0 (lowest) and 10 (highest), describing if there is any opportunity enablement or risk reduction by achiving this item. E.g. By achieving the result, are we building up certain technical or specialist skills from which we will benefit later in the implementation or which will allow us to achieve certain later results more easily or at all? Are there risks that are minimized by achieving a certain result? Minimum: `0`. Maximum: `10`. Default: `0`.
  - **`jobsize`** *(integer)*: A value between 1 (shortest) and 10 (longest), describing, the approximation of the expected effort or statement about how long it takes to deliver the value for a delivery or result.
If you really need a Jobsize of 0, something went wrong.. Minimum: `1`. Maximum: `10`. Default: `0`.

  Examples:
  ```yaml
  $comment: 'Item with a wsjf of 3: ((1 + 1+ 1) / 1) - mid ranked'
  jobsize: 1
  opportunity_enablement_or_risk_reduction: 1
  time_criticality: 1
  user_business_value: 1
  ```

  ```yaml
  $comment: 'Item with a wsjf of 12: ((10 + 1+ 1) / 1) - ranked high'
  jobsize: 1
  opportunity_enablement_or_risk_reduction: 1
  time_criticality: 1
  user_business_value: 10
  ```

  ```yaml
  $comment: 'Item with a wsjf of 1.2: ((10 + 1+ 1) / 10) -> ranked low'
  jobsize: 10
  opportunity_enablement_or_risk_reduction: 1
  time_criticality: 1
  user_business_value: 10
  ```

- <a id="definitions/Reference"></a>**`Reference`** *(object)*: A reference to a file or url with additional context which may be useful to a reader.
  - **`name`** *(string)*: a short-name for the uri.
  - **`description`** *(string)*: a describtion in natural words, what someone could expect by using the link of this reference.
  - **`link`** *(string, format: uri, required)*: A URI at which additional information about this deliverable may be found (whether that be documentation or a tracking ticket).
- <a id="definitions/Release"></a>**`Release`** *(object)*: releases which provide enhancements in the form of deliverables to the stakeholders.
  - **`tag`** *(string, required)*: a short-name for the release.
  - **`description`** *(string)*: a describtion in natural words,what should or must be part of this release.
  - **`reference`**: Refer to *[#/definitions/Reference](#definitions/Reference)*.
- <a id="definitions/DeliverableState"></a>**`DeliverableState`** *(string)*: The state of an item on the roadmap. Must be one of: `["TODO", "DOING", "DONE", "SKIP"]`. Default: `"TODO"`.
- <a id="definitions/ObjectiveState"></a>**`ObjectiveState`** *(string)*: The state of an objective-item. Must be one of: `["IDEA", "PLANNED", "COMMITED", "ACHIEVED", "SKIP"]`. Default: `"IDEA"`.
- <a id="definitions/MilestoneState"></a>**`MilestoneState`** *(string)*: The state of an milestone-item. Must be one of: `["IDEA", "PLANNED", "COMMITED", "REACHED", "SKIP"]`. Default: `"IDEA"`.
- <a id="definitions/Requirement"></a>**`Requirement`** *(string)*: An RFC2119 verb which describes how a specific requirement should be treated. Must be one of: `["MUST", "SHOULD", "MAY"]`. Default: `"SHOULD"`.
- <a id="definitions/TodoState"></a>**`TodoState`** *(string)*: The state of an item on a todo-list. Must be one of: `["OPEN", "DOING", "CLOSED"]`. Default: `"OPEN"`.
