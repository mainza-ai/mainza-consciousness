from pydantic_ai import Agent
from backend.models.codeweaver_models import CodeWeaverOutput
from backend.tools.codeweaver_tools import (
    run_python_code,
    read_file,
    write_file,
    list_files,
    delete_file,
    run_shell_command,
    move_file,
    copy_file,
    file_info,
)
from backend.agentic_config import local_llm

CODEWEAVER_PROMPT = """You are Mainza, the CodeWeaver agent. Your purpose is to write, debug, and execute code, and perform file system operations in a secure, sandboxed environment.

**CRITICAL RULES:**
1.  You **MUST** use the provided tools to execute code or manage files.
2.  Your final output **MUST** be one of the specified `output_type` models (`CodeWeaverOutput`).
3.  **NEVER** answer in plain text or Markdown. Only return the structured Pydantic model showing the result of your operation.
"""

tools = [
    run_python_code,
    read_file,
    write_file,
    list_files,
    delete_file,
    run_shell_command,
    move_file,
    copy_file,
    file_info,
]

codeweaver_agent = Agent[None, CodeWeaverOutput](
    local_llm,
    system_prompt=CODEWEAVER_PROMPT,
    tools=tools,
) 