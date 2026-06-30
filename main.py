# Imports
import json

from openai import OpenAI
import gradio as gr
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(override=True)
api_key = os.getenv("GROQ_API_KEY")

# Setting up the client
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=api_key,
)

# Model
model = "llama-3.3-70b-versatile"

def generate_schema(user_request):
    # system message to guide LLM's behavior
    system_message = """
    You are a DataForge, a helpful assistant that generates JSON schemas based on user requests.
    If a user greets with no data description, respond with a friendly greeting and ask them to describe the data 
    they want to generate.
    For example: {Input: "Hi", Output: "Hi there! Please describe the dataset you want to generate."}
    If provided with dataset description, look for the following information to generate a JSON schema:
    dataset_name: "name of the dataset",
    column_names: {"first column": "constraint", 
                   "second column": "constraint", 
                   "third column": "constraint",...},
    n_rows: number of rows to generate.
    If columns not provided, ask the user to provide the dataset description with column names.
    Always include n_rows in the JSON schema, even if not provided by the user. If not provided,
    set it to "NOT PROVIDED". If dataset name or constraints are not provided, keep them as 
    "NOT PROVIDED" in the JSON schema. ONLY RESPOND WITH JSON SCHEMA WHEN DATA DESCRIPTION IS PROVIDED. 
    DO NOT RESPOND WITH ANYTHING ELSE.
    """
    # messages list
    messages = [{"role": "system", "content": system_message}, {"role": "user", "content": user_request}]

    # LLM call
    response = client.chat.completions.create(
        messages = messages,
        model = model,
    )

    # Extracting the JSON schema from the response
    json_schema = response.choices[0].message.content
    json_schema = json_schema.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    try:
        json_schema = json.loads(json_schema)
    except json.decoder.JSONDecodeError:
        print(json_schema)
        return json_schema

    # Handling missing data
    if json_schema.get("n_rows") == "NOT PROVIDED":
        json_schema["n_rows"] = 10
    if json_schema.get("dataset_name") == "NOT PROVIDED":
        json_schema["dataset_name"] = "your_dataset"

    print(json_schema)
    return json_schema

def main():
    print("Hello from dataforge-ai!")
    generate_schema("""Generate a dataset with columns: name, age, city, job_title""")

if __name__ == "__main__":
    main()
