<p align = "center">
  <img src = "https://github.com/gianwario/CADOCS/blob/main/cadocs_logo.png?raw=true" width = "400" heigth = "200">
</p>

# CADOCS Conversational Agent

## Introduction

**CADOCS** is a conversational agent working on the Slack platform and able to use third-party tools to identify and manage *community smells* in software development communities on GitHub.

Specifically, this is the principal repository of the system and contains the code for the client part that directly interacts with the user on the Slack platform.

### Pre-Print of the Paper

[Link to the paper pre-print](https://stefanolambiase.github.io/assets/papers/ICSME_CADOCS_2022.pdf)

### Demo of the Tool 
[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/a2hOoE1M8hk/0.jpg)](https://www.youtube.com/watch?v=a2hOoE1M8hk)
<br/>

### Installation video
NOT Updated
[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/ffdimm2CvO0/0.jpg)](https://www.youtube.com/watch?v=ffdimm2CvO0)
<br/>

## Content of the Repository

The main elements of the repository are described below:

- src: it contains the source code of the conversational agent
- resources: it contains the survey created to build the dataset for the NLU model

## Other Tools

The entire CADOCS tool is composed of three modules:
- **CADOCS** (this repository): it is the Slack App used to interact with users.
- **CADOCS_NLU_Model** [link](https://github.com/alfcan/CADOCS_NLU_Model): it is the ML service used to interpret the users' intents.
- **csDetector** [link](https://github.com/alfcan/csDetector): the augmented and wrapped version of csDetector, used in our tool to detect community smells and other socio-technical metrics.
The links are referred to our modified versions of the tools.

## Detectable Community Smells

The complete list of detectable community smells—through the use of csDetector—and the associated refactoring strategies.

| Community Smell | Description | Refactoring Strategies |
|---|---|---|
| Organizational Silo | Siloed areas of the community that do not communicate, except through one or two of their respective members. | Restructure the community, Create communication plan, Mentoring, Cohesion exercising, Monitoring, and Introducing a social-rewarding mechanism. |
| Black Cloud | Information overload due to lack of structured communications or cooperation governance. | Create communication plan, Restructure the community, and Introduce a Social sanctioning mechanism. | 
| Radio Silence | One interposes herself into every formal interaction across more sub-communities with little flexibility to introduce other channels. | Restructure the community, Create communication plan, Mentoring, Cohesion exercising, Monitoring, and Introduce a Social sanctioning mechanism. | 
| Prima Donnas | A team of people is unwilling to respect external changes from other team members due to inefficiently structured collaboration. | NA | 
| Sharing Villainy | Cause of a lack of information exchange, team members share essential knowledge such as outdated, wrong and unconfirmed information. | NA | 
| Organizational Skirmish | A misalignment between different expertise levels of individuals involved in the project leads to dropped productivity and affects the project's timeline and cost. | NA | 
| Solution Defiance | The development community presents different levels of cultural and experience background, leading to the division of the community into similar subgroups with completely conflicting opinions. | NA | 
| Truck Factor Smell | Risk of significant knowledge loss due to the turnover of developers resulting from the fact that project information and knowledge are concentrated in a minority of the developers. | NA | 
| Unhealthy Interaction | Long delays in stakeholder communications cause slow, light and brief conversations and discussions. | NA | 
| Toxic Communication | Toxic interactions and conflicting opinions among developers could push them to leave the project. | NA |

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

## How to Install CADOCS: Conversational Agent Locally

There are several ways to install the tool. We discuss them individually below.
<!--
### Case 1: Integration in Slack (*Recommended*)

You can integrate our conversational agent directly into your Slack workflow following the steps listed below.
Since it will use our own hosted services, you won't need to install any of the modules we built to develop the tool, and for this reason it is the easiest way to use CADOCS. 

#### Requirements

- A Slack account and a Slack workspace

#### Installation Steps

- Log into your workspace and add our CADOCS app:
<a href="https://slack.com/oauth/v2/authorize?client_id=3537687436610.3523126127575&scope=channels:history,channels:read,chat:write,files:write,im:history,im:read,im:write,users:read&user_scope="><img alt="Add to Slack" height="40" width="139" src="https://platform.slack-edge.com/img/add_to_slack.png" srcSet="https://platform.slack-edge.com/img/add_to_slack.png 1x, https://platform.slack-edge.com/img/add_to_slack@2x.png 2x" /></a>
- (Optional) Invite CADOCS in one of your channels if you don't want to use it through the app's channel
- You are done! 

-->

### Case 1: Slack App Installation (*Recommended*)

Since we made each of the modules needed by CADOCS available on the web, you can install only the current project to run the tool.

You will have to create your own Slack App, host the CADOCS project and tweak the configuration file in order to make everything work together.

In the Requirements section, you will find the softwares and helpers you will need to install the tool. We suggest you to use the same versions we used, which will be specified alongside the requirements.

#### Requirements

- A Slack account and a Slack workspace
- Python 3.8.3
- ngrok (https://ngrok.com/download)
- Having installed the CADOCS_NLU project (further details are available in the project's repository)
- Having installed the csDetector enhanced project (further details are available in the project's repository, please refer to the branch "dev")


#### Installation Steps

- Step 1: Local installation of CADOCS (Recommended)
  - Clone the current repository on your system
  - In our repository, find the *requirements.txt* file which contains the dependencies needed
  - Create a virtual environment, run the following command: *python -m venv .venv*
  - Activate the environment and run the following command: *pip install -r requirements.txt*

- Step 2: Creation of a new Slack App
  - Go to the following URL https://api.slack.com/
  - Follow the instruction to create a new app
  - Within the __OAuth & Permissions__ section, make sure you give the following __Bot Token Scopes__:
    - channels:history, channels:read
    - chat:write
    - files:write
    - im:history, im:write, im:read
    - users:read
  - Install the app in your workspace

- Step 3: Setting up the web service
  - Install ngrok on your system
  - Follow the instructions on the ngrok site to authenticate and initialize the software
  - Open a tunnel to your machine (on the 5002 port) through the command: *ngrok http 5002* 
  - Keep in mind the forwording url generated by ngrok (it will look like this: https://##############.eu.ngrok.io)

- Step 4: Configuration of the Agent
  - Open the project on your system with the IDE you prefer (__We suggest using Visual Studio Code or PyCharm__)
  - Create a new file in the /src folder named "__.env__" 
  - Within the .env file, insert the following information (with the name we will provide)
  
  ```
    SLACK_TOKEN = The Bot User OAuth Token that you will find in the OAuth & Permissions section within the app you created in the Step 2
    SLACK_EVENT_TOKEN = The Signing Secret that you will find in the Basic Information section within the app you created in the Step 2
    GIT_PAT = GitHub Personal Access Token that you can generate within the Developer Settings in your GitHub account settings (make sure you give at least the "Repo" permissions)
    MINIMUM_CONFIDENCE = A numeric value that indicates the minumum confidence needed by the agent to execute an intent (We suggest 0.55)
    CADOCSNLU_URL_PREDICT = https://sesacadocs.eu.ngrok.io/cadocsNLU/predict
    CADOCSNLU_URL_UPDATE = https://sesacadocs.eu.ngrok.io/cadocsNLU/update
    CSDETECTOR_URL_GETSMELLS = https://sesacadocs.eu.ngrok.io/csDetector/getSmells
    CSDETECTOR_URL_UPLOADS = https://sesacadocs.eu.ngrok.io/csDetector/uploads/
  ```
  - Within your IDE (or through command line if you feel more comfortable), make sure that the environment used to execute the tool is the one you created in Step 1 
  - With the environment activated, run the module *slack_api_connection.py* from the CADOCS directory (command: *python src/api/slack_api_connection.py*)

- Step 5: Put it all together
  - Open the Slack app you created in the Step 2 
  - In the __Event Subscription__ section, toggle ON the __Enable Events__ button and, in the __Subscribe to bot events__ section, add:
    - message.channels
    - message.im
  - In the __Interactivity & Shortcuts__ section, toggle ON the __Interactivity__ button
  - Insert the following URLs:
    - In the __Event Subscription__ section, insert as the request URL: YOUR_NGROK_URL/slack/events
    - In the __Interactivity & Shortcuts__ section, insert as the request URL: YOUR_NGROK_URL/slack/action-received
  - Reinstall the app in your workspace
  
## Contributors

<a href="https://github.com/alfcan/CADOCS/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=alfcan/CADOCS" />
</a>

<!--
## References

Please, if you want to cite our work use the following *bibtex* code:

```bibtex

```
-->
