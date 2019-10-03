import shlex
from collections import OrderedDict

from .utils import TemporaryConfigFiles


def helm_install_steps(config, lego_config, nginx_config, jupyterhub_config):

    # Helm initial installation of services
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

    kube_lego_install = f"""
    helm upgrade --install kube-lego stable/kube-lego \
    --namespace ingress \
    --version=0.4.2 \
    --values {lego_config}
    """
    helm_install["kube_lego_install"] = shlex.split(kube_lego_install)

    nginx_ingress_install = f"""
    helm upgrade --install nginx-ingress stable/nginx-ingress \
    --namespace ingress \
    --version=1.6.17 \
    --values {nginx_config}
    """
    helm_install["nginx_ingress_install"] = shlex.split(nginx_ingress_install)

    jupyterhub_install = f"""
    helm upgrade --install jupyterhub jupyterhub/jupyterhub \
    --namespace jupyterhub  \
    --version=0.8.2 \
    --values {jupyterhub_config}
    """
    helm_install["jupyterhub_install"] = shlex.split(jupyterhub_install)

    return helm_install.items()


def setup_jupyterhub(config, env):
    lego_config = env.get_template("kube-lego.yaml").render(config)
    nginx_config = env.get_template("nginx-ingress.yaml").render(config)
    jupyterhub_config = env.get_template("jupyterhub.yaml").render(config)
    with TemporaryConfigFiles(n_files=3) as (
        lego_config_file,
        nginx_config_file,
        jupyterhub_config_file,
    ):
        lego_config_file.write(lego_config)
        lego_config_file.seek(0)
        nginx_config_file.write(nginx_config)
        nginx_config_file.seek(0)
        jupyterhub_config_file.write(jupyterhub_config)
        jupyterhub_config_file.seek(0)
        for name, cmd in helm_install_steps(
            config,
            lego_config_file.name,
            nginx_config_file.name,
            jupyterhub_config_file.name,
        ):
            # TODO: Run subprocess.run(cmd) here...
