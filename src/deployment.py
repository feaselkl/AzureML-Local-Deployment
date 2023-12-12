from azure.ai.ml import MLClient
from azure.ai.ml.entities import (
    ManagedOnlineEndpoint,
    ManagedOnlineDeployment,
    Model,
    Environment,
    CodeConfiguration,
)
from azure.identity import AzureCliCredential

subscription_id = "{your subscription id}"
resource_group = "{your resource group}"
workspace = "{your workspace}"

# Lines 11-13 are here for demo purposes.
# For a production-quality script, you would want to create a
# .azureml folder with a config.json file. This file would
# contain subscription ID, resource group, and workspace name.

ml_client = MLClient(
    AzureCliCredential(), subscription_id, resource_group, workspace
)

# Define an endpoint name
endpoint_name = "web-svc-local-test"
# create an online endpoint
endpoint = ManagedOnlineEndpoint(
    name = endpoint_name, 
    description="Test a local endpoint",
    auth_mode="key"
)
ml_client.online_endpoints.begin_create_or_update(endpoint, local=True)

model=Model(path="trained_models/model.pkl")

# Failure mode 1: cannot use a remote AML environment
#env=ml_client.environments.get(name="AzureML-sklearn-1.0-ubuntu20.04-py38-cpu", version="33")
env = Environment(
    conda_file="conda.yaml",
    image="mcr.microsoft.com/azureml/openmpi4.1.0-ubuntu20.04:latest",
)

test_deployment = ManagedOnlineDeployment(
    name="websvclocalvideo",
    endpoint_name=endpoint_name,
    model=model,
    environment=env,
    code_configuration=CodeConfiguration(
        #code=".", scoring_script="failure_2_score_remote_model.py"
        #code=".", scoring_script="failure_3_score_invalid_script.py"
        #code=".", scoring_script="failure_4_score_script_error.py"
        code=".", scoring_script="score_model_local.py"
    ),
    instance_type="Standard_DS3_v2",
    instance_count=1,
)
ml_client.online_deployments.begin_create_or_update(test_deployment, local=True)
