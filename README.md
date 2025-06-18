# LinkedIn Content Manager Agent System

The LinkedIn Content Manager Agent System was created to solve a simple problem: staying up to date about a topic like AI nowadays takes too much time. Scrolling for relevant news, filtering through noise, and specially identifying trending opinions takes too much.

This agents system automates that process. The agents find relevant news, summarize key points, detect opinion trends from social platforms, and suggest potential post topics. It saves hours of manual work.

## Disclaimer

This is a proof of concept. Parts are fragile. The code is not optimized or production-ready. It was quickly put together to test an idea. Use it for inspiration, not as a base for deployment.

## What it does

You define your area of interest. The system does the rest:

- Finds recent news related to your topic
- Summarizes and ranks articles based on your interest
- Analyzes social network chatter around the topic
- Outputs a structured report with insights and content ideas

It doesn’t try to write full posts for you. That’s not the point. Actually that is a terrible idea. LLM-generated writing is average by nature. But finding the right thing to write about and being up to date in the discussions, LLMs are excellent at that.

## Why this is interesting

The typical approach to using LLMs for content creation is wrong: write entire posts. This rarely works well. 

This tool flips the process:

- Use LLMs for discovery, summarization, analysis, and ideation
- Leave final writing to the user

From a tech perspective, this is also a strong case study on orchestrating multiple tasks through agents.

## How it works

This app uses **CrewAI** to manage different agents and tools:

- One to gather news
- One to summarize and prioritize
- One to crawl social platforms and detect trends
- One to generate a report

CrewAI simplifies task delegation and sequencing. It's not perfect, but it’s an effective framework for rapid prototyping.

### Future direction

This codebase was built using CrewAI templates and some quick iteration. A more advanced version would be rewritten with:

- **MCP** (Multi-agent Control Plane)
- **Guardrails** for validation and control

These upgrades would increase robustness and allow better handling of ambiguity and user-specific behavior.

## What this could become

As a tool, it works. I use it daily to stay informed with minimal effort. It gives me back hours of time.

That said, this likely isn’t a long-term product. LLM integration into major platforms will make this kind of standalone solution unnecessary. The core logic will be swallowed into broader ecosystems.

Still, this is a great example of how powerful and fast LLM-based scripting can be.

## Setup and usage

To run the project and generate your content report:

```bash
crewai run
```

This command will:

- Trigger the agent workflow

- Generate a full report with news summaries, trend insights, and suggested topics

## Tech
- CrewAI for LLM orchestration
- Third parties Google News + Reddit APIs
