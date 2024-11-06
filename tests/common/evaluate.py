import os

import yaml
import pandas as pd
import glob
from datetime import datetime

from .plot import (
    compute_confusion_matrix_and_metrics,
    print_confusion_matrix,
    print_metrics,
    plot_confusion_matrix,
)

IMPACT_EVALUATION_TYPE = "impact"
DROUGHT_EVALUATION_TYPE = "drought"
EVALUATION_TYPES = [IMPACT_EVALUATION_TYPE, DROUGHT_EVALUATION_TYPE]


class ClimateImpactExtractorEvaluation:
    def __init__(self, test_name, annotations_path, evaluation_type, result_dir=None):
        self.test_name = test_name
        self.annotations_path = annotations_path
        if result_dir:
            self.results_dir = result_dir
        else:
            result_dirs = glob.glob(f"./results/{self.test_name}/[0-9]*_[0-9]*")
            result_dirs.sort(
                key=lambda x: datetime.strptime(x.split("/")[-1], "%Y-%m-%d_%H-%M-%S"),
                reverse=True,
            )
            if result_dirs:
                self.results_dir = result_dirs[0]
            else:
                raise Exception(
                    f"No results directory found for test {self.test_name}."
                )
        if not os.path.exists(self.results_dir):
            raise Exception(
                f"Results directory {self.results_dir} does not exist. Run the test first."
            )
        print("Using results directory:", self.results_dir)
        self.plot_dir = f"{self.results_dir}/plots"
        os.makedirs(self.plot_dir, exist_ok=True)
        with open(
            f"{self.results_dir}/config.yaml", "r", encoding="utf-8"
        ) as config_file:
            config = yaml.safe_load(config_file)
            self.impacts = config.get("impacts")
            self.impact_names = [impact["tag"] for impact in self.impacts]
        self.evaluation_type = evaluation_type

    def run(self):
        if self.evaluation_type == IMPACT_EVALUATION_TYPE:
            self.evaluate_impact()
        elif self.evaluation_type == DROUGHT_EVALUATION_TYPE:
            self.evaluate_drought()
        else:
            raise Exception(
                f"Invalid evaluation type {self.evaluation_type}. Must be one of {EVALUATION_TYPES}"
            )

    def evaluate_impact(self):
        # Load the impact results as pandas dataframe
        impact_results_path = f"{self.results_dir}/summary.csv"
        df_results = pd.read_csv(impact_results_path)
        # Load the annotations
        df_annotations = pd.read_csv(self.annotations_path)
        # Evaluate the impact results

        df_results["article_filepath"] = df_results["article_filename"]
        df_results["article_filename"] = df_results["article_filepath"].apply(
            lambda x: x.split("/")[-1]
        )

        # Get a evaluation dataframe with the entries from the annotations (the truth) and the results articles (the predictions). Link the true and predictions by the URL.
        df_evaluation = pd.merge(
            df_annotations,
            df_results,
            left_on="url",
            right_on="article_url",
            how="inner",
        )

        # Evaluate each impact
        for impact in self.impact_names:
            self.evaluate_single_impact(df_evaluation, impact)

    def evaluate_drought(self):
        # Load the impact results as pandas dataframe
        impact_results_path = f"{self.results_dir}/summary.csv"
        df_results = pd.read_csv(impact_results_path)
        # Load the annotations
        df_annotations = pd.read_csv(self.annotations_path)
        # Evaluate the impact results

        df_results["article_filepath"] = df_results["article_filename"]
        df_results["article_filename"] = df_results["article_filepath"].apply(
            lambda x: x.split("/")[-1]
        )

        # Get a evaluation dataframe with the entries from the annotations (the truth) and the results articles (the predictions). Link the true and predictions by the URL.
        df_evaluation = pd.merge(
            df_annotations,
            df_results,
            left_on="url",
            right_on="article_url",
            how="inner",
        )

        # From the evaluation df, get drought's true and predicted labels
        df_evaluation["drought_true"] = df_evaluation["drought_label"]
        df_evaluation["drought_predicted"] = df_evaluation["article_drought"]

        # Plot confusion matrix and calculate metrics for drought label
        cm, metrics = compute_confusion_matrix_and_metrics(df_evaluation, "drought")
        print_confusion_matrix("drought", cm)
        print_metrics("drought", **metrics)
        plot_confusion_matrix("drought", cm, metrics, self.plot_dir)
        print("-" * 50)

    def evaluate_single_impact(self, df_evaluation, impact):
        # From the evaluation df, get each impact's true and predicted labels
        df_evaluation[f"{impact}_true"] = df_evaluation[f"{impact}_label"]
        df_evaluation[f"{impact}_predicted"] = df_evaluation[
            "article_impacts_aggregated"
        ].apply(lambda x: impact in x)

        # Plot confusion matrix and calculate metrics for each impact
        cm, metrics = compute_confusion_matrix_and_metrics(df_evaluation, impact)
        print_confusion_matrix(impact, cm)
        print_metrics(impact, **metrics)
        plot_confusion_matrix(impact, cm, metrics, self.plot_dir)
        print("-" * 50)
