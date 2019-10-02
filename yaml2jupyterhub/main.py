import os
import tempfile
import yaml

import click
from jinja2 import Environment, FileSystemLoader

from .k8s_setup_aws import k8s_setup_aws_steps
from .helm_setup import helm_setup_steps
from .helm_install import helm_install_steps

here = os.path.abspath(os.path.dirname(__file__))

templates_dir = os.path.join(here, "templates")
env = Environment(loader=FileSystemLoader(templates_dir))

default_config_file = os.path.join(here, "yaml2jupyterhub.yaml")


def flatten(d, parent_key=""):
    items = []
    for k, v in d.items():
        new_key = parent_key + "-" + k if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten(v, new_key).items())
        else:
            items.append((new_key, v))
    return dict(items)


def load_config(path):
    """ Load configuration file """

    if not os.path.exists(path):
        raise ValueError(f"Could not find configuration file {path}")

    with open(path, "r") as f:
        config = yaml.safe_load(f)
    config = flatten(config)

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
    help="Cluster configuration file",
)
def create(config_file):
    # Get user configuration values
    config = load_config(default_config_file)
    # Overwrite defaults with user-provided values
    if os.path.abspath(config_file) != default_config_file:
        config.update(load_config(config_file))
    # Ensure that all config values are strings
    config = {key: str(value) for key, value in config.items()}

    # Setup Kubernetes cluster
    k8s_template = env.get_template("k8s-cluster-aws.yaml")
    k8s_config = k8s_template.render(config)
    # Create temporary cluster configuration yaml file for eksctl
    with tempfile.NamedTemporaryFile(suffix=".yaml", mode="w") as tmpfile:
        tmpfile.write(k8s_config)
        print("Kubernetes setup commands:")
        for name, cmd in k8s_setup_aws_steps(config, cluster_config=tmpfile.name):
            print(f"\t{cmd}")
            # TODO: Run subprocess.run(cmd) here...

    # Setup Helm
    print("Helm setup commands:")
    for name, cmd in helm_setup_steps(config):
        print(f"\t{cmd}")
        # TODO: Run subprocess.run(cmd) here...

    # Install JupyterHub
    # TODO: handle relevant configuration options
    print("Helm installation commands:")
    for name, cmd in helm_install_steps(config):
        print(f"\t{cmd}")
        # TODO: Run subprocess.run(cmd) here...


@main.command(short_help="Delete cluster")
@click.option("-n", "--name", help="Name of cluster")
@click.option(
    "-f",
    "--file",
    "config_file",
    default=default_config_file,
    show_default=True,
    help="Cluster configuration file",
)
def delete(name, config_file):
    print("Not currently implemented...")
