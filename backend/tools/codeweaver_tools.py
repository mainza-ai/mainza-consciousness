from backend.utils.neo4j import driver
from backend.models.codeweaver_models import *
from pydantic_ai import RunContext
import subprocess
import shutil
import os as pyos

def run_python_code(ctx: RunContext, code: str) -> CodeWeaverOutput:
    try:
        exec_globals = {}
        exec(code, exec_globals)
        return CodeWeaverOutput(result={"output": exec_globals})
    except Exception as e:
        return CodeWeaverOutput(result={"error": str(e)})

def read_file(ctx: RunContext, file_path: str) -> CodeWeaverOutput:
    try:
        with open(file_path, "r") as f:
            content = f.read()
        return CodeWeaverOutput(result={"content": content})
    except Exception as e:
        return CodeWeaverOutput(result={"error": str(e)})

def write_file(ctx: RunContext, file_path: str, content: str) -> CodeWeaverOutput:
    try:
        with open(file_path, "w") as f:
            f.write(content)
        return CodeWeaverOutput(result={"status": "written", "file_path": file_path})
    except Exception as e:
        return CodeWeaverOutput(result={"error": str(e)})

def list_files(ctx: RunContext, directory: str = ".") -> CodeWeaverOutput:
    try:
        files = pyos.listdir(directory)
        return CodeWeaverOutput(result={"files": files})
    except Exception as e:
        return CodeWeaverOutput(result={"error": str(e)})

def delete_file(ctx: RunContext, file_path: str) -> CodeWeaverOutput:
    try:
        pyos.remove(file_path)
        return CodeWeaverOutput(result={"status": "deleted", "file_path": file_path})
    except Exception as e:
        return CodeWeaverOutput(result={"error": str(e)})

def run_shell_command(ctx: RunContext, command: str) -> CodeWeaverOutput:
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return CodeWeaverOutput(result={"stdout": result.stdout, "stderr": result.stderr, "returncode": result.returncode})
    except Exception as e:
        return CodeWeaverOutput(result={"error": str(e)})

def move_file(ctx: RunContext, src: str, dst: str) -> CodeWeaverOutput:
    try:
        shutil.move(src, dst)
        return CodeWeaverOutput(result={"status": "moved", "src": src, "dst": dst})
    except Exception as e:
        return CodeWeaverOutput(result={"error": str(e)})

def copy_file(ctx: RunContext, src: str, dst: str) -> CodeWeaverOutput:
    try:
        shutil.copy(src, dst)
        return CodeWeaverOutput(result={"status": "copied", "src": src, "dst": dst})
    except Exception as e:
        return CodeWeaverOutput(result={"error": str(e)})

def file_info(ctx: RunContext, file_path: str) -> CodeWeaverOutput:
    try:
        stat = pyos.stat(file_path)
        return CodeWeaverOutput(result={"stat": stat})
    except Exception as e:
        return CodeWeaverOutput(result={"error": str(e)}) 