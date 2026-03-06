import pandas as pd

def load_data(anonymized_path, auxiliary_path):
    """
    Load anonymized and auxiliary datasets.
    """
    anon = pd.read_csv(anonymized_path)
    aux = pd.read_csv(auxiliary_path)
    return anon, aux


def link_records(anon_df, aux_df):
    """
    Attempt to link anonymized records to auxiliary records
    using exact matching on quasi-identifiers.

    Returns a DataFrame with columns:
      anon_id, matched_name
    containing ONLY uniquely matched records.
    """
    if "zip3" not in anon_df.columns and "zip" in anon_df.columns:
        anon_df = anon_df.copy()
        anon_df["zip3"] = aux_df["zip"].astype(str).str[:3]

    quasi_ids = ["age", "gender", "zip3"]
    merged = anon_df.merge(aux_df, on=quasi_ids, how="inner")
    match_counts = merged.groupby("anon_id").size()
    unique_ids = match_counts[match_counts == 1].index
    unique_matches = merged[merged["anon_id"].isin(unique_ids)][["anon_id", "name"]].copy()
    unique_matches = unique_matches.rename(columns={"name": "matched_name"})

    return unique_matches.reset_index(drop=True)


def deanonymization_rate(matches_df, anon_df):
    """
    Compute the fraction of anonymized records
    that were uniquely re-identified.
    """
    n_matched = len(matches_df)
    n_total = len(anon_df)
    return n_matched / n_total if n_total > 0 else 0.0
