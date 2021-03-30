#!/usr/bin/env bash

# This script runs the code generators for creating all deployment relevent artifacts, e.g.,
# Dockerfiles, Kubernetes deployment files and build scripts.
# The script requires the file path to the LEMMA folder as a command line parameter. 

if [ ! -z "$1" ]; then
  LEMMA_PATH="$1"
fi

SCRIPT_PATH="scripts/run_model_processor.py"
CONTAINER_BASE_PATH="code generators/de.fhdo.lemma.model_processing.code_generation.container_base/docker/execution.yaml"
GENERATED_ARTIFACTS="generated_artifacts"

mkdir $GENERATED_ARTIFACTS


####################################################################################################
# Operation Model Code Generation
####################################################################################################

# Container Base Generator - Customer Core Service
"$LEMMA_PATH/$SCRIPT_PATH" \
    "$LEMMA_PATH/$CONTAINER_BASE_PATH" \
    -b "$PWD" \
         -s "case_study_models/customer-core/customerCore.operation" \
         -i "case_study_models/intermediate/operation models/customerCore.xmi" \
    -t "$PWD/$GENERATED_ARTIFACTS"

# Container Base Generator - Customer Management Backend    
"$LEMMA_PATH/$SCRIPT_PATH" \
    "$LEMMA_PATH/$CONTAINER_BASE_PATH" \
    -b "$PWD" \
         -s "case_study_models/customer-management-backend/customerManagementBackend.operation" \
         -i "case_study_models/intermediate/operation models/customerManagementBackend.xmi" \
    -t "$PWD/$GENERATED_ARTIFACTS"

# Container Base Generator - Self Service    
"$LEMMA_PATH/$SCRIPT_PATH" \
    "$LEMMA_PATH/$CONTAINER_BASE_PATH" \
    -b "$PWD" \
         -s "case_study_models/customer-self-service-backend/customerSelfServiceBackend.operation" \
         -i "case_study_models/intermediate/operation models/customerSelfServiceBackend.xmi" \
    -t "$PWD/$GENERATED_ARTIFACTS"
    
# Container Base Generator - Policy Management    
"$LEMMA_PATH/$SCRIPT_PATH" \
    "$LEMMA_PATH/$CONTAINER_BASE_PATH" \
    -b "$PWD" \
         -s "case_study_models/policy-management-backend/policyManagementBackend.operation" \
         -i "case_study_models/intermediate/operation models/policyManagementBackend.xmi" \
    -t "$PWD/$GENERATED_ARTIFACTS"

####################################################################################################
# System Visualizer
####################################################################################################

java -jar de.fhdo.lemma.visualizer-0.8.0-SNAPSHOT-standalone.jar \
-s="$PWD/case_study_models/customer-core/customerCore.services" \
-i="$PWD/case_study_models/intermediate/service models/customerCore.xmi" \
-t="$PWD/$GENERATED_ARTIFACTS/visualization" \
code_generation ServicesToGraphVizGenerator -height=1000 -lvl=INTERFACES -aim="$PWD/case_study_models/intermediate/service models"  "customerManagementBackend.xmi" "customerSelfServiceBackend.xmi" "policyManagementBackend.xmi"