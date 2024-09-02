import ast
import csv
import os

import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    confusion_matrix,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
)

import numpy as np

from ciena_llm.config.loader import ConfigLoader

TEST_NAME = "noticias-elpais-sample-194-anotado-e2e"
SEQIA_RESULTS_SUMMARY = (
    f"/home/javier/Developer/SeqIA/seqia/results/{TEST_NAME}/summary.csv"
)
GEN_RESULTS_SUMMARY = (
    f"/home/javier/Developer/SeqIA/ciena_llm/results/{TEST_NAME}/summary.csv"
)
LABELS_DROUGHT = f"/home/javier/Developer/SeqIA/data/{TEST_NAME}/corpus/all.csv"
RESULTS_DIR = f"./results/{TEST_NAME}/"
os.makedirs(os.path.dirname(RESULTS_DIR), exist_ok=True)

IMPACTS = [impact["tag"] for impact in ConfigLoader().config["impacts"]]

with open(SEQIA_RESULTS_SUMMARY, "r", encoding="utf-8") as f:
    seqia_results = list(csv.DictReader(f))
    seqia_results.sort(key=lambda x: x["article_filename"])

with open(GEN_RESULTS_SUMMARY, "r", encoding="utf-8") as f:
    gen_results = list(csv.DictReader(f))
    gen_results.sort(key=lambda x: x["article_filename"])

with open(LABELS_DROUGHT, "r", encoding="utf-8") as f:
    labels_drought = list(csv.DictReader(f, delimiter="\t"))
    labels_drought.sort(key=lambda x: x["filename"])

################################################################################
# GET COMPARISONS FILE
################################################################################

comparisons = []
for seqia_result, gen_result, label in zip(seqia_results, gen_results, labels_drought):
    comparison = {}
    try:
        assert seqia_result["article_filename"] == gen_result["article_filename"]
        assert os.path.basename(seqia_result["article_filename"]) == label["filename"]
    except AssertionError:
        continue

    impacts_seqia = set(ast.literal_eval(seqia_result["article_impacts_aggregated"]))
    impacts_gen = set(ast.literal_eval(gen_result["article_impacts_aggregated"]))

    drought_label = "True" if label["drought"] == "1" else "False"
    impacts_label = [impact for impact in IMPACTS if label[impact] == "1"]

    comparison = {
        "drought_match": (
            seqia_result["article_drought"] == gen_result["article_drought"]
        ),
        "drought_seqia": seqia_result["article_drought"],
        "drought_gen": gen_result["article_drought"],
        "drought_label": drought_label,
        "label_match": gen_result["article_drought"] == drought_label,
        "impacts_match": (impacts_seqia == impacts_gen),
        "impacts_mismatch_number": (len(impacts_seqia ^ impacts_gen)),
        "impacts_seqia": impacts_seqia,
        "impacts_gen": impacts_gen,
        "impacts_label": impacts_label,
        "filename": seqia_result["article_filename"],
    }
    comparisons.append(comparison)


comparisons_no_drought_match = [
    comparison for comparison in comparisons if not comparison["drought_match"]
]

comparisons_no_impacts_match = [
    comparison for comparison in comparisons if not comparison["impacts_match"]
]

comparisons_filtered = [
    comparison
    for comparison in comparisons
    # if (not comparison["drought_match"])
    # or (not comparison["impacts_match"])
    # or (not comparison["label_match"])
]

with open(f"{RESULTS_DIR}/comparisons.csv", "w", encoding="utf-8") as f:
    keys = list(comparisons_filtered[0].keys())

    dict_writer = csv.DictWriter(f, keys)
    dict_writer.writeheader()
    dict_writer.writerows(comparisons_filtered)

# print(f"Conflict in drought: {len(comparisons_no_drought_match)}/{len(comparisons)}")
# print(f"Conflict in impacts: {len(comparisons_no_impacts_match)}/{len(comparisons)}")
# print(
#     f"Average mismatch impact number (between only impact mismatches): {sum([c["impacts_mismatch_number"] for c in comparisons_no_impacts_match])/len(comparisons_no_impacts_match):.3}"
# )
# print(f"Conflict any (drought/impacts): {len(comparisons_filtered)}/{len(comparisons)}")


################################################################################
# GET CONFUSION MATRICES
################################################################################


