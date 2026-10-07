from pathlib import Path

import pandas as pd


def append_batch(
    train_path: str = "data/train_batch1.csv",
    batch_path: str = "data/train_batch2.csv",
) -> int:
    """Ghep batch mot lan, giu lai cac dong trung hop le trong du lieu goc."""
    df_train = pd.read_csv(train_path)
    df_new = pd.read_csv(batch_path)
    if list(df_train.columns) != list(df_new.columns):
        raise ValueError("Batch moi phai co cung cot va thu tu cot voi tap train")
    if df_new.empty:
        print("Batch moi rong, khong cap nhat du lieu.")
        return len(df_train)

    # Script luon ghep o cuoi file; doi chieu ca batch thay vi drop_duplicates,
    # vi Adult co the chua cac mau trung nhau that su.
    if len(df_train) >= len(df_new) and df_train.tail(len(df_new)).reset_index(
        drop=True
    ).equals(df_new.reset_index(drop=True)):
        print(f"Batch da duoc ghep, giu nguyen {len(df_train)} mau.")
        return len(df_train)

    df_updated = pd.concat([df_train, df_new], ignore_index=True)
    target = Path(train_path)
    temporary = target.with_suffix(target.suffix + ".tmp")
    df_updated.to_csv(temporary, index=False)
    temporary.replace(target)
    print(f"Cap nhat du lieu: {len(df_train)} -> {len(df_updated)} mau")
    return len(df_updated)


if __name__ == "__main__":
    append_batch()
