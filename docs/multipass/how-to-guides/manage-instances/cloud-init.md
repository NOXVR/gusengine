<!-- Source: https://documentation.ubuntu.com/multipass/stable/how-to-guides/manage-instances/launch-customized-instances-with-multipass-and-cloud-init/ -->
# Launch customized instances with Multipass and cloud-init

# Launch customized instances with Multipass and cloud-init[¶](#launch-customized-instances-with-multipass-and-cloud-init)

You can set up instances with a customized environment or configuration using the launch command along with a custom cloud-init YAML file and an optional post-launch health check to ensure everything is working correctly.

Below are some common examples of using `cloud-init` with Multipass to create customized instances. The `cloud-init` file is provided by the Multipass team, but users are free to create and use their own personal `cloud-init` configurations.

## 📦 anbox-cloud-appliance[¶](#anbox-cloud-appliance)

Launch with:

multipass launch \
  --name anbox-cloud-appliance \
  --cpus 4 \
  --memory 4G \
  --disk 50G \
  --timeout 900 \
  --cloud-init https://raw.githubusercontent.com/canonical/multipass/refs/heads/main/data/cloud-init-yaml/cloud-init-anbox.yaml

## ⚙️ charm-dev[¶](#charm-dev)

Launch with:

multipass launch 24.04 \
  --name charm-dev \
  --cpus 2 \
  --memory 4G \
  --disk 50G \
  --timeout 1800 \
  --cloud-init https://raw.githubusercontent.com/canonical/multipass/refs/heads/main/data/cloud-init-yaml/cloud-init-charm-dev.yaml

Health check:

multipass exec charm-dev -- bash -c "
 set -e
 charmcraft version
 mkdir -p hello-world
 cd hello-world
 charmcraft init
 charmcraft pack
"

## 🐳 docker[¶](#docker)

Launch with:

multipass launch 24.04 \
  --name docker \
  --cpus 2 \
  --memory 4G \
  --disk 40G \
  --cloud-init https://raw.githubusercontent.com/canonical/multipass/refs/heads/main/data/cloud-init-yaml/cloud-init-docker.yaml

Health check:

multipass exec docker -- bash -c "docker run hello-world"

You can also optionally add aliases:

multipass prefer docker
multipass alias docker:docker docker
multipass alias docker:docker-compose docker-compose
multipass prefer default
multipass aliases

See also: [`How to use command aliases`](../use-instance-command-aliases/)

## 🎞️ jellyfin[¶](#jellyfin)

Launch with:

multipass launch 22.04 \
  --name jellyfin \
  --cpus 2 \
  --memory 4G \
  --disk 40G \
  --cloud-init https://raw.githubusercontent.com/canonical/multipass/refs/heads/main/data/cloud-init-yaml/cloud-init-jellyfin.yaml

## ☸️ minikube[¶](#minikube)

Launch with:

multipass launch \
  --name minikube \
  --cpus 2 \
  --memory 4G \
  --disk 40G \
  --timeout 1800 \
  --cloud-init https://raw.githubusercontent.com/canonical/multipass/refs/heads/main/data/cloud-init-yaml/cloud-init-minikube.yaml

Health check:

multipass exec minikube -- bash -c "set -e
  minikube status
  kubectl cluster-info"

## 🤖 ros2-humble[¶](#ros2-humble)

Launch with:

multipass launch 22.04 \
  --name ros2-humble \
  --cpus 2 \
  --memory 4G \
  --disk 40G \
  --timeout 1800 \
  --cloud-init https://raw.githubusercontent.com/canonical/multipass/refs/heads/main/data/cloud-init-yaml/cloud-init-ros2-humble.yaml

Heath check:

multipass exec ros2-humble -- bash -c "
  set -e

  colcon --help
  rosdep --version
  ls /etc/ros/rosdep/sources.list.d/20-default.list
  ls /home/ubuntu/.ros/rosdep/sources.cache

  ls /opt/ros/humble
"

## 🤖 ros2-jazzy[¶](#ros2-jazzy)

Launch with:

multipass launch 24.04 \
  --name ros2-jazzy \
  --cpus 2 \
  --memory 4G \
  --disk 40G \
  --timeout 1800 \
  --cloud-init https://raw.githubusercontent.com/canonical/multipass/refs/heads/main/data/cloud-init-yaml/cloud-init-ros2-jazzy.yaml

Health check:

multipass exec ros2-jazzy -- bash -c "
  set -e

  colcon --help
  rosdep --version
  ls /etc/ros/rosdep/sources.list.d/20-default.list
  ls /home/ubuntu/.ros/rosdep/sources.cache

  ls /opt/ros/jazzy
"