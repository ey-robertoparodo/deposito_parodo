# Application Documentation Template

**Application Owner**: Your Name, you@example.com
<br>**Document Version**: 0.1.0
<br>**Reviewers**: Information not available.

## Key Links

* [Code Repository](`Information not available.`)
* [Deployment Pipeline](`Information not available.`)
* [API](`Information not available.`) ([Swagger Docs](`Information not available.`))
* [Cloud Account](`Information not available.`)
* [Project Management Board](`Information not available.`)
* [Application Architecture](`src/guide_creator_flow/main.py`, `src/guide_creator_flow/crews/**`, `src/guide_creator_flow/tools/custom_tool.py`, `utilis/**`)

## General Information 

<div style="color: gray">
EU AI Act <a href="https://artificialintelligenceact.eu/article/11/" style="color:blue; text-decoration:underline">Article 11</a>; <a href="https://artificialintelligenceact.eu/annex/4/" style="color:blue; text-decoration:underline">Annex IV</a> paragraph 1, 2, 3
<!-- info: this section covers the AI Act requirement of a description of the intended purpose, version and provider, relevant versions and updates. In Article 11, 2(d) a datasheet is required which describes all training methodologies and techniques as well as the characteristics of the training dataset, general description of the dataset, information about their provenance, scope and main characteristics, how the data was obtained and selected, labelling procedures conducted, and data cleaning methodologies deployed. -->
<p></p>
</div>


**Purpose and Intended Use**:
    
* The application orchestrates a multi-agent flow (crewai Flow) to: (1) check topical relevance of a user question, (2) retrieve relevant text chunks from local PDF documents using a FAISS vector store, (3) generate an evidence-grounded answer and a Markdown report, and (4) evaluate answer quality with RAGAS metrics.
* Problem addressed: enabling Retrieval-Augmented Generation (RAG) over local PDFs to answer user questions grounded in provided documents.
* Target users and stakeholders: developers or analysts experimenting with RAG workflows and documentation generation; educational/lab setting.
* KPIs: RAGAS metrics such as context_precision, context_recall, faithfulness, answer_relevancy; successful report generation.
* Ethical/regulatory considerations: transparency about model use (Azure OpenAI), avoiding hallucinations as instructed in task configs, and respecting local document usage. Additional DPIA/legal review: Information not available.
* Prohibited uses: High-risk domains without further controls; authoritative legal/medical/safety advice. Formal list: Information not available.
* **Operational environment:** Local Python execution per `pyproject.toml`; Azure OpenAI via env vars (`AZURE_API_BASE`, `AZURE_API_KEY`, `AZURE_API_VERSION`).


## Risk classification

<div style="color: gray">
Prohibited Risk: EU AI Act Chapter II <a href="https://artificialintelligenceact.eu/article/5/" style="color:blue; text-decoration:underline">Article 5</a>
<br>High-Risk: EU AI Act Chapter III, Section 1 <a href="https://artificialintelligenceact.eu/article/6/" style="color:blue; text-decoration:underline">Article 6</a>, <a href="https://artificialintelligenceact.eu/article/7/" style="color:blue; text-decoration:underline">Article 7</a>  
<br>Limited Risk: Chapter IV <a href="https://artificialintelligenceact.eu/article/50/" style="color:blue; text-decoration:underline">Article 50</a>
<p></p>
</div>

<!--info: The AI Act classifies AI systems into four different risk categories. The EU AI Act categorizes AI systems into four risk levels: unacceptable, high, limited, and minimal risk, each with corresponding regulatory requirements.  
Unacceptable risk (Chapter II, Article 5) includes systems that pose a clear threat to safety or fundamental rights (e.g. social scoring, recidivism scoring) and are banned.  
High-risk systems are delineated in Chapter III, Section 1, Articles 6 and 7, including AI used in sensitive domains like healthcare, law enforcement, education, employment, and critical infrastructure. These must meet strict requirements and conduct conformity assessment practices, including risk management, transparency, and human oversight.  
Limited-risk systems, delineated in Chapter IV Article 50, such as chatbots, must meet transparency obligations (e.g. disclosing AI use).  
Minimal-risk systems, like spam filters or AI in video games, face no specific requirements. -->

