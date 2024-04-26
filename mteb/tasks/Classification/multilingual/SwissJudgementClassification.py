from __future__ import annotations

from datasets import Dataset

from mteb.abstasks import AbsTaskClassification, MultilingualTask
from mteb.abstasks.TaskMetadata import TaskMetadata


class SwissJudgementClassification(MultilingualTask, AbsTaskClassification):
    metadata = TaskMetadata(
        name="SwissJudgementClassification",
        description="Multilingual, diachronic dataset of Swiss Federal Supreme Court cases annotated with the respective binarized judgment outcome (approval/dismissal)",
        reference="https://aclanthology.org/2021.nllp-1.3/",
        dataset={
            "path": "rcds/swiss_judgment_prediction",
            "revision": "29806f87bba4f23d0707d3b6d9ea5432afefbe2f",
        },
        type="Classification",
        category="s2s",
        eval_splits=["test"],
        eval_langs={
            "de": ["deu-Latn"],
            "fr": ["fra-Latn"],
            "it": ["ita-Latn"],
        },
        main_score="accuracy",
        date=("2020-12-15", "2022-04-08"),
        form=["written"],
        domains=["Legal"],
        task_subtypes=[
            "Political classification",
        ],
        license="CC-BY-4.0",
        socioeconomic_status="mixed",
        annotations_creators="expert-annotated",
        dialect=[],
        text_creation="found",
        bibtex_citation="""@misc{niklaus2022empirical,
    title={An Empirical Study on Cross-X Transfer for Legal Judgment Prediction},
    author={Joel Niklaus and Matthias Stürmer and Ilias Chalkidis},
    year={2022},
    eprint={2209.12325},
    archivePrefix={arXiv},
    primaryClass={cs.CL}
}
""",
        n_samples={"test": 17357},
        avg_character_length={"test": 3411.72},
    )
    """
    def dataset_transform(self):
        for lang in self.langs:
            self.dataset[lang]["test"] = self.dataset[lang]["test"].select(
                range(min(2048, len(self.dataset[lang]["test"])))
            )
    """

    def dataset_transform(self):
        for lang in self.langs:
            X = self.dataset[lang]["test"]["text"]
            y = self.dataset[lang]["test"]["label"]

            samples_per_label = min(2048, len(X))
            X_undersampled, y_undersampled, add_info = self._undersample_data(
                X, y, samples_per_label
            )

            self.dataset[lang]["test"] = Dataset.from_dict(
                {"text": X_undersampled, "label": y_undersampled}
            )
