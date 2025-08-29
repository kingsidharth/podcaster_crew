# Podcaster Crew

Welcome to the Podcaster Crew project, powered by [crewAI](https://crewai.com). This template is designed to help you set up a multi-agent AI system with ease, leveraging the powerful and flexible framework provided by crewAI. Our goal is to enable your agents to collaborate effectively on complex tasks, maximizing their collective intelligence and capabilities.

## Installation

Ensure you have Python >=3.10 <3.14 installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install uv:

```bash
pip install uv
```


Next, navigate to your project directory and install the dependencies:

(Optional) Lock the dependencies and install them by using the CLI command:
```bash
crewai install
```

### Setup

1. Create `.env` file at project root and add:

```
MODEL=gpt-4.1-mini-2025-04-14
OPENAI_API_KEY=sk-
GEMINI_API_KEY=
SERPER_API_KEY=
```

You'll need to add credits for these:
OpenAI API Key: https://platform.openai.com/api-keys
Gemini API Key: https://aistudio.google.com/apikey
Serper API Key: https://serper.dev/


## Running the Project

To kickstart your crew of AI agents and begin task execution, run this from the root folder of your project:

```bash
$ crewai run
```

This command initializes the podcaster Crew, assembling the agents and assigning them tasks as defined in your configuration.

This example, unmodified, will run the create a `report.md` file with the output of a research on LLMs in the root folder.

## Customising
- Modify `src/podcaster/config/agents.yaml` to define your agents
- Modify `src/podcaster/config/tasks.yaml` to define your tasks
- Modify `src/podcaster/crew.py` to add your own logic, tools and specific args
- Modify `src/podcaster/main.py` to add custom inputs for your agents and tasks

## Support

For support, questions, or feedback regarding the Podcaster Crew or crewAI, visit CrewAI [documentation](https://docs.crewai.com).
