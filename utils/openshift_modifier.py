from openshift.dynamic import DynamicClient, exceptions
from kubernetes import client
from kubernetes.client.rest import ApiException
from openshift.helper.userpassauth import OCPLoginConfiguration
import base64


username = 'admin'
password = 'redhat'


def login_to_cloudlet(apihost):
    kubeConfig = OCPLoginConfiguration(ocp_username=username, ocp_password=password)
    kubeConfig.host = apihost
    kubeConfig.verify_ssl = False

    # Retrieve the auth token
    kubeConfig.get_token()

    k8s_client = client.ApiClient(kubeConfig)
    dyn_client = DynamicClient(k8s_client)
    return dyn_client


def modify_console_url(dyn_client, cloudlet_fqdn):
    # Change the Console URL to console from console-openshift-console
    ingress_group = dyn_client.resources.get(
        api_version="config.openshift.io/v1",
        kind="Ingress"
    )

    ingress_patch_body = {
        "spec": {
            "componentRoutes": [
                {
                    "hostname": f"console.apps.{cloudlet_fqdn}",
                    "name": "console",
                    "namespace": "openshift-console"
                }
            ]
        }
    }


    ingress_group.patch(
        body=ingress_patch_body,
        name="cluster",
        content_type="application/merge-patch+json")


def modify_tab_title(dyn_client, cloudlet_name):
    # Change the Tab title RHOCP to cloudlet name
    consoles_group = dyn_client.resources.get(
        api_version="operator.openshift.io/v1",
        kind="Console",
    )

    console_patch_body = {
        "spec": {
            "customization": {
                "customLogoFile": {
                    "key": "cloudleton.png",
                    "name": "cloudlet-logo"
                },
                "customProductName": f"{cloudlet_name}"
            }
        }
    }

    # patch the consoles.operator.openshift.io object
    consoles_group.patch(
        name="cluster",
        body=console_patch_body,
        content_type="application/merge-patch+json",
    )


def create_configmap(dyn_client, cloudlet_name):
    # Read the image file in binary mode and encode it as Base64
    with open(f"outputs/{cloudlet_name}.png", "rb") as f:
        image_data = base64.b64encode(f.read()).decode('utf-8')


    # define the JSON patch body
    cm_patch_body = {
        "apiVersion": "v1",
        "kind": "ConfigMap",
        "metadata": {
            "name": "cloudlet-logo",
            "namespace": "openshift-config"
        },
        "binaryData": {
            "cloudleton.png": image_data
        }
    }

    # create the ConfigMap in OpenShift
    configmaps_group = dyn_client.resources.get(
        api_version="v1",
        kind="ConfigMap",
    )

    try:
        configmaps_group.get(name="cloudlet-logo", namespace="openshift-config")
        print("ConfigMap 'cloudlet-logo' already exists, skipping creation...")
    except ApiException as e:
        if e.status == 404:
            # if the ConfigMap doesn't exist, create it
            configmaps_group.create(body=cm_patch_body)
            print("ConfigMap 'cloudlet-logo' created successfully.")
        else:
            raise e


def create_modified_openshift(cloudlet_name):
    cloudlet_fqdn = f"{cloudlet_name}.cloudlet-dev.com"
    apihost = f'https://api.{cloudlet_fqdn}:6443'
    dyn_client = login_to_cloudlet(apihost)
    create_configmap(dyn_client, cloudlet_name)
    modify_console_url(dyn_client, cloudlet_fqdn)
    modify_tab_title(dyn_client, cloudlet_name)

