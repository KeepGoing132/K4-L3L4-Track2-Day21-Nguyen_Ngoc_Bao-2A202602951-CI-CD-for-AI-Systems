import importlib

import numpy as np
import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def api(tmp_path, monkeypatch):
    monkeypatch.delenv("ARTIFACT_BUCKET", raising=False)
    monkeypatch.setenv("MODEL_PATH", str(tmp_path / "missing.joblib"))
    module = importlib.import_module("src.serve")
    monkeypatch.setattr(module, "model", None)
    return module, TestClient(module.app)


def test_missing_model_is_not_healthy(api):
    _, client = api
    assert client.get("/healthz").status_code == 503
    assert client.post("/score", json={"features": [0] * 10}).status_code == 503


def test_invalid_feature_count(api):
    _, client = api
    assert client.post("/score", json={"features": [0] * 9}).status_code == 400


@pytest.mark.parametrize("prediction,label", [(0, "thu_nhap_thap"), (1, "thu_nhap_cao")])
def test_loaded_model_health_and_prediction(api, monkeypatch, prediction, label):
    module, client = api

    class Model:
        def predict(self, features):
            assert list(features.columns) == module.FEATURE_NAMES
            assert features.iloc[0].tolist() == [28, 2, 14, 2, 11, 0, 1, 0, 0, 45]
            return np.array([prediction])

    monkeypatch.setattr(module, "model", Model())
    assert client.get("/healthz").json() == {"status": "ok"}
    response = client.post("/score", json={"features": [28, 2, 14, 2, 11, 0, 1, 0, 0, 45]})
    assert response.status_code == 200
    assert response.json() == {"prediction": prediction, "label": label}
