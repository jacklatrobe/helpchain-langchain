# Build the image
docker build -t langchain-service .

# Tag the image
docker tag langchain-service registry.digitalocean.com/helpchain/langchain-service

# Push the image
docker push registry.digitalocean.com/helpchain/langchain-service


## Example output:
