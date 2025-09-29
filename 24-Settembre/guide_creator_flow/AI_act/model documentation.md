# Guide Creator Flow (RAG) - Model Documentation
<!-- info: Derived from the project code under src/guide_creator_flow -->

<div style="color:gray">
    EU AI Act <a href="https://artificialintelligenceact.eu/article/11/" style="color:blue; text-decoration:underline">Article 11</a>, paragraph 1
    <!-- info:  
    The AI Act requires a description of  
    (a) the intended purpose, version, and provider,  
    (b) a description of how the system interacts with software and hardware,  
    (c) relevant versions and updates,  
    (d) all the forms in which the AI system is put into service
    The overview part should also include:  
    (e) the hardware on which the system is intended to run,  
    (f) whether the system is part of the safety component of a product,  
    (g) a basic description of the user interface, and  
    (h) the instructions for use for the deployers. 
    -->
    <p></p>
</div>

**Model Owner**: Name and contact information
<br>**Document Version**: 0.1.0 (from `pyproject.toml`)
<br>**Reviewers**: Information not available.

## Overview 

<div style="color:gray">
EU AI Act <a href="https://artificialintelligenceact.eu/article/11/" style="color:blue; text-decoration:underline">Article 11</a>, paragraph 1

<!-- info: This section enables all stakeholders to have a glimpse into the model selection, design, and development processes.  
You can use this section to provide transparency to users and high-level information to all relevant stakeholders.-->
<p></p>
</div>

### Model Type

**Model Type:** Retrieval-Augmented Generation (RAG) pipeline orchestrated via crewAI Flow with LLM-in-the-loop (Azure OpenAI Chat) and vector search (FAISS via LangChain).

### Model Description 

<div style="color:gray">
    EU AI Act <a href="https://artificialintelligenceact.eu/article/11/" style="color:blue; text-decoration:underline">Article 11</a> ; <a href="https://artificialintelligenceact.eu/annex/4/" style="color:blue; text-decoration:underline">Annex IV</a>  paragraph 1(a)
    <p></p>
</div>

* Description
  A multi-agent RAG system that: (1) evaluates query relevance to a predefined topic, (2) retrieves relevant document chunks from a FAISS vector store built from local PDFs, (3) generates an evidence-grounded answer using an Azure OpenAI chat model, (4) produces a Markdown report, and (5) evaluates output quality with RAGAS metrics. Orchestration is implemented with crewAI Flow (`PoemFlow`) coordinating three crews: `PoemCrew` (relevance), `RagCrew` (retrieval via `RAGSearch` tool), and `OutputCrew` (answer + article). Embeddings and LLM are provided by Azure OpenAI through LangChain. Intended purpose is guided Q&A/report generation within the configured topic domain.

### Status 
<!-- scope: telescope -->
<!-- info: Select **one:** -->
**Status Date:** 2025-09-25

**Status:** Under Preparation

### Relevant Links

Information not available.

### Developers

Information not available.

### Owner
<!-- info: Remember to reference developers and owners emails. -->
* Information not available.

## Version Details and Artifacts 

<div style="color:gray">
    EU AI Act <a href="https://artificialintelligenceact.eu/article/11/" style="color:blue; text-decoration:underline">Article 11</a> ; <a href="https://artificialintelligenceact.eu/annex/4/" style="color:blue; text-decoration:underline">Annex IV</a> paragraph 1(c)
    <p></p>
</div>

<!-- scope: periscope -->
<!-- info: Provide details about the current model version
and which model version the current model card corresponds to.

For models without version number, use "Not currently tracked"
but be sure to track the release date of the model.
-->


**Current Model Version:**
0.1.0 (from `pyproject.toml`)

**Model Version Release Date:**
Information not available.

**Model Version at last Model Documentation Update:**
0.1.0

**Artifacts:**

* Vector index persisted locally under `faiss_index_example/` (e.g., `index.faiss`, `index.pkl`).
* Source PDFs under `docs/` used to build the vector store.
* No trainable model weights (LLM and embeddings accessed via Azure OpenAI APIs).

## Intended and Known Usage

### Intended Use
<!-- info: This section focuses on the initial purpose and/or reasoning
for creating the model. It is important to define this section as the intended use directly affects the AI Act classification. For example:
A face recognition model for personal photo apps → Limited risk
The same model used for law enforcement → High or unacceptable risk


