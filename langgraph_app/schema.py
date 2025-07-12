# schema.py

from typing import TypedDict, List, Dict, Optional


class DailyData(TypedDict):
    """
    Represents the business data for a single day.

    Attributes:
        date (str): The date of the data point in YYYY-MM-DD format.
        sales (float): Total revenue generated on that day.
        cost (float): Total operational or marketing cost on that day.
        number_of_customers (int): Number of customers acquired that day (used for CAC calculation).
    """
    date: str
    sales: float
    cost: float
    number_of_customers: int


class State(TypedDict):
    """
    The shared state used across LangGraph nodes.

    Attributes:
        raw_data (List[DailyData]): Historical daily business data including today's.
        processed (Optional[Dict]): Output of the processing_node containing computed metrics.
        recommendation (Optional[Dict]): Final analysis result with alerts and recommendations.
    """
    raw_data: List[DailyData]
    processed: Optional[Dict]
    recommendation: Optional[Dict]
