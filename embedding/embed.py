import pandas as pd
import os
import tiktoken
from openai import OpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

DOMAIN = "developer.mozilla.org"

def remove_newlines(series):
    series = series.str.replace('\n', ' ')
    series = series.str.replace('\\n', ' ')
    series = series.str.replace(' ', ' ')
    series = series.str.replace(' ', ' ')
    return series

# create a list to store the text files
texts = []
print(f"Starting to process files from text/{DOMAIN}/")

#Get all the text files in the text directory
for file in os.listdir("text/" + DOMAIN + "/"):
    print(f"Processing file: {file}")
    # Open the file and read the text
    with open("text/" + DOMAIN + "/" + file, "r", encoding = "UTF-8") as f:
        text = f.read()
        filename = file[:-4].replace("_", "/")

    # Skip only login pages and contributor pages
    if 'user/fxa/login' in filename or 'contributors.txt' in file:
        print(f"Skipping file: {file}")
        continue            

    # Add the text to the list
    texts.append((filename, text))

print(f"Total files processed: {len(texts)}")

# Create a dataframe with the texts
df = pd.DataFrame(texts, columns=["fname", "text"])
print(f"Initial DataFrame shape: {df.shape}")

df['text'] = df.fname + ". " + remove_newlines(df.text)
print("Saving scraped.csv...")
df.to_csv('processed/scraped.csv')
print("scraped.csv saved successfully")

tokenizer = tiktoken.get_encoding("cl100k_base")

print("Reading scraped.csv...")
df = pd.read_csv('processed/scraped.csv', index_col=0)
df.columns = ['title', 'text']
print(f"DataFrame after reading scraped.csv shape: {df.shape}")

df['n_tokens'] = df.text.apply(lambda x: len(tokenizer.encode(x)))
print(f"Average tokens per document: {df['n_tokens'].mean():.2f}")

chunk_size = 1000 # Max number of tokens
print(f"Starting text splitting with chunk_size: {chunk_size}")

text_splitter = RecursiveCharacterTextSplitter(length_function = len, 
                                               chunk_size=chunk_size, 
                                               chunk_overlap=0,
                                               add_start_index=False)

shortened = []
total_rows = len(df)
for idx, row in enumerate(df.iterrows(), 1):
    if row[1]['text'] is None:
        print(f"Skipping row {idx}/{total_rows} - None text")
        continue
    if row[1]['n_tokens'] > chunk_size:
        print(f"Splitting row {idx}/{total_rows} - {row[1]['n_tokens']} tokens")
        chunks = text_splitter.create_documents([row[1]['text']])
        for chunk in chunks:
            shortened.append(chunk.page_content)
    else:
        shortened.append(row[1]['text'])
    
    if idx % 10 == 0:
        print(f"Processed {idx}/{total_rows} rows")

print(f"Creating final DataFrame with {len(shortened)} chunks")
df = pd.DataFrame(shortened, columns=['text'])
df['n_tokens'] = df.text.apply(lambda x: len(tokenizer.encode(x)))
print(f"Final DataFrame shape before embeddings: {df.shape}")

print("Generating embeddings...")
df['embeddings'] = df.text.apply(lambda x: client.embeddings.create(input=x, model='text-embedding-ada-002').data[0].embedding)
print("Embeddings generated successfully")

print("Saving embeddings.csv...")
df.to_csv('processed/embeddings.csv')
print("Process completed successfully")