Example Use Case: A university research team develops a machine learning model to predict the likelihood of hospital readmission among diabetic patients over the age of 65, using data from a regional healthcare network. The model is trained and validated specifically on this elderly population and is intended to support hospital planning and academic research. However, the team does not document the model’s intended use or demographic limitations. A health-tech company later integrates the model into a mobile app aimed at helping diabetes patients of all ages manage their care. The model performs poorly for younger users, frequently overestimating their risk of readmission. This leads to unnecessary anxiety, inappropriate self-care decisions, and false alerts to care providers. The misapplication draws criticism for lacking transparency, and regulators question the ethics of deploying a model outside its original context.   -->

* Description
  Assist users in generating evidence-grounded answers and a Markdown report to a user query constrained by a topic (default: "Regolamenti universitari o fondi pensione/ viaggi in Francia"). The system retrieves relevant chunks from local PDFs, synthesizes an answer via an Azure OpenAI chat model, and evaluates with RAGAS. Execution is via `crewai run` or the `kickoff`/`run_crew` entry points.

### Domain(s) of use

* Description
  Internal knowledge assistance and documentation/report creation on the configured topic domain using local PDF sources.


**Specific tasks performed:**
* Relevance evaluation of user query (`PoemCrew`).
* Document retrieval via FAISS retriever (`RagCrew` using `RAGSearch`).
* RAG answer generation and Markdown report authoring (`OutputCrew`).
* RAGAS evaluation (context precision/recall, faithfulness, answer relevancy; optional correctness).

  **Instructions for use for deployers**:
<div style="color:gray">
    EU AI Act <a href="https://artificialintelligenceact.eu/article/11/" style="color:blue; text-decoration:underline">Article 13</a> ; <a href="https://artificialintelligenceact.eu/annex/4/" style="color:blue; text-decoration:underline">Annex IV</a> 
    <p></p>
</div>

### Out Of Scope Uses

Information not available.

### Known Applications 

<div style="color:gray">
    EU AI Act <a href="https://artificialintelligenceact.eu/article/11/" style="color:blue; text-decoration:underline">Article 11</a> ; <a href="https://artificialintelligenceact.eu/annex/4/" style="color:blue; text-decoration:underline">Annex IV</a>  paragraph 1(f)
    <p></p>
</div>

<!-- info: Fill out the following section if the model has any
current known usages.
-->

Information not available.

Note, this table may not be exhaustive.  Model users and documentation consumers at large
are highly encouraged to contribute known usages.

## Model Architecture 

<div style="color:gray">
EU AI Act <a href="https://artificialintelligenceact.eu/article/11/" style="color:blue; text-decoration:underline">Article 11</a>; <a href="https://artificialintelligenceact.eu/annex/4/" style="color:blue; text-decoration:underline">Annex IV</a>  paragraph 2(b), 2(c)

Info – AI Act requirements:  
This section should contain a description of the elements of the model and the processes of its training and development.  

Article 11(2)(b) requires the design specifications of a system, model selection, and what the system is designed to optimize for, as well as potential trade-offs.  

Article 11(2)(c) requires a description of the system’s architecture, how software components are built on or feed into each other, and the computational resources needed to develop, train, test, and validate the system.
</div>


<!-- Info: Describing the architecture is fundamental for reproducibility, transparency, and effective maintenance. Without clear records of the model’s layers, activation functions, input/output shapes, and training configurations, it becomes difficult to reproduce results, debug issues, or update the model reliably.  -->


* Architecture Description
 
* Key components
    
* Hyperparameter tuning methodology
  Information not available. (No training loop; retrieval parameters are statically configured.)
 
* Training Methodology
  Not applicable (no model training; uses API-hosted LLM and embeddings, and builds a local FAISS index from PDFs).
 
* Training duration
  Not applicable.
     
* Compute resources used
  Not specified. Runs locally and calls Azure OpenAI services.
     
 
### Data Collection and Preprocessing

<div style="color:gray">
    EU AI Act <a href="https://artificialintelligenceact.eu/article/11/" style="color:blue; text-decoration:underline">Article 11</a>; <a href="https://artificialintelligenceact.eu/annex/4/" style="color:blue; text-decoration:underline">Annex IV</a>  paragraph 2(d)
    <p></p>
</div>

<!--check data documentation to avoid duplicates of information and link it in this sectiion

In Article 11, 2 (d) a datasheet is required which describes all training methodologies and techniques as well as the characteristics of the training dataset, general description of the dataset, information about their provenance, scope and main characteristics, how the data was obtained and selected labelling procedures conducted and data cleaning methodologies deployed -->

