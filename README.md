# roadmap
Manage your project and team roadmaps in YAML

## Goals
My development approach is to implement the core functions of https://github.com/SierraSoftworks/roadmap. This concerns the creation of different views (e.g. Markdown, HTML, Graph and PDF).

I mainly focus on mapping the following structure:
 - A **project** has any number of objectives
    - An **objective** has any number of milestones
        - A **milestone** has any number of deliverables
            - a **deliverable** can be assigned to a release.
- A number of **milestones** as an indicator for overall-progress of this roadmap (to be compliant with SierraSoftworks/roadmap)
- The **timeline** and the **project metadata** are unchanged
- The whole thing is supplemented by **release** assignments

In advance, i like to support some more planning approaches.

Objectives, milestones, deliverables and releases can have none or one reference (e.g. to your ticketsystem or document or whatever).

## roadmap.yaml
The main structure of a roadmap.yaml is as follows:
- *title*: A brief title which describes this road map.
- *description*: A markdown formatted description of what this road map represents and any additional context which may be useful to a reader.
- **authors**: A list of authors who were/are involved in the creation of the roadmap
- **timeline**: A list of important dates which relates to this road map.
- **releases**: A list of releases which provide enhancements in the form of deliverables to the stakeholders

### Support different planning approaches
roadmap.py is able to handle the following planning approaches:
- **Roadmap only with Objectives**
    - **objectives**: Is a list of objectives which the team is working towards over the course of this roadmap.
- **Roadmap with Objective-Key-Results** (OKRs)
    - **objectives** is a list of objectives which the team is working towards over the course of this roadmap.
    - **keyresult** every objective can have one or as many keyresults as needed
- **Roadmap with Objectives and some Milestones** for each Objective
    - **objectives** is a list of objectives which the team is working towards over the course of this roadmap.
    - **milestones** is a list of milestones to reach the corresponding objective
- **Roadmap with Objectives and separate Milestones**

A Milestone can have as many Deliverables as needed.

### Sequence is crucial. 
The order of the objects of an entity indicates their logical or temporal sequence.

### roadmap entities and attributes

#### author
- **name***: mandatory; Name of the author
- *contact*: Some kind of contact informatione to contact the author (email, phone, adress)

#### timeline
- **date***: mandatory
- **title***: mandatory
- *description*: A markdown formatted description of what this timeline marker represents, or additional context associated with it.

#### release
- **tag***: mandatory; a short and meaningful tag of your release
- *description*: Describe in natural words, what should or must be part of this release
- *reference*: additional information about this release

#### objective
- **title***: mandatory; a short and meaningful summary of the objective
- *description*: Describe in natural words, what is to be achieved for whom and why
- *reference*: additional information about this objective
- *state*:
    - IDEA
    - PLANNED
    - COMMITED
    - ACHIEVED
    - SKIP
- milestones: any number of **milestone** to reach this objective (or none)

#### milestone
- **title***: mandatory; a short and meaningful summary of the milestone
- *description*: describe in natural words, what should be achived to whom
A milestone act as an indicator of progress for his objective.
- *reference*: additional information about this milestone
- *state*:
    - IDEA
    - PLANNED
    - COMMITED
    - REACHED
    - SKIP
- *deliverables*: any number of deliverable to reach this milestone (or none)

#### deliverable
- **title***: mandatory; a short and meaningful summary of the deliverable
- *description*: describe in natural words, what should be delivered to whom
- *state*
    - TODO
    - DOING
    - DONE
    - SKIP
- *requirement*: An [RFC2119](https://datatracker.ietf.org/doc/html/rfc2119) verb which describes how a specific requirement should be treated.
    - MUST
    - SHOULD
    - MAY
- *date*: The deliverable should, must or may be available by this date at the latest
- *release*: The deliverable should, must or may be part of this release; to reference one release from *releases* use *release.tag* as reference
- *reference*: additional information about this deliverable

#### reference
- **link***: mandatory; A URI at which additional information about this deliverable may be found (whether that be documentation or a tracking ticket).
- *name*: a name for your reference
- *description*: describe in natural words, what someone could expect by using the link of this reference

## Howto Run Example (Work in Progress)
 - Clone this repository
 - Install requirements
 ```pip install -r requirements.txt```
- run roadmap.py
```python3 roadmap.py```
- watch roadmap.md

## Inspired by
This project is heavyly inspired by https://github.com/SierraSoftworks/roadmap

### Key differences and how to handle them
Roadmap is a clone, implemented in python - should be no problem :)
 
Roadmap Structure is slightly different. In particular, **references** are treated differently.
Instead of:
```        
reference: URI_TO_REFERENCE 
```
use:
```        
    reference: 
        link: URI_TO_REFERENCE 
```
In addition, milestones are also permitted for objectives and objectives can contain key results as well as milestones.