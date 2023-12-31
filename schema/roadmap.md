# JSON Schema

*A roadmap represents a high-level plan for a project or team.*

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
  - **`state`**: Refer to *[#/definitions/ObjectiveState](#definitions/ObjectiveState)*.
  - **`reference`**: Refer to *[#/definitions/Reference](#definitions/Reference)*.
  - **`milestones`** *(array)*: The list of milestones which act as indicators of progress for this objective.
    - **Items**: Refer to *[#/definitions/Milestone](#definitions/Milestone)*.
  - **`keyresults`** *(array)*: The list of key-results which make up this Objective. Key-Results usually map to specific pieces of work which may be delegated to a member of your team.
    - **Items**: Refer to *[#/definitions/Keyresult](#definitions/Keyresult)*.

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
  - **`title`** *(string, required)*: A brief name associated with this milestone to describe the value shift.
  - **`description`** *(string)*: A markdown formatted description of what this milestone represents and, if appropriate, the justification for its presence and prioritization.
  - **`state`**: Refer to *[#/definitions/MilestoneState](#definitions/MilestoneState)*.
  - **`reference`**: Refer to *[#/definitions/Reference](#definitions/Reference)*.
  - **`deliverables`** *(array)*: The list of deliverables which make up this milestone. Deliverables usually map to specific pieces of work which may be delegated to a member of your team.
    - **Items**: Refer to *[#/definitions/Deliverable](#definitions/Deliverable)*.

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
  - **`reference`**: Refer to *[#/definitions/Reference](#definitions/Reference)*.
  - **`state`**: Refer to *[#/definitions/DeliverableState](#definitions/DeliverableState)*.
  - **`requirement`**: Refer to *[#/definitions/Requirement](#definitions/Requirement)*.
- <a id="definitions/Keyresult"></a>**`Keyresult`** *(object)*: A specific piece of work which may be delegated to a member of the team.
  - **`title`** *(string, required)*: A brief name describing this result.
  - **`description`** *(string)*: A markdown formatted description of what this result entails and why it is necessary for this objective.
  - **`date`** *(string)*: the date (quarter, month, day,...) where the keyresult should be achieved.
  - **`reference`**: Refer to *[#/definitions/Reference](#definitions/Reference)*.
  - **`state`**: Refer to *[#/definitions/DeliverableState](#definitions/DeliverableState)*.
  - **`requirement`**: Refer to *[#/definitions/Requirement](#definitions/Requirement)*.
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
