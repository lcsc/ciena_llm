import random
from typing import List, Dict, Any
from datasets import load_dataset, Dataset


class NewsElPaisDataset:
    def __init__(
        self,
        dataset_name: str = "javiervela/news-elpais-binary",
        split: str = "test",
        label_field: str = "drought",
        seed: int = 42,
    ):
        self.dataset_name: str = dataset_name
        self.split: str = split
        self.label_field: str = label_field
        self.seed: int = seed
        self.dataset: Dataset = self._load_dataset()

    def _load_dataset(self) -> Dataset:
        random.seed(self.seed)
        dataset: Dataset = load_dataset(self.dataset_name, split=self.split)
        return dataset

    def get_subset(self, num_positive: int, num_negative: int) -> List[Dict[str, Any]]:
        positives: List[Dict[str, Any]] = [
            example for example in self.dataset if example[self.label_field] == 1
        ]
        negatives: List[Dict[str, Any]] = [
            example for example in self.dataset if example[self.label_field] == 0
        ]

        if len(positives) < num_positive:
            print(
                f"Warning: Requested {num_positive} positive samples, but only {len(positives)} are available."
            )
            num_positive = len(positives)

        if len(negatives) < num_negative:
            print(
                f"Warning: Requested {num_negative} negative samples, but only {len(negatives)} are available."
            )
            num_negative = len(negatives)

        positive_subset: List[Dict[str, Any]] = random.sample(positives, num_positive)
        negative_subset: List[Dict[str, Any]] = random.sample(negatives, num_negative)

        return positive_subset + negative_subset


# Example usage:
if __name__ == "__main__":
    dataset = NewsElPaisDataset()
    subset = dataset.get_subset(num_positive=20, num_negative=10)
    print(type(subset))
    print(f"Retrieved subset with {len(subset)} examples.")
