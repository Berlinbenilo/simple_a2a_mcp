import httpx
from a2a.client import A2ACardResolver
from a2a.types import (
    AgentCard
)

BASE_URLS = ["http://localhost:10000"]


class AgentDiscovery:
    """
    Discovers A2A Agents by reading a registry file of URLs and
    querying each one's /.well-known/agent.json endpoint to retrieve
    an AgentCard

    Attributes:
        base_urls (List[str]): List of base URLs for A2A Agents.
    """

    def __init__(self):
        """
        Initialise the AgentDiscovery
        """

        self.base_urls = BASE_URLS

    async def list_agent_cards(self) -> list[AgentCard]:
        """
        Asynchronously fetches AgentCards from each
        base URL in the registry.

        Returns:
            list[AgentCard]: List of AgentCards retrieved from the agents.
        """
        cards: list[AgentCard] = []

        async with httpx.AsyncClient(timeout=300.0) as httpx_client:
            for base_url in self.base_urls:
                resolver = A2ACardResolver(
                    base_url=base_url.rstrip('/'),
                    httpx_client=httpx_client
                )
                card = await resolver.get_agent_card()

                cards.append(card)

        return cards
