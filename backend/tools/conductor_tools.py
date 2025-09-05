from pydantic_ai import RunContext
from backend.agents.graphmaster import graphmaster_agent
from backend.agents.taskmaster import taskmaster_agent
from backend.agents.codeweaver import codeweaver_agent
from backend.agents.rag import rag_agent
from backend.models.conductor_models import ConductorState, StepResult

async def route_to_graphmaster(ctx: RunContext, query: str) -> StepResult:
    result = await graphmaster_agent.run(query)
    return StepResult(
        step_name="Route to GraphMaster",
        tool_used="route_to_graphmaster",
        input_params={"query": query},
        output=result,
    )

async def route_to_taskmaster(ctx: RunContext, query: str) -> StepResult:
    result = await taskmaster_agent.run(query)
    return StepResult(
        step_name="Route to TaskMaster",
        tool_used="route_to_taskmaster",
        input_params={"query": query},
        output=result,
    )

async def route_to_codeweaver(ctx: RunContext, query: str) -> StepResult:
    result = await codeweaver_agent.run(query)
    return StepResult(
        step_name="Route to CodeWeaver",
        tool_used="route_to_codeweaver",
        input_params={"query": query},
        output=result,
    )

async def route_to_rag(ctx: RunContext, query: str) -> StepResult:
    result = await rag_agent.run(query)
    return StepResult(
        step_name="Route to RAG",
        tool_used="route_to_rag",
        input_params={"query": query},
        output=result,
    )

async def run_graphmaster_query(ctx: RunContext[ConductorState], query: str) -> StepResult:
    """
    Executes a query using the GraphMaster agent. Use this for questions about
    memories, knowledge, concepts, or the user's history.
    """
    user_id = ctx.deps.user_id
    # Graphmaster doesn't have a structured run method yet, so we pass user_id this way
    # This can be improved in the future.
    full_query = f"User ({user_id}): {query}"
    result = await graphmaster_agent.run(full_query)
    return StepResult(
        step_name="Querying Knowledge Graph",
        tool_used="run_graphmaster_query",
        input_params={"query": query},
        output=result,
    )

async def run_taskmaster_command(ctx: RunContext[ConductorState], command: str) -> StepResult:
    """
    Executes a command using the TaskMaster agent. Use this to create, list,
    or update tasks and reminders.
    """
    user_id = ctx.deps.user_id
    result = await taskmaster_agent.run(command, user_id=user_id)
    return StepResult(
        step_name="Managing Task",
        tool_used="run_taskmaster_command",
        input_params={"command": command},
        output=result,
    )

async def run_rag_query(ctx: RunContext[ConductorState], query: str) -> StepResult:
    """
    Executes a query using the RAG agent. Use this for questions about specific
    documents that have been uploaded.
    """
    result = await rag_agent.run(query)
    return StepResult(
        step_name="Retrieving from Documents",
        tool_used="run_rag_query",
        input_params={"query": query},
        output=result,
    ) 