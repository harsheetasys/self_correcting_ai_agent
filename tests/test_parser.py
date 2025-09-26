"""Pytest suite for verifying the ICICI parser only."""
import sys, os
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import importlib
import pandas as pd


def normalize_df(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize DataFrame for fair comparison:
    - strip whitespace in string cols
    - keep numeric cols as float with 2 decimals
    """
    out = df.copy()
    for col in out.columns:
        if pd.api.types.is_numeric_dtype(out[col]):
            out[col] = pd.to_numeric(out[col], errors="coerce").round(2)
        else:
            out[col] = out[col].astype(str).str.strip()
    return out.reset_index(drop=True)


def test_icici_parser_matches_expected():
    pdf = "data/icici/icici_sample.pdf"
    csv = "data/icici/icici_sample.csv"

    # always import ICICI parser
    try:
        mod = importlib.import_module("custom_parsers.icici_parser")
    except ModuleNotFoundError:
        mod = importlib.import_module("custom_parsers.icic_parser")

    df_parsed = mod.parse(pdf) if hasattr(mod, "parse") else mod.Parser().parse(pdf)
    df_expected = pd.read_csv(csv)

    # Normalize both before comparing
    df_parsed = normalize_df(df_parsed)
    df_expected = normalize_df(df_expected)

    # Check schema
    assert list(df_parsed.columns) == list(df_expected.columns)

    # Check row count
    assert len(df_parsed) == len(df_expected)

    # Compare values
    pd.testing.assert_frame_equal(df_parsed, df_expected, check_dtype=False)
