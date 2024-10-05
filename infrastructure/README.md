# Deployment

## Dependency
* K8s (tested on Docker Desktop on macOS) with `kubectl` configured
* `helm` package manager

## Development Environment Setup
* `docker build -t poc:latest .` to build the Processor image
* `docker build -t api:latest -f Dockerfile-API .` to build the API image
* `cd ./infrastructure`
* `kong.sh` to install Kubernetes Gateway API and configure Gateway with Kong
* `helm dependency build`
* `helm install poc .`