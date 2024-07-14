from langfuse import Langfuse
from config import settings
import numpy as np
import os

from langfuse.decorators import observe
 
os.environ["LANGFUSE_PUBLIC_KEY"] = settings.LANGFUSE_PK_KEY
os.environ["LANGFUSE_SECRET_KEY"] = settings.LANGFUSE_SK_KEY
os.environ["LANGFUSE_HOST"] = settings.LANGFUSE_HOST
 
langfuse = Langfuse()
 
langfuse.auth_check()

rng = np.random.default_rng(12345)

def eval(input, output, expected_ouput):
    # Add your eval here
    return  rng.random()

def model(input):
    messages = [
        {"role":"system", "content": "TEST PROMPT"},
        {"role":"user", "content": input}
    ]
    # Add your model here
    output = input
    return output

@observe()
def main():
    dataset = langfuse.get_dataset("sale_conv")
 
    for item in dataset.items:
        with item.observe(
            run_name="test-hallucinations",
        ) as trace_id:
            output = model(item.input)
    
            langfuse.score(
                trace_id=trace_id,
                name="hallucinations",
                value=eval(item.input, output, item.expected_output),
            )
    
    langfuse.flush()

if __name__=="__main__": 
    main() 