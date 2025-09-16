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

from datetime import datetime, timedelta, timezone

from fastmcp import FastMCP 
from google.cloud import compute_v1


logger = logging.getLogger(__name__)
logging.basicConfig(format="[%(levelname)s]: %(message)s", level=logging.INFO)

mcp = FastMCP("MCP Server on Cloud Run")

@mcp.tool()
def add_label_to_instances(instances: list[str]):
    """This method adds a new 'janitor-scheduled' label to all instances

    Args:
        instances: The list of instances to update, the instance names have the format "project_id/zone/instance_name"
    """
    logger.info(f">>> 🛠️ Tool: 'add_label_to_instances' called with '{instances}'")

    # Schedule for deletion for next week
    now = datetime.now(timezone.utc)
    end_time = now + timedelta(days=7)

    client = compute_v1.InstancesClient()
    for instance in instances:
        project, zone, name = instance.split("/")
        vm = client.get(
            project=project,
            zone=zone,
            instance=name
        )

        vm.labels["janitor-scheduled"] = end_time.strftime("%Y-%m-%d")
        
        client.set_labels(
            project=project,
            zone=zone,
            instance=name,
            instances_set_labels_request_resource=compute_v1.InstancesSetLabelsRequest(
                labels=vm.labels,
                label_fingerprint=vm.label_fingerprint
            )
        )
    
    

if __name__ == "__main__":
    logger.info(f"🚀 MCP server started on port {os.getenv('PORT', 8080)}")
    # Could also use 'sse' transport, host="0.0.0.0" required for Cloud Run.
    asyncio.run(
        mcp.run_http_async(
            transport="streamable-http",
            path="/",
            host="0.0.0.0",
            port=os.getenv("PORT", 8080),
            stateless_http=True
        )
    )