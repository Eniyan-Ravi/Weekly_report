from mcp.server.mcpserver import MCPServer

mcp = MCPServer("LLM Tool Demo")


@mcp.tool()
def add(a: float, b: float) -> float:
    """Add two numbers together."""
    return a + b


@mcp.tool()
def subtract(a: float, b: float) -> float:
    """Subtract the second number from the first number."""
    return a - b


@mcp.tool()
def multiply(a: float, b: float) -> float:
    """Multiply two numbers together."""
    return a * b


@mcp.tool()
def get_weather(city: str) -> str:
    """Get the current weather for a city."""
    
    weather = {
        "chennai": "Sunny, 32°C",
        "bangalore": "Cloudy, 25°C",
        "mumbai": "Rainy, 28°C",
    }

    return weather.get(
        city.lower(),
        f"Weather data for {city} is not available."
    )


if __name__ == "__main__":
    mcp.run()