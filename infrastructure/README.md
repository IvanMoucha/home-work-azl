# Deployment
## Dependency
* K8s (tested on Docker Desktop on macOS)
* `helm` package manager
## Development Environment Setup
* `docker build -t poc:latest .`
* `cd ./infrastructure`
* `helm dependency update`
* `helm install poc .`