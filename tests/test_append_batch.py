import pandas as pd
import pytest

from append_batch import append_batch


def test_append_once_preserves_duplicate_samples(tmp_path):
    train_path = tmp_path / "train.csv"
    batch_path = tmp_path / "batch.csv"
    pd.DataFrame({"age": [20, 20], "target": [0, 0]}).to_csv(train_path, index=False)
    pd.DataFrame({"age": [20, 40], "target": [0, 1]}).to_csv(batch_path, index=False)
    assert append_batch(train_path, batch_path) == 4
    first_result = train_path.read_bytes()
    assert append_batch(train_path, batch_path) == 4
    assert train_path.read_bytes() == first_result
    assert pd.read_csv(train_path)["age"].tolist() == [20, 20, 20, 40]


def test_wrong_schema_does_not_modify_training_data(tmp_path):
    train_path = tmp_path / "train.csv"
    batch_path = tmp_path / "batch.csv"
    pd.DataFrame({"age": [20], "target": [0]}).to_csv(train_path, index=False)
    pd.DataFrame({"target": [1], "age": [40]}).to_csv(batch_path, index=False)
    original = train_path.read_bytes()
    with pytest.raises(ValueError):
        append_batch(train_path, batch_path)
    assert train_path.read_bytes() == original
