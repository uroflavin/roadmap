# roadmap
Manage your project and team road maps in YAML

This project is heavyly inspired by https://github.com/SierraSoftworks/roadmap, with some key-differences:
 - roadmap is a clone, implemented in python
 - the roadmap-structure is slightly different

My development approach is to implement the main functions of https://github.com/SierraSoftworks/roadmap. This concerns the creation of a view as HTML and PDF.

I mainly focus on mapping the following structure:
 - A **project** has any number of objectives
    - An **objective** has any number of milestones
        - A **milestone** has any number of deliverables
            - a **deliverable** can be assigned to a release.
- **timeline** and the **project metadata** are unchanged
- The whole thing is supplemented by **release** assignments

Objectives, milestones, deliverables and releases can have any number of references.

## roadmap.yaml
The main structure of a roadmap.yaml is as follows:
- *title*: A brief title which describes this road map.
- *description*: A markdown formatted description of what this road map represents and any additional context which may be useful to a reader.
- **authors**: A list of authors who were/are involved in the creation of the roadmap
- **timeline**: A list of important dates which relates to this road map.
- **releases**: A list of releases which provide enhancements in the form of deliverables to the stakeholders
- **objectives**: A list of objectives which the team is working towards over the course of this road map.

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
    - DONE
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
    - DONE
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
- *release*: The deliverable should, must or may be part of this release
- *reference*: additional information about this deliverable

#### reference
- **link***: mandatory; A URI at which additional information about this deliverable may be found (whether that be documentation or a tracking ticket).
- *name*: a name for your reference
- *description*: describe in natural words, what someone could expect by using the link of this reference