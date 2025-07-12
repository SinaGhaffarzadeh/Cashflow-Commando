# nodes.py

# Import shared state schema
from langgraph_app.schema import State
from typing import Dict


def input_node(state: State) -> State:
    """
    This node receives the raw input state and simply returns it unchanged.
    It acts as the entry point for the LangGraph pipeline.
    """
    print("✅ Received input data")
    return state


def processing_node(state: State) -> State:
    """
    This node performs business logic calculations:
    - Computes daily profit
    - Calculates % change in sales and cost vs. previous day
    - Computes CAC (Customer Acquisition Cost) for today and yesterday
    - Calculates % increase in CAC
    """
    data = state["raw_data"]

    # Today's and yesterday's data (fallback to zeroed dummy if only one day exists)
    today = data[-1]
    yesterday = data[-2] if len(data) > 1 else {"sales": 0, "cost": 0, "number_of_customers": 1}

    # Profit calculation
    profit = today["sales"] - today["cost"]

    # Percentage change in sales and cost compared to yesterday
    sales_pct_change = ((today["sales"] - yesterday["sales"]) / yesterday["sales"] * 100) if yesterday["sales"] else 0
    cost_pct_change = ((today["cost"] - yesterday["cost"]) / yesterday["cost"] * 100) if yesterday["cost"] else 0

    # CAC = cost / number of customers
    today_cac = today["cost"] / today["number_of_customers"] if today["number_of_customers"] else float('inf')
    yesterday_cac = yesterday["cost"] / yesterday["number_of_customers"] if yesterday["number_of_customers"] else float('inf')

    # Percent increase in CAC
    cac_increase_pct = ((today_cac - yesterday_cac) / yesterday_cac * 100) if yesterday_cac else 0

    # Store computed metrics in the state
    state["processed"] = {
        "profit": round(profit, 2),
        "sales_pct_change": round(sales_pct_change, 2),
        "cost_pct_change": round(cost_pct_change, 2),
        "today_cac": round(today_cac, 2),
        "yesterday_cac": round(yesterday_cac, 2),
        "cac_increase_pct": round(cac_increase_pct, 2),
    }

    print("📊 Processed data:", state["processed"])
    return state


def recommendation_node(state: State) -> State:
    """
    This node analyzes the processed metrics and produces:
    - Profit/loss status
    - Alerts if any issues (e.g., CAC spike, negative profit)
    - Actionable recommendations
    """
    metrics = state["processed"]
    
    output = {
        "profit_or_loss": "profit" if metrics["profit"] >= 0 else "loss",
        "alerts": [],
        "recommendations": []
    }

    # Generate alerts and suggestions based on business rules
    if metrics["profit"] < 0:
        output["alerts"].append("Negative profit detected.")
        output["recommendations"].append("Reduce costs if profit is negative.")

    if metrics["cac_increase_pct"] > 20:
        output["alerts"].append(f"CAC increased by {metrics['cac_increase_pct']}%.")
        output["recommendations"].append("Review marketing campaigns if CAC increased significantly.")

    if metrics["sales_pct_change"] > 0:
        output["recommendations"].append("Consider increasing advertising budget if sales are growing.")

    # Store the recommendation output in the state
    state["recommendation"] = output
    print("💡 Final Decision Output:", output)
    return state