* **Steps Involved**:
  * Data collection: Local PDF files under `docs/` are read using `PyPDF2.PdfReader`.
  * Data cleaning: Not explicitly implemented; raw text is concatenated per PDF. Errors on reading a file are printed and the file is skipped.
        
  * Data transformation: Text is split into overlapping chunks using `RecursiveCharacterTextSplitter` with the separators list defined in code.


       
### Data Splitting 

* **Subset Definitions**:
  * **Training set**: Not applicable.
  * **Validation set**: Not applicable.
  * **Test set**: Not applicable.
* **Splitting Methodology**:
  * Not applicable.
* **Proportions**:
  * Not applicable.
* **Reproducibility**:
  * Not applicable.
    
**Data Shuffling**:

* Shuffle applied: Not applicable. 
 
## Model Training Process 

<div style="color:gray">
    EU AI Act <a href="https://artificialintelligenceact.eu/article/11/" style="color:blue; text-decoration:underline">Article 11</a> ; <a href="https://artificialintelligenceact.eu/annex/4/" style="color:blue; text-decoration:underline">Annex IV</a>  paragraph 2(c, g), paragraph 3

<!-- AI Act requirements info:  
In Article 11 paragraph 2(c), details about the computational resources needed to develop, train, test, and validate AI systems are required.  

Moreover, in accordance with Article 11 paragraph 2(g), this section must include the validation and testing procedures used, the data involved, and the main metrics adopted to measure accuracy, robustness, and compliance with the requirements laid out in Chapter III, Section 2.  

Paragraph 3 further requires detailed information about the monitoring, functioning, and control of the system, as well as logging of testing, with reports dated and signed by responsible stakeholders.-->
<p></p>
</div>


**Details of Processes**:

* **Initialisation**: Load environment variables; build or load FAISS index from `docs/` PDFs; create retriever with MMR parameters; configure Azure OpenAI clients via env vars.
* **Loss Function**: Not applicable.
* **Optimiser**: Not applicable.
* **Hyperparameters**: Retrieval parameters (k=4, fetch_k=20, lambda_mult=0.3); chunk_size=2000; chunk_overlap=400.
        
## Model Training and Validation 
 
 <div style="color:gray">
@@
 </div>
 
 Objective: Clarify what the model is supposed to achieve. 
 
-* Problem statement (e.g., classification of X, prediction of Y)
-* Business goals (accuracy, fairness, speed)
-* Metrics selected (e.g., accuracy, precision, recall, F1-score, AUC-ROC, MAE, RMSE)
-Rationale for each metric (why accuracy? why F1-score?)
-
-* Model predictions on the validation set evalutaion description. 
+* Problem statement: Generate evidence-grounded answers and a Markdown article to a user query using local documents.
+* Business goals: Produce accurate, faithful, and relevant responses grounded in retrieved context.
+* Metrics selected: RAGAS metrics — context_precision, context_recall, faithfulness, answer_relevancy (answer_correctness optionally when reference available).
+Rationale for each metric: Directly aligned with grounding, coverage, and relevance in RAG systems.

* Model predictions on the validation set evalutaion description: Not applicable (no supervised training/validation split). 

<!--
- Performance metrics (e.g., accuracy, F1 score, RMSE) are monitored.
- Documeting this step is important as it enables to detect errors and performance issues early on: Overfitting can be detected using validation loss trends.
-->

<!--### Performance Metrics

- Evaluation Metrics Used (e.g., Accuracy, Precision, Recall, AUC-ROC)
- Benchmarking Results
- Validation Process
- Real-World Performance
- Stress testing
- Performance across different environments and populations -->

**Hyperparameter Tuning**:
  Information not available (static configuration in code).
        
**Regularisation**:
  Not applicable.
    
**Early Stopping**:
  Not applicable.
 
## Model Testing and Evaluation

<!--
- Performance metrics (e.g., accuracy, F1 score, RMSE) are monitored.
- Documeting this step is important as it enables to detect errors and performance issues early on: Overfitting can be detected using validation loss trends.
-->

<!-- Example: In medical diagnosis, using accuracy alone can be misleading in imbalanced datasets, potentially missing critical cases like cancer. Metrics like recall (which measures the percentage of actual cancer cases the model correctly identifies. Critical for minimizing missed diagnoses), precision ( to ensure that when the model predicts cancer, it’s actually correct—important to reduce false alarms), F1 score, and AUC-ROC provide a more meaningful assessment by accounting for the real-world impact of false positives and false negatives. Choosing the right metrics ensures models are effective, trustworthy, and aligned with practical goals and consequences.

