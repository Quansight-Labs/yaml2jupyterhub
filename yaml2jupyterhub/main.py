import os
import shlex
import subprocess

import click
import yaml
from jinja2 import Environment, FileSystemLoader

from .utils import flatten
from .k8s_setup import setup_k8s
from .helm_setup import setup_helm
from .jupyterhub_setup import setup_jupyterhub

here = os.path.abspath(os.path.dirname(__file__))

templates_dir = os.path.join(here, "templates")
env = Environment(loader=FileSystemLoader(templates_dir))

default_config_file = os.path.join(here, "yaml2jupyterhub.yaml")


def _load_single_config(path):

    if not os.path.exists(path):
        raise ValueError(f"Could not find configuration file {path}")

    with open(path, "r") as f:
        config = yaml.safe_load(f)
    config = flatten(config)

    config = {key: value for key, value in config.items() if value is not None}
    # Ensure that config values are strings
    config = {
        key: list(map(str, value)) if isinstance(value, list) else str(value)
        for key, value in config.items()
    }

    return config


def load_config(path, default=default_config_file):
    """ Load configuration file """

    config = _load_single_config(default)

    # Overwrite defaults with user-provided values
    if os.path.abspath(path) != os.path.abspath(default):
        config.update(_load_single_config(path))

    return config


@click.group()
def main():
    """ yaml2jupyterhub command line interface """
    pass


@main.command(short_help="Create cluster")
@click.option(
    "-f",
    "--file",
    "config_file",
    default=default_config_file,
    show_default=True,
    help="Cluster configuration file.",
)
def create(config_file):
    config = load_config(config_file)

    # Setup Kubernetes cluster
    setup_k8s(config, env)

    # Setup Helm
    setup_helm(config, env)

    # Install JupyterHub
    setup_jupyterhub(config, env)


@main.command(short_help="Delete cluster")
@click.option(
    "-f",
    "--file",
    "config_file",
    default=default_config_file,
    show_default=True,
    help="Cluster configuration file",
)
def delete(name, config_file):
    config = load_config(config_file)

    delete = f"eksctl delete cluster --name {config['name']} --region {config['region']} --wait"
    delete_cmd = shlex.split(delete)
    subprocess.run(delete_cmd)