* Limited risk (chatbot-style content generation; not listed as high-risk in Annex III).
* Reasoning: Developer-focused RAG demo; no biometric, employment, education, credit, healthcare, law enforcement, or critical infrastructure functions.
   
## Application Functionality 

<div style="color: gray">
EU AI Act <a href="https://artificialintelligenceact.eu/article/11/" style="color:blue; text-decoration:underline">Article 11</a> ; <a href="https://artificialintelligenceact.eu/annex/4/" style="color:blue; text-decoration:underline">Annex IV</a>, paragraph 1, 2, 3
<!-- Info: this section covers the delineation of the general purpose of the system required in Article 1, with a focus on defining what the system should do and how it should work.-->
<p></p>
</div>


* **Instructions for use for deployers**: <div style="color: gray">(EU AI Act <a href="https://artificialintelligenceact.eu/article/13/" style="color:blue; text-decoration:underline">Article 13</a>)</div>
* Set `AZURE_API_BASE`, `AZURE_API_KEY`, `AZURE_API_VERSION` environment variables.
* Install dependencies as per `pyproject.toml`/`README.md`.
* Place PDFs under `24-Settembre/guide_creator_flow/docs` or update paths in `utilis/db_vet.py`.
* Run: `crewai run` or `python -m guide_creator_flow.main`.
* **Model Capabilities**:
  * Can: retrieve chunks from local PDFs; generate grounded answers and a Markdown report; compute RAGAS metrics.
  * Cannot: browse the web; provide calibrated confidence; act autonomously without user input.
  * Supported languages: Italian/English prompts; Azure models are multilingual.
* **Input Data Requirements**:
  * PDFs accessible in the expected `docs/` folder.
  * Valid input: a natural-language question relevant to configured topic.
  * Invalid input: missing env vars, empty/invalid PDFs, off-topic questions (routed to "Not Relevant").
* **Output Explanation**:
  * Outputs: `output/report.md` (answer) and `ragas_results.csv` (metrics).
  * Answers are grounded in retrieved text; uncertainty expressed by stating information gaps per task config.
* **System Architecture Overview**:
  * Flow in `src/guide_creator_flow/main.py`: relevance -> retrieval -> answer/report -> evaluation.
  * Crews: `poem_crew`, `rag_crew` (uses `RAGSearch`), `output_crew`.
  * Vector store: FAISS via LangChain, built from PDFs; embeddings via Azure OpenAI.

## Models and Datasets

<div style="color: gray">
  EU AI Act <a href="https://artificialintelligenceact.eu/article/11/" style="color:blue; text-decoration:underline">Article 11</a>; <a href="https://artificialintelligenceact.eu/annex/4/" style="color:blue; text-decoration:underline">Annex IV</a> paragraph 2 (d)
<p></p>
</div>

<!--All information about models and datasets that are used in the application should be found in their respective dataset or model documentation.  The purpose here is mainly to provide links to those documentation. --> 
<!--In Article 11, 2 (d) a datasheet is required which describes all training methodologies and techniques as well as the charatcteristics of the training dataset, general description of the dataset, information about their provenance, scope and main characteristics, how the data was obtained and selected labelling procedures conducted and data cleaning methodologies deployed -->

### Models

Link to all model integrated in the AI/ML System

| Model   | Link to Single Source of Truth | Description of Application Usage |
|---------|--------------------------------|----------------------------------|
| AzureChatOpenAI (deployment "gpt-4o") | `Information not available.` | Generates relevance checks, RAG answers, and ground-truth synthesis for RAGAS.
| AzureOpenAIEmbeddings | `Information not available.` | Computes embeddings for FAISS vector store and for RAGAS evaluation.

### Datasets

Link to all dataset documentation and information used to evaluate the AI/ML System.  
(Note, Model Documentation should also contain dataset information and links for all datasets used to train and test each respective model) 

