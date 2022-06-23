[![Created Badge](https://badges.pufler.dev/created/gianwario/CADOCS)](https://badges.pufler.dev)
[![Visits Badge](https://badges.pufler.dev/visits/gianwario/CADOCS)](https://badges.pufler.dev)

<p align = "center">
  <img src = "https://github.com/gianwario/CADOCS/blob/main/cadocs_logo.png?raw=true" width = "400" heigth = "200">
</p>

# CADOCS Conversational Agent

## Introduction

**CADOCS** is a conversational agent working on the Slack platform and able to use third-party tools to identify and manage *community smells* in software development communities on GitHub.

Specifically, this is the principal repository of the system and contains the code for the client part that directly interacts with the user on the Slack platform.

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/5EpKtnF8jys/0.jpg)](https://www.youtube.com/watch?v=5EpKtnF8jys)

## Content of the Repository

The main elements of the repository are described below:

- src: it contains the source code of the conversational agent;
- resources: divided as follow:
  - surveys: 

## Other Tools

The entire CADOCS tool is composed of three modules:
- **CADOCS** (this repository): it is the Slack App used to interact with users.
- **CADOCS_NLU_Model** [link](https://github.com/vipenti/CADOCS_NLU_Model): it is the ML service used to interpret the users' intents.
- **csDetector** [link](https://github.com/gianwario/csDetector): the augmented and wrapped version of csDetector, used in our tool to detect community smells and other socio-technical metrics.

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

- Anaconda 3 - 2022.05 - 64bit
- Windows 10
- Microsoft Visual C++ Build Tools 14.0 or higher (In order to run Anaconda) 
- A Slack account and a Slack workspace
- (Optional, if you won't use Anaconda to install it) Python 3.8.3 
- ngrok (https://ngrok.com/download)

#### Installation Steps

- Step 1: Local installation of CADOCS (Recommended, using Anaconda)
  - Clone the current repository on your system
  - In our repository, find the *cadocs_chatbot_env.yaml* file which contains the environment and the dependencies needed
  - Through the Anaconda Powershell, run the following command: *conda env create -f ENV_FILE_NAME.yaml*

In case you faced some error installing the Anaconda environment, please proceed with the Step 1.1

- (Optional) Step 1.1: Local installation of CADOCS (Manual)
  - Clone the current repository on your system
  - In our repository, find the *cadocs_chatbot_env.yaml* file which contains the environment and the dependencies needed
  - Create a new Python 3.8.3 environment
  - Within the previously mentioned file, you will find each of the dependencies needed to run the tool
  - Install by hand each of them in your env

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
    ACTIVE_LEARNING_THRESHOLD = A numeric value that indicates the threshold of confidence needed by the agent to ask if its prediction was correct (We suggest 0.77) 
    MINIMUM_CONFIDENCE = A numeric value that indicates the minumum confidence needed by the agent to execute an intent (We suggest 0.55)
    CADOCSNLU_URL_PREDICT = https://sesacadocs.eu.ngrok.io/cadocsNLU/predict
    CADOCSNLU_URL_UPDATE = https://sesacadocs.eu.ngrok.io/cadocsNLU/update
    CSDETECTOR_URL_GETSMELLS = https://sesacadocs.eu.ngrok.io/csDetector/getSmells
    CSDETECTOR_URL_UPLOADS = https://sesacadocs.eu.ngrok.io/csDetector/uploads/
  ```
  - Within your IDE (or through command line if you feel more comfortable), make sure that the environment used to execute the tool is the one you created in the Step 1 
  - With the environment activated, run the module *slack_api_connection.py*

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
  - Follow the instructions in the demo video to use CADOCS!

### Case 2: Full Local Installation

This case is the trickiest one. Since CADOCS is based on three different modules, you will have to install by hand the three environments needed to execute each module. 

After having installed each of them, you will have to create your own Slack App like the previous case.

This section will explain how to put together the three modules in order to make CADOCS work. Please refer to the previous section in order to install the current project.

#### Requirements

- Having installed the CADOCS_NLU project (further details are available in the project's repository)
- Having installed the csDetector enhanced project (further details are available in the project's repository)

#### Installation Steps

- Step 1: Installation of CADOCS
  - Follow the first three steps listed in the precious section (and refer to their requirements too)
- Step 2: Configuration of CADOCS
  - Open the project on your system with the IDE you prefer (__We suggest using Visual Studio Code or PyCharm__)
  - Create a new file in the /src folder named "__.env__" 
  - Within the .env file, insert the following information (with the name we will provide)
  
  ```
    SLACK_TOKEN = The Bot User OAuth Token that you will find in the OAuth & Permissions section within the app you created in the Step 2
    SLACK_EVENT_TOKEN = The Signing Secret that you will find in the Basic Information section within the app you created in the Step 2
    GIT_PAT = GitHub Personal Access Token that you can generate within the Developer Settings in your GitHub settings
    ACTIVE_LEARNING_THRESHOLD = A numeric value that indicates the threshold of confidence needed by the agent to ask if its prediction was correct (We suggest 0.77) 
    MINIMUM_CONFIDENCE = A numeric value that indicates the minumum confidence needed by the agent to execute an intent (We suggest 0.55)
    CADOCSNLU_URL_PREDICT = YOUR_NGROK_URL/cadocsNLU/predict
    CADOCSNLU_URL_UPDATE = YOUR_NGROK_URL/cadocsNLU/update
    CSDETECTOR_URL_GETSMELLS = YOUR_NGROK_URL/csDetector/getSmells
    CSDETECTOR_URL_UPLOADS = YOUR_NGROK_URL/csDetector/uploads/
  ```
  - Within your IDE (or through command line if you feel more comfortable), make sure that the environment used to execute the tool is the one you created in the Step 1 
  - With the environment activated, run the module *slack_api_connection.py*

- Step 3: Execution of the helper modules
  - Execute the NLU web service (please refer to the CADOCS_NLU project)
  - Execute the csDetector web service (please refer to the csDetector project)

- Step 4: Put it all together
  - Open the Slack app you created previously
  - In the __Event Subscription__ section, toggle ON the __Enable Events__ button and, in the __Subscribe to bot events__ section, add:
    - message.channels
    - message.im
  - In the __Interactivity & Shortcuts__ section, toggle ON the __Interactivity__ button
  - Insert the following URLs:
    - In the __Event Subscription__ section, insert as the request URL: YOUR_NGROK_URL/slack/events
    - In the __Interactivity & Shortcuts__ section, insert as the request URL: YOUR_NGROK_URL/slack/action-received
  - Reinstall the app in your workspace
  - Follow the instructions in the demo video to use CADOCS!

## Contributors

[![Contributors Display](https://badges.pufler.dev/contributors/gianwario/CADOCS?size=75&padding=5&bots=true)](https://badges.pufler.dev)

<!--
## References

Please, if you want to cite our work use the following *bibtex* code:

```bibtex

```
-->
