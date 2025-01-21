import numpy as np
import pandas as pd
from openai import OpenAI
from typing import List
from scipy import spatial
from dotenv import load_dotenv

import os

load_dotenv()

def distances_from_embeddings(
 query_embedding: List[float],
 embeddings: List[List[float]],
 distance_metric="cosine",
 ) -> List[List]:
    distance_metrics = {
        "cosine": spatial.distance.cosine,
        "L1": spatial.distance.chebyshev,
        "L2": spatial.distance.euclidean,
        "Linf": spatial.distance.chebyshev,
    }
    distances = [distance_metrics[distance_metric](query_embedding, embedding)
    for embedding in embeddings
    ]
    return distances
openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def create_context(question, df, max_len=1800):
    """
    Create a context for a question by finding the most similar
    context from the dataframe
    """
    # Get the embeddings for the question
    q_embeddings = openai.embeddings.create(
        input=question, model='text-embedding-3-small').data[0].embedding

    # Get the distances from the embeddings
    df['distances'] = distances_from_embeddings(
        q_embeddings,
        df['embeddings'].values,
        distance_metric='cosine'
    )

    returns = []
    cur_len = 0

    # Sort by distance and add the text to the context until the context is too long
    for i, row in df.sort_values('distances', ascending=True).iterrows():
        # Add the length of the text to the current length
        cur_len += row['n_tokens'] + 4
        
        # If the context is too long, break
        if cur_len > max_len:
            break
            
        # Else add it to the text that is being returned
        returns.append(row["text"])
    
    # Return the context
    return "\n\n###\n\n".join(returns)

def answer_question(
    df: pd.DataFrame,
    model: str = "gpt-4o",
    question: str = "What is the meaning of life?",
    max_len: int = 1800,
    debug: bool = False,
    max_tokens: int = 150,
    stop_sequence: str | None = None
) -> str:
    """
    Answer a question based on the most similar context from the dataframe texts
    """
    context = create_context(
        question,
        df,
        max_len=max_len,
    )
    
    if debug:
        print("Context:\n" + context)
        print("\n\n")
        print(f"Model: {model}")
        print(f"Question: {question}")
        print(f"Max Tokens: {max_tokens}")
        print(f"Stop Sequence: {stop_sequence}")
    
    try:
        prompt = (
            "Answer the question based on the context below, and if the question "
            "can't be answered based on the context, say \"I don't know.\" Try to "
            "cite sources to the links in the context when possible.\n\n"
            f"Context: {context}\n\n"
            "---\n\n"
            f"Question: {question}\n"
            "Answer:"
        )
        
        print(prompt)
        
        response = openai.chat.completions.create(
            model=model,
            messages=[{
                "role": "user",
                "content": prompt
            }],
            temperature=0,
            max_tokens=max_tokens,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=stop_sequence,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(e)
        return ""