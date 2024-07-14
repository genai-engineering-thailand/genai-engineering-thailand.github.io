from langfuse import Langfuse
from config import settings
from uptrain import EvalLLM, Evals
import os
 
os.environ["LANGFUSE_PUBLIC_KEY"] = settings.LANGFUSE_PK_KEY
os.environ["LANGFUSE_SECRET_KEY"] = settings.LANGFUSE_SK_KEY
os.environ["LANGFUSE_HOST"] = settings.LANGFUSE_HOST
 
langfuse = Langfuse()
 
langfuse.auth_check()

def get_traces(service_name,limit=10000):
    all_data = []
    page = 1
 
    while True:
        response = langfuse.client.trace.list(
            tags=[f'service_name:{service_name}'],
            page=page,
            order_by=None
        )
        if not response.data:
            break
        page += 1
        all_data.extend(response.data)
        if len(all_data) > limit:
            break
 
    return all_data[:limit]

def main():
    traces_sample = get_traces("sale")
    evaluation_batch = []
    for t in traces_sample:
        observations = [langfuse.client.observations.get(o) for o in t.observations]
        for o in observations:
            if (o.name == "VectorStoreRetriever"):
                evaluation_batch.append({
                    "trace_id": t.id,
                    "context": o.output,
                    "question": t.input,
                    "response": t.output
                })
    
    eval_llm = EvalLLM(openai_api_key=settings.OPENAI_KEY)
    results = eval_llm.evaluate(
        data=evaluation_batch,
        checks=[Evals.CONTEXT_RELEVANCE, Evals.FACTUAL_ACCURACY, Evals.RESPONSE_COMPLETENESS]
    )

    for row in results:
        for metric_name in ["context_relevance", "factual_accuracy","response_completeness"]:
            langfuse.score(
                name=metric_name,
                value=row["score_"+metric_name],
                trace_id=row["trace_id"]
            )


if __name__=="__main__": 
    main() 