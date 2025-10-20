#!/usr/bin/env python3
"""
Joke MCP Server - Built with FastMCP
A simple MCP server that provides jokes through various tools.
Compatible with Microsoft Copilot Studio and other MCP clients.
"""

import random
from typing import Literal
from fastmcp import FastMCP

# Joke collections
PROGRAMMING_JOKES = [
    {
        "setup": "Why do programmers prefer dark mode?",
        "punchline": "Because light attracts bugs!"
    },
    {
        "setup": "Why do Java developers wear glasses?",
        "punchline": "Because they don't C#!"
    },
    {
        "setup": "How many programmers does it take to change a light bulb?",
        "punchline": "None. It's a hardware problem!"
    },
    {
        "setup": "What's a programmer's favorite hangout place?",
        "punchline": "Foo Bar!"
    },
    {
        "setup": "Why did the programmer quit his job?",
        "punchline": "Because he didn't get arrays (a raise)!"
    }
]

DAD_JOKES = [
    {
        "setup": "What do you call a bear with no teeth?",
        "punchline": "A gummy bear!"
    },
    {
        "setup": "Why don't eggs tell jokes?",
        "punchline": "They'd crack each other up!"
    },
    {
        "setup": "What do you call a fake noodle?",
        "punchline": "An impasta!"
    },
    {
        "setup": "Why don't scientists trust atoms?",
        "punchline": "Because they make up everything!"
    },
    {
        "setup": "What did the ocean say to the beach?",
        "punchline": "Nothing, it just waved!"
    }
]

KNOCK_KNOCK_JOKES = [
    {
        "setup": "Knock knock. Who's there? Interrupting cow. Interrupting cow w—",
        "punchline": "MOOOOO!"
    },
    {
        "setup": "Knock knock. Who's there? Boo. Boo who?",
        "punchline": "Don't cry, it's just a joke!"
    },
    {
        "setup": "Knock knock. Who's there? Tank. Tank who?",
        "punchline": "You're welcome!"
    }
]

# Initialize the FastMCP server
mcp = FastMCP("Joke Server 😄")


@mcp.tool()
def get_random_joke() -> str:
    """Get a random joke from all categories"""
    all_jokes = PROGRAMMING_JOKES + DAD_JOKES + KNOCK_KNOCK_JOKES
    joke = random.choice(all_jokes)
    return f"😄 {joke['setup']}\n\n{joke['punchline']}"


@mcp.tool()
def get_joke_by_category(
    category: Literal["programming", "dad", "knock_knock"]
) -> str:
    """Get a random joke from a specific category
    
    Args:
        category: The category of joke to retrieve (programming, dad, or knock_knock)
    """
    if category == "programming":
        joke = random.choice(PROGRAMMING_JOKES)
    elif category == "dad":
        joke = random.choice(DAD_JOKES)
    elif category == "knock_knock":
        joke = random.choice(KNOCK_KNOCK_JOKES)
    else:
        raise ValueError(f"Unknown category: {category}")
    
    return f"😄 [{category.upper()} JOKE]\n\n{joke['setup']}\n\n{joke['punchline']}"


@mcp.tool()
def get_multiple_jokes(count: int) -> str:
    """Get multiple random jokes at once
    
    Args:
        count: Number of jokes to retrieve (1-10)
    """
    if not 1 <= count <= 10:
        raise ValueError("Count must be between 1 and 10")
    
    all_jokes = PROGRAMMING_JOKES + DAD_JOKES + KNOCK_KNOCK_JOKES
    selected_jokes = random.sample(all_jokes, min(count, len(all_jokes)))
    
    jokes_text = "\n\n---\n\n".join([
        f"😄 Joke {i+1}:\n{joke['setup']}\n\n{joke['punchline']}"
        for i, joke in enumerate(selected_jokes)
    ])
    
    return jokes_text


@mcp.tool()
def list_joke_categories() -> str:
    """List all available joke categories"""
    categories = [
        "📚 PROGRAMMING - Tech and coding jokes",
        "👨 DAD - Classic dad jokes",
        "🚪 KNOCK_KNOCK - Knock knock jokes"
    ]
    return "Available joke categories:\n\n" + "\n".join(categories)


# Resources provide read-only access to data
@mcp.resource("joke://stats")
def get_joke_stats() -> str:
    """Get statistics about the joke collection"""
    total = len(PROGRAMMING_JOKES) + len(DAD_JOKES) + len(KNOCK_KNOCK_JOKES)
    return f"""Joke Server Statistics:
    
📚 Programming jokes: {len(PROGRAMMING_JOKES)}
👨 Dad jokes: {len(DAD_JOKES)}
🚪 Knock-knock jokes: {len(KNOCK_KNOCK_JOKES)}
📊 Total jokes: {total}
"""


# Run the server
if __name__ == "__main__":
    import sys
    
    # Check command line arguments for transport type
    # Default to HTTP for Copilot Studio
    if len(sys.argv) > 1 and sys.argv[1] == "--stdio":
        # STDIO transport for local tools like Claude Desktop
        print("Starting Joke MCP Server with STDIO transport...", file=sys.stderr)
        mcp.run(transport="stdio")
    else:
        # HTTP transport for Copilot Studio
        print("Starting Joke MCP Server with HTTP transport on http://localhost:8000/mcp", file=sys.stderr)
        print("Use --stdio flag for STDIO transport", file=sys.stderr)
        mcp.run(transport="http", host="0.0.0.0", port=8000, path="/mcp")
