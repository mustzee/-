#!/bin/bash

echo "=========================================="
echo "k3s 워커 노드 설치 시작"
echo "=========================================="

# 시스템 업데이트
export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get upgrade -y

# 토큰과 마스터 IP 읽기
if [ ! -f /vagrant/node-token ]; then
  echo "오류: 마스터 노드 토큰을 찾을 수 없습니다."
  echo "마스터 노드를 먼저 시작해주세요."
  exit 1
fi

K3S_TOKEN=$(cat /vagrant/node-token)
K3S_MASTER_IP=$(cat /vagrant/master-ip)
K3S_URL="https://${K3S_MASTER_IP}:6443"

echo "마스터 노드: ${K3S_URL}"

# 현재 노드 IP 가져오기
NODE_IP=$(ip addr show eth1 | grep "inet " | awk '{print $2}' | cut -d/ -f1)
echo "워커 노드 IP: ${NODE_IP}"

# k3s 워커 설치
echo "k3s 워커 설치 중..."
curl -sfL https://get.k3s.io | K3S_URL=$K3S_URL K3S_TOKEN=$K3S_TOKEN sh -s - \
  --node-ip ${NODE_IP} \
  --flannel-iface eth1

echo "=========================================="
echo "워커 노드 설치 완료!"
echo "=========================================="
echo "마스터 노드에서 확인:"
echo "  vagrant ssh k8s-master-1"
echo "  kubectl get nodes"
echo "=========================================="
