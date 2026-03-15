from langchain_core.tools import tool

from src.RAG.retriever import (
    get_worst_anomalies,
    get_anomaly_by_sample_id,
    get_window_around_sample,
)
from src.RAG.prompt_builder import build_context_from_df


@tool
def fetch_worst_anomalies(limit: int = 5) -> str:
    """Fetch the worst anomaly records ranked by anomaly score."""
    df = get_worst_anomalies(limit)
    return build_context_from_df(df)


@tool
def fetch_anomaly_by_sample_id(sample_id: int) -> str:
    """Fetch one anomaly record by sample ID."""
    df = get_anomaly_by_sample_id(sample_id)
    return build_context_from_df(df)


@tool
def fetch_window_around_sample(sample_id: int, window_size: int = 20) -> str:
    """Fetch rows around a given sample ID to inspect behavior before and after an anomaly."""
    df = get_window_around_sample(sample_id, window_size)
    return build_context_from_df(df)
