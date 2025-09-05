from pydantic_ai import Agent
from backend.models.taskmaster_models import Task, TaskList
from backend.tools.taskmaster_tools import create_task, get_task_by_id, update_task_status, list_open_tasks
from backend.agentic_config import local_llm
from typing import Union

TASKMASTER_PROMPT = """You are Mainza, the TaskMaster agent. Your sole purpose is to manage tasks for the user. Interpret the user's natural language command and use the provided tools to perform the correct action.

**CRITICAL RULES:**
1.  You **MUST** use the provided tools to interact with the task system: `create_task`, `get_task_by_id`, `update_task_status`, `list_open_tasks`.
2.  Your final output **MUST** be one of the specified `output_type` models.
3.  **NEVER** answer in plain text or Markdown. Only return the structured Pydantic model representing the result of the tool call.

**Tool Guidelines:**
- For "create a task", "remind me to", "add a to-do" -> use `create_task`.
- For "what are my tasks", "show my to-do list" -> use `list_open_tasks`.
- For "mark task as done", "complete the task" -> use `update_task_status`.
- For specific task queries, use `get_task_by_id` if an ID is provided.
"""

tools = [
    create_task,
    get_task_by_id,
    update_task_status,
    list_open_tasks,
]

taskmaster_agent = Agent(
    local_llm,
    system_prompt=TASKMASTER_PROMPT,
    tools=[create_task, get_task_by_id, update_task_status, list_open_tasks],
) 