# Architecture description
The actual achitecture description can be found here: ![Architecture overview](docs/architecture.md)

# Installation steps
01. `kubectl apply -f deployment/db-configmap.yaml` - Set up environment variables for the pods
02. `kubectl apply -f deployment/db-secret.yaml` - Set up secrets for the pods
03. `kubectl apply -f deployment/postgres.yaml` - Set up a Postgres database running PostGIS
04. `kubectl apply -f deployment/uda-person.yaml` - Set up the service and deployment for the Person Microsrvice
05. `kubectl apply -f deployment/uda-connection.yaml` - Set up the service and deployment for the Connectioni Microsrvice
06. `kubectl apply -f deployment/udaconnect-app.yaml` - Set up the service and deployment for the web app
07. `sh scripts/run_db_command.sh <POD_NAME>` - Seed your database against the `postgres` pod. (`kubectl get pods` will give you the `POD_NAME`)
08. `kubectl apply -f deployment/kafka-deployment.yaml` - Set up the deployment for Kafka
09. `kubectl apply -f deployment/kafk-service.yaml` - Set up the service for Kafka
10. `kubectl apply -f deployment/kafk-topic-job.yaml` - Set up the queue inside Kafka



### Verifying it Works
Once the project is up and running, you should be able to see 3 deployments and 3 services in Kubernetes:
`kubectl get pods` and `kubectl get services` - should both return `udaconnect-app`, `udaconnect-person`, and `postgres`


These pages should also load on your web browser:
* `http://localhost:30010/` - OpenAPI Documentation for Person Endpoint
* `http://localhost:30020/` - OpenAPI Documentation for command pattern implementation rest endpoint
* `http://localhost:30000/` - Frontend ReactJS Application




docker build -t usuelter/udac-connection:latest --push .
docker build -t usuelter/udac-person:latest --push .