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
from datetime import datetime, timezone

import google.auth.transport.requests
import google.oauth2.id_token

from google.cloud import compute_v1

def get_current_date():
    """Returns the current date in the YYYY-MM-DD format"""
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def stop_vms(instances: list[str]):
    """Stops the given instances

    Args:
        current_date: The current date in YYYY-MM-DD format.
        instances: The list of instances to stop, the instance names have the format "project_id/zone/instance_name"
    """
    client = compute_v1.InstancesClient()
    for instance in instances:
        project_id, zone, instance_name = instance.split("/")
        client.stop(project=project_id, zone=zone, instance=instance_name)


def get_bearer_token(audience: str) -> str:
    request = google.auth.transport.requests.Request()
    token = google.oauth2.id_token.fetch_id_token(request, audience)
    return token
