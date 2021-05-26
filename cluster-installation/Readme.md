# Kubernetes Cluster on Mac

The instructions below describe how to creates the Kubernetes cluster on Mac.

## Initializing the Master Node

Ssh into the master node with `vagrant ssh master`, run the below command as root.
This initializes the control-plane node. 

```
# kubeadm init --pod-network-cidr 172.18.0.0/16 --apiserver-advertise-address 10.8.8.10
```

Run the below command as a non-root user:

```
$ mkdir -p $HOME/.kube
$ sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
$ sudo chown $(id -u):$(id -g) $HOME/.kube/config
```

I'm using Pod network as Calico here. The below command applies the manifest for Calico.

```
$ kubectl apply -f https://docs.projectcalico.org/v3.14/manifests/calico.yaml
```

## Joining the Worker Nodes

Ssh into the worker node with `vagrant ssh worker-1` & `vagrant ssh worker-1`, 
run the below command as root to join worker nodes to the kubernetes master.

```
kubeadm join 10.8.8.10:6443 --token <token>  --discovery-token-ca-cert-hash sha256:<hash>
```




## Verifying the Installation

To verify the installation was successful, run the below command on your master node.

```
$ kubectl get nodes -o wide
NAME       STATUS   ROLES    AGE     VERSION   INTERNAL-IP   EXTERNAL-IP   OS-IMAGE             KERNEL-VERSION       CONTAINER-RUNTIME
master     Ready    master   13m     v1.18.0   10.8.8.10     <none>        Ubuntu 18.04.5 LTS   4.15.0-142-generic   docker://19.3.14
worker-1   Ready    <none>   9m2s    v1.18.0   10.8.8.21     <none>        Ubuntu 18.04.5 LTS   4.15.0-142-generic   docker://19.3.14
worker-2   Ready    <none>   4m59s   v1.18.0   10.8.8.22     <none>        Ubuntu 18.04.5 LTS   4.15.0-142-generic   docker://19.3.14
```

Try creating a nginx pod 

```
$ kubectl run nginx --image=nginx
pod/nginx created
$ kubectl get pods
NAME    READY   STATUS    RESTARTS   AGE
nginx   1/1     Running   0          9s
```
