from typing import TypedDict

from langgraph.graph import StateGraph
from langgraph.graph import END

from agents.classifier_agent import classify_query
from agents.rag_agent import retrieve_context
from agents.response_agent import generate_answer


class FarmerState(TypedDict):
    question: str
    classification: str
    context: str
    answer: str


# NODE 1

def classify_node(state):
    result = classify_query(state["question"])

    return {
        "classification": result
    }


# NODE 2

def rag_node(state):
    context = retrieve_context(state["question"])

    return {
        "context": context
    }


# NODE 3

def response_node(state):
    answer = generate_answer(
        question=state["question"],
        context=state["context"]
    )

    return {
        "answer": answer
    }


# NODE 4

def reject_node(state):
    return {
        "answer": "It's not farmer or farm related question."
    }


# CONDITIONAL ROUTING

def route_question(state):
    if state["classification"] == "FARM":
        return "rag"

    return "reject"


builder = StateGraph(FarmerState)

builder.add_node("classifier", classify_node)
builder.add_node("rag", rag_node)
builder.add_node("response", response_node)
builder.add_node("reject", reject_node)

builder.set_entry_point("classifier")

builder.add_conditional_edges(
    "classifier",
    route_question,
    {
        "rag": "rag",
        "reject": "reject"
    }
)

builder.add_edge("rag", "response")
builder.add_edge("response", END)
builder.add_edge("reject", END)

farmer_graph = builder.compile()