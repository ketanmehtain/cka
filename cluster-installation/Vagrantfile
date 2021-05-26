BOX_IMAGE = "ubuntu/bionic64"
WORKER_COUNT = 2

Vagrant.configure("2") do |config|
  config.vm.box = BOX_IMAGE

  config.vm.define "master" do |node|
    node.vm.hostname = "master"
    node.vm.network :private_network, ip: "10.8.8.10"
    node.vm.provider :virtualbox do |vb|
      vb.name = "master"
      vb.memory = 2048
      vb.cpus = 2
    end
    node.vm.provision "shell", path: "common.sh"
  end
  
  (1..WORKER_COUNT).each do |i|
    config.vm.define "worker-#{i}" do |node|
      node.vm.hostname = "worker-#{i}"
      node.vm.network :private_network, ip: "10.8.8.#{i + 20}"
      node.vm.provider :virtualbox do |vb|
        vb.name = "worker-#{i}"
        vb.memory = 1024
        vb.cpus = 2
      end
      node.vm.provision "shell", path: "common.sh"
    end
  end

  config.vm.provision "shell",
    run: "always",
    inline: "swapoff -a"
end

