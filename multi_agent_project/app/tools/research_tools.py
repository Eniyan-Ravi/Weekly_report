from langchain_core.tools import tool

def run_search(query: str) -> str:
    from ddgs import DDGS

    results = DDGS().text(query, max_results=5)
    return "\n\n".join(
        f"Title: {r['title']}\nURL: {r['href']}\nContent: {r['body']}"
        for r in results
    ) or f"No results found for: {query}"

@tool
def search_research(query: str) -> str:
    """Search for information related to a research query."""
    return run_search(query)


RESEARCH_TOOLS = [search_research]
