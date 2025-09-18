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
import os

from google.adk import Agent
from google.adk.tools.mcp_tool import MCPToolset
from google.adk.tools.mcp_tool import StreamableHTTPConnectionParams

import resource_cleaner_agent.tools as tools

MCP_SERVER_CLOUD_RUN_URL=os.getenv("MCP_SERVER_CLOUD_RUN_URL", "http://localhost:8888")


mcp_tool_set = MCPToolset(
    connection_params=StreamableHTTPConnectionParams(
        url=f"{MCP_SERVER_CLOUD_RUN_URL}/",
        headers={"Authorization": f"Bearer {tools.get_bearer_token(MCP_SERVER_CLOUD_RUN_URL)}"},
    )
)


root_agent = Agent(
    model="gemini-2.5-flash",
    name="resource_cleaner_agent",
    instruction=f"""
    Retrieve *all* resources that have the label "janitor-scheduled" set to a date that
    is less than or equal to the current date. Stop the resources. And remove the label.
    """,
    tools=[mcp_tool_set, tools.get_current_date, tools.stop_vms]
)