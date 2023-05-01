from openshift.dynamic import DynamicClient, exceptions
from kubernetes import client
from openshift.helper.userpassauth import OCPLoginConfiguration

cloudlet_name = "ocp410-dev"
cloudlet_fqdn = f"{cloudlet_name}.cloudlet-dev.com"
apihost = f'https://api.{cloudlet_fqdn}:6443'
username = 'admin'
password = 'redhat'

kubeConfig = OCPLoginConfiguration(ocp_username=username, ocp_password=password)
kubeConfig.host = apihost
kubeConfig.verify_ssl = False

# Retrieve the auth token
kubeConfig.get_token()

print('Auth token: {0}'.format(kubeConfig.api_key))
print('Token expires: {0}'.format(kubeConfig.api_key_expires))

k8s_client = client.ApiClient(kubeConfig)
dyn_client = DynamicClient(k8s_client)




# Change the Console URL to console from console-openshift-console
ingress_group = dyn_client.resources.get(
    api_version="config.openshift.io/v1",
    kind="Ingress"
)

ingress_patch_body = {
    "spec": {
        "componentRoutes": [
            {
                "hostname": "console.apps.ocp410-dev.cloudlet-dev.com",
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


# Change the Tab title RHOCP to cloudlet name
consoles_group = dyn_client.resources.get(
    api_version="operator.openshift.io/v1",
    kind="Console",
)

console_patch_body = {
    "spec": {
        "customization": {
            "customLogoFile": {
                "key": "cloudleton-resized.png",
                "name": "ocp-logo-test"
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
