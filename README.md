# Azure ML Local Deployment

This repository provides example code for a YouTube video on local deployment to Azure Machine Learning. You can see all of the Azure ML videos I've created using [this YouTube playlist](https://www.youtube.com/playlist?list=PLeWL8zChJ2uuGs-8nvxMdo26XkYGWt7ui). The video for this repository is entitled [Troubleshooting Azure ML deployments locally](https://youtu.be/bue85m7lbjQ).

## The Model and Data

This data I used to train the accompanying model comes from the [Chicago Parking Ticket database, courtesy of Daniel Hutmacher](https://sqlsunday.com/2022/12/05/new-demo-database/).  I sampled 1,000,000 records from it and [the file I used is available in CSV format](https://cspolybasepublic.blob.core.windows.net/cstrainingpublicdata/ChicagoParkingTickets.txt).

You can see how I trained the model in my [Getting Beyond the Basics with Azure Machine Learning repository](https://github.com/feaselkl/Beyond-the-Basics-with-AzureML).

## Running the Code

Because this is intended as a learning experience, I purposefully included several ways for this script to fail, so you can see what sorts of error messages and problems you are likely to experience during development.

### Requirements

This repo assumes you have the following already installed on your machine:

* Python (preferably the [Anaconda distribution](https://www.anaconda.com/download#downloads)), with `pip` installed:  `conda install -c anaconda pip`
* [The Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli)
* The Azure ML Azure CLI extension:  `az extension add -n ml`
* Pip packages:  `pip install azure-ai-ml`, `pip install azure-identity`
* [Docker Desktop](https://www.docker.com/products/docker-desktop/) or some other Docker container service
* [Visual Studio Code](https://code.visualstudio.com/download)

Before you run the code, make sure your console has you logged into Azure via CLI:

```cmd
az login
```

Note that you must be logged into `az cli` with an account which has access to the subscription, resource group, and workspace.

### Deployment Code Notes

In `deployment.py`, you will need to fill in your subscription ID, resource group name, and workspace name on lines 11-13. This is **not** a recommended practices for deployment scripts you would check into source control, but will work fine for a local demonstration.

Other than lines 11-13, the deployment code should be runnable as-is. The endpoint and deployment operations are also idempotent, meaning that you should be able to re-run the commands without getting an error, regardless of whether you already have the endpoint and deployment set up on your machine or not.

## Failure Modes

There are four major failure modes we cover in this repository:

1. You cannot use curated Azure ML environments for a local deployment. You can only use a Docker container image to which you have direct access (either because it is publicly available or because you have built the container image and hosted it in a repository to which you have access).
2. Local deployments may not access the Azure ML model registry. You must use a model file.
3. Your scoring script must include `init()` and `run()` endpoints.
4. The `init()` and `run()` endpoints must behave correctly.

The `score_model_local.py` file represents a valid working example of a scoring script for an Azure ML managed online endpoint. Note that it has decorators from [the InferenceSchema library](https://github.com/Azure/InferenceSchema) because I used this example in a demonstration video connecting Power BI to Azure Machine Learning.

The `score_model_remote.py` file represents what a scoring script would look like for a **remote** deployment. This script will not work for local deployments.