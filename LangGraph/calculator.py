from typing import TypedDict
from langgraph.graph import StateGraph, START, END


#state
class CalculatorState(TypedDict):
    num1: float
    num2: float
    operator: str
    result: float

#Nodes
def parse_input(state: CalculatorState):
    """validate the calculator input."""
    operator = state["operator"].strip()
    return {
        "operator": operator
    }


def add(state: CalculatorState):
    result = state["num1"] + state["num2"]
    return {
        "result": result
    }


def subtract(state: CalculatorState):
    result = state["num1"] - state["num2"]
    return {
        "result": result
    }


def multiply(state: CalculatorState):
    result = state["num1"] * state["num2"]
    return {
        "result": result
    }


def divide(state: CalculatorState):
    if state["num2"] == 0:
        raise ValueError("Cannot divide by zero.")
    result = state["num1"] / state["num2"]
    return {
        "result": result
    }


# 3. Conditional routing func
def choose_operation(state: CalculatorState):
    """Decide which node should execute next."""
    operator = state["operator"]
    if operator == "+":
        return "add"
    elif operator == "-":
        return "subtract"
    elif operator == "*":
        return "multiply"
    elif operator == "/":
        return "divide"
    else:
        raise ValueError(f"Unsupported operator: {operator}")


#Create the graph
graph = StateGraph(CalculatorState)


#Add nodes
graph.add_node("parse_input", parse_input)
graph.add_node("add", add)
graph.add_node("subtract", subtract)
graph.add_node("multiply", multiply)
graph.add_node("divide", divide)

#Add edges
graph.add_edge(START, "parse_input")

# Conditional edge
graph.add_conditional_edges(
    "parse_input",
    choose_operation,
    {
        "add": "add",
        "subtract": "subtract",
        "multiply": "multiply",
        "divide": "divide"
    }
)


# Every operation finishes the graph
graph.add_edge("add", END)
graph.add_edge("subtract", END)
graph.add_edge("multiply", END)
graph.add_edge("divide", END)

#Compile
app = graph.compile()


#Run the calculator
num1 = float(input("Enter first number: "))
operator = input("Enter operator (+, -, *, /): ")
num2 = float(input("Enter second number: "))
result = app.invoke({
    "num1": num1,
    "num2": num2,
    "operator": operator,
    "result": 0
})

print("Result:", result["result"])

print("Result:", result["result"])