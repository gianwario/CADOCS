[![Visits Badge](https://badges.pufler.dev/visits/gianwario/CADOCS)](https://badges.pufler.dev)

<p align = "center">
  <img src = "https://github.com/gianwario/CADOCS/blob/main/cadocs_logo.png?raw=true" width = "400" heigth = "200">
</p>

# CADOCS Conversational Agent

## Introduction

**CADOCS** is a conversational agent working on the Slack platform and able to use third-party tools to identify and manage *community smells* in software development communities on GitHub.

Specifically, this is the principal repository of the system and contains the code for the client part that directly interacts with the user on the Slack platform.

[video del tool]

## Content of the Repository

The main elements of the repository are described below:

- src: it contains the source code of the conversational agent;
- resources: divided as follow:
  - surveys: 

## Other Tools

The entire CADOCS tool is composed of three modules:
- **CADOCS** (this repository): it is the Slack App used to interact with users.
- **CADOCS_NLU_Model** (link): it is the ML service used to interpret the users' intents.
- **csDetector** (link): the augmented and wrapped version of csDetector, used in our tool to detect community smells and other socio-technical metrics.

<!--
## Authors

List of authors:

- **Gianmario Voria** — *g.voria6@studenti.unisa.it* — University of Salerno, Salerno, Italy
- **Viviana Pentangelo** — *v.pentangelo4@studenti.unisa.it* — University of Salerno, Salerno, Italy
- **Antonio Della Porta** — *a.dellaporta26@studenti.unisa.it* — University of Salerno, Salerno, Italy
- **Stefano Lambiase** — *slambiase@unisa.it* — Software Engineering (SeSa) Lab, Department of Computer Science - University of Salerno, Salerno, Italy
- **Gemma Catolino** — *g.catolino@tilburguniversity.edu* — Jheronimus Academy of Data Science - Tilburg University, 's-Hertogenbosch, Netherlands
- **Fabio Palomba** — *fpalomba@unisa.it* — Software Engineering (SeSa) Lab, Department of Computer Science - University of Salerno, Salerno, Italy
- **Filomena Ferrucci** — *fferrucci@unisa.it* — Software Engineering (SeSa) Lab, Department of Computer Science - University of Salerno, Salerno, Italy
-->

## How to Install the Tool Locally

There are several ways to install the tool. We discuss them individually below.

### Case 1: Integration in Slack (*Recommended*)

You can integrate our conversational agent directly into your Slack workflow following the steps listed below.
Since it will use our own hosted services, you won't need to install any of the modules we built to develop the tool, and for this reason it is the easiest way to use CADOCS. 

#### Requirements

- A Slack Workspace

#### Installation Steps

- Log into your workspace and add our CADOCS app;
- (Optional) Invite CADOCS in one of your channels if you don't want to use it through the app's channel;
- You are done! 

### Case 2: Slack App Installation

Since we made each of the modules needed by CADOCS available on the web, you can install only the current project to run the tool.

You will have to create your own Slack App, host the CADOCS project and tweak the configuration file in order to make everything work together.

#### Requirements

- requisito 1
- requisito 2

#### Installation Steps

- Step 1
- Step 2

### Case 3: Full Local Installation

This case is a the trickiest one. Since CADOCS is based on three different modules, you will have to install by hand the three environments needed to execute each module. 

After having installed each of them, you will have to create your own Slack App like the previous case.

In the following list you will find the step needed to make the current module---the Slack app---working. Please refer to the others repositories to install and integrate the remaining projects (the NLU model and csDetector, which are linked above)

#### Requirements

- requisito 1
- requisito 2

#### Installation Steps

- Step 1
- Step 2


## Contributors

<a href="https://github.com/gianwario/CADOCS/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=gianwario/CADOCS" />
</a>

<!--
## References

Please, if you want to cite our work use the following *bibtex* code:

```bibtex

```
-->
