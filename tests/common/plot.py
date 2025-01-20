import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from sklearn.metrics import (
    confusion_matrix,
    accuracy_score,
    cohen_kappa_score,
    f1_score,
    precision_score,
    recall_score,
)
import seaborn as sns


def compute_confusion_matrix_and_metrics(df, class_name):
    total_instances = len(df)

    # Print the types and unique values of the true and predicted values
    true_values = df[f"{class_name}_true"].apply(lambda x: 1 if x else 0)
    predicted_values = df[f"{class_name}_predicted"].apply(lambda x: 1 if x else 0)

    cm = confusion_matrix(true_values, predicted_values, labels=[0, 1])
    accuracy = accuracy_score(true_values, predicted_values)

    # Check if confusion matrix is valid for kappa calculation
    if np.sum(cm) == 0 or np.sum(np.sum(cm, axis=0) * np.sum(cm, axis=1)) == 0:
        kappa = float("nan")
    else:
        kappa = cohen_kappa_score(true_values, predicted_values)

    precision = precision_score(true_values, predicted_values, zero_division=0)
    recall = recall_score(true_values, predicted_values, zero_division=0)
    f1 = f1_score(true_values, predicted_values, zero_division=0)

    metrics = {
        "total_instances": total_instances,
        "accuracy": round(accuracy, 3),
        "kappa": round(kappa, 3) if not np.isnan(kappa) else "nan",
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
                metrics["kappa"],
                metrics["precision"],
                metrics["recall"],
                metrics["f1"],
            ]
        ]
    )
    table_columns = ["Total", "Accuracy", "Kappa", "Precision", "Recall", "F1 Score"]

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


def print_metrics(class_name, total_instances, accuracy, precision, recall, f1, kappa):
    print(f"Metrics:")
    print(f"Class: {class_name.upper()}\n")

    print(f"Total Instances: {total_instances}")
    print(f"Accuracy: {accuracy:.3f}")
    if kappa == "nan":
        print(f"Kappa: {kappa}")
    else:
        print(f"Kappa: {kappa:.3f}")
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
