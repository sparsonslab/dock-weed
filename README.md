# Dock Weed

Dock weed is a library and application for creating and running directed acyclic graphs (DAGS)
of Docker containers. These graphs can be used for general workflows and for optimisation.

Workflow frameworks such as [Nextflow](https://www.nextflow.io/) and [Airflow](https://airflow.app/)
also can be used to create and run DAGs of containers. However, the emphasis is on the running
rather than the creating. Each container is run as a "task". The running and completion of each task 
is monitored and tasks can be run on a defined schedule. However, the DAG itself has to be defined 
imperatively in code by either defining the task precedence or making a series of task function calls.


The purpose of Docker Weed is:
- To be able to define container DAGs declaratively rather than imperatively, in a form that can be 
  specified as a JSON.
- To be able to define connections (edges) between containers (nodes) in an adaptable fashion.
- To automatically determine node run order by topological sorting.
- To be able to run DAGs with random inputs for Monte-Carlo simulation and optimisation.

Docker Weed is not (yet) focused on orchestration - i.e. scheduling and failure detection.


**This project is a work in progress.**

---
Copyright (c) 2025-2025. Dr Sean Paul Parsons. All rights reserved.