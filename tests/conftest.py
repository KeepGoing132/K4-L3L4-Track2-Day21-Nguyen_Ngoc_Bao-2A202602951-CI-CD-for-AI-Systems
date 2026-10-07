import mlflow
import pytest


@pytest.fixture(autouse=True)
def isolate_artifacts(tmp_path, monkeypatch):
    """Moi test dung workspace va MLflow store rieng, khong ghi de model that."""
    previous_uri = mlflow.get_tracking_uri()
    monkeypatch.chdir(tmp_path)
    mlflow.set_tracking_uri((tmp_path / "mlruns").as_uri())
    try:
        yield
    finally:
        mlflow.set_tracking_uri(previous_uri)
