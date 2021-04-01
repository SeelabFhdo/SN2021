## Validation Package for our Springer Nature Article "Applying Model-Driven Engineering to Stimulate the Adoption of DevOps Processes in Small and Medium-Sized Development Organizations"
### Content description
---
This repository contains the artifacts used during the different phases of our proposed workflow for DevOps teams for model-driven microservice development, including those we create due to the workflow. Additionally, we link the repositories of the source code we used in the workflow down below. 

#### Lakeside Mutual Case Study
The folder [case_study_models](https://github.com/SeelabFhdo/SN2021/tree/master/case_study_models) contains reconstructed LEMMA models from our case study in an Eclipse project, which can be imported to the prepared Eclipse instance with our plugins. 

The OpenAPI specifications of the services of the Lakeside Mutual case study are included in the folder [case_study_api_documentation](https://github.com/SeelabFhdo/SN2021/tree/master/case_study_api_documentation) of this repository. 

#### Workflow Artifacts
The generated LEMMA models based on the API documentation of the case study (cf. Subsection 6.2 in our manuscript) are included in the folder [pregenerated_lemma_models_from_openapi](https://github.com/SeelabFhdo/SN2021/tree/master/pregenerated_lemma_models_from_openapi) of this repository. 

The folder [pregenerated_visualization_artifacts](https://github.com/SeelabFhdo/SN2021/tree/master/pregenerated_visualization_artifacts) contains the generated artifacts from the LEMMA Visualizer (cf. Subsection 6.4 in our manuscript). 

The folder [pregenerated_deployment_specification_artifacts](https://github.com/SeelabFhdo/SN2021/tree/master/pregenerated_deployment_specification_artifacts) comprises the generated deployment specifications based on the LEMMA operation models of the case study (cf. Subsection 6.5 and Subsection 6.6).

For counting the generated artifacts' Lines of Code (cf. Section 7), we provide a script, which is located in the [loc_count](https://github.com/SeelabFhdo/SN2021/tree/master/loc_count) folder.

In order to validate the results and rerun the generation steps of the workflow, we provide a step-by-step guideline below, including a [run_code_generation.sh](https://github.com/SeelabFhdo/SN2021/blob/master/run_code_generation.sh) for building all artifacts.

### Source Code
---
The source code used in the Model-Driven Engineering workflow in our contribution is part of the following repositories:
- [LEMMA Repository](https://github.com/SeelabFhdo/lemma)
- [Case Study Lakeside Mutual](https://github.com/Microservice-API-Patterns/LakesideMutual)

### Reproducing the Workflow Steps
---

The reproduction of the workflow steps described in Section 6 of the journal requires the preparation of a local Eclipse instance:
1. Download Eclipse release 2020-12 (4.18.0) of the [Eclipse IDE for Java and DSL Developers](https://www.eclipse.org/downloads/packages/release/2020-12/r/eclipse-ide-java-and-dsl-developers).
2. Install the current ATL package from this update site: [https://download.eclipse.org/mmt/atl/updates/releases](https://download.eclipse.org/mmt/atl/updates/releases/).
3. Extract the JAR archives in the [`dropins.zip`](https://github.com/SeelabFhdo/jss2020/blob/master/dropins.zip) file from this repository to the `dropins` folder of the Eclipse release downloaded in Step 1. The JAR archives in the ZIP file are pre-compiled plugins for LEMMA's modeling languages and the plugins mentioned in our article (see above).
4. Restart Eclipse.

Installing the necessary software on the operating system:
1. Install docker for running the [LEMMAs container_base code generator](https://github.com/SeelabFhdo/lemma/tree/master/code%20generators/de.fhdo.lemma.model_processing.code_generation.container_base)
2. Install the python packages libxml2, lxml, and pyyaml to use LEMMAs code generation scripts (pip3 install ...). 
3. To execute our workflow node.js, rpm, and [GraphViz](https://graphviz.org/) need to be installed on the system to execute the visualization stage of our workflow.
4. To use the LoC_counting script you need Python 3 and the [`cloc` utility](https://github.com/AlDanial/cloc). 

For the actual reproduction, please follow these steps:
1. Clone this repository to your harddrive.
2. Run the prepared Eclipse instance (see above).
3. In the running Eclipse instance, import the `Lakeside Mutual` Eclipse projects contained in the cloned [case_study_lemma_models](https://github.com/SeelabFhdo/SN2021/tree/master/case_study_lemma_models) folder into the current workspace.
4. To generate the LEMMA models based on the OpenAPI specification navigate to the `LEMMA` element and select `Extract LEMMA models from OpenAPI URL`. After finishing the extraction process the models are created in the target location. Please note, that the folder has to be manually refreshed to make the created models visible. 
5. To start the refinement stages of our proposed workflow the created service and data models can be edited by the use of LEMMAS' eclipse editor.
6. For continuing the workflow the different models need to be transformed into their intermediate stage to be used by the [container_base generator](https://github.com/SeelabFhdo/lemma/tree/master/code%20generators/de.fhdo.lemma.model_processing.code_generation.container_base) and the system visualizer. Therefore, navigate to the `LEMMA` element again and select `Generate Intermediate Service Models` and `Generate Intermediate Operation Model` to run the model transformation.
7. Clone the official LEMMA repository to your disk to enable the use of the code generators.
8. Run the [run_container_base_generators.sh](https://github.com/SeelabFhdo/SN2021/blob/master/run_container_base_generators.sh) script. <!--- The script expects the absolute path of the [scripts](https://github.com/SeelabFhdo/lemma/tree/master/scripts) folder as a command line argument to run properly. ---> The script excepts the absolute path of the LEMMA folder, i.e., the cloned LEMMA repository, as a command line argument to run properly. 
9. The script creates a `generated_artifacts` folder, which contains all generated artifacts. 

For replicating the LoC counting follow these steps:
1. To replicate the validation results mentioned in Section 7 of the article, review or execute the scripts from the cloned [loc_count](https://github.com/SeelabFhdo/SN2021/tree/master/loc_count) folder. 