| Dataset / Source Folder | Link to Single Source of Truth | Description of Application Usage |
|-------------------------|--------------------------------|----------------------------------|
| Local PDFs under `24-Settembre/guide_creator_flow/docs` | `Information not available.` | Primary source expected by the retriever for building/loading FAISS index.
| `src/guide_creator_flow/crews/rag_crew/input_directory` | `Information not available.` | Example brochures included; not loaded by current retriever path.
| `24-Settembre/guide_creator_flow/documents` | `Information not available.` | Additional example PDFs; not loaded by current retriever path.

## Deployment
    
* Infrastructure and environment details (e.g., cloud setup, APIs).
* Integration with external systems or applications.

### Infrastructure and Environment Details

* **Cloud Setup**:
  * Information not available; repository shows local execution.
  * Requires Azure OpenAI credentials via environment variables.
* **APIs**:
  * Uses Azure OpenAI Chat and Embeddings; endpoints/versions from env vars.
  * Authentication via `AZURE_API_KEY`.
  * Latency/scalability expectations: Information not available.

## Integration with External Systems

<div style="color:gray">
  EU AI Act <a href="https://artificialintelligenceact.eu/article/11/" style="color:blue; text-decoration:underline">Article 11</a> ; <a href="https://artificialintelligenceact.eu/annex/4/" style="color:blue; text-decoration:underline">Annex IV</a> paragraph 1 (b, c, d, g, h), 2 (a)
  <p></p>
</div>

* **Systems**:
  * Dependencies: crewAI, LangChain, FAISS, PyPDF2, RAGAS, Azure OpenAI (chat + embeddings).
  * Data flow: User input -> Relevance check (`PoemCrew`) -> Retrieval (`RagCrew` with `RAGSearch`) -> Answer/report (`OutputCrew`) -> Evaluation (`ragas_prova.execute_ragas`).
  * Error-handling: Env var validation in `utilis.models`; PDF parsing errors logged and skipped; no webhooks.

## Deployment Plan

* **Infrastructure**:
  * Environments: development (local). Staging/production: Information not available.
  * Resource scaling/backup: Information not available.
* **Integration Steps**:
  * Install deps; set Azure env vars; place PDFs under `docs/`; run the flow.
  * Dependencies: see `pyproject.toml`.
  * Rollback: Information not available.
* **User Information**: Local developer machine.


## Lifecycle Management

<div style="color:gray">
  EU AI Act <a href="https://artificialintelligenceact.eu/article/11/" style="color:blue; text-decoration:underline">Article 11</a>; <a href="https://artificialintelligenceact.eu/annex/4/" style="color:blue; text-decoration:underline">Annex IV</a> paragraph 6
  <p></p>
</div>
    
* Monitoring procedures for performance and ethical compliance.
  * Information not available.
* Versioning and change logs for model updates.
  * Application version defined in `pyproject.toml` (0.1.0). Detailed changelog: Information not available.
* **Metrics**:
  * Application performance: Information not available.
  * Model performance: RAGAS metrics (context_precision, context_recall, faithfulness, answer_relevancy, answer_correctness where applicable).
  * Infrastructure: Information not available.
* **Key Activities**:
  * Evaluate outputs with RAGAS (`ragas_results.csv`) and iterate.
  * Update PDFs and rebuild FAISS index when documents change.
  * Dependency/model updates: Information not available.
* **Documentation Needs**:
  * **Monitoring Logs**: Information not available.
  * **Incident Reports**: Information not available.
  * **Retraining Logs**: Not applicable; embeddings index rebuilt from PDFs.
  * **Audit Trails**: Information not available.
-**Manteinance of change logs**: 
* new features added
* updates to existing functionality
* deprecated features
* removed features
* bug fixes
* security and vulnerability fixes

### Risk Management System