## Model Validation and Testing
- **Assess the metrics of model performance** 
   - accuracy:
   - precision: 
   - recall:
   - F1 score:

- **Advanced performance metrics**
  - ROC-AUC:
    - trade-off between true positive rate and false positive rate
  - PR- AUC
     - Evaluating precision and recall trade-off
  - Specificity
    - (True Negatives/(True Negatives+False Positives))
  - Log Loss (Cross-Entropy Loss):
    - Penalises incorrect probabilities assigned to classes.


- **Context dependant metrics**: 
  - Regression Metrics: For tasks predicting continuous values
  - Clustering Metrics: for tasks grouping similar data points
  - Ranking Metrics: for tasks predicting rankings (e.g., search engines recommendation systems)
  - NLP processing metrics (e.g., text classification, sequence-to-sequence tasks)


- **Fairness Metrics**:
    
    - Ensure the model treats different groups (e.g., based on gender, race) equitably.
    - Examples: Demographic parity, equal opportunity, and disparate impact.
- **Explainability Metrics**:
    
    - Measure how understandable and interpretable are the model’s decisions.
    - Examples: Feature importance, fidelity (how well explanations match the model), and sparsity (using fewer features for explanations).
    - 
- **Robustness Metrics**:
    
    - Assess how well the model performs under challenging or unexpected conditions.
    - Examples: Adversarial robustness, performance under data drift, and sensitivity to input changes.
 
- Limitations of the performance after the tests
- Simulate deployment scenarios to understand real-world implications.
- Define thresholds for acceptable performance levels.
- Justify the choice of metrics based on the application’s purpose.
   
--> 

 **Performance Metrics**:
     
* RAGAS evaluation outputs (saved to `ragas_results.csv`): context_precision, context_recall, faithfulness, answer_relevancy (and optionally answer_correctness).
 
  **Confusion Matrix**:
     
* Not applicable.
 
  **ROC Curve and AUC**:
     
* Not applicable.
 
  **Feature Importance**:
     
* Not applicable.
 
  **Robustness Testing**:
 
* Information not available.
 
  **Comparison to Baselines**:
     
* Information not available.

### Model Bias and Fairness Analysis 

<div style="color:gray">
    EU AI Act <a href="https://artificialintelligenceact.eu/article/11/" style="color:blue; text-decoration:underline">Article 11</a> ; <a href="https://artificialintelligenceact.eu/annex/4/" style="color:blue; text-decoration:underline">Annex IV</a>  paragraph 2 (f, g), paragraph 3, 4
    <p></p>
</div>

<!-- info: This section aims to cover the AI Act requirements layed out in Article 11 paragraph 2 g that requires the description of the potential discriminatory impacts. 
Paragraph 4 requires the assessment of the appropriateness of the performance metrics.-->  



