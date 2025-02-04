# coding: utf-8
from __future__ import unicode_literals

import os
import pytest
# from spacy.tokens import Doc
from spacy.gold import GoldCorpus
from spacy import util

# from ...util import apply_transition_sequence

TEST_FILES_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'test_files',
    )


@pytest.mark.xfail
@pytest.mark.parametrize(
    "test_file",
    [("de_pud-ud-test.stts.json"),]
)
def test_de_parser_depset(NLP, test_file):
    """Check that no tags outside the tagset are used."""
    gold_deps = set(["ROOT", "ac", "adc", "ag", "ams", "app", "avc", "cc", "cd", "cj", "cm", "cp", "cvc", "da", "dm", "ep", "ju", "mnr", "mo", "ng", "nk", "nmc", "oa", "oc", "og", "op", "par", "pd", "pg", "ph", "pm", "pnc", "punct", "rc", "re", "rs", "sb", "sbp", "sp", "svp", "uc", "vo"])

    data_path = os.path.join(TEST_FILES_DIR, test_file)
    data_path = util.ensure_path(data_path)
    if not data_path.exists():
        raise FileNotFoundError("Test corpus not found", data_path)
    corpus = GoldCorpus(data_path, data_path)
    dev_docs = list(corpus.dev_docs(NLP, gold_preproc=False))

    pred_deps = set()
    parser = NLP.get_pipe('parser')

    for doc, _ in dev_docs:
        parser(doc)
        pred_deps = pred_deps.union(set([t.dep_ for t in doc]))

    assert len(pred_deps - gold_deps) == 0
