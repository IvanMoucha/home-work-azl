
# High Level Architecture
![azl-hmw-hld.drawio.png](docs/azl-hmw-hld.drawio.png)
* The PoC Architecture is containing two main components and a few sub-modules
  * The Data Ingestion and Processing module together with increment processor
    * The Data Ingestion is responsible for ingesting the data from the source
    * The Data Processor is enriching data and store unique data in the data store and store all increments remotely
    * Error handler for processing corrupted data(notifications, logging, etc)
  * API to provide Read access to the data
    * API Gateway to provide access to the API itself
    * AutH server to allow authentication on API level

# PoC Implementation Summary
## Infrastructure
* Kubernetes Cluster: Provides the underlying infrastructure for the PoC.
  * Tested using Docker Desktop on macOS.
  * Manual docker builds for two images: Processor and API.
  * Helm package manager used for managing Kubernetes applications.
  * Helm chart in infrastructure directory sets up the PoC.

## Data Ingestion and Processing Module
* Wrapped in `processor.py`.
* Data Ingestion: Responsible for ingesting data from the source.  
  * Implemented in `src/data_pipeline/ingestion.py`.
  * Uses scheduled tasks to fetch and process data.
* Data Processor: Process and enriches data and stores unique data in the data store, while storing all increments remotely.  
  * Implemented in `src/data_pipeline/processor.py`.
  * Utilizes PostgreSQL for data storage.
  * Emulate business logic as enricher via `src/data_pipeline/enricher.py`.
  * Can provide LLM summary for the Phys Science News via `src/data_pipeline/ai.py`
* Error Handler: Manages processing of corrupted data, including notifications and logging.  
  * Implemented in `src/data_pipeline/corruption_handler.py`.
  * Uses logging mechanisms to track errors.
* Remote exporter: Exports data to remote storage.  
  * Implemented in `src/data_pipeline/exporter.py`.
  * Uses local file storage to emulate the functionality.

## API Module
* API: Provides read access to the data.  
  * Implemented in `api.py`.
  * Built using FastAPI framework.
  * Exposes endpoints for data retrieval together with simple health check endpoint.
  * OpenAPI documentation available at `/docs`.
  * Swagger UI available at `/redoc`.
* API Gateway: Provides access to the API itself.  
  * Configured using Kong API Gateway.
  * Helm chart in infrastructure directory sets up Kong.
* AutH: Allows authentication on API level via API Key.  
  * Uses Kong plugins for rate limiting and key authentication.
  * Configured in `api-ingress.yaml` with KongPlugin and KongConsumer.

# Move to Production - considerations
* Scalability
  * Utilize scalable services and distributed processing frameworks between Ingestion and Processing to handle changes in datasets (e.g., Apache Kafka, Spark).
  * Make Processing module scalable (parallelization).
  * Externalize LLM model to a separate service (preferable with dedicated GPU) or use external API like OpenAI.
* Reliability 
  * Improve quality of codebase (proper error handling, readability, etc.)
  * Implement retry mechanisms in the Data Ingestion Module.
  * Use monitoring tools to track system health and performance (APM).
  * Integrate logging at each stage for debugging and auditing purposes.
  * Set up alerts for failures or performance bottlenecks.
* Data Integrity
  * Manual/automated process for manage corrupted data.
  * Regularly backup the database and have disaster recovery plans in place.
* Security
  * Implementation AutH backend for API access and user management. 
  * Proper API Key management.
  * Ensure data encryption at rest and transit.
  * Implementation of Secret Management for sensitive data.
  * Regularly update authentication protocols and monitor for unauthorized access.
  * Automated and regular scanning of source code and all container for vulnerabilities.
* CI/CD
  * Implement tests for each module.
  * Implement CI/CD pipelines for automated deployment, testing and security scanning.

# Development
[src/README.md](src/README.md)

# Deployment
[infrastructure/README.md](infrastructure/README.md)
