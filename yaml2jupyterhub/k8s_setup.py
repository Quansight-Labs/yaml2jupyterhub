import subprocess
import shlex
from collections import OrderedDict

from .utils import TemporaryConfigFiles


def k8s_setup_aws_steps(config, cluster_config):

    k8s_setup = OrderedDict()

    # 1. Create cluster from yaml definition
    create_cluster = f"eksctl create cluster -f {cluster_config}"
    k8s_setup["create_cluster"] = shlex.split(create_cluster)

    # 2. List available node groups and cluster setup
    list_node_groups = f"eksctl get nodegroups --cluster {config['name']}"
    k8s_setup["list_node_groups"] = shlex.split(list_node_groups)

    return k8s_setup.items()


def setup_k8s(config, env):
    k8s_config = env.get_template("k8s-cluster-aws.yaml").render(config)
    with TemporaryConfigFiles() as tmpfile:
        tmpfile.write(k8s_config)
        tmpfile.seek(0)
        for name, cmd in k8s_setup_aws_steps(config, cluster_config=tmpfile.name):
            proc = subprocess.run(cmd)
            if proc.returncode != 0:
                raise ValueError(
                    f"The following command returned an exit code of {proc.returncode}:\n\n{cmd}"
                )
