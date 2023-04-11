## Based ofF:
## https://docs.digitalocean.com/tutorials/build-deploy-first-image/
## NOTE: This has now been automated with GitHub actions

# Build the image
docker build -t langchain-service .

# Tag the image
docker tag langchain-service registry.digitalocean.com/helpchain/langchain-service

# Push the image
docker push registry.digitalocean.com/helpchain/langchain-service

# Load kubeconfig from cluster to kubectl
doctl kubernetes cluster kubeconfig save helpchain

# Create secrets in the kube for the docker registry
doctl registry kubernetes-manifest | kubectl apply -f -

# Patch the service account to use these secrets
kubectl patch serviceaccount default -p '{"imagePullSecrets": [{"name": "registry-helpchain"}]}'

# Deploy the langchain-service to the kube cluster
kubectl create deployment langchain-service --image=registry.digitalocean.com/helpchain/langchain-service

# Expose the app through a kube load balancer
kubectl expose deployment langchain-service --type=LoadBalancer --port=80 --target-port=80

# Get the IP of the load balancer to connect to the app - if it doesn't appear first time, you can re-run the command soon
doctl compute load-balancer list --format Name,Created,IP,Status
echo "If that didn't work yet, wait 30 seconds and run the command again:"
echo "doctl compute load-balancer list --format Name,Created,IP,Status"