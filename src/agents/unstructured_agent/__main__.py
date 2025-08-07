import click
import uvicorn
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentSkill, AgentCard, AgentCapabilities

from src.agents.unstructured_agent.agent_executor import UnstructuredAgentExecutor


@click.command()
@click.option('--host', default='localhost', help='Host for the agent server')
@click.option('--port', default=10000, help='Port for the agent server')
def main(host: str, port: int):
    """
    Main function to create and run the website builder agent.
    """
    skill = AgentSkill(
        id="unstructured_agent_skill",
        name="unstructured_agent_skill",
        description="A skill for the unstructured agent that can answer questions based on a user's resume.",
        tags=["unstructured", "resume", "question-answering", "vector-search"],
        examples=[
            """What is the education of Swetha.""",
            """How many company swetha worked on.""",
        ]
    )

    agent_card = AgentCard(
        name="unstructured_agent",
        description="An agent that can answer questions based on a user's resume using vector search and build with "
                    "langgraph react agent.",
        url=f"http://{host}:{port}/",
        version="1.0.0",
        default_input_modes=["text"],
        default_output_modes=["text"],
        skills=[skill],
        capabilities=AgentCapabilities(streaming=True),
    )

    request_handler = DefaultRequestHandler(
        agent_executor=UnstructuredAgentExecutor(),
        task_store=InMemoryTaskStore()
    )

    server = A2AStarletteApplication(
        agent_card=agent_card,
        http_handler=request_handler
    )

    uvicorn.run(server.build(), host=host, port=port)


if __name__ == "__main__":
    main()
