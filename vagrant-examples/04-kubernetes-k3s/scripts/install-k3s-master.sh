#!/bin/bash

echo "=========================================="
echo "k3s 마스터 노드 설치 시작"
echo "=========================================="

# 시스템 업데이트
export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get upgrade -y

# k3s 마스터 설치
echo "k3s 설치 중..."
curl -sfL https://get.k3s.io | sh -s - \
  --write-kubeconfig-mode 644 \
  --node-ip 192.168.50.11 \
  --flannel-iface eth1

# k3s 시작 대기
echo "k3s 시작 대기 중..."
sleep 20

# 토큰 저장 (워커 노드가 접근할 수 있도록)
sudo cat /var/lib/rancher/k3s/server/node-token > /vagrant/node-token
echo "192.168.50.11" > /vagrant/master-ip

# kubeconfig를 vagrant 사용자 홈에 복사
mkdir -p /home/vagrant/.kube
sudo cp /etc/rancher/k3s/k3s.yaml /home/vagrant/.kube/config
sudo chown vagrant:vagrant /home/vagrant/.kube/config

# kubectl alias 설정
echo 'alias k=kubectl' >> /home/vagrant/.bashrc
echo 'source <(kubectl completion bash)' >> /home/vagrant/.bashrc

# kubectl 설치 확인
export KUBECONFIG=/etc/rancher/k3s/k3s.yaml

# 샘플 deployment 생성
cat > /vagrant/sample-deployment.yaml << 'EOF'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  labels:
    app: nginx
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:latest
        ports:
        - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
spec:
  type: NodePort
  selector:
    app: nginx
  ports:
  - protocol: TCP
    port: 80
    targetPort: 80
    nodePort: 30080
EOF

echo "=========================================="
echo "마스터 노드 설치 완료!"
echo "=========================================="
echo "노드 정보:"
kubectl get nodes
echo "=========================================="
echo ""
echo "사용법:"
echo "  vagrant ssh k8s-master-1"
echo "  kubectl get nodes"
echo "  kubectl get pods -A"
echo "=========================================="
