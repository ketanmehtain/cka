#!/usr/bin/env bash

apt-get update && apt-get install apt-transport-https ca-certificates curl software-properties-common
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
echo "deb  http://apt.kubernetes.io/  kubernetes-xenial  main" > /etc/apt/sources.list.d/kubernetes.list
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
add-apt-repository \
  "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) \
  stable"
apt-get update
apt-get install -y avahi-daemon libnss-mdns traceroute htop httpie bash-completion docker-ce=5:19.03.14~3-0~ubuntu-bionic kubeadm=1.22.0-00 kubelet=1.22.0-00 kubectl=1.22.0-00
cat > /etc/docker/daemon.json <<EOF
{
  "exec-opts": ["native.cgroupdriver=systemd"],
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "100m"
  },
  "storage-driver": "overlay2"
}
EOF

mkdir -p /etc/systemd/system/docker.service.d

systemctl daemon-reload
systemctl restart docker

ip=$(/sbin/ifconfig enp0s8|grep -E 'inet[^0-9]'|awk '{print $2}')
sudo sed -i "s/^ExecStart=$/Environment=\"KUBELET_EXTRA_ARGS=--node-ip=$ip\"\nExecStart=/" /etc/systemd/system/kubelet.service.d/10-kubeadm.conf
