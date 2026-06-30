# Imports
import json
import csv
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

# Function to convert user request in natural language to structured JSON
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

    return json_schema

def generate_dataset(json_schema):
    #  System message to guide LLM's behavior
    system_message = """
    You are a data generator. Given a JSON schema, generate exactly n_rows of realistic data. 
    Respect all constraints (types, ranges, unique values, enums). Respond ONLY with JSON array of objects, 
    one object per row. Even if JSON schema has "NOT PROVIDED", don't leave any blanks, fill them with realistic values. 
    No explanation, no markdown, just raw JSON array.
    """

    messages = [{"role": "system", "content": system_message}, {"role": "user", "content": json.dumps(json_schema)}]

    response = client.chat.completions.create(
        messages = messages,
        model = model,
    )

    # Extracting JSON dictionary from the response
    returned_data = response.choices[0].message.content
    returned_data = returned_data.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    returned_dict = json.loads(returned_data)

    # Writing the generated data into a CSV file
    with open(f"{json_schema["dataset_name"]}.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=json_schema["column_names"].keys())
        writer.writeheader()
        writer.writerows(returned_dict)


def main():
    print("Hello from dataforge-ai!")
    json_schema = generate_schema("""Generate a dataset with columns: name, age, city, job_title""")
    print(json_schema)
    generate_dataset(json_schema)

if __name__ == "__main__":
    main()
