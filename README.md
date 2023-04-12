# helpchain-langchain
helpchain-langchain - The langchain component of the HelpChain chatbot platform by LCG

HelpChain LangChain is a containerised backend microservice for LangChain that is hosted on Kubernetes. It is designed to provide advanced language processing capabilities, including data-awareness and agentic interaction, to your applications.

## Getting Started
See the file in .github/workflows/ for an example of how to automate the deployment.
~~~
docker build .
docker push
kubectl apply -f config/deployment.yml
~~~

### Prerequisites
- Docker, for building images
- Kubernetes, for hosting deployed images
- Kubectl, for managing clusters and deployments
- GitHub Actions, if you want to automate the above

### Installation

1. Clone the repository
2. Edit the code
3. Push back to github
4. Actions take care of the rest

## Further reading
 - https://docs.digitalocean.com/tutorials/build-deploy-first-image/
 - https://docs.digitalocean.com/products/kubernetes/how-to/deploy-using-github-actions/