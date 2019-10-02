import shlex
from collections import OrderedDict


def helm_install_steps(config):

    # Helm initial installation of services
    # helm configuration in `helm-config/<service-name>.yaml`
    helm_install = OrderedDict()

    add_incubator = """
    helm repo add incubator http://storage.googleapis.com/kubernetes-charts-incubator
    """
    helm_install["add_incubator"] = shlex.split(add_incubator)

    add_jupyterhub = """
    helm repo add jupyterhub https://jupyterhub.github.io/helm-chart/
    """
    helm_install["add_jupyterhub"] = shlex.split(add_jupyterhub)

    helm_update = "helm repo update"
    helm_install["helm_update"] = shlex.split(helm_update)

    kube_lego_install = """
    helm upgrade --install kube-lego stable/kube-lego \
    --namespace ingress \
    --version=0.4.2 \
    --values helm-config/kube-lego.yaml
    """
    helm_install["kube_lego_install"] = shlex.split(kube_lego_install)

    nginx_ingress_install = """
    helm upgrade --install nginx-ingress stable/nginx-ingress \
    --namespace ingress \
    --version=1.6.17 \
    --values helm-config/nginx-ingress.yaml
    """
    helm_install["nginx_ingress_install"] = shlex.split(nginx_ingress_install)

    jupyterhub_install = """
    helm upgrade --install jupyterhub jupyterhub/jupyterhub \
    --namespace jupyterhub  \
    --version=0.8.2 \
    --values helm-config/jupyterhub.yaml
    """
    helm_install["jupyterhub_install"] = shlex.split(jupyterhub_install)

    return helm_install.items()
