# Self-hosted LLM on GCP

![image info](event_cover.png)


### Resource
[Video](https://youtu.be/bLSB1-iEct0) | [Material](material) | [Knowledge Summary](https://txt.lukkiddd.com/genai-engineer-thailand-0/)


### Summary 

*The following content is summarized by Gemini.*

**Topic 1: Introduction**
- This is the first event hosted by GenAI Engineer Thailand, a community for people who are interested in generative AI.
- The goal of this event is to share knowledge and learn from each other.
- The speaker for this event is Mr. Coco - Senior AI/ML Engineer from ArcFusion.ai

**Topic 2: LLM deployment on GCP**
- Large Language Model (LLM) inference is memory bound, not compute bound. This means it takes longer to load data into GPU memory than it does to process the data itself. 
- Because of this, the bottleneck for LLM inference is the size of the model that can fit into GPU memory.
- Techniques to reduce memory usage and speed up inference include quantization, like AutoGPTQ (reducing the representation size of data) or FlashAttention (modifying the Attention mechanism).
- Ray Serve and vLLM are frameworks that can be used for LLM deployment. 
- Ray and vLLM are tools used together to run large language models (LLMs) efficiently:
    - Ray:
        - Distributed computing framework
        - Manages resources across multiple machines
        - Enables parallel processing and scaling
    - vLLM:
        - Open-source LLM inference engine
        - Optimizes memory usage for faster inference

Together, Ray and vLLM provide a powerful solution for deploying and scaling LLMs in production environments. They are often used to build high-performance LLM serving systems that can handle large volumes of requests.