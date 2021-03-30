#!/usr/bin/env bash

cloc --by-file --force-lang-def="cloc_defs/cloc_lemma_ops_def" "../../case_study_lemma_models/" --exclude-dir=intermediate