<div style="color:gray">
  EU AI Act <a href="https://artificialintelligenceact.eu/article/9/" style="color:blue; text-decoration:underline">Article 9</a>
  <br>EU AI Act <a href="https://artificialintelligenceact.eu/article/11/" style="color:blue; text-decoration:underline">Article 11</a>
  ; <a href="https://artificialintelligenceact.eu/annex/4/" style="color:blue; text-decoration:underline">Annex IV</a>
  <p></p>
</div>
<!--**Instructions:**  A thorough risk management system is mandated by the AI Act, especially for high-risk AI systems. This section documents the  proactive efforts to ensure the AI system operates safely and ethically. In general in this section you should document all the measures undertaken to make sure that a system operates safely on the market. Example: Consider a facial recognition system used for real-time law enforcement in public spaces. This is categorized as high-risk under the EU AI Act. If developers document the risk that the system might misidentify individuals—particularly among minority groups due to biased training data—they can plan for rigorous dataset audits, independent bias testing, and establish human oversight in decision-making. Without documenting this risk, the system might be deployed without safeguards, leading to wrongful detentions and legal liabilities. Systematic documentation ensures these issues are not only identified but addressed before harm occurs.-->


**Risk Assessment Methodology:** Information not available.

**Identified Risks:** 

**Potential Harmful Outcomes:** Hallucinated content; misinterpretation of PDFs; exposure of sensitive data if PDFs contain such content; dependency on Azure availability.

**Likelihood and Severity:** Moderate likelihood of minor inaccuracies; low severity in developer/demo scope. Not intended for high-risk use.

#### Risk Mitigation Measures

**Preventive Measures:** Relevance gating; instructions to avoid hallucinations; grounding answers on retrieved passages; local data control.

**Protective Measures:** State information gaps when evidence is insufficient; skip unreadable PDFs; explicit env var checks raise clear errors.

## Testing and Validation (Accuracy, Robustness, Cybersecurity)

<div style="color:gray">
  EU AI Act <a href="https://artificialintelligenceact.eu/article/15/" style="color:blue; text-decoration:underline">Article 15</a>
  <p></p>
</div>

**Testing and Validation Procedures (Accuracy):**
The flow writes an answer to `output/report.md` and then computes RAGAS metrics via `utilis/ragas_prova.py`, saving results to `ragas_results.csv`.

**Performance Metrics:** context_precision, context_recall, faithfulness, answer_relevancy, answer_correctness (when reference available).

**Validation Results:** Information not available; produced per run in `ragas_results.csv`.

**Measures for Accuracy:** Maintain high-quality PDFs; tune retriever parameters (`k`, `fetch_k`, `lambda_mult`); adjust chunking (`chunk_size`, `chunk_overlap`).

  
### Accuracy throughout the lifecycle

**Data Quality and Management:** Ensure PDFs are accurate and current; verify extracted text quality; rebuild FAISS index after document updates.

**Model Selection and Optimisation:** FAISS + Azure OpenAI; parameters controlled in `utilis/vectore_store.py` and `utilis/document.py`.

**Feedback Mechanisms:** Manual review of generated report and RAGAS CSV; iterate documents and prompts.

### Robustness 

<-- Retrieval robustness depends on PDF text extraction quality and FAISS index consistency; criticalities include malformed PDFs and missing Azure env configuration. -->

**Robustness Measures:**

* Error handling for PDF parsing; env var checks; deterministic local index reuse/build.

**Scenario-Based Testing:**

* Test irrelevant queries (expect router to branch to "Not Relevant").
    
* Missing PDFs should yield empty retrieval; tasks instruct to signal insufficient information.
    

**Redundancy and Fail-Safes:**
    
* Not implemented. Information not available.
    
**Uncertainty Estimation:**
    
* Not implemented. Information not available.
    

### Cybersecurity 

<div style="color:gray">
  EU AI Act <a href="https://artificialintelligenceact.eu/article/11/" style="color:blue; text-decoration:underline">Article 11</a>; <a href="https://artificialintelligenceact.eu/annex/4/" style="color:blue; text-decoration:underline">Annex IV</a> paragraph 2 (h)
  <p></p>
</div>

