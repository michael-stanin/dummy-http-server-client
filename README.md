# Build instructions

## Server:
docker image build -t python-http-server ./server/

## Client:
docker image build -t python-http-client ./client/


# Run instructions

## Server:
cd server
docker run --rm -it --name python-http-server -p 8080:8080 python-http-server


## Client:
cd client
docker run python-http-client


# Run both server and client docker images

## Build
docker-compose build

## Startup
docker-compose up

## Shutdown
docker-compose down

# Run both server and client in k8s environment (minikube)
Set the imagePullPolicy to Never in both deployments to actually use local docker images

minikube start

eval $(minikube docker-env)

docker image build -t python-http-server ./server/

docker image build -t python-http-client ./client/

kubectl apply -f ./client/client-deployment.yaml

kubectl apply -f ./server/server-deployment.yaml

If you want a networking pod:
https://docs.microsoft.com/en-us/troubleshoot/azure/azure-kubernetes/connection-issues-application-hosted-aks-cluster#access-the-clusterip-service
