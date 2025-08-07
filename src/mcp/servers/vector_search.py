from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field

from src.constants.vectorstore_properties import vector_store

mcp = FastMCP(
    "vector_search",
    host="localhost",
    port=3000,
    stateless_http=True,
)


class VectorSearchInput(BaseModel):
    query: str = Field(description="The search query to find relevant documents in the vector database.")
    top_k: int = Field(default=5, description="Number of top documents to return.")


class VectorSearchResponse(BaseModel):
    content: str = Field(description="Retrieved document contents from vector search")


@mcp.tool("vector_search", description="Search for relevant information in the vector database.")
async def vector_search(search_input: VectorSearchInput) -> VectorSearchResponse:
    """
    Use this tool to search for relevant information in the vector database. This tool MUST be used for all user
    queries that require information retrieval.
    :param search_input: query (string) - the search query, top_k (int) - number of results to return,
    :return: List of documents containing the search results
    """
    results = await vector_store.asimilarity_search(search_input.query, k=search_input.top_k)
    contents = "\n".join([doc.page_content for doc in results])
    return VectorSearchResponse(content=contents)


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
