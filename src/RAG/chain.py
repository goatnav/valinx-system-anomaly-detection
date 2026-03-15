from langchain_ollama import ChatOllama

from src.RAG.tools import (
    fetch_worst_anomalies,
    fetch_anomaly_by_sample_id,
    fetch_window_around_sample,
)

TOOLS = [
    fetch_worst_anomalies,
    fetch_anomaly_by_sample_id,
    fetch_window_around_sample,
]

SYSTEM_PROMPT = """
You are VALinX, an AI assistant for analyzing system anomalies.

Use tools when the user asks about specific anomaly records, sample IDs, worst anomalies,
or behavior around an anomaly.

When tool results are returned:
- do not just copy the records back
- summarize the most important patterns
- point out which metrics seem most unusual
- mention when the likely cause is uncertain
- keep answers concise but useful

If the user asks for raw details, you may include them briefly.
Do not invent evidence.
If tool output is missing or insufficient, say so clearly.
If the user asks a general conceptual question, answer directly without using tools when appropriate.
""".strip()



def build_llm():
    llm = ChatOllama(
        model="qwen2.5:3b",
        temperature=0,
    )

    return llm.bind_tools(TOOLS)
