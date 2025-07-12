# main.py

# Import necessary modules
import pandas as pd  # For reading CSV and handling tabular data
from langgraph_app.schema import DailyData, State  # TypedDict schemas for input and state structure
from langgraph_app.graph_builder import build_graph  # Function to build the LangGraph workflow

# Step 1: Load business data from CSV
df = pd.read_csv("data/business_data.csv")  # Reads daily business data (e.g., sales, costs, customers)
raw_data: list[DailyData] = df.to_dict(orient="records")  # Converts DataFrame to list of dictionaries matching DailyData schema

# Step 2: Build the LangGraph computational workflow
graph = build_graph()  # Returns a compiled LangGraph instance with defined nodes and edges

# Step 3: Prepare the initial state to pass into the agent
initial_state: State = {
    "raw_data": raw_data,         # Full input data (multiple days)
    "processed": None,            # Will be filled after processing node runs
    "recommendation": None        # Will be filled after recommendation node runs
}

# Step 4: Run the LangGraph agent with the input data
result = graph.invoke(initial_state)  # Executes the full graph pipeline on the input state

# Step 5: Output the result (recommendations based on the business analysis)
print("✅ Final Output:", result["recommendation"])  # Displays alerts, profit/loss status, and advice
