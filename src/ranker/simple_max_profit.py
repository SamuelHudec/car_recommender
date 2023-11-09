import logging

import pandas as pd
logger = logging.getLogger("re_rank_candidates")

RANKING_COLUMNS = ["item_id", "reco_id", "re_rank"]
ID_COLUMN = "item_id"

class SimpleMaxProfit():
    def __init__(self, candidates: pd.DataFrame, data: pd.DataFrame) -> None:
        self.candidates = candidates
        self.data = data
        self.FALL_BACK = False

    def _merge_stats_to_candidates(self) -> pd.DataFrame:
        df_to_rank = self.candidates.merge(self.data, left_on="reco_id", right_on=ID_COLUMN, suffixes=("", "_full"))
        df_to_rank.drop(f"{ID_COLUMN}_full", axis=1, inplace=True)

        # I did inner join check if I join everything
        if self.candidates.shape[0] != df_to_rank.shape[0]:
            self.FALL_BACK = True
            logger.error("Re-ranker, Data didn't merged. Return retriever candidates")

        return df_to_rank

    def _check_ranks(self, data: pd.DataFrame) -> None:
        # check if algo generates unique rank for each item sequence based
        all_rank_sum = sum(range(1, data["reco_rank"].max() + 2))
        rank_counts = data.groupby(ID_COLUMN)["re_rank"].sum().reset_index()
        if sum(rank_counts["re_rank"] == all_rank_sum) != self.data.shape[0]:
            self.FALL_BACK = True
            logger.error("Re-ranker failed in assigning new rankings. Return retriever candidates")

    def forward(self) -> pd.DataFrame:
        df_to_rank = self._merge_stats_to_candidates()
        # add rank to prices to distinguish between same price by rank this is safe when prices are high like here
        df_to_rank["to_rank_by"] = df_to_rank["Price"] + df_to_rank["reco_rank"]
        df_to_rank["re_rank"] = df_to_rank.groupby([ID_COLUMN])["to_rank_by"].rank(method="dense", ascending=False)
        self._check_ranks(df_to_rank)

        # fallback is better to recommend notting
        if self.FALL_BACK:
            # TODO: find a different way how to fall back
            df_to_rank["re_rank"] = df_to_rank["reco_rank"]
        logger.info(f"Fallback value {self.FALL_BACK}")
        logger.info(f"Re-ranker DONE")
        return df_to_rank[RANKING_COLUMNS]

