# DataForge AI 🛢️

An AI-powered synthetic dataset generator that converts natural language descriptions 
into downloadable CSV datasets.

## How It Works

1. Describe the dataset you want in plain English
2. Click "Generate Dataset"
3. Download your CSV

## 🌐 Try DataForge AI Yourself!  
**Link to deployed application: [Launch the DataForge AI App](https://huggingface.co/spaces/krishMakwana-0801/dataforge-ai)**


## Example Inputs

**Detailed:**
Generate a dataset of 25 rows for an e-commerce orders table.
Columns: order_id (integer, unique), customer_name (string),
product (string), quantity (integer, between 1 and 10),
price (float, between 5.99 and 499.99), status (string,
one of: pending, shipped, delivered, cancelled)

Sample Output of above prompt can be seen in e-commerce orders.csv

**Minimal:**
Generate a dataset with columns: name, age, city, job_title

## Architecture

Two-stage LLM pipeline built on Groq:

- **LLM 1 (Schema Extractor)** : Parses natural language into a structured JSON schema, inferring types, constraints, and defaults
- **LLM 2 (Data Generator)** : Takes the schema and generates realistic, constraint-respecting row data
- **Python** : Validates defaults, enforces row counts, writes CSV

## Tech Stack
- Groq API (llama-3.3-70b-versatile)
- Gradio
- Python
- Hugging Face Spaces

## Setup
1. Clone the repo
2. Run `uv sync`
3. Add your Groq API key to `.env`:
GROQ_API_KEY=your_key_here
4. Run `python app.py`