import shlex
from collections import OrderedDict


def helm_setup_steps(config):

    helm_setup = OrderedDict()

    # 1. Create service account for helm
    helm_service_account = """
    kubectl --namespace kube-system \
            create serviceaccount tiller
    """
    helm_setup["helm_service_account"] = shlex.split(helm_service_account)

    # 2. Give helm full permissions to manage cluster
    helm_permissions = """
    kubectl create clusterrolebinding tiller \
            --clusterrole cluster-admin \
            --serviceaccount=kube-system:tiller
    """
    helm_setup["helm_permissions"] = shlex.split(helm_permissions)

    # 3. Initialize helm on the server
    helm_initialize = "helm init --service-account tiller --wait"
    helm_setup["helm_initialize"] = shlex.split(helm_initialize)

    # 4. Secure tiller
    secure_tiller = """
    kubectl patch deployment tiller-deploy \
            --namespace=kube-system \
            --type=json \
            --patch='[{"op": "add", "path": "/spec/template/spec/containers/0/command", "value": ["/tiller", "--listen=localhost:44134"]}]'
    """
    helm_setup["secure_tiller"] = shlex.split(secure_tiller)

    # 5. Wait for tiller to start
    helm_setup["wait_tiller_online"] = ["sleep", config["helm_startup_wait"]]

    return helm_setup.items()


def setup_helm(config, env):
    for name, cmd in helm_setup_steps(config):
        # TODO: Run subprocess.run(cmd) here...
