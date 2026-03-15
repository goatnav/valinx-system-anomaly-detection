from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage

from src.RAG.chain import build_llm, SYSTEM_PROMPT
from src.RAG.tools import (
    fetch_worst_anomalies,
    fetch_anomaly_by_sample_id,
    fetch_window_around_sample,
)

TOOL_MAP = {
    fetch_worst_anomalies.name: fetch_worst_anomalies,
    fetch_anomaly_by_sample_id.name: fetch_anomaly_by_sample_id,
    fetch_window_around_sample.name: fetch_window_around_sample,
}



def run_turn(llm, user_input: str) -> str:
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=user_input),
    ]

    response = llm.invoke(messages)

    while getattr(response, "tool_calls", None):
        messages.append(response)

        for tool_call in response.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call.get("args", {})
            tool = TOOL_MAP[tool_name]
            tool_result = tool.invoke(tool_args)

            messages.append(
                ToolMessage(
                    content=tool_result,
                    tool_call_id=tool_call["id"],
                )
            )

        response = llm.invoke(messages)

    return response.content


def main():
    llm = build_llm()

    print("VALinX is ready. Type 'exit' to quit.\n")

    while True:
        user_input = input("Ask VALinX: ").strip()

        if user_input.lower() in {"exit", "quit"}:
            print("Goodbye.")
            break

        answer = run_turn(llm, user_input)
        print("\nVALinX:\n")
        print(answer)
        print()


if __name__ == "__main__":
    main()
