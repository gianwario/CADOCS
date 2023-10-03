# CADOCS | CONTRIBUTING

## Commits

For contributing commit messagges must follow the standard of [Conventional Commits](https://www.conventionalcommits.org/).

Part of the following document is taken from https://github.com/angular/angular/blob/22b96b9/CONTRIBUTING.md#-commit-message-guidelines

### Commit Message Format

Each commit message consists of a `header`, a `body` and a `footer`. The header has a special format that includes a `type`, a `scope` and a `subject`:

```
<type>(<scope>): <summary>
<BLANK LINE>
<body>
<BLANK LINE>
<footer>
```

The **header** is mandatory and the **scope** of the header must be omitted if the change is common among the packages, otherwise it's mandatory.

```
<type>(<scope>): <description>
  │       │             │
  │       │             └─⫸ A brief description of the commit
  │       │
  │       └─⫸ Commit Scope: api | service | chatbot | intent
  │
  └─⫸ Commit Type: build|ci|docs|feat|fix|refactor|impr|style|test
```

#### Description

- use the imperative, present tense: "change" not "changed" nor "changes"
- don't capitalize the first letter
- no dot (.) at the end

#### Type

Must be one of the following:

- build: Changes that affect the build system or external dependencies
- ci: Changes to our CI configuration files and scripts
- docs: Documentation only changes
- feat: A new feature
- fix: A bug fix
- refactor: A code change that neither fixes a bug nor adds a feature
- impr: Improve an existing feature or existing dataset
- style: Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc)
- test: Adding missing tests or correcting existing tests

### Scope

The scope must be the project section within the change is happening.

Supported scopes:

- `api`: scope to handling api connection for platforms
- `service`: scope to define support methods for complex functionalities
- `chatbot`: scope to handling chatbot functionalities
- `intent`: scope to resolve user intents

### Body

The **body** is optional. Just as in the **description**, use the imperative, present tense: "fix" not "fixed" nor "fixes".
The body should extend the content of the description.

### Footer

The footer is optional. The footer should contain the GitHub issue reference that this commit **Closes**.

## Branches

New branches must follow this format for their names: `<type>/<scope>/<description>`

- `type` and `scope` refer to the ones described in the Commits section.
- `description` must be a word representing the changes happening in the branch.

### Branching strategy

The branches will be defined as follows: a _main long branch_, named `dev`, which serves as the development branch; starting from this branch there will be four other long branches, each dedicated to a specific change request (CR). These branches will be named after the identifiers of the corresponding CRs.

In addition to the long branches, we will also use _short branches_, which are temporary branches created from the specific long branch of each CR and have a limited scope and duration.
Whenever a developer starts working on a specific feature or activity related to a CR, he or she creates a short branch for that particular activity.

Once the activity is completed, the changes will be merged into the corresponding _long branch_ (i.e., the CR-specific branch).

Once the integration of all subfunctions is complete, the CR-specific long branch will be merged with the `dev` branch.
