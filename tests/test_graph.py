# test_graph.py

from langgraph_app.schema import State
from langgraph_app.graph_builder import build_graph

def test_agent_output():
    """
    Unit test to validate the LangGraph pipeline output for sample business data.

    This test checks:
    - Presence and correctness of the 'profit_or_loss' key.
    - Whether CAC increase is detected.
    - Whether a recommendation is made when sales are increasing.
    """

    # Initialize the graph using the graph builder
    graph = build_graph()

    # Sample business data with two days for comparison
    state: State = {
        "raw_data": [
            {"date": "2025-07-01", "sales": 2500, "cost": 1500, "number_of_customers": 100},  # CAC = 15.0
            {"date": "2025-07-02", "sales": 3000, "cost": 2000, "number_of_customers": 100}   # CAC = 20.0
        ],
        "processed": None,
        "recommendation": None
    }

    # Run the LangGraph agent
    result = graph.invoke(state)
    rec = result["recommendation"]

    # === Assertions ===
    # Ensure key exists and logic is correct
    assert "profit_or_loss" in rec, "Missing 'profit_or_loss' in output"
    assert rec["profit_or_loss"] == "profit", "Incorrect profit calculation"
    
    # Check that CAC increase alert is present
    assert any("CAC increased" in alert for alert in rec["alerts"]), "Expected CAC increase alert"
    
    # Check for relevant recommendation
    assert "Consider increasing advertising budget if sales are growing." in rec["recommendations"], \
        "Expected sales growth recommendation"

    print("✅ Test passed.")


if __name__ == "__main__":
    # Run the test when the script is executed directly
    test_agent_output()