**Data Security:**
Use local storage for PDFs and FAISS index; manage Azure credentials via environment variables; avoid committing secrets.

**Access Control:**
Local execution context; no user management implemented. Information not available for multi-user setups.

**Incident Response :**
Information not available.


These measures include using environment variables for credentials. Additional security hardening, monitoring, and incident processes are not defined in the repository.

  

## Human Oversight 

<div style="color:gray">
  EU AI Act <a href="https://artificialintelligenceact.eu/article/11/" style="color:blue; text-decoration:underline">Article 11</a>;; <a href="https://artificialintelligenceact.eu/annex/4/" style="color:blue; text-decoration:underline">Annex IV</a> paragraph 2(e)
  <br>EU AI Act <a href="https://artificialintelligenceact.eu/article/14/" style="color:blue; text-decoration:underline">Article 14</a>
  <p></p>
</div>

<!-- info: AI Act Article 11, paragraph 2(e) requirements: assessment of the human oversight measures needed in accordance with Article 14, including the assessment of the technical measures needed to facilitate the integration of the outputs of the AI systems by deployers. -->


**Human-in-the-Loop Mechanisms:**  User provides the question; if marked not relevant, user is prompted again. Outputs (`report.md`) are reviewed by humans.

**Override and Intervention Procedures:** Users can stop execution and modify inputs or configuration; no autonomous actions are performed.

**User Instructions and Training:** See repository `README.md` for setup and run steps. Additional training: Information not available.

**Limitations and Constraints of the System:** Limited to local PDFs; accuracy depends on extraction quality; requires Azure credentials; no web retrieval; no uncertainty estimates.


## Incident Management
<!-- what happens when things go wrong. This part is particularly important to provide information on how incidents were dealth with and the processes put in place to minimize damage when things go wrong. -->
* **Common Issues**:
  * Missing Azure env vars -> `EnvironmentError` in `utilis.models`.
  * No/invalid PDFs -> empty retrieval or skipped files; fix source documents under `docs/`.
  * FAISS index not found/corrupt -> app rebuilds index from PDFs; ensure `faiss_index_example/` is writable.
  * Network/API errors -> check Azure endpoint and key; consider adding retries.
* **Support Contact**:
  * Project maintainer: Information not available. Framework help: see links in `README.md` (crewai docs, GitHub, Discord).


### Troubleshooting AI Application Deployment

This section outlines potential issues that can arise during the deployment of an AI application, along with their causes, resolutions, and best practices for mitigation.


#### Infrastructure-Level Issues

##### Insufficient Resources

* **Problem**: Inaccurate resource estimation for production workloads.
  * Unexpected spikes in user traffic can lead to insufficient resources such as compute, memory or storage that can lead to crashes and bad performance

* **Mitigation Strategy**:
<!-- describe here the resolution strategy such as:
-  Enable autoscaling (e.g., Kubernetes Horizontal Pod Autoscaler).
  - Monitor usage metrics and adjust resource allocation dynamically.
  - Implement rate-limiting for traffic spikes. -->


##### Network Failures

* **Problem**:  network bottlenecks  can lead to inaccessible or experiences latency of the application.

* **Mitigation Strategy**:
<!-- 
  - Test network connectivity 
  - Use content delivery networks (CDNs) or regional load balancers.
  - Ensure proper failover mechanisms.-->


##### Deployment Pipeline Failures

* **Problem**: pipeline fails to build, test, or deploy because of issues of compatibility between application code and infrastructure, environment variables or credentials misconfiguration.

* **Mitigation Strategy**: 
<!--:
  - Roll back to the last stable build.
  - Fix pipeline scripts and use containerisation for environment consistency.
  - Enable verbose logging for error diagnostics.-->


#### Integration Problems

##### API Failures

* **Problem**: External APIs or internal services are unreachable due to network errors or authentication failures.

* **Mitigation Strategy**:
<!--:
  - Implement retries with exponential backoff.
  - Validate API keys or tokens and refresh as needed.
  - Log and monitor API responses for debugging. -->

##### Data Format Mismatches

