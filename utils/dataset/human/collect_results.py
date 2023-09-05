import argparse
import json
import os
import csv
from collections import defaultdict
from easydict import EasyDict

from result_storage import ResultStorage

def read_serialized(file_name):
    """Read json and yaml file"""
    if file_name is not None:
        with open(file_name, "r") as f:
            if file_name.endswith(".json"):
                return EasyDict(json.load(f))
            else:
                raise FileNotFoundError
    return EasyDict()


CONTENT_FOLDER = "/misc/vlgscratch4/LakeGroup/emin/ADEPT-Dataset-Release"

CASE_PAIRS = {
    "create": [("disappear", 2),
               ("disappear", 0),
               ("disappear", 3),
               ("disappear", 4)],
    "vanish": [("disappear_fixed", 1),
               ("disappear_fixed", 0),
               ("disappear_fixed", 3),
               ("disappear_fixed", 4)],
    "short-overturn": [("overturn", 0),
                       ("overturn", 1)],
    "long-overturn": [("overturn", 3),
                      ("overturn", 2)],
    "visible-discontinuous": [("discontinuous", 2),
                              ("discontinuous", 3),
                              ("discontinuous", 5),
                              ("discontinuous", 4)],
    "invisible-discontinuous": [("discontinuous", 1),
                                ("discontinuous", 0),
                                ("discontinuous", 5),
                                ("discontinuous", 4)],
    "delay": [("delay", 1),
              ("delay", 0)],
    "block": [("block", 1),
              ("block", 0)]
}

SHAPE_CATS = ["geometric", "real-life", "in-class", "out-class"]

_prefix = "| negative log likelihood: "

_human_pairs = read_serialized(os.path.join(CONTENT_FOLDER, "dataset", "human", "pairs.json"))["origin"]


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--summary_folder", type=str)
    parser.add_argument("--summary_folders", type=str, nargs="+")
    parser.add_argument("--summary_file", type=str)
    parser.add_argument("--violations", type=str)
    parser.add_argument("--shape_cats", type=str)
    parser.add_argument("--use_surprise_metric", type=int, default=True)
    parser.add_argument("--output_folder", type=str)
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    max_scores = read_serialized(args.summary_file)
    experiment = os.path.split(args.summary_file)[-1][:-5]

    with open("{}{}_absolute.csv".format(args.output_folder, experiment), "w") as f_absolute, open("{}/{}_relative.csv".format(args.output_folder, experiment), "w")as f_relative:
        
        absolute_writer = csv.DictWriter(f_absolute, fieldnames=["name", "all", *CASE_PAIRS], dialect="excel-tab")
        relative_writer = csv.DictWriter(f_relative, fieldnames=["name", "all", *CASE_PAIRS], dialect="excel-tab")

        absolute_writer.writeheader()
        relative_writer.writeheader()

        for i in range(2):
            if i == 1:
                scores = {k: v for k, v in max_scores.items() if k in _human_pairs}
                experiment = experiment + "_on-human"
            else:
                scores = max_scores
            max_storage = ResultStorage(scores, use_surprise_metric=args.use_surprise_metric)

            absolute_score = dict(all=max_storage.get_absolute_accuracy())
            for case in CASE_PAIRS:
                absolute_score[case] = max_storage.get_absolute_accuracy(violations=case)
            absolute_writer.writerow(dict(name=experiment, **absolute_score))
            for shape in SHAPE_CATS:
                absolute_score = dict(all=max_storage.get_absolute_accuracy(shape_cats=shape))
                for case in CASE_PAIRS:
                    absolute_score[case] = max_storage.get_absolute_accuracy(violations=case, shape_cats=shape)
                absolute_writer.writerow(dict(name=experiment + "_" + shape, **absolute_score))

            relative_score = dict(all=max_storage.get_relative_accuracy())
            for case in CASE_PAIRS:
                relative_score[case] = max_storage.get_relative_accuracy(violations=case)
            relative_writer.writerow(dict(name=experiment, **relative_score))
            for shape in SHAPE_CATS:
                relative_score = dict(all=max_storage.get_relative_accuracy(shape_cats=shape))
                for case in CASE_PAIRS:
                    relative_score[case] = max_storage.get_relative_accuracy(violations=case, shape_cats=shape)
                relative_writer.writerow(dict(name=experiment + "_" + shape, **relative_score))
