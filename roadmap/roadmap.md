# Roadmap for roadmap.py

This is the planning roadmap for the [uroflavin/roadmap](https://github.com/uroflavin/roadmap) project. 
It acts as both the plan for implementing this tool as well as a demonstration of what a roadmap might look like.

One of the things you'll immediately notice about this file is that it uses *Markdown* for formatting of text and is designed around a structured YAML schema. 
The goal is to make this as easy as possible for humans to read and reason about, while also enabling powerful visualizations to be generated based on the content.


## Authors

- Uroflavin *uroflavin@gmail.com*


## Important Dates

- **2023-12-09** | Project Start
This is the day that the project was started.

- **2023-12-17** | Demo Day
This is the scheduled date for the first demo of this project to a wider audience.
## Objectives

### 🚀 We provide a single, universal, schema for high-level planning
The goal of this project is, primarily, to provide a single schema that can be used by different teams to describe the work they are doing and their future intentions. 
The usefulness and applicability of this schema to real-world problem domains will determine whether anything else we do here is of value.

- [see json-schema.org](https://json-schema.org/)
 


#### ~~[R1] **MUST::DONE** | Provide a schema defintion~~
Develop a schema that fulfills the main requirements of the objective
- [see README](https://github.com/uroflavin/roadmap/blob/main/schema/roadmap.json)

#### [R2] **MAY::TODO** | Complete examples in schema-definition
Complete the examples so that every user of the schema is able to find suitable examples for their specific use cases
- [see README](https://github.com/uroflavin/roadmap/blob/main/schema/roadmap.json)
### 🚀 We provide official tooling for most common use cases
While the goal of having a single unified schema for planning is that it enables the development of tools that automate various aspects of planning, most teams are not going to adopt this if the fundamentals aren't already solved for them. 
This includes things like being able to visualize your road map in common formats, validating it against the schema etc.

### 🚀 We have exceptional documentation
Adoption of something intended to make planning easier is only going to be successful if it is easy to use, and a critical part of that is great documentation. 
Our goal is that someone with no familiarity with our tooling can ramp up and have an initial road map ready for use within only a few minutes.


## Milestones

### **▶ REACHED | Design and Planning**
The design and planning stage is where we're figuring out how this project should work and, broadly, what kind of information we want to show on our road maps.

- [explaining design and planning principles](https://www.turing.com/blog/principles-of-software-development-guide/)
#### ~~📦 **MUST::DONE** | README~~
We need to add a README file explaining the purpose of this project and giving some basic examples of its use.

- [see README](https://github.com/uroflavin/roadmap/blob/main/README.md)

#### ~~📦 **MUST::DONE** | Roadmap~~
We need to know what the roadmap file format looks like, so we'll get started with an example roadmap to kick the tyres.

- [see roadmap.yml](https://github.com/uroflavin/roadmap/blob/main/examples/roadmap.yml)

### **▶ REACHED | Roadmap Schema**
Once we know how we want a road map file to look, we should put together a schema for the file. 
This will allow us to document the file structure and provide a first class editing experience to people using it.

#### ~~📦 **MUST::DONE** | roadmap.schema.json~~
Put together a JSONSchema file describing the road map file format.

- [see roadmap.json](https://github.com/uroflavin/roadmap/blob/main/schema/roadmap.json)

#### ~~📦 **MUST::DONE** | Publish Schema~~
Publish the schema file on [github](https://https://github.com/uroflavin/roadmap) so that people can reference it easily.

- [see roadmap.json](https://github.com/uroflavin/roadmap/blob/main/schema/roadmap.json)

### **▶ REACHED | Markdown Renderer**
The Goal is, to implement an markdown renderer, which is capable to render this yml as markdown.

#### ~~📦 **MUST::DONE** | Understand SierraWorks Basic Markdown~~
Understand the Syntax of the go-template from https://github.com/SierraSoftworks/roadmap/blob/main/tools/roadmap-md/roadmap.basic.md

#### ~~📦 **MUST::DONE** | jinja2 template~~
Develop a jinja2 template for markdown output of the roadmap

#### ~~📦 **MUST::DONE** | markdonw-renderer~~
Put some code in roadmap.py to render roadmap as Markdown

- [see Markdown-result of this roadmap.yml](https://github.com/uroflavin/roadmap/blob/main/roadmap/roadmap.md)

### **▶ COMMITED | HTML**
The Goal is, to implement a html-renderer, which is capable to render this yml as html

#### ~~📦 **MUST::DONE** | html-template from original source~~
Develop a template for html output of the roadmap
Use SierraSoftworks-Go-Template as a starting point

- [see SierraSoftworks-Go-Template](https://github.com/SierraSoftworks/roadmap/blob/main/tools/roadmap-html/roadmap.html)

#### ~~📦 **MUST::DONE** | html-renderer~~
Put some code in roadmap.py to render roadmap as HTML

- [see HTML-result of this roadmap.yml](https://github.com/uroflavin/roadmap/blob/main/roadmap/roadmap.html)

### **▶ PLANNED | Graphviz**
The Goal is, to implement a dot-file, which is capable to render this yml as graphviz.

#### 📦 **MUST::TODO** | dot-template
Develop a dot-template for graphviz output of the roadmap

- [see SierraSoftworks-Go-Template](https://github.com/SierraSoftworks/roadmap/blob/main/tools/roadmap-graphviz/roadmap.dot)

#### 📦 **MUST::TODO** | dot-renderer
Put some code in roadmap.py to render roadmap as dot-file

### **▶ IDEA | Web Renderer**
GraphViz is great, but being able to see things like the description of your deliverables and their current state is something that most users are probably going to find quite useful. 
Pair that with a need to make tinkering and experimentation easy and there are few things better than an interactive website to show your road map.
The goal here is to produce something which is easy and pleasurable to use, which shows your road map in a format which can be understood and makes interacting with it as low-fuss as possible.

#### 📦 **MUST::TODO** | Web Renderer
The most important part of this milestone is the development of a web based renderer which can present a road map file. 
This renderer is going to form the basis for our user flows, including acting as a realtime preview for the editor and a final output for the repository viewer.      

#### 📦 **SHOULD::TODO** | Markdown To HTML as JINJA2 Function
The renderer should support Markdown

#### 📦 **MAY::TODO** | Renderer Package
Some teams might want to host a version of the renderer on their own website, in which case we should provide them with a package that lets them use the Road Map web renderer