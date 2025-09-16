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

from datetime import datetime, timedelta, timezone

from google.adk import Agent
from google.cloud import compute_v1


def get_current_date():
    """Returns the current date in the YYYY-MM-DD format"""
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def can_be_stopped(vm_status: str, scheduled_date: str, current_date: datetime) -> bool:
    return vm_status == "RUNNING" and datetime.strptime(scheduled_date, "%Y-%m-%d") <= current_date


def stop_vms(current_date: str, instances: list[str]):
    """Stops the given instances

    Args:
        current_date: The current date in YYYY-MM-DD format.
        instances: The list of instances to stop, the instance names have the format "project_id/zone/instance_name"
    """
    current_date_obj = datetime.strptime(current_date, "%Y-%m-%d")
    client = compute_v1.InstancesClient()
    for instance in instances:
        print(f"Stopping instance: {instance} for {current_date}")
        project_id, zone, instance_name = instance.split("/")
        vm = client.get(project=project_id, zone=zone, instance=instance_name)
        if can_be_stopped(vm.status, vm.labels.get("janitor-scheduled", "9999-12-31"), current_date_obj):
            client.stop(project=project_id, zone=zone, instance=instance_name)
            vm.labels.pop("janitor-scheduled", None)
            client.set_labels(
                project=project_id,
                zone=zone,
                instance=instance_name,
                instances_set_labels_request_resource=compute_v1.InstancesSetLabelsRequest(
                    labels=vm.labels,
                    label_fingerprint=vm.label_fingerprint
                )
            )


root_agent = Agent(
    model="gemini-2.5-flash",
    name="cleanup_agent",
    instruction=f"""
      You are responsible for stopping VMs that are idle and have the label 'janitor-scheduled' set
      to a date that is either today or in the past.
    """,
    tools=[get_current_date, stop_vms]
)