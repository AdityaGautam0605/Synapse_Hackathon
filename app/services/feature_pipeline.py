import numpy as np
import pandas as pd


# ---------------------------
# Helper Feature Functions
# ---------------------------

def compute_acwr(load: np.ndarray, acute_days=7, chronic_days=28):
    acute = pd.Series(load).rolling(acute_days, min_periods=1).mean()
    chronic = pd.Series(load).rolling(chronic_days, min_periods=1).mean()
    with np.errstate(divide="ignore", invalid="ignore"):
        acwr = acute / chronic
    return acwr.fillna(0).values


def compute_monotony(load: np.ndarray, window_days=7):
    mean = pd.Series(load).rolling(window_days, min_periods=1).mean()
    std = pd.Series(load).rolling(window_days, min_periods=1).std()
    with np.errstate(divide="ignore", invalid="ignore"):
        monotony = mean / std
    return monotony.fillna(0).values


def compute_fatigue_proxy(load: np.ndarray, decay=0.1):
    fatigue = np.zeros_like(load)
    for i in range(1, len(load)):
        fatigue[i] = fatigue[i-1] * (1 - decay) + load[i]
    return fatigue


# ---------------------------
# Main Feature Builder
# ---------------------------

def build_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # ---- Detect Load Column ----
    load_candidates = [
        c for c in df.columns
        if "load" in c.lower()
        or "intensity" in c.lower()
        or "rpe" in c.lower()
    ]

    if not load_candidates:
        raise ValueError("No workload column found in dataset.")

    load_col = load_candidates[0]

    load = df[load_col].fillna(df[load_col].median()).values

    # ---- ACWR ----
    df["acwr"] = compute_acwr(load)

    # ---- Monotony ----
    df["monotony_index"] = compute_monotony(load)

    # ---- Fatigue Proxy ----
    df["fatigue_proxy"] = compute_fatigue_proxy(load)

    # ---- Rolling Means ----
    for w in [3, 7, 14]:
        df[f"load_roll_mean_{w}d"] = (
            pd.Series(load).rolling(w, min_periods=1).mean().values
        )

    # ---- Keep Only Numeric Columns ----
    numeric_cols = df.select_dtypes(
        include=[np.float64, np.float32, np.int64, np.int32]
    ).columns

    df = df[numeric_cols].fillna(0)

    return df