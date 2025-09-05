from pydantic_ai import RunContext
from backend.utils.neo4j import driver
from backend.models.taskmaster_models import Task, TaskOutput
from typing import List
import uuid

def create_task(ctx: RunContext, description: str, user_id: str, linked_to: str = None) -> TaskOutput:
    """
    Creates a new task node in the graph and links it to a user.
    Optionally, it can link the task to a Concept or Entity.
    """
    task_id = str(uuid.uuid4())
    with driver.session() as session:
        cypher = """
        MATCH (u:User {user_id: $user_id})
        CREATE (t:Task {
            task_id: $task_id,
            description: $description,
            completed: false
        })
        CREATE (t)-[:ASSIGNED_TO]->(u)
        """
        params = {
            "user_id": user_id,
            "task_id": task_id,
            "description": description,
        }
        # If a node to link to is provided, add that logic
        if linked_to:
            cypher += """
            WITH t
            MATCH (n) WHERE n.concept_id = $linked_to OR n.entity_id = $linked_to
            CREATE (t)-[:RELATED_TO]->(n)
            """
            params["linked_to"] = linked_to
        
        cypher += " RETURN t"
        
        result = session.run(cypher, params)
        task_node = result.single()["t"]
        task = Task(**task_node)
        return TaskOutput(status="success", message=f"Task '{description}' created.", task=task)

def get_task_by_id(ctx: RunContext, task_id: str) -> TaskOutput:
    """Retrieves a single task by its ID."""
    with driver.session() as session:
        cypher = "MATCH (t:Task {task_id: $task_id}) RETURN t"
        result = session.run(cypher, {"task_id": task_id})
        record = result.single()
        if not record:
            return TaskOutput(status="error", message="Task not found.")
        task = Task(**record["t"])
        return TaskOutput(status="success", message="Task found.", task=task)

def update_task_status(ctx: RunContext, task_id: str, completed: bool) -> TaskOutput:
    """Updates the status of a task."""
    with driver.session() as session:
        cypher = "MATCH (t:Task {task_id: $task_id}) SET t.completed = $completed RETURN t"
        result = session.run(cypher, {"task_id": task_id, "completed": completed})
        record = result.single()
        if not record:
            return TaskOutput(status="error", message="Task not found.")
        task = Task(**record["t"])
        status = "completed" if completed else "re-opened"
        return TaskOutput(status="success", message=f"Task status updated to {status}.", task=task)

def list_open_tasks(ctx: RunContext, user_id: str) -> TaskOutput:
    """Lists all non-completed tasks for a given user."""
    with driver.session() as session:
        cypher = """
        MATCH (u:User {user_id: $user_id})<-[:ASSIGNED_TO]-(t:Task)
        WHERE t.completed = false
        RETURN t
        """
        result = session.run(cypher, {"user_id": user_id})
        tasks = [Task(**record["t"]) for record in result]
        return TaskOutput(status="success", message=f"Found {len(tasks)} open tasks.", tasks=tasks) 