# yaml2jupyterhub

*This package is still under active development. Do not use it.*

`yaml2jupyterhub` deploys a JupyterHub equipped with a Dask cluster on a given cloud provider based on a user-provided configuration file.


## Usage

Create a cluster using the `yaml2jupyterhub create` command:

```console
yaml2jupyterhub create --file my_cluster_config.yaml
```

Delete a cluster using the `yaml2jupyterhub delete` command:

```console
yaml2jupyterhub delete --file my_cluster_config.yaml
```


## Configuration

There are several configuration options related to the cluster that is started. The possible options, along with their default values, are shown below:

```yaml
cloudprovider: aws
name: yaml2jupyterhub-cluster
region: us-east-2
general-pool:
  instance-types: m5.large
user-pool:
  instance-types: m5.large
  min-size: 0
  max-sze: 10
cpu-pool:
  instance-types: m5.large
  min-size: 0
  max-sze: 10
helm-startup-wait: 15
```


## License

[MIT License](LICENSE)