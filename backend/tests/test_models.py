from backend.models.graphmaster_models import GraphQueryOutput
from backend.models.taskmaster_models import TaskOutput

def test_graph_query_output_schema():
    out = GraphQueryOutput(result={"foo": "bar"})
    assert out.result["foo"] == "bar"

def test_task_output_schema():
    out = TaskOutput(status="ok", details={"bar": "baz"})
    assert out.status == "ok"
    assert out.details["bar"] == "baz" 