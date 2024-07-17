
# Introduction
This project demonstrates one way of leveraging LLM as a copilot in assisting data record classification task. The approach employs prompt engineering technique called "ReAct" as a reasoning module that enables our Agent to be able to interact with external information beyond LLM knowledge scope.

## Setup 

1. make sure you have `conda` installed


2. create `.env` in this folder containing the following keys to set LLM API key:
```
TYPHOON_API_KEY=...
```

3. setup python environment
```
$ make setup-env
```

4. setup python dependencies 
```
$ make setup-deps
```

5. attach `agent_llm.ipynb` to conda env `genai_share` to run the notebook.