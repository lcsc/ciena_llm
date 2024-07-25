import ast
import csv
import os

TEST_NAME = "news-elpais-binary-50T-50F"
SEQIA_RESULTS_SUMMARY = (
    f"/home/javier/Developer/SeqIA/seqia/results/{TEST_NAME}/summary.csv"
)
GEN_RESULTS_SUMMARY = f"/home/javier/Developer/SeqIA/seqia_gen/results/{TEST_NAME}/summary.csv"
RESULTS_DIR = f"./results/{TEST_NAME}/"
os.makedirs(os.path.dirname(RESULTS_DIR), exist_ok=True)

with open(SEQIA_RESULTS_SUMMARY, "r", encoding="utf-8") as f:
    seqia_results = list(csv.DictReader(f))
    seqia_results.sort(key=lambda x: x["article_filename"])

with open(GEN_RESULTS_SUMMARY, "r", encoding="utf-8") as f:
    gen_results = list(csv.DictReader(f))
    gen_results.sort(key=lambda x: x["article_filename"])

comparisons = []
for seqia_result, gen_result in zip(seqia_results, gen_results):
    comparison = {}
    assert seqia_result["article_filename"] == gen_result["article_filename"]

    impacts_seqia = set(ast.literal_eval(seqia_result["article_impacts_aggregated"]))
    impacts_gen = set(ast.literal_eval(gen_result["article_impacts_aggregated"]))

    comparison = {
        "drought_match": (
            seqia_result["article_drought"] == gen_result["article_drought"]
        ),
        "drought_seqia": seqia_result["article_drought"],
        "drought_gen": gen_result["article_drought"],
        "impacts_match": (impacts_seqia == impacts_gen),
        "impacts_mismatch_number": (len(impacts_seqia ^ impacts_gen)),
        "impacts_seqia": impacts_seqia,
        "impacts_gen": impacts_gen,
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
    if (not comparison["drought_match"]) or (not comparison["impacts_match"])
]

with open(f"{RESULTS_DIR}/comparisons.csv", "w", encoding="utf-8") as f:
    keys = list(comparisons_filtered[0].keys())

    dict_writer = csv.DictWriter(f, keys)
    dict_writer.writeheader()
    dict_writer.writerows(comparisons_filtered)

print(f"Conflict in drought: {len(comparisons_no_drought_match)}/{len(comparisons)}")
print(f"Conflict in impacts: {len(comparisons_no_impacts_match)}/{len(comparisons)}")
print(f"Average mismatch impact number (between only impact mismatches): {sum([c["impacts_mismatch_number"] for c in comparisons_no_impacts_match])/len(comparisons_no_impacts_match):.3}")
print(f"Conflict any (drought/impacts): {len(comparisons_filtered)}/{len(comparisons)}")
