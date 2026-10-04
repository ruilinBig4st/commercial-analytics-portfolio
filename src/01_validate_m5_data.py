from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw" / "m5"

EXPECTED_FILES = {
    "calendar.csv": {
        "date",
        "wm_yr_wk",
        "d",
    },
    "sell_prices.csv": {
        "store_id",
        "item_id",
        "wm_yr_wk",
        "sell_price",
    },
    "sales_train_evaluation.csv": {
        "id",
        "item_id",
        "dept_id",
        "cat_id",
        "store_id",
        "state_id",
        "d_1",
    },
}


def validate_file(file_name: str, required_columns: set[str]) -> bool:
    file_path = RAW_DIR / file_name

    if not file_path.exists():
        print(f"[MISSING] {file_name}")
        return False

    size_mb = file_path.stat().st_size / (1024 ** 2)
    sample = pd.read_csv(file_path, nrows=5)

    missing_columns = required_columns - set(sample.columns)

    print(f"\n[FOUND] {file_name}")
    print(f"Size: {size_mb:.2f} MB")
    print(f"Columns: {len(sample.columns)}")
    print(f"Sample shape: {sample.shape}")

    if missing_columns:
        print(f"[FAILED] Missing columns: {sorted(missing_columns)}")
        return False

    print("[PASSED] Required columns are present")
    return True


def main() -> None:
    print(f"Checking data directory: {RAW_DIR}")

    results = [
        validate_file(file_name, required_columns)
        for file_name, required_columns in EXPECTED_FILES.items()
    ]

    if all(results):
        print("\nAll M5 raw data checks passed.")
    else:
        print("\nOne or more M5 data checks failed.")


if __name__ == "__main__":
    main()