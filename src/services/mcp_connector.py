import asyncio
import logging

from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool import StdioConnectionParams
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPServerParams

from mcp import StdioServerParameters
from rich import print
from src.constants.config import servers_config

# ADDED: Configure logging for MCP cleanup issues to reduce noise during shutdown
logging.getLogger("mcp").setLevel(logging.ERROR)
logger = logging.getLogger(__name__)


class MCPConnector:
    """
    Discovers the MCP servers from the config.
    Config will be loaded by the MCP discovery class
    Then it lists each server's tools
    and then caches them as MCPToolsets that are compatible with
    Google's Agent Development Kit
    """

    def __init__(self):
        self.servers_config = servers_config
        self.tools: list[MCPToolset] = []

    def _load_all_tools(self):
        """
        Loads all tools from the discovered MCP servers
        and caches them as MCPToolsets.
        """

        tools = []

        for name, server in self.servers_config.items():
            try:
                if server.get("command") == "streamable_http":
                    conn = StreamableHTTPServerParams(url=server["args"][0])
                else:
                    conn = StdioConnectionParams(
                        server_params=StdioServerParameters(
                            command=server["command"],
                            args=server["args"]
                        ),
                        timeout=5
                    )

                mcp_toolset = MCPToolset(connection_params=conn)
                print(
                    f"[bold green]Loaded tools from server [cyan]'{name}'[/cyan]:[/bold green]")
                tools.append(mcp_toolset)

            except Exception as e:
                print(f"[bold red]Error loading tools from server '{name}': {e} (skipping)[/bold red]")
        self.tools = tools

    def get_tools(self) -> list[MCPToolset]:
        """
        Returns the cached list of MCPToolsets.
        """

        self._load_all_tools()
        return self.tools.copy()