# 방화벽

## 목차
- [방화벽 기초](#방화벽-기초)
- [iptables](#iptables)
- [firewalld](#firewalld)
- [ufw (Uncomplicated Firewall)](#ufw-uncomplicated-firewall)
- [nftables](#nftables)
- [실전 예제](#실전-예제)

---

## 방화벽 기초

### 방화벽 개념

```bash
# 방화벽 유형:
# 1. 패킷 필터링: IP, 포트, 프로토콜 기반
# 2. 상태 추적 (Stateful): 연결 상태 추적
# 3. 애플리케이션: 애플리케이션 레벨 필터링

# Linux 방화벽:
# - Netfilter: 커널의 패킷 필터링 프레임워크
# - iptables: 전통적인 방화벽 도구 (legacy)
# - nftables: 현대적인 대체제
# - firewalld: RHEL/CentOS 기본
# - ufw: Ubuntu 기본

# 체인 (Chains):
# INPUT: 들어오는 패킷
# OUTPUT: 나가는 패킷
# FORWARD: 포워딩되는 패킷
# PREROUTING: 라우팅 전
# POSTROUTING: 라우팅 후

# 테이블 (Tables):
# filter: 기본 필터링
# nat: NAT (주소 변환)
# mangle: 패킷 변경
# raw: 연결 추적 예외
```

---

## iptables

### 기본 명령어

```bash
# 규칙 확인
$ sudo iptables -L
$ sudo iptables -L -v  # Verbose
$ sudo iptables -L -n  # 숫자로 (이름 해석 안 함)
$ sudo iptables -L -v -n --line-numbers

# 특정 체인
$ sudo iptables -L INPUT
$ sudo iptables -L OUTPUT
$ sudo iptables -L FORWARD

# NAT 테이블
$ sudo iptables -t nat -L

# 규칙 개수와 패킷 수
$ sudo iptables -L -v

# 정책 확인
$ sudo iptables -S
$ sudo iptables -S INPUT

# 규칙 초기화
$ sudo iptables -F  # Flush
$ sudo iptables -F INPUT  # 특정 체인만
$ sudo iptables -t nat -F  # NAT 테이블

# 모든 규칙 삭제 + 정책 ACCEPT
$ sudo iptables -P INPUT ACCEPT
$ sudo iptables -P OUTPUT ACCEPT
$ sudo iptables -P FORWARD ACCEPT
$ sudo iptables -F
$ sudo iptables -X  # 사용자 정의 체인 삭제
$ sudo iptables -t nat -F
$ sudo iptables -t mangle -F
```

### 규칙 추가

```bash
# 기본 구문
$ sudo iptables -A CHAIN -j TARGET

# 특정 포트 허용 (TCP)
$ sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT
$ sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT
$ sudo iptables -A INPUT -p tcp --dport 443 -j ACCEPT

# 특정 포트 범위
$ sudo iptables -A INPUT -p tcp --dport 1000:2000 -j ACCEPT

# UDP 포트
$ sudo iptables -A INPUT -p udp --dport 53 -j ACCEPT

# 특정 소스 IP 허용
$ sudo iptables -A INPUT -s 192.168.1.100 -j ACCEPT

# 특정 소스 네트워크
$ sudo iptables -A INPUT -s 192.168.1.0/24 -j ACCEPT

# 특정 목적지
$ sudo iptables -A OUTPUT -d 8.8.8.8 -j ACCEPT

# 특정 인터페이스
$ sudo iptables -A INPUT -i eth0 -j ACCEPT
$ sudo iptables -A OUTPUT -o eth0 -j ACCEPT

# 조합
$ sudo iptables -A INPUT -p tcp -s 192.168.1.0/24 --dport 22 -j ACCEPT

# 상태 추적 (중요!)
$ sudo iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
$ sudo iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT

# 루프백 허용
$ sudo iptables -A INPUT -i lo -j ACCEPT

# ICMP (ping) 허용
$ sudo iptables -A INPUT -p icmp -j ACCEPT
$ sudo iptables -A INPUT -p icmp --icmp-type echo-request -j ACCEPT

# 특정 MAC 주소
$ sudo iptables -A INPUT -m mac --mac-source 00:11:22:33:44:55 -j ACCEPT

# 시간 제한
$ sudo iptables -A INPUT -p tcp --dport 80 -m time --timestart 09:00 --timestop 18:00 -j ACCEPT

# 연결 수 제한
$ sudo iptables -A INPUT -p tcp --dport 80 -m connlimit --connlimit-above 10 -j REJECT

# 속도 제한 (DDoS 방어)
$ sudo iptables -A INPUT -p tcp --dport 80 -m limit --limit 25/minute --limit-burst 100 -j ACCEPT
```

### 규칙 삽입 및 삭제

```bash
# 첫 번째에 삽입
$ sudo iptables -I INPUT 1 -p tcp --dport 22 -j ACCEPT

# 특정 위치에 삽입
$ sudo iptables -I INPUT 3 -p tcp --dport 443 -j ACCEPT

# 규칙 삭제 (번호로)
$ sudo iptables -D INPUT 3

# 규칙 삭제 (내용으로)
$ sudo iptables -D INPUT -p tcp --dport 80 -j ACCEPT

# 규칙 교체
$ sudo iptables -R INPUT 1 -p tcp --dport 2222 -j ACCEPT
```

### 기본 정책

```bash
# 기본 정책 설정
$ sudo iptables -P INPUT DROP
$ sudo iptables -P FORWARD DROP
$ sudo iptables -P OUTPUT ACCEPT

# 주의: 원격 연결 시 INPUT DROP 전에 SSH 허용 규칙 추가!
$ sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT
$ sudo iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
$ sudo iptables -P INPUT DROP
```

### 로깅

```bash
# 로그 규칙
$ sudo iptables -A INPUT -j LOG --log-prefix "iptables-dropped: "

# 거부 전에 로깅
$ sudo iptables -A INPUT -p tcp --dport 23 -j LOG --log-prefix "Telnet attempt: "
$ sudo iptables -A INPUT -p tcp --dport 23 -j DROP

# 로그 레벨
$ sudo iptables -A INPUT -j LOG --log-level 4 --log-prefix "iptables: "

# 로그 확인
$ sudo tail -f /var/log/kern.log | grep iptables
$ sudo journalctl -f | grep iptables
```

### NAT (Network Address Translation)

```bash
# SNAT (Source NAT) - 출발지 주소 변경
$ sudo iptables -t nat -A POSTROUTING -o eth0 -j SNAT --to-source 203.0.113.1

# MASQUERADE (동적 IP용)
$ sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE

# DNAT (Destination NAT) - 목적지 주소 변경, 포트 포워딩
$ sudo iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 80 -j DNAT --to-destination 192.168.1.10:8080

# 포트 포워딩 예제
$ sudo iptables -t nat -A PREROUTING -p tcp --dport 8080 -j DNAT --to-destination 192.168.1.100:80
$ sudo iptables -A FORWARD -p tcp -d 192.168.1.100 --dport 80 -j ACCEPT

# IP 포워딩 활성화
$ sudo sysctl -w net.ipv4.ip_forward=1

# 영구 설정
$ sudo vi /etc/sysctl.conf
net.ipv4.ip_forward=1
$ sudo sysctl -p
```

### 저장 및 복원

```bash
# Ubuntu/Debian
$ sudo apt install iptables-persistent

# 저장
$ sudo iptables-save > /etc/iptables/rules.v4
$ sudo ip6tables-save > /etc/iptables/rules.v6

# 또는
$ sudo netfilter-persistent save

# 복원
$ sudo iptables-restore < /etc/iptables/rules.v4

# 또는
$ sudo netfilter-persistent reload

# RHEL/CentOS
$ sudo service iptables save
$ sudo systemctl save iptables

# 수동 백업
$ sudo iptables-save > ~/iptables-backup.txt
$ sudo iptables-restore < ~/iptables-backup.txt
```

### 실전 웹서버 규칙

```bash
#!/bin/bash
# firewall-web-server.sh

# 초기화
iptables -F
iptables -X
iptables -t nat -F

# 기본 정책
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT

# 루프백
iptables -A INPUT -i lo -j ACCEPT

# 상태 추적
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# SSH
iptables -A INPUT -p tcp --dport 22 -m state --state NEW -m limit --limit 3/min -j ACCEPT

# HTTP/HTTPS
iptables -A INPUT -p tcp --dport 80 -j ACCEPT
iptables -A INPUT -p tcp --dport 443 -j ACCEPT

# ICMP (ping)
iptables -A INPUT -p icmp --icmp-type echo-request -j ACCEPT

# 로그
iptables -A INPUT -m limit --limit 5/min -j LOG --log-prefix "iptables-dropped: " --log-level 7

# 저장
iptables-save > /etc/iptables/rules.v4
```

---

## firewalld

### 기본 명령어

```bash
# 상태 확인
$ sudo firewall-cmd --state
$ sudo systemctl status firewalld

# 서비스 시작/중지
$ sudo systemctl start firewalld
$ sudo systemctl stop firewalld
$ sudo systemctl enable firewalld

# 현재 설정 보기
$ sudo firewall-cmd --list-all
$ sudo firewall-cmd --list-all-zones

# 활성 존
$ sudo firewall-cmd --get-active-zones

# 기본 존
$ sudo firewall-cmd --get-default-zone
$ sudo firewall-cmd --set-default-zone=public

# 존 목록
$ sudo firewall-cmd --get-zones

# 서비스 목록
$ sudo firewall-cmd --get-services

# 인터페이스 존 확인
$ sudo firewall-cmd --get-zone-of-interface=eth0
```

### 서비스 관리

```bash
# 서비스 추가 (임시)
$ sudo firewall-cmd --add-service=http
$ sudo firewall-cmd --add-service=https

# 영구 설정
$ sudo firewall-cmd --permanent --add-service=http
$ sudo firewall-cmd --permanent --add-service=https

# 여러 서비스
$ sudo firewall-cmd --permanent --add-service={http,https,ssh}

# 서비스 제거
$ sudo firewall-cmd --remove-service=http
$ sudo firewall-cmd --permanent --remove-service=http

# 현재 서비스 목록
$ sudo firewall-cmd --list-services
$ sudo firewall-cmd --permanent --list-services

# 설정 재로드
$ sudo firewall-cmd --reload

# 완전 재시작
$ sudo firewall-cmd --complete-reload
```

### 포트 관리

```bash
# 포트 추가
$ sudo firewall-cmd --add-port=8080/tcp
$ sudo firewall-cmd --permanent --add-port=8080/tcp

# 포트 범위
$ sudo firewall-cmd --add-port=5000-5100/tcp
$ sudo firewall-cmd --permanent --add-port=5000-5100/tcp

# UDP 포트
$ sudo firewall-cmd --add-port=53/udp
$ sudo firewall-cmd --permanent --add-port=53/udp

# 여러 포트
$ sudo firewall-cmd --permanent --add-port={80/tcp,443/tcp,8080/tcp}

# 포트 제거
$ sudo firewall-cmd --remove-port=8080/tcp
$ sudo firewall-cmd --permanent --remove-port=8080/tcp

# 포트 목록
$ sudo firewall-cmd --list-ports
$ sudo firewall-cmd --permanent --list-ports
```

### Rich Rules

```bash
# 특정 IP 허용
$ sudo firewall-cmd --permanent --add-rich-rule='rule family="ipv4" source address="192.168.1.100" accept'

# 특정 IP 차단
$ sudo firewall-cmd --permanent --add-rich-rule='rule family="ipv4" source address="203.0.113.50" reject'

# 특정 IP에서 특정 포트 허용
$ sudo firewall-cmd --permanent --add-rich-rule='rule family="ipv4" source address="192.168.1.0/24" port port="22" protocol="tcp" accept'

# 로깅
$ sudo firewall-cmd --permanent --add-rich-rule='rule family="ipv4" source address="10.0.0.0/8" service name="ssh" log prefix="SSH attempt: " level="info" accept'

# 속도 제한
$ sudo firewall-cmd --permanent --add-rich-rule='rule service name="ssh" limit value="3/m" accept'

# Rich rule 목록
$ sudo firewall-cmd --list-rich-rules
$ sudo firewall-cmd --permanent --list-rich-rules

# Rich rule 제거
$ sudo firewall-cmd --permanent --remove-rich-rule='rule family="ipv4" source address="192.168.1.100" accept'
```

### 존 관리

```bash
# 새 존 생성
$ sudo firewall-cmd --permanent --new-zone=customzone

# 존에 서비스 추가
$ sudo firewall-cmd --permanent --zone=customzone --add-service=http

# 인터페이스를 존에 할당
$ sudo firewall-cmd --permanent --zone=public --add-interface=eth0
$ sudo firewall-cmd --permanent --zone=internal --add-interface=eth1

# 소스 추가 (IP 범위를 특정 존에)
$ sudo firewall-cmd --permanent --zone=trusted --add-source=192.168.1.0/24

# 존 정보
$ sudo firewall-cmd --zone=public --list-all
$ sudo firewall-cmd --permanent --info-zone=public

# 특정 존에 규칙 추가
$ sudo firewall-cmd --zone=public --add-service=http
```

### 포트 포워딩

```bash
# 로컬 포트 포워딩
$ sudo firewall-cmd --permanent --add-forward-port=port=80:proto=tcp:toport=8080
$ sudo firewall-cmd --permanent --add-forward-port=port=443:proto=tcp:toport=8443

# 다른 호스트로 포워딩
$ sudo firewall-cmd --permanent --add-forward-port=port=80:proto=tcp:toaddr=192.168.1.10
$ sudo firewall-cmd --permanent --add-forward-port=port=80:proto=tcp:toport=8080:toaddr=192.168.1.10

# IP 마스커레이드 활성화 (필요 시)
$ sudo firewall-cmd --permanent --add-masquerade
$ sudo firewall-cmd --permanent --query-masquerade

# 포워딩 목록
$ sudo firewall-cmd --list-forward-ports
```

### Direct Rules (iptables 직접 사용)

```bash
# Direct rule 추가
$ sudo firewall-cmd --permanent --direct --add-rule ipv4 filter INPUT 0 -p tcp --dport 9000 -j ACCEPT

# Direct rule 목록
$ sudo firewall-cmd --direct --get-all-rules

# Direct rule 제거
$ sudo firewall-cmd --permanent --direct --remove-rule ipv4 filter INPUT 0 -p tcp --dport 9000 -j ACCEPT
```

---

## ufw (Uncomplicated Firewall)

### 기본 사용법

```bash
# 상태 확인
$ sudo ufw status
$ sudo ufw status verbose
$ sudo ufw status numbered

# UFW 활성화
$ sudo ufw enable

# UFW 비활성화
$ sudo ufw disable

# 재시작
$ sudo ufw reload

# 초기화
$ sudo ufw reset

# 기본 정책
$ sudo ufw default deny incoming
$ sudo ufw default allow outgoing
$ sudo ufw default deny forward
```

### 규칙 추가

```bash
# 포트 허용
$ sudo ufw allow 22
$ sudo ufw allow 22/tcp
$ sudo ufw allow 80/tcp
$ sudo ufw allow 443/tcp

# 포트 거부
$ sudo ufw deny 23

# 포트 범위
$ sudo ufw allow 6000:6100/tcp

# 서비스 이름으로
$ sudo ufw allow ssh
$ sudo ufw allow http
$ sudo ufw allow https

# 특정 IP 허용
$ sudo ufw allow from 192.168.1.100

# 특정 IP의 특정 포트
$ sudo ufw allow from 192.168.1.100 to any port 22

# 특정 네트워크
$ sudo ufw allow from 192.168.1.0/24

# 특정 네트워크의 특정 포트
$ sudo ufw allow from 192.168.1.0/24 to any port 3306

# 특정 인터페이스
$ sudo ufw allow in on eth0 to any port 80
$ sudo ufw allow in on eth1 to any port 3306

# 특정 IP로의 연결
$ sudo ufw allow out to 8.8.8.8

# 프로토콜 지정
$ sudo ufw allow proto tcp from any to any port 80,443
$ sudo ufw allow proto udp from any to any port 53
```

### 규칙 삭제

```bash
# 규칙 번호로 삭제
$ sudo ufw status numbered
$ sudo ufw delete 3

# 규칙 내용으로 삭제
$ sudo ufw delete allow 80/tcp
$ sudo ufw delete allow from 192.168.1.100
```

### 고급 규칙

```bash
# 로깅
$ sudo ufw logging on
$ sudo ufw logging off
$ sudo ufw logging low
$ sudo ufw logging medium
$ sudo ufw logging high

# 애플리케이션 프로파일
$ sudo ufw app list
$ sudo ufw app info 'Apache Full'
$ sudo ufw allow 'Apache Full'
$ sudo ufw allow 'Nginx Full'
$ sudo ufw allow 'OpenSSH'

# 속도 제한 (DDoS 방어)
$ sudo ufw limit ssh
$ sudo ufw limit 22/tcp

# 거부와 차단의 차이
$ sudo ufw deny 23  # REJECT (응답 전송)
$ sudo ufw reject 23  # REJECT
# DROP은 direct rules 필요
```

### 애플리케이션 프로파일 만들기

```bash
# 프로파일 파일 생성
$ sudo vi /etc/ufw/applications.d/myapp

[MyApp]
title=My Application
description=My custom application
ports=8080,8443/tcp

# 프로파일 업데이트
$ sudo ufw app update MyApp

# 사용
$ sudo ufw allow MyApp
```

---

## nftables

### 기본 명령어

```bash
# 규칙 확인
$ sudo nft list ruleset

# 테이블 목록
$ sudo nft list tables

# 특정 테이블
$ sudo nft list table inet filter

# 체인 목록
$ sudo nft list chains

# 규칙 초기화
$ sudo nft flush ruleset

# 테이블 삭제
$ sudo nft delete table inet filter
```

### 테이블 및 체인 생성

```bash
# 테이블 생성
$ sudo nft add table inet filter

# 체인 생성 (INPUT)
$ sudo nft add chain inet filter input { type filter hook input priority 0 \; policy drop \; }

# 체인 생성 (OUTPUT)
$ sudo nft add chain inet filter output { type filter hook output priority 0 \; policy accept \; }

# 체인 생성 (FORWARD)
$ sudo nft add chain inet filter forward { type filter hook forward priority 0 \; policy drop \; }
```

### 규칙 추가

```bash
# 루프백 허용
$ sudo nft add rule inet filter input iif lo accept

# 상태 추적
$ sudo nft add rule inet filter input ct state established,related accept

# SSH 허용
$ sudo nft add rule inet filter input tcp dport 22 accept

# HTTP/HTTPS
$ sudo nft add rule inet filter input tcp dport {80, 443} accept

# 특정 IP
$ sudo nft add rule inet filter input ip saddr 192.168.1.100 accept

# 특정 IP의 특정 포트
$ sudo nft add rule inet filter input ip saddr 192.168.1.0/24 tcp dport 22 accept

# ICMP
$ sudo nft add rule inet filter input icmp type echo-request accept

# 속도 제한
$ sudo nft add rule inet filter input tcp dport 22 limit rate 3/minute accept
```

### 설정 저장 및 복원

```bash
# 저장
$ sudo nft list ruleset > /etc/nftables.conf

# 복원
$ sudo nft -f /etc/nftables.conf

# 서비스 활성화
$ sudo systemctl enable nftables
$ sudo systemctl start nftables
```

---

## 실전 예제

### 예제 1: 기본 서버 방화벽 (iptables)

```bash
#!/bin/bash
# basic-firewall.sh

# 초기화
iptables -F
iptables -X
iptables -t nat -F

# 기본 정책
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT

# 루프백
iptables -A INPUT -i lo -j ACCEPT

# 상태 추적
iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT

# SSH (속도 제한)
iptables -A INPUT -p tcp --dport 22 -m conntrack --ctstate NEW -m recent --set
iptables -A INPUT -p tcp --dport 22 -m conntrack --ctstate NEW -m recent --update --seconds 60 --hitcount 4 -j DROP
iptables -A INPUT -p tcp --dport 22 -j ACCEPT

# HTTP/HTTPS
iptables -A INPUT -p tcp -m multiport --dports 80,443 -j ACCEPT

# ICMP
iptables -A INPUT -p icmp --icmp-type echo-request -m limit --limit 1/s -j ACCEPT

# 로그
iptables -A INPUT -m limit --limit 5/min -j LOG --log-prefix "iptables-DROP: " --log-level 7

# 저장
iptables-save > /etc/iptables/rules.v4

echo "Firewall configured successfully"
```

### 예제 2: 웹 서버 방화벽 (ufw)

```bash
#!/bin/bash
# setup-ufw-webserver.sh

# 초기화
sudo ufw --force reset

# 기본 정책
sudo ufw default deny incoming
sudo ufw default allow outgoing

# SSH (속도 제한)
sudo ufw limit 22/tcp

# HTTP/HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# 특정 관리 IP에서만 접근
sudo ufw allow from 203.0.113.0/24 to any port 22

# 로깅
sudo ufw logging on

# 활성화
sudo ufw --force enable

echo "UFW configured for web server"
```

### 예제 3: DB 서버 방화벽 (firewalld)

```bash
#!/bin/bash
# setup-firewalld-db.sh

# MySQL/MariaDB 포트는 특정 웹서버에서만
sudo firewall-cmd --permanent --add-rich-rule='rule family="ipv4" source address="192.168.1.10" port port="3306" protocol="tcp" accept'

# PostgreSQL
sudo firewall-cmd --permanent --add-rich-rule='rule family="ipv4" source address="192.168.1.0/24" port port="5432" protocol="tcp" accept'

# SSH
sudo firewall-cmd --permanent --add-service=ssh

# 관리용 IP만 SSH 허용
sudo firewall-cmd --permanent --add-rich-rule='rule family="ipv4" source address="203.0.113.100" service name="ssh" accept'
sudo firewall-cmd --permanent --remove-service=ssh

# 재로드
sudo firewall-cmd --reload

echo "Firewalld configured for database server"
```

---

## 문제 해결

### 방화벽 때문에 접속 안 될 때

```bash
# 1. 방화벽 상태 확인
$ sudo iptables -L -v -n
$ sudo ufw status verbose
$ sudo firewall-cmd --list-all

# 2. 임시로 방화벽 비활성화
$ sudo ufw disable
$ sudo systemctl stop firewalld

# 3. 규칙 확인 후 필요한 포트 열기
$ sudo ufw allow 22
$ sudo firewall-cmd --add-port=22/tcp

# 4. 로그 확인
$ sudo tail -f /var/log/kern.log | grep iptables
$ sudo journalctl -f -u firewalld
```

### 규칙이 적용 안 될 때

```bash
# 저장 확인
$ sudo iptables-save
$ sudo firewall-cmd --runtime-to-permanent

# 재로드
$ sudo ufw reload
$ sudo firewall-cmd --reload
$ sudo systemctl restart iptables
```

---

## 요약

방화벽 도구:

1. **iptables**: 강력하지만 복잡
2. **firewalld**: RHEL/CentOS 기본, 동적 관리
3. **ufw**: Ubuntu 기본, 사용하기 쉬움
4. **nftables**: 현대적, iptables 후계

---

[다음: 패키지 관리 (APT) →](../09-package-management/apt-debian.md)

[← 파일 전송으로 돌아가기](file-transfer.md)

[← 목차로 돌아가기](../README.md)
