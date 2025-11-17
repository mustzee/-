# Kubernetes (k3s) 클러스터

k3s를 사용한 경량 Kubernetes 클러스터 환경입니다.

## 포함된 내용

- Ubuntu 20.04 LTS
- k3s (경량 Kubernetes)
- 1개의 마스터 노드
- 2개의 워커 노드
- kubectl 명령어 도구

## 클러스터 구성

| 노드 | 호스트명 | IP 주소 | 메모리 | CPU |
|------|---------|---------|--------|-----|
| 마스터 | k8s-master-1 | 192.168.50.11 | 2GB | 2 |
| 워커 1 | k8s-worker-1 | 192.168.50.21 | 1GB | 1 |
| 워커 2 | k8s-worker-2 | 192.168.50.22 | 1GB | 1 |

## 사용 방법

### 1. 클러스터 시작

```bash
# 모든 노드 시작
vagrant up

# 또는 개별 시작
vagrant up k8s-master-1
vagrant up k8s-worker-1
vagrant up k8s-worker-2
```

### 2. 마스터 노드 접속

```bash
vagrant ssh k8s-master-1
```

### 3. 클러스터 상태 확인

```bash
# 노드 확인
kubectl get nodes

# 모든 Pod 확인
kubectl get pods -A

# 네임스페이스 확인
kubectl get namespaces

# 서비스 확인
kubectl get services -A
```

## kubectl 기본 명령어

### 노드 관리
```bash
# 노드 목록
kubectl get nodes

# 노드 상세 정보
kubectl describe node k8s-worker-1

# 노드 리소스 사용량
kubectl top nodes  # metrics-server 필요
```

### Pod 관리
```bash
# Pod 목록 (기본 네임스페이스)
kubectl get pods

# 모든 네임스페이스의 Pod
kubectl get pods -A

# Pod 상세 정보
kubectl describe pod <pod-name>

# Pod 로그 확인
kubectl logs <pod-name>
kubectl logs -f <pod-name>  # 실시간 로그

# Pod 내부 접속
kubectl exec -it <pod-name> -- /bin/sh
```

### Deployment 관리
```bash
# Deployment 생성
kubectl create deployment nginx --image=nginx

# Deployment 목록
kubectl get deployments

# Deployment 스케일링
kubectl scale deployment nginx --replicas=3

# Deployment 삭제
kubectl delete deployment nginx
```

### Service 관리
```bash
# Service 생성
kubectl expose deployment nginx --port=80 --type=NodePort

# Service 목록
kubectl get services

# Service 상세 정보
kubectl describe service nginx
```

## 샘플 애플리케이션 배포

### 1. Nginx 배포

마스터 노드에 접속 후:

```bash
# 샘플 deployment 적용
kubectl apply -f /vagrant/sample-deployment.yaml

# 배포 확인
kubectl get deployments
kubectl get pods
kubectl get services

# NodePort로 접속 (호스트에서)
curl http://192.168.50.11:30080
curl http://192.168.50.21:30080
curl http://192.168.50.22:30080
```

### 2. 간단한 웹 앱 배포

```bash
# Deployment 생성
cat <<EOF | kubectl apply -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hello-app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: hello
  template:
    metadata:
      labels:
        app: hello
    spec:
      containers:
      - name: hello
        image: gcr.io/google-samples/hello-app:1.0
        ports:
        - containerPort: 8080
EOF

# Service 생성
kubectl expose deployment hello-app --type=NodePort --port=8080

# 포트 확인
kubectl get service hello-app

# 접속 테스트
curl http://192.168.50.11:<node-port>
```

## YAML 매니페스트 예제

### deployment.yaml
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: myapp
        image: nginx:latest
        ports:
        - containerPort: 80
        resources:
          requests:
            memory: "64Mi"
            cpu: "250m"
          limits:
            memory: "128Mi"
            cpu: "500m"
```

### service.yaml
```yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
spec:
  type: NodePort
  selector:
    app: myapp
  ports:
  - protocol: TCP
    port: 80
    targetPort: 80
    nodePort: 30100
```

적용:
```bash
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```

## 유용한 kubectl 명령어

```bash
# 네임스페이스 생성
kubectl create namespace dev

# 특정 네임스페이스에 배포
kubectl apply -f deployment.yaml -n dev

# 리소스 감시
kubectl get pods -w

# 리소스 삭제
kubectl delete -f deployment.yaml

# 모든 리소스 확인
kubectl get all

# 설정 확인
kubectl config view

# 컨텍스트 확인
kubectl config get-contexts

# YAML 형식으로 출력
kubectl get pod <pod-name> -o yaml

# JSON 형식으로 출력
kubectl get pod <pod-name> -o json
```

## 호스트에서 kubectl 사용 (선택사항)

호스트 머신에 kubectl을 설치한 경우:

```bash
# kubeconfig 복사
vagrant ssh k8s-master-1 -c "sudo cat /etc/rancher/k3s/k3s.yaml" > k3s.yaml

# API 서버 주소 변경
sed -i 's/127.0.0.1/192.168.50.11/g' k3s.yaml

# kubeconfig 설정
export KUBECONFIG=$(pwd)/k3s.yaml

# 또는
kubectl --kubeconfig=./k3s.yaml get nodes
```

## 모니터링

### k9s 설치 (선택사항)

마스터 노드에서:

```bash
# k9s 다운로드 및 설치
wget https://github.com/derailed/k9s/releases/download/v0.27.4/k9s_Linux_amd64.tar.gz
tar -xzf k9s_Linux_amd64.tar.gz
sudo mv k9s /usr/local/bin/
rm k9s_Linux_amd64.tar.gz

# k9s 실행
k9s
```

## 트러블슈팅

### 노드가 Ready 상태가 아닌 경우

```bash
# 노드 상태 확인
kubectl get nodes
kubectl describe node <node-name>

# k3s 서비스 상태 확인
sudo systemctl status k3s  # 마스터
sudo systemctl status k3s-agent  # 워커

# 로그 확인
sudo journalctl -u k3s -f  # 마스터
sudo journalctl -u k3s-agent -f  # 워커
```

### Pod가 Pending 상태인 경우

```bash
# Pod 상태 확인
kubectl describe pod <pod-name>

# 이벤트 확인
kubectl get events --sort-by=.metadata.creationTimestamp
```

### 워커 노드가 클러스터에 조인되지 않는 경우

```bash
# 워커 노드에서
sudo systemctl restart k3s-agent

# 마스터 노드에서 토큰 재확인
sudo cat /var/lib/rancher/k3s/server/node-token
```

## 클러스터 관리

```bash
# 특정 노드 중지
vagrant halt k8s-worker-1

# 특정 노드 시작
vagrant up k8s-worker-1

# 특정 노드 재시작
vagrant reload k8s-worker-1

# 모든 노드 중지
vagrant halt

# 클러스터 삭제
vagrant destroy -f
```

## 리소스 정리

```bash
# 모든 Deployment 삭제
kubectl delete deployments --all

# 모든 Service 삭제
kubectl delete services --all

# 특정 네임스페이스 삭제
kubectl delete namespace dev
```

## 학습 리소스

- [Kubernetes 공식 문서](https://kubernetes.io/docs/)
- [k3s 문서](https://docs.k3s.io/)
- [kubectl 치트시트](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)

## 팁

- k3s는 전체 Kubernetes보다 가볍고 빠르게 설치됩니다
- 개발/테스트 환경에 적합합니다
- 프로덕션 환경에도 사용 가능합니다
- kubectl alias: `k` 사용 가능 (예: `k get pods`)
