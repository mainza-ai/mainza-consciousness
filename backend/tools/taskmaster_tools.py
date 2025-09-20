from pydantic_ai import RunContext
from backend.utils.neo4j_unified import neo4j_unified
from backend.models.taskmaster_models import Task, TaskOutput
from typing import List
import uuid
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def create_task(ctx: RunContext, description: str, user_id: str, linked_to: str = None) -> TaskOutput:
    """
    Creates a new task node in the graph and links it to a user.
    Optionally, it can link the task to a Concept or Entity.
    """
    task_id = str(uuid.uuid4())
    start_time = datetime.now()
    
    try:
        cypher = """
        MATCH (u:User {user_id: $user_id})
        CREATE (t:Task {
            task_id: $task_id,
            description: $description,
            completed: false,
            created_at: datetime(),
            status: 'pending',
            priority: 'medium'
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
        
        result = neo4j_unified.execute_write_query(cypher, params)
        task_node = result[0]["t"] if result else None
        
        if task_node:
            task = Task(**task_node)
            execution_time = (datetime.now() - start_time).total_seconds()
            logger.debug(f"TaskMaster create_task executed in {execution_time:.3f}s")
            return TaskOutput(status="success", message=f"Task '{description}' created.", task=task)
        else:
            return TaskOutput(status="error", message="Failed to create task - no result returned.")
            
    except Exception as e:
        execution_time = (datetime.now() - start_time).total_seconds()
        logger.error(f"TaskMaster create_task failed after {execution_time:.3f}s: {e}")
        return TaskOutput(status="error", message=f"Failed to create task: {str(e)}")

def get_task_by_id(ctx: RunContext, task_id: str) -> TaskOutput:
    """Retrieves a single task by its ID."""
    start_time = datetime.now()
    
    try:
        cypher = "MATCH (t:Task {task_id: $task_id}) RETURN t"
        result = neo4j_unified.execute_query(cypher, {"task_id": task_id}, use_cache=True)
        
        if result:
            task = Task(**result[0]["t"])
            execution_time = (datetime.now() - start_time).total_seconds()
            logger.debug(f"TaskMaster get_task_by_id executed in {execution_time:.3f}s")
            return TaskOutput(status="success", message="Task found.", task=task)
        else:
            return TaskOutput(status="error", message="Task not found.")
            
    except Exception as e:
        execution_time = (datetime.now() - start_time).total_seconds()
        logger.error(f"TaskMaster get_task_by_id failed after {execution_time:.3f}s: {e}")
        return TaskOutput(status="error", message=f"Failed to retrieve task: {str(e)}")

def update_task_status(ctx: RunContext, task_id: str, completed: bool) -> TaskOutput:
    """Updates the status of a task."""
    start_time = datetime.now()
    
    try:
        cypher = "MATCH (t:Task {task_id: $task_id}) SET t.completed = $completed, t.updated_at = datetime() RETURN t"
        result = neo4j_unified.execute_write_query(cypher, {"task_id": task_id, "completed": completed})
        
        if result:
            task = Task(**result[0]["t"])
            execution_time = (datetime.now() - start_time).total_seconds()
            logger.debug(f"TaskMaster update_task_status executed in {execution_time:.3f}s")
            status = "completed" if completed else "re-opened"
            return TaskOutput(status="success", message=f"Task status updated to {status}.", task=task)
        else:
            return TaskOutput(status="error", message="Task not found.")
            
    except Exception as e:
        execution_time = (datetime.now() - start_time).total_seconds()
        logger.error(f"TaskMaster update_task_status failed after {execution_time:.3f}s: {e}")
        return TaskOutput(status="error", message=f"Failed to update task: {str(e)}")

def list_open_tasks(ctx: RunContext, user_id: str) -> TaskOutput:
    """Lists all non-completed tasks for a given user."""
    start_time = datetime.now()
    
    try:
        cypher = """
        MATCH (u:User {user_id: $user_id})<-[:ASSIGNED_TO]-(t:Task)
        WHERE t.completed = false
        RETURN t
        ORDER BY t.created_at DESC
        """
        result = neo4j_unified.execute_query(cypher, {"user_id": user_id}, use_cache=True)
        tasks = [Task(**record["t"]) for record in result]
        
        execution_time = (datetime.now() - start_time).total_seconds()
        logger.debug(f"TaskMaster list_open_tasks executed in {execution_time:.3f}s")
        return TaskOutput(status="success", message=f"Found {len(tasks)} open tasks.", tasks=tasks)
        
    except Exception as e:
        execution_time = (datetime.now() - start_time).total_seconds()
        logger.error(f"TaskMaster list_open_tasks failed after {execution_time:.3f}s: {e}")
        return TaskOutput(status="error", message=f"Failed to list tasks: {str(e)}") 