![](https://lh7-rt.googleusercontent.com/docsz/AD_4nXclauxwg1nWuPj2z0TcgUK9y69AqHzk_-jQ5BJwYeDkjPSOLVddFcHJ6-oOiuZ2p4Rk3VpqyKw9CvU7N1LOqYtpdjN6CV_hhTxTtpNj4auLmqhsaIQ5fRLIPnVpZOnhtR63YNELlg?key=Lv0_1kRp5_LSkJabUJ8gjQ)Implicit Bias, Measurement Bias, Temporal Bias, Selection Bias, Confounding Bias

#### Bias Detection Methods Used
    

**Pre-processing:** Resampling, Reweighting,Transformation (data imputation, changing order of data); Relabeling, Blinding
    
**In-processing:** Transfer learning, Reweighting, Constraint optimization, Adversarial Learning, Regularization, Bandits
    
**Post-processing:** Transformation, Calibration, Thresholding
    


**Results of Bias Testing:**
    Information not available.
    

#### Mitigation Measures
    

**Fairness adjustments:** Introduce fairness criteria (like demographic parity, equal opportunity, or equalized odds) into the model training process. 
    
**Adversarial Debiasing:** Use adversarial networks to remove biased information during training. The main model tries to make accurate predictions, while an adversary network tries to predict sensitive attributes from the model's predictions.
    

#### Retraining approaches

**Fairness Regularization:** Modify the model's objective function to penalize bias. This introduces regularization terms that discourage the model from making predictions that disproportionately affect certain groups.
    
**Fair Representation Learning:** Learn latent representations of the input data that remove sensitive attributes, ensuring that downstream models trained on these representations are fair.
    
### Post-Processing Techniques

**Fairness-Aware Recalibration:** After the model is trained, adjust decision thresholds separately for different demographic groups to reduce disparities in false positive/false negative rates.
    
**Output Perturbation:** Introduce randomness or noise to model predictions to make outcomes more equitable across groups.
    
**Fairness Impact Statement:** Explain trade-offs made to satisfy certain fairness criterias
    

## Model Interpretability and Explainability 

<div style="color:gray">
    EU AI Act <a href="https://artificialintelligenceact.eu/article/11/" style="color:blue; text-decoration:underline">Article 11</a>; <a href="https://artificialintelligenceact.eu/annex/4/" style="color:blue; text-decoration:underline">Annex IV</a>  paragraph 2(e)
    <p></p>
</div>

**Explainability Techniques Used:**
  <!-- for example: Shapley values, LIME, etc. Both SHAP and LIME are explainability techniques that help to understand why a machine learning model made a specific prediction — especially when the model is a complex "black box" like a random forest, gradient boosting, or deep neural net. Shap Uses game theory to assign each feature a value showing how much it contributed to a prediction. Lime builds a simple, interpretable model (like a linear model) near the point of interest to explain the prediction -->
    
  Examples: 
    SHAP (SHapley Additive exPlanations), 
    LIME (Local Interpretable Model-agnostic Explanations)

**Post-hoc Explanation Models**

* Feature Importance, Permutation Importance, SHAP (SHapley Additive exPlanations), LIME (Local Interpretable Model-agnostic Explanations):
* Partial Dependence Plots (PDP) 
* Counterfactual Explanations
* Surrogate Models
* Attention Mechanisms (for Deep Learning)
    

**Model-Specific Explanation Techniques**

<!-- info: this part is important to delineate why a model makes a decision or to debug and identify if the model is focusing on the right parts of the input. Especially fundamental for models deployed in critical domains such as medical, financial and legal or law enforcement. This section can be useful to draft the user-interface section of the documentation.) -->

* Grad-CAM (Gradient-weighted Class Activation Mapping) for CNNs and RNNs: especially for computer vision applications 
* Layer-wise Relevance Propagation (LRP): Works well for CNNs, fully connected nets, and some RNNs (classification focused)
* TreeSHAP (SHAP for Decision Trees)
    

How interpretable is the model’s decision-making process? 
Information not available.


<!--
Some technical tools that can aid transparency include:
- Data Lineage Tools: Track the flow and transformation of data (e.g., Apache Atlas, Pachyderm).
- Explainability Libraries: SHAP, LIME, Captum, TensorFlow Explain.
- Version Control Systems: Git, DVC (Data Version Control) for datasets and models. -->

### EU Declaration of conformity 

<div style="color:gray">
    EU AI Act <a href="https://artificialintelligenceact.eu/article/47/" style="color:blue; text-decoration:underline">Article 47</a>(d)
    <p></p>
</div>

 <!-- when applicable and certifications are available: it requires a systems name as well as the name and address of the provider; a statement that the EU declaration of conformity referred to in Article 47 is issued under the sole responsibility of the provider; a statement that the AI system is in conformity with this Regulation and, if applicable, with any other relevant Union law that provides for the issuing of the EU declaration of conformity referred to in Article 47, Where an AI system involves the processing of personal data;  a statement that that AI system complies with Regulations (EU) 2016/679 and (EU) 2018/1725 and Directive (EU) 2016/680, reference to the harmonised standards used or any other common specification in relation to which
conformity is declared; the name and identification number of the notified body, a description of the conformity
assessment procedure performed, and identification of the certificate issued; the place and date of issue of the declaration, the name and function of the person who signed it, as well as an
indication for, or on behalf of whom, that person signed, a signature.-->

### Standards applied

Information not available.

## Documentation Metadata

### Version
<!-- info: provide version of this document, if applicable (dates might also be useful) -->
0.1.0

### Template Version
<!-- info: link to model documentation template (i.e. could be a GitHub link) -->
Information not available.

### Documentation Authors
<!-- info: Give documentation authors credit

Select one or more roles per author and reference author's
emails to ease communication and add transparency. -->

* Information not available.
