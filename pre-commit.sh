#!/bin/zsh
jsonschema2md --examples-as-yaml --show-examples all schema/roadmap.json schema/roadmap.md
git add schema/roadmap.md
#git commit --amend -C HEAD
