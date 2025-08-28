import asyncio
import logging
import os

from fastmcp import FastMCP 


logger = logging.getLogger(__name__)
logging.basicConfig(format="[%(levelname)s]: %(message)s", level=logging.INFO)

mcp = FastMCP("MCP Server on Cloud Run", stateless_http=True)

HERO_LOOKUP = {
  "MYSTICAL": [
    "Αλκμήνη",
    "سارة"
  ],
  "TECHNOLOGICAL": [
    "晴香",
    "سارة"
  ],
  "CRIMINAL": [
    "Ծովինար",
    "Кассиопея",
    "თამარი"
  ]
}

@mcp.tool()
def match_hero(available_heroes: list[str], threat_type: str) -> str:
    """Use this to find the matching hero to a threat type.

    Args:
        available_heroes: The list of available heroes 
        threat_type: The classification of the threat type, one of MYSTICAL, TECHNOLOGICAL or CRIMINAL

    Returns:
        The most appropriate hero, or the empty string if no hero matches
    """
    logger.info(f">>> 🛠️ Tool: 'match_hero' called with '{available_heroes}' and '{threat_type}'")
    
    heroes_for_threat = HERO_LOOKUP.get(threat_type, [])
    matching_heroes = list(set(available_heroes) & set(heroes_for_threat))
    return matching_heroes[0] if matching_heroes else ""


if __name__ == "__main__":
    logger.info(f"🚀 MCP server started on port {os.getenv('PORT', 8080)}")
    # Could also use 'sse' transport, host="0.0.0.0" required for Cloud Run.
    asyncio.run(
        mcp.run_async(
            transport="streamable-http",
            path="/",
            host="0.0.0.0",
            port=os.getenv("PORT", 8080),
        )
    )