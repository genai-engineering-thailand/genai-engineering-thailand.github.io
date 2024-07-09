# Introduction to Ollama

![image info](./event_cover.png)

### Resource

[Video](https://www.youtube.com/watch?v=oWIi7MVHQpw) | [Material](./material/content.md) | [Knowledge Summary](https://txt.lukkiddd.com/introduction-to-ollama/)

### Summary

_The following content is summarized by Gemini._

**Introduction**

The speaker introduces himself as Pako, a Tech guy from PALO IT. He is excited to share what he learned about Ollama.

**Why run LLM or SLM locally:**

The speaker discusses why one would want to run LLM or SLM locally when there are already commercial, well-known servers available. Reasons for running locally include:

- Developer can learn and experiment with LM concepts more easily on their own machine without any cost.
- It helps improve coding skills in writing prompts as the local LM is not as powerful as mainstream models.

**What is Ollama**:

Ollama is a wrapper for llama.cpp. It allows you to run LLM on your local CPU or laptop. Ollama converts the model to a format that can be run on the CPU. It is a powerful tool that can run various things including converting models.
Ollama improves developer experience by allowing them to run LLM and serve as an APIs. This means you can use large language models through APIs. Ollama becomes versatile and can be used in Docker, Kubernetes environments, etc. It can also be called through NodeJS, Python, etc. Ollama comes with good community support on Discord.

**Background of Ollama:**

The speaker talks about the background of Ollama. Since the developers of Ollama previously worked on Docker, the command line interface (CLI) is similar to Docker. For instance, commands like push model, pull model, and ama run are similar to Docker commands.

**How to use OLM:**

Ollama is not necessarily the fastest because it runs on your local machine. Be patient when running models as it depends on your CPU. Ollama itself is not a model, it runs models that are converted to gguf format. Converting models to gguf is not difficult and there are tools available including Ollama itself. There are instructions and libraries to convert various model formats to gguf.

The speaker walks through downloading and running Ollama from the Github page. He shows that Ollama can list models available on the machine and you can see the configuration by running the show config command. Ollama also has templates which are ready-made prompts that can be used. It can also run LoRA adapters.

**What's Next**

The speaker suggests exploring Kubernetes with Ollama to run models on Kubernetes. He also recommends exploring creating custom models and using Ollama with libraries like Tensorflow or PyTorch. Finally, he suggests trying out fine-tuning models from UnSloth and using them in Ollama.
