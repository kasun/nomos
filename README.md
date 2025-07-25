<h1>
  <a href="https://github.com/dowhiledev/nomos">
    <img src="docs/assets/banner.jpg" alt="NOMOS">
  </a>
</h1>

<div>

![PyPI - Version](https://img.shields.io/pypi/v/nomos?style=flat-square)
[![npm version](https://img.shields.io/npm/v/nomos-sdk.svg?style=flat-square)](https://www.npmjs.com/package/nomos-sdk)
[![codecov](https://codecov.io/gh/dowhiledev/nomos/graph/badge.svg?token=MXRK9HGE5R&style=flat-square)](https://codecov.io/gh/dowhiledev/nomos)
[![Test](https://github.com/dowhiledev/nomos/actions/workflows/test.yml/badge.svg?style=flat-square)](https://github.com/dowhiledev/nomos/actions/workflows/test.yml)
[![Release](https://github.com/dowhiledev/nomos/actions/workflows/publish.yml/badge.svg?style=flat-square)](https://github.com/dowhiledev/nomos/actions/workflows/publish.yml)
[![Docker Image Version](https://img.shields.io/docker/v/chandralegend/nomos-base?style=flat-square)](https://hub.docker.com/r/chandralegend/nomos-base)
[![Open Issues](https://img.shields.io/github/issues-raw/dowhiledev/nomos?style=flat-square)](https://github.com/dowhiledev/nomos/issues)

</div>

> [!NOTE]
> Looking for client-side integration? Check out our [TypeScript/JavaScript SDK](support/ts-sdk/README.md).

**NOMOS** is a framework for building advanced LLM-powered assistants with structured, multi-step workflows. It helps you create sophisticated AI agents through configurable flows, tools, and integrations — making complex agent development accessible from no-code to full-code approaches.

```bash
pip install nomos[cli]
```

To learn more about NOMOS, check out [the documentation](docs/md/). If you're looking for quick prototyping, try our [Playground](https://nomos-builder.vercel.app/) for drag-and-drop agent creation.

<details>
<summary>Table of Contents</summary>

- [Why use NOMOS?](#why-use-nomos)
- [NOMOS Ecosystem](#nomos-ecosystem)
- [Key Features](#key-features)
- [Documentation](#documentation)
- [Additional Resources](#additional-resources)

**[Complete Documentation](docs/md/) | [Try Playground](https://nomos-builder.vercel.app/) | [Quick Start Guide](docs/md/getting-started.md)**

</details>

---

## Why use NOMOS?

NOMOS helps developers build sophisticated AI agents through structured workflows and configurable components, making complex agent development accessible to teams of all skill levels.

Use NOMOS for:
- **Multi-step agent workflows**. Create complex, stateful interactions with step-by-step flow definitions, each with specialized tools and intelligent routing between conversation states.
- **Rapid prototyping to production**. Start with our Playground for no-code prototyping, then seamlessly transition to YAML configuration or full Python implementation as your needs evolve.
- **Tool ecosystem integration**. Leverage your existing Python functions, or integrate with CrewAI, LangChain tools, and any Python package through our unified tool system with automatic documentation generation.
- **Production-ready deployment**. Built-in session management, error handling, monitoring, and Docker deployment options make it easy to scale from prototype to production.

## NOMOS Ecosystem

While NOMOS can be used standalone, it integrates with a growing ecosystem of tools and services designed for agent development:

- **[Playground](https://nomos-builder.vercel.app/)** - Design and prototype agent flows with our drag-and-drop interface. Perfect for rapid iteration and collaboration between technical and non-technical team members.
- **[TypeScript SDK](support/ts-sdk/README.md)** - Full-featured client library for web and Node.js applications, enabling seamless integration of NOMOS agents into your frontend applications.
- **[Docker Base Images](docs/md/deployment.md#docker-base-image)** - Pre-configured containers for rapid deployment with built-in support for Redis, PostgreSQL, and monitoring integrations.
- **[CLI Tools](docs/md/cli-usage.md)** - Comprehensive command-line interface for agent development, testing, and deployment with `nomos init`, `nomos run`, `nomos train`, `nomos serve`, `nomos test`, `nomos schema`, and `nomos --version` commands.

## Key Features

| Category | Feature | Description |
|----------|---------|-------------|
| **Architecture** | Step-based Flows | Define agent behavior as sequences of steps with tools and transitions |
| | Advanced Flow Management | Organize steps into flows with shared context and components |
| | Flow Memory | Each flow maintains context with intelligent cross-flow summarization |
| **Development** | Multiple Config Options | Python API or declarative YAML configuration |
| | Playground | Drag-and-drop interface for designing flows **[Try it live →](https://nomos-builder.vercel.app/)** |
| | Interactive CLI | Bootstrap agents with `nomos init`, run with `nomos run` |
| **Tools & Integration** | Tool Integration | Register Python functions, packages, CrewAI, or LangChain tools |
| | Auto Documentation | Tool descriptions generated from docstrings |
| | External Packages | Reference any Python package function via configuration |
| **LLM Support** | Multiple Providers | OpenAI, Mistral, Gemini, Ollama, and HuggingFace |
| | Structured Responses | Step-level answer models for JSON/object responses |
| | Persona-driven | Consistent, branded agent responses |
| | Decision Examples | Retrieve relevant examples to guide step decisions |
| **Production Ready** | Session Management | Redis/PostgreSQL storage for conversation persistence |
| | Error Handling | Built-in recovery with configurable retry limits |
| | API Integration | FastAPI endpoints for web and WebSocket interaction |
| | Monitoring | Elastic APM tracing and distributed monitoring |
| | Docker Deployment | Pre-built base image for rapid deployment |
| **Extensibility** | Custom Components | Build your own tools, steps, and integrations |
| | Scalable Design | Horizontal scaling with stateless architecture |


## Documentation

For detailed information, check out our comprehensive guides:

| Guide | Description |
|-------|-------------|
| [Getting Started](docs/md/getting-started.md) | Installation, setup, and your first agent |
| [CLI Usage](docs/md/cli-usage.md) | Complete command-line interface guide |
| [Configuration](docs/md/configuration.md) | Python API and YAML configuration |
| [Flow Management](docs/md/flow-management.md) | Advanced workflow organization |
| [LLM Support](docs/md/llm-support.md) | Supported models and providers |
| [Examples](docs/md/examples.md) | Real-world implementation examples |
| [Deployment](docs/md/deployment.md) | Production deployment strategies |
| [Community](docs/md/community.md) | Contributing, support, and project information |

## Additional Resources

- **[Tutorials](docs/md/getting-started.md)**: Step-by-step guides for getting started with NOMOS, from installation to your first agent.
- **[How-to Guides](docs/md/)**: Quick, actionable code snippets for common tasks like tool integration, flow management, and deployment.
- **[Examples](docs/md/examples.md)**: Real-world implementations including a barista ordering system, financial advisor, and travel planner.
- **[API Reference](docs/md/configuration.md)**: Detailed documentation on Python API and YAML configuration options.
- **[CLI Reference](docs/md/cli-usage.md)**: Complete command-line interface documentation for development and deployment.

Join the NOMOS community! For roadmap, support, contributing guidelines, and more, see our [Community Guide](docs/md/community.md).
