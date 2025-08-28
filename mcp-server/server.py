# MIT License
#
# Copyright (c) 2025 Murat Eken
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
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