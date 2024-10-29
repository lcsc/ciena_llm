import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
import seaborn as sns


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
