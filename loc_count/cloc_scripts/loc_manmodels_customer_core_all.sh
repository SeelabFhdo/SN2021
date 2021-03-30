#!/usr/bin/env bash

cloc --by-file --force-lang-def="cloc_defs/cloc_lemma_def" "../../case_study_lemma_models/customer-core/" --exclude-dir=intermediate
