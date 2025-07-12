# graph_builder.py

# Import LangGraph's StateGraph for building workflows
from langgraph.graph import StateGraph

# Import the shared state schema used by all nodes
from langgraph_app.schema import State

# Import node functions that define the logic for each step in the graph
from langgraph_app.nodes import input_node, processing_node, recommendation_node

def build_graph():
    """
    Constructs and compiles a LangGraph with three main nodes:
    1. Input node - receives raw business data
    2. Processing node - computes metrics like profit, CAC, and percentage change
    3. Recommendation node - generates decision support messages based on the metrics

    Returns:
        Compiled LangGraph object ready to be invoked.
    """
    
    # Initialize a graph with the shared state schema
    builder = StateGraph(State)

    # Add the nodes (functions) to the graph
    builder.add_node("input", input_node)             # Start node: passes input unchanged
    builder.add_node("process", processing_node)      # Computes business metrics
    builder.add_node("recommend", recommendation_node)  # Generates alerts and advice

    # Define the flow of the graph
    builder.set_entry_point("input")                  # Input node is the entry point
    builder.add_edge("input", "process")              # After input, go to processing
    builder.add_edge("process", "recommend")          # After processing, go to recommendation
    builder.set_finish_point("recommend")             # End the graph at the recommendation node

    # Compile and return the executable graph
    return builder.compile()
