import shlex
from collections import OrderedDict


def k8s_setup_aws_steps(config, cluster_config):

    k8s_setup = OrderedDict()

    # 1. Create cluster from yaml definition
    create_cluster = f"eksctl create cluster -f {cluster_config}"
    k8s_setup["create_cluster"] = shlex.split(create_cluster)

    # 2. List available node groups and cluster setup
    list_node_groups = f"eksctl get nodegroups --cluster {config['name']}"
    k8s_setup["list_node_groups"] = shlex.split(list_node_groups)

    return k8s_setup.items()
