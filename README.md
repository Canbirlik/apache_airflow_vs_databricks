# 🚀 Orchestration Showdown: Apache Airflow vs. Databricks Workflows

This repository provides the core code examples used to compare two major workflow management paradigms in data engineering: **Apache Airflow** (the external orchestrator) and **Databricks Workflow Jobs** (the integrated execution platform).

The examples demonstrate a simple **Extract, Transform, Load (ETL)** process where data is pulled from a public API (`randomuser.me`).

---

## 📂 Repository Contents

This repository contains two key files, each demonstrating a different approach to scheduling the same ETL logic:

### 1. `random_user_api_workflow.py` (Apache Airflow DAG)

This file defines a modern **Airflow DAG** using the **TaskFlow API** (`@dag` and `@task` decorators).

* **Paradigm:** External Orchestration.
* **Key Features Demonstrated:**
    * **TaskFlow API:** Defining tasks as standard Python functions.
    * **XCom:** Automatic passing of data (JSON output) between tasks using Python `return` statements.
    * **Explicit Dependencies:** Using the `>>` bitwise operator (`fetch_data_ti >> extract_transform_ti`) to clearly define the workflow sequence.
* **Role:** Airflow manages *when* the tasks run and *in what order*, but the execution itself is done by Airflow's workers.

### 2. `Demo Workflow Job.ipynb` (Databricks Notebook)

This file contains the **same ETL logic** embedded within a single Databricks Notebook, designed to be run as a Databricks Workflow Job.

* **Paradigm:** Integrated Execution and Orchestration.
* **Key Features Demonstrated:**
    * **Single Execution Unit:** All three steps (Fetch, Transform, Load) are consolidated into a single notebook/script.
    * **Managed Compute:** When run as a Job, Databricks automatically provisions an optimized, cost-effective **Job Cluster** (Spark) for execution and terminates it afterward.
* **Role:** Databricks handles both the **scheduling** and the **scalable execution**, making it ideal for tasks involving massive data volumes.

---

## 🎯 Comparison Summary

| Feature | Apache Airflow (Code 1) | Databricks Workflows (Code 2) |
| :--- | :--- | :--- |
| **Primary Role** | Sequence Control (Orchestration) | Execution and Scaling (Integrated) |
| **Compute** | Requires **external** workers/resources to run the code. | Provisions **managed Spark Clusters** automatically. |
| **Workflow Unit** | Multiple, chained `@task` functions. | Single **Notebook** or DLT Pipeline. |
| **Best Used For** | Multi-system, multi-cloud workflows (Centralized Control). | Large-scale data processing within the Lakehouse. |

---

### ⚙️ Getting Started

To run the Airflow DAG:

1.  Ensure your Airflow environment is running (e.g., via Docker Compose).
2.  Place `random_user_api_workflow.py` into your Airflow's designated `dags` folder.
3.  Trigger the DAG via the Airflow UI.