* **Problem**: Crashes or errors due to unexpected data formats such as changes in the schema of external data sources or missing data validation steps.

* **Mitigation Strategy**: 

<!--
  - Use schema validation tools (e.g., JSON schema validators).
  - Add versioning to APIs and validate inputs before processing.-->

#### Data Quality Problems

* **Problem**: Inaccurate or corrupt data leads to poor predictions.
* **Causes**:
  * No data validation or cleaning processes.
  * Inconsistent labelling in training datasets.

* **Mitigation Strategy**: 
<!--
- **Resolution**:
  - Automate data quality checks (e.g., Great Expectations framework).
  - Regularly audit and clean production data.-->


#### Model-Level Issues

##### Performance or Deployment Issues

* **Problem**: Incorrect or inconsistent results due to data drift or inadequate training data for the real world deployment domain. 

* **Mitigation Strategy**:

<!--
- **Resolution**:
  - Monitoring for data drift and retraining of the model as needed.
  - Regularly update the model -->


#### Safety and Security Issues

##### Unauthorised Access

* **Problem**: Sensitive data or APIs are exposed due to misconfigured authentication and authorization.

##### Data Breaches

* **Problem**: User or model data is compromised due to insecure storage or lack of monitoring and logging of data access. 

* **Mitigation Strategy**: 
<!--
- **Resolution**:
  - Use secure storage services (e.g., AWS KMS).
  - Implement auditing for data access and alerts for unusual activity.
  6.1. Delayed or Missing Data-->


#### Monitoring and Logging Failures

##### Missing or Incomplete Logs

* **Problem**: Lack of information to debug issues due to inefficient logging. Critical issues go unnoticed, or too many false positives occur by lack of implementation ofactionable information in alerts. 

* **Mitigation Strategy**: 


<!--
- **Resolution**:
  - Fine-tune alerting thresholds and prioritise critical alerts.
  - Use tools like Prometheus Alertmanager to manage and group alerts. -->


#### Recovery and Rollback

##### Rollback Mechanisms

* **Problem**: New deployment introduces critical errors.

* **Mitigation Strategy**: 

<!--
- **Resolution**:
  - Use blue-green or canary deployments to minimise impact.
  - Maintain backups of previous versions and configurations. -->

##### Disaster Recovery

* **Problem**: Complete system outage or data loss.

* **Mitigation Strategy**:

<!--
- **Resolution**:
  - Test and document disaster recovery plans.
  - Use automated backups and verify restore procedures.-->

### EU Declaration of conformity 

<div style="color: gray">
  EU AI Act <a href="https://artificialintelligenceact.eu/article/47/" style="color:blue; text-decoration:underline">Article 47</a>
  <p></p>
</div>

<!-- when applicable and certifications are available: it requires a systems name as well as the name and address of the provider; a statement that the EU declaration of conformity referred to in Article 47 is issued under the sole responsibility of the provider; a statement that the AI system is in conformity with this Regulation and, if applicable, with any other relevant Union law that provides for the issuing of the EU declaration of conformity referred to in Article 47, Where an AI system involves the processing of personal data;  a statement that that AI system complies with Regulations (EU) 2016/679 and (EU) 2018/1725 and Directive (EU) 2016/680, reference to the harmonised standards used or any other common specification in relation to which
conformity is declared; the name and identification number of the notified body, a description of the conformity
assessment procedure performed, and identification of the certificate issued; the place and date of issue of the declaration, the name and function of the person who signed it, as well as an
indication for, or on behalf of whom, that person signed, a signature.-->

### Standards applied

<!-- Document here the standards and frameworks used-->
Information not available.

## Documentation Metadata

### Template Version
<!-- info: link to model documentation template (i.e. could be a GitHub link) -->
Information not available.

### Documentation Authors
<!-- info: Give documentation authors credit

Select one or more roles per author and reference author's
emails to ease communication and add transparency. -->

* **Your Name, Team:** Gruppo 2
* **Information not available, Team:** (Contributor)
* **Information not available, Team:** (Contributor)