def plot_confusion_matrix(true, pred, title, true_label, pred_label, save_path):

    assert len(true) == len(pred)

    # Generate confusion matrix
    cm = confusion_matrix(true, pred)

    # Calculate metrics
    accuracy = accuracy_score(true, pred)
    precision = precision_score(true, pred)
    recall = recall_score(true, pred)
    f1 = f1_score(true, pred)

    # Create a figure with GridSpec
    fig = plt.figure(figsize=(10, 8))
    gs = fig.add_gridspec(2, 1, height_ratios=[4, 1])

    # Plot the confusion matrix heatmap
    ax0 = fig.add_subplot(gs[0])
    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=[f"{pred_label} Negative", f"{pred_label} Positive"],
        yticklabels=[f"{true_label} Negative", f"{true_label} Positive"],
        ax=ax0,
    )
    ax0.set_xlabel(f"{pred_label}")
    ax0.set_ylabel(f"{true_label}")
    ax0.set_title(title)

    # Add the metrics table below the heatmap
    ax1 = fig.add_subplot(gs[1])
    ax1.axis("off")  # Hide the axis

    # Data for the table
    table_data = [
        [f"Total", len(true)],
        [f"Accuracy", f"{accuracy:.2f}"],
        [f"Precision", f"{precision:.2f}"],
        [f"Recall", f"{recall:.2f}"],
        [f"F1 Score", f"{f1:.2f}"],
    ]

    # Create table
    table = ax1.table(
        cellText=table_data,
        colWidths=[0.2, 0.2],
        loc="center",
        cellLoc="center",
        colLabels=["Metric", "Value"],
        bbox=[0, 0, 1, 1],
    )
    table.auto_set_font_size(False)
    table.set_fontsize(12)

    # Set table styles
    for key, cell in table.get_celld().items():
        cell.set_linewidth(0.5)
        if key[0] == 0:  # Header row
            cell.set_fontsize(14)
            cell.set_text_props(weight="bold")
            cell.set_facecolor("#cccccc")

    plt.tight_layout()
    plt.savefig(save_path)


# BINARY

seqia_results_drought = {
    os.path.basename(result["article_filename"]): result["article_drought"] == "True"
    for result in seqia_results
}

gen_results_drought = {
    os.path.basename(result["article_filename"]): result["article_drought"] == "True"
    for result in gen_results
}

labels = {label["filename"]: label["drought"] == "1" for label in labels_drought}


filenames = [filename for filename in seqia_results_drought]

seqia_predictions_labels_drought = [
    seqia_results_drought[filename] for filename in filenames
]
gen_predictions_labels_drought = [
    gen_results_drought[filename] for filename in filenames
]
true_labels_drought = [labels[filename] for filename in filenames]


# True vs Seqia (Binary)
plot_confusion_matrix(
    true_labels_drought,
    seqia_predictions_labels_drought,
    title="True vs Seqia (Binary)",
    true_label="True",
    pred_label="Seqia",
    save_path=f"{RESULTS_DIR}/confusion_matrices/true_vs_seqia_binary.png",
)

# True vs Gen (Binary)
plot_confusion_matrix(
    true_labels_drought,
    gen_predictions_labels_drought,
    title="True vs Gen (Binary)",
    true_label="True",
    pred_label="Gen",
    save_path=f"{RESULTS_DIR}/confusion_matrices/true_vs_gen_binary.png",
)


# IMPACTS
for impact in IMPACTS:
    seqia_results_impacts = {
        os.path.basename(result["article_filename"]): impact
        in result["article_impacts_aggregated"]
        for result in seqia_results
    }

    gen_results_impacts = {
        os.path.basename(result["article_filename"]): impact
        in result["article_impacts_aggregated"]
        for result in gen_results
    }

    labels_impacts = {
        label["filename"]: label[impact] == "1" for label in labels_drought
    }

    filenames = [
        filename
        for filename in seqia_results_impacts
        if seqia_results_drought[filename]
        or gen_results_drought[filename]
        or labels[filename]
    ]

    seqia_predictions_labels_impacts = [
        seqia_results_impacts[filename] for filename in filenames
    ]
    gen_predictions_labels_impacts = [
        gen_results_impacts[filename] for filename in filenames
    ]
    true_labels_impacts = [labels_impacts[filename] for filename in filenames]

    # True vs Seqia (Impacts)
    plot_confusion_matrix(
        true_labels_impacts,
        seqia_predictions_labels_impacts,
        title=f"True vs Seqia (Impacts: {impact})",
        true_label="True",
        pred_label="Seqia",
        save_path=f"{RESULTS_DIR}/confusion_matrices/true_vs_seqia_impact_{impact}.png",
    )

    # True vs Gen (Impacts)
    plot_confusion_matrix(
        true_labels_impacts,
        gen_predictions_labels_impacts,
        title=f"True vs Gen (Impacts: {impact})",
        true_label="True",
        pred_label="Gen",
        save_path=f"{RESULTS_DIR}/confusion_matrices/true_vs_gen_impact_{impact}.png",
    )
