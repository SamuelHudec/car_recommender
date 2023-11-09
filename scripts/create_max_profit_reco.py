import argparse
import warnings
import logging

from src.preprocess.preprocess_knn import GetTrainingDataKNN
from src.retriever.knn import RetrieverKNN
from src.ranker.simple_max_profit import SimpleMaxProfit
from src.utils.data import data_dumper

warnings.simplefilter(action='ignore', category=FutureWarning)
logging.basicConfig(level=logging.INFO)

# this is just sample how it can look like for one case one carousel

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--path_to_data",
        help="Full path or table end point",
        default="http://127.0.0.1:5000/table/car_details_v4",
    )
    parser.add_argument(
        "--output_path",
        help="Full path or table end point",
        default="http://127.0.0.1:5000/table/recommendations",
    )
    return parser.parse_args()

def main(args: argparse.Namespace) -> None:
    preprocessor = GetTrainingDataKNN(path_to_data=args.path_to_data)
    train, df_full = preprocessor.forward()

    retriever = RetrieverKNN(train_data=train)
    candidates = retriever.forward()

    ranker = SimpleMaxProfit(candidates=candidates, data=df_full)
    recommendations = ranker.forward()

    data_dumper(data=recommendations, path=args.output_path)

    print(recommendations.loc[recommendations["item_id"] == "i5581931906452788333"])

if __name__ == "__main__":
    args = parse_args()
    main(args)
