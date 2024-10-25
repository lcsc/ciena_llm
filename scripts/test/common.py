import logging
import os
import tempfile

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
import seaborn as sns
import yaml

from ciena_llm import ClimateImpactExtractor


def setup_logging(logging_file: str):
    # Create a custom logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)  # Set the root logger to the lowest level

    # Create handlers
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)  # Set the stream handler to INFO level

    file_handler = logging.FileHandler(logging_file, mode="w")
    file_handler.setLevel(logging.DEBUG)  # Set the file handler to DEBUG level

    # Create formatters and add them to the handlers
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    stream_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)

    # Set specific loggers to WARNING level
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)

    # Uncomment if needed
    # set_verbose(True)
    # set_debug(True)


def compute_confusion_matrix_and_metrics(df, class_name):
    total_instances = len(df)
    cm = confusion_matrix(df[f"{class_name}_true"], df[f"{class_name}_predicted"])
    accuracy = accuracy_score(df[f"{class_name}_true"], df[f"{class_name}_predicted"])
    precision = precision_score(df[f"{class_name}_true"], df[f"{class_name}_predicted"])
    recall = recall_score(df[f"{class_name}_true"], df[f"{class_name}_predicted"])
    f1 = f1_score(df[f"{class_name}_true"], df[f"{class_name}_predicted"])

    metrics = {
        "total_instances": total_instances,
        "accuracy": round(accuracy, 3),
        "precision": round(precision, 3),
        "recall": round(recall, 3),
        "f1": round(f1, 3),
    }

    return cm, metrics


def plot_confusion_matrix(class_name, cm, metrics, plot_dir):

    # Create subplots
    _, ax = plt.subplots(figsize=(10, 8))

    # Plot confusion matrix with logarithmic color scale
    sns.heatmap(cm, annot=True, fmt="d", ax=ax, cmap="Blues", norm=LogNorm())
    ax.set_title(class_name)
    ax.set_xlabel("Predicted Label")
    ax.set_ylabel("True Label")

    # Create table
    table_data = np.array(
        [
            [
                metrics["total_instances"],
                metrics["accuracy"],
                metrics["precision"],
                metrics["recall"],
                metrics["f1"],
            ]
        ]
    )
    table_columns = ["Total", "Accuracy", "Precision", "Recall", "F1 Score"]

    table = ax.table(
        cellText=table_data,
        colLabels=table_columns,
        loc="bottom",
        bbox=[0, -0.5, 1, 0.2],
    )
    table.scale(1, 1.5)

    plt.subplots_adjust(bottom=0.6)

    # Save the figure
    plt.savefig(f"{plot_dir}/{class_name}_confusion_matrix.png", bbox_inches="tight")
    plt.close()


def print_metrics(class_name, total_instances, accuracy, precision, recall, f1):
    print(f"Metrics:")
    print(f"Class: {class_name.upper()}\n")

    print(f"Total Instances: {total_instances}")
    print(f"Accuracy: {accuracy:.3f}")
    print(f"Precision: {precision:.3f}")
    print(f"Recall: {recall:.3f}")
    print(f"F1 Score: {f1:.3f}")
    print("\n")


def print_confusion_matrix(class_name, cm):
    print(f"Confusion Matrix:")
    print(f"Class: {class_name.upper()}\n")

    header = "\t".join([f"Pred {i}" for i in range(len(cm))])
    print(f"True\\Pred\t{header}")

    for i, row in enumerate(cm):
        row_str = "\t".join(map(str, row))
        print(f"True {i}\t\t{row_str}")

    print("\n")


class ClimateImpactExtractorTest:
    def __init__(self, test_name, dataset_dir, dataset_path, override_config=None):
        self.test_name = test_name
        self.dataset_dir = dataset_dir
        self.dataset_path = dataset_path
        self.override_config = override_config
        self.results_dir = f"./results/{self.test_name}/"
        os.makedirs(os.path.dirname(self.results_dir), exist_ok=True)
        setup_logging(f"{self.results_dir}/execution.log")

    def run(self):
        if self.override_config:
            with tempfile.NamedTemporaryFile(
                suffix=".yaml", delete=False
            ) as temp_config_file:
                override_config_path = temp_config_file.name
                yaml_str = yaml.dump(
                    self.override_config, default_flow_style=False, allow_unicode=True
                )
                temp_config_file.write(yaml_str.encode("utf-8"))
        else:
            override_config_path = None

        extractor = ClimateImpactExtractor(override_config_path)
        articles = extractor(dataset_path=self.dataset_path)
        extractor.write_summary_to_csv(articles, f"{self.results_dir}/summary.csv")
        extractor.write_location_to_csv(articles, f"{self.results_dir}/locations.csv")
        extractor.write_config(f"{self.results_dir}/config.yaml")
        extractor.write_prompts_to_json(f"{self.results_dir}/prompts.json")


IMPACT_EVALUATION_TYPE = "impact"
# LOCATION_EVALUATION_TYPE = "location"
EVALUATION_TYPES = [IMPACT_EVALUATION_TYPE]  # , LOCATION_EVALUATION_TYPE]


class ClimateImpactExtractorEvaluation:
    def __init__(self, test_name, annotations_path, evaluation_type):
        self.test_name = test_name
        self.annotations_path = annotations_path
        self.results_dir = f"./results/{self.test_name}/"
        if not os.path.exists(self.results_dir):
            raise Exception(
                f"Results directory {self.results_dir} does not exist. Run the test first."
            )
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

        # Get a evaluation dataframe with the entries from the anntations (the truth) and the results articles (the predictions). Link the true and predictions by the URL.
        df_evaluation = pd.merge(
            df_annotations,
            df_results,
            left_on="url",
            right_on="article_url",
            how="inner",
        )

        # From the evaluation df, get drought and each impact's true and predicted labels
        df_evaluation["drought_true"] = df_evaluation["drought_label"]
        df_evaluation["drought_predicted"] = df_evaluation["article_drought"]

        for impact in self.impact_names:
            df_evaluation[f"{impact}_true"] = df_evaluation[f"{impact}_label"]
            df_evaluation[f"{impact}_predicted"] = df_evaluation[
                "article_impacts_aggregated"
            ].apply(lambda x: impact in x)

        # Plot confusion matrix and calculate metrics for drought label
        cm, metrics = compute_confusion_matrix_and_metrics(df_evaluation, "drought")
        print_confusion_matrix("drought", cm)
        print_metrics("drought", **metrics)
        plot_confusion_matrix("drought", cm, metrics, self.plot_dir)
        print("-" * 50)

        # Plot confusion matrix and calculate metrics for each impact
        for impact in self.impact_names:
            cm, metrics = compute_confusion_matrix_and_metrics(df_evaluation, impact)
            print_confusion_matrix(impact, cm)
            print_metrics(impact, **metrics)
            plot_confusion_matrix(impact, cm, metrics, self.plot_dir)
            print("-" * 50)
