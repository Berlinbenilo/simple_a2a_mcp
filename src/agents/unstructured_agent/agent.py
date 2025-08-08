import asyncio
import os
from typing import List, Literal

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from pydantic import BaseModel

load_dotenv(override=True)

memory = MemorySaver()


def _fetch_mcp_tools_sync() -> List:
    """
    Helper function: runs the async MultiServerMCPClient code in a synchronous manner.
    Fetches the remote tools from your MCP server(s).
    """
    servers_config = {
        "vector_search": {
            "url": "http://localhost:3000/mcp/",
            "transport": "streamable_http",
        }
    }

    async def _fetch_tools():
        client = MultiServerMCPClient(servers_config)
        return await client.get_tools()

    return asyncio.run(_fetch_tools())


class ResponseFormat(BaseModel):
    """Respond to the user in this format."""
    status: Literal["input_required", "completed", "error"] = "input_required"
    message: str


class UnstructuredAgent:
    """UnstructuredAgent is a LangGraph agent that uses Google Generative AI to answer questions about a user's
    resume and personal information."""
    SYSTEM_INSTRUCTION = """You are an assistant that help user to answer about personal information that prvided in 
    there resume. You can use "vector_search" tool to search for relevant information in the vector database.
    If user ask anything other than resume related information, asnwer with "I am not sure about that, please" \
    "ask me about my resume" """

    def __init__(self):
        self.tools = _fetch_mcp_tools_sync()

        self.model = ChatGoogleGenerativeAI(model="gemini-2.0-flash",
                                            google_api_key=os.getenv("GOOGLE_API_KEY"))
        self.graph = create_react_agent(
            self.model,
            tools=self.tools,
            checkpointer=memory,
            prompt=self.SYSTEM_INSTRUCTION,
            response_format=ResponseFormat,
        )

    async def invoke(self, query: str, session_id: str):
        """ Invoke the agent with a query and session ID.
        Args:
            query (str): The user's query.
            session_id (str): The session ID for tracking the conversation.
        Yields:
            Return a stream of updates back to the caller as the agent processes the query

        {
            'is_task_complete': bool,  # Indicates if the task is complete
            'updates': str,  # Updates on the task progress
            'content': str  # Final result of the task if complete
        }
        """
        config = {"configurable": {"thread_id": session_id}}
        await self.graph.ainvoke({"messages": [("user", query)]}, config)
        current_state = self.graph.get_state(config)
        structured_response = current_state.values.get("structured_response")
        print("===============STATE=====================")
        print(current_state)
        print("===============STRUCTURED RESPONSE=====================")
        print(structured_response)
        if structured_response and isinstance(structured_response, ResponseFormat):
            if structured_response.status == "completed":
                yield {
                    "is_task_complete": True,
                    "content": structured_response.message,
                }
        yield {
            "is_task_complete": False,
            "updates": " Agent is processing your request, please wait...",
        }
