import os
import pandas as pd
import uuid
from langchain_openai import ChatOpenAI
from langchain_experimental.agents import create_pandas_dataframe_agent
from dotenv import load_dotenv

# Environment Variables
print('Loading Environment Variables.... ', end=' ')
load_dotenv()
print('done')

# Configuration
BASE_URL = os.getenv('BASE_URL')
API_KEY = os.getenv('API_KEY')
LLM_MODEL = os.getenv('LLM_MODEL')

if not BASE_URL:
    print('[ERROR] No Base URL (LLM)\nUpdate "BASE_URL" Environment Variable and try again.')
    exit()
if not API_KEY:
    print('[ERROR] No API Key (LLM)\nUpdate "API_KEY" Environment Variable and try again.')
    exit()
if not LLM_MODEL:
    print('[ERROR] No LLM Model Specified (LLM)\nUpdate "LLM_MODEL" Environment Variable and try again.')
    exit()

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "Titanic-Dataset.csv")
OUTPUT_PLOT_DIR = os.path.join(BASE_DIR, "outputs")
os.makedirs(OUTPUT_PLOT_DIR, exist_ok=True)

# model Setup
model = ChatOpenAI(
    base_url=BASE_URL,
    api_key=API_KEY,
    temperature=0,
    model=LLM_MODEL
)

# System Prompt
PREFIX_PROMPT = """
You are TailorTalk, a friendly data analyst.

COLUMNS: PassengerId, Survived, Pclass, Name, Sex, Age, SibSp, Parch, Ticket, Fare, Cabin, Embarked.

CRITICAL INSTRUCTIONS:
1. You have access to a pandas DataFrame named `df`. 
2. This `df` variable is ALREADY LOADED in your environment and contains the FULL Titanic dataset.
3. DO NOT recreate the dataframe using a dictionary or sample data.
4. DO NOT assume the data is limited to the rows you see in the prompt.
5. Perform all calculations, aggregations, and filtering on the existing `df` variable.
6. Round the results obtained to 2 decimal places.

VISUALIZATION RULES:
- When asked for charts, use matplotlib or seaborn.
- Always use plt.switch_backend('Agg') before saving.
- You must save the figure to the path provided in the user's request.
"""

# Agent Setup
agent = create_pandas_dataframe_agent(
    llm=model,
    df=pd.read_csv(DATA_PATH),
    verbose=True,
    allow_dangerous_code=True,
    prefix=PREFIX_PROMPT
)

def process_query_concurrently(query: str):
    """
    Generates a unique path for this specific run to prevent race conditions.
    """
    run_id = str(uuid.uuid4())
    unique_plot_path = os.path.join(OUTPUT_PLOT_DIR, f"plot_{run_id}.png")
    
    # Inject the unique path constraint directly into this specific query
    dynamic_instruction = f"""
    \n\nIMPORTANT: If generating a plot, you MUST save the figure exactly to this path: r'{unique_plot_path}'
    """
    full_query = query + dynamic_instruction
    
    try:
        response = agent.invoke(full_query)
        return response['output'], unique_plot_path
    except Exception as e:
        return f"I encountered an error analyzing that: {str(e)}", None
