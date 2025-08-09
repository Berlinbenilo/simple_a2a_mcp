<h1 align="center">A2A protocol & MCP</h1>
This project implements google's [A2A protocol] and [MCP] from scratch, which allows you to create a custom agent that can interact with other agents and perform tasks in a collaborative manner.

## Getting Started

### Prerequisites

*   Python 3.11+
*   `uv`

### Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/Berlinbenilo/simple_a2a_mcp.git
    cd simple_a2a_mcp
    ```
2.  **Create and activate the virtual environment:**

*   **macOS/Linux:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```
  *   **Windows:**
      ```bash
      python -m venv .venv
      .venv\Scripts\activate
      ```
3.  **Install dependencies:**
    ```bash
    uv pip install -r requirements.txt
    ```

## How to Run

1.  **Streamable HTTP Server:**
    The vector search server is using chroma db for store document information to retrieve resume data (trail data).
    ```bash
    uv run python3 -m src.mcp.servers.arithmetic_server
    uv run python3 -m src.mcp.servers.vector_search
    ```
2.  **Unstructured langgraph Agent:**

    The unstructured agent is a simple agent that can perform vector search using the MCP protocol.
    ```bash
    uv run python3 -m src.agents.unstructured_agent
    ```
3.  **Host Agent:**
    ```bash
    uv run python3 -m src.agents.host_agent
    ```
4.  **CMD App:**
    ```bash
    uv run python main.py
    ```

### Note: 
Main app will start a command line interface where you can interact with the agents. Feel free to add your own agents and implement your own logic.
Note: I haven't included the chroma db database in the repository, so you will need to create a database and add 
your own documents to it. You can use the `src/mcp/servers/vector_search.py` script to add documents to the database.
Also give your own description to the documents, so the vector search can work properly.