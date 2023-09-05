import argparse
import os
import random
from shape_net import SHAPE_CATEGORY

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


def get_shapes_from_cat(shape_cat):
    if shape_cat == "geometric":
        big_shapes = ["cube", "sphere", "cone", "cylinder"]
    elif shape_cat == "real-life":
        big_shapes = [x for x in SHAPE_CATEGORY if x not in ["cube", "sphere", "cone", "cylinder"]]
    elif shape_cat == "in-class":
        big_shapes = ["{:04d}".format(x) for x in range(55) if x % 5 != 0]
    else:
        big_shapes = ["{:04d}".format(x) for x in range(55) if x % 5 == 0]
    return big_shapes
