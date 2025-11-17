# 네트워크 명령어

## 목차
- [네트워크 설정](#네트워크-설정)
- [네트워크 진단](#네트워크-진단)
- [네트워크 트래픽](#네트워크-트래픽)
- [원격 접속](#원격-접속)
- [파일 전송](#파일-전송)

---

## 네트워크 설정

### ip - 네트워크 설정 (현대적 방법)

```bash
# IP 주소 확인
$ ip addr
$ ip a

# 특정 인터페이스
$ ip addr show eth0

# 간단한 출력
$ ip -br addr

# IP 추가
$ sudo ip addr add 192.168.1.100/24 dev eth0

# IP 삭제
$ sudo ip addr del 192.168.1.100/24 dev eth0

# 인터페이스 활성화/비활성화
$ sudo ip link set eth0 up
$ sudo ip link set eth0 down

# 라우팅 테이블
$ ip route
$ ip r

# 기본 게이트웨이 추가
$ sudo ip route add default via 192.168.1.1

# 특정 네트워크 라우트
$ sudo ip route add 10.0.0.0/24 via 192.168.1.254

# ARP 테이블
$ ip neigh
$ ip n

# 네트워크 통계
$ ip -s link

# 색상 출력
$ ip -c addr
```

### ifconfig (레거시, 하지만 여전히 유용)

```bash
# 모든 인터페이스
$ ifconfig

# 특정 인터페이스
$ ifconfig eth0

# IP 설정
$ sudo ifconfig eth0 192.168.1.100 netmask 255.255.255.0

# 인터페이스 활성화/비활성화
$ sudo ifconfig eth0 up
$ sudo ifconfig eth0 down

# MTU 설정
$ sudo ifconfig eth0 mtu 1500

# Promiscuous 모드 (패킷 스니핑)
$ sudo ifconfig eth0 promisc
```

### NetworkManager

```bash
# nmcli - 네트워크 매니저 CLI
$ nmcli

# 일반 상태
$ nmcli general status

# 연결 목록
$ nmcli connection show

# 활성 연결
$ nmcli connection show --active

# 디바이스 목록
$ nmcli device

# WiFi 목록
$ nmcli device wifi list

# WiFi 연결
$ nmcli device wifi connect "SSID" password "PASSWORD"

# 연결 활성화/비활성화
$ nmcli connection up "Wired connection 1"
$ nmcli connection down "Wired connection 1"

# 고정 IP 설정
$ nmcli connection modify "Wired connection 1" \
  ipv4.addresses 192.168.1.100/24 \
  ipv4.gateway 192.168.1.1 \
  ipv4.dns "8.8.8.8 8.8.4.4" \
  ipv4.method manual

# DHCP로 변경
$ nmcli connection modify "Wired connection 1" ipv4.method auto
```

---

## 네트워크 진단

### ping - 연결 테스트

```bash
# 기본 ping
$ ping google.com

# 횟수 지정
$ ping -c 4 google.com

# 간격 지정 (초)
$ ping -i 0.5 google.com

# 패킷 크기
$ ping -s 1000 google.com

# Flood ping (root)
$ sudo ping -f google.com

# IPv6
$ ping6 ipv6.google.com

# 인터페이스 지정
$ ping -I eth0 192.168.1.1

# 타임스탬프
$ ping -D google.com

# 조용한 모드 (요약만)
$ ping -c 10 -q google.com
```

### traceroute - 경로 추적

```bash
# 기본 traceroute
$ traceroute google.com

# ICMP 사용
$ sudo traceroute -I google.com

# 최대 홉 수
$ traceroute -m 20 google.com

# 포트 지정
$ traceroute -p 80 google.com

# 대기 시간
$ traceroute -w 2 google.com

# 동시 쿼리 수
$ traceroute -q 2 google.com

# tracepath (권한 불필요)
$ tracepath google.com

# MTU 경로 찾기
$ tracepath -b google.com
```

### nslookup / dig / host - DNS 조회

```bash
# nslookup
$ nslookup google.com
$ nslookup google.com 8.8.8.8  # DNS 서버 지정

# dig (더 자세함)
$ dig google.com

# 간단한 출력
$ dig +short google.com

# 특정 레코드 타입
$ dig google.com A      # IPv4
$ dig google.com AAAA   # IPv6
$ dig google.com MX     # 메일 서버
$ dig google.com NS     # 네임 서버
$ dig google.com TXT    # TXT 레코드

# 역방향 조회
$ dig -x 8.8.8.8

# 추적
$ dig +trace google.com

# DNS 서버 지정
$ dig @8.8.8.8 google.com

# host (가장 간단)
$ host google.com
$ host 8.8.8.8  # 역방향
```

### netstat / ss - 네트워크 통계

```bash
# netstat (레거시)
# 모든 연결
$ netstat -a

# 리스닝 포트
$ netstat -l
$ netstat -tuln  # TCP/UDP, 숫자, 리스닝

# 프로그램 이름 포함
$ sudo netstat -tulpn

# 라우팅 테이블
$ netstat -r

# 인터페이스 통계
$ netstat -i

# ss (현대적, 빠름)
# 모든 소켓
$ ss -a

# 리스닝
$ ss -l

# TCP만
$ ss -t

# UDP만
$ ss -u

# 프로세스 정보
$ sudo ss -p

# 상태별
$ ss state established
$ ss state listening

# 포트별
$ ss sport = :80
$ ss dport = :443

# 통합 예제
$ sudo ss -tulpn | grep LISTEN
```

### telnet / nc - 포트 테스트

```bash
# telnet으로 포트 확인
$ telnet example.com 80

# netcat (nc)으로 포트 스캔
$ nc -zv example.com 80

# 포트 범위 스캔
$ nc -zv example.com 20-25

# UDP 포트
$ nc -zuv example.com 53

# 리스닝 서버 시작
$ nc -l 8080  # 8080 포트에서 대기

# 파일 전송 (수신)
$ nc -l 8080 > received_file

# 파일 전송 (발신)
$ nc target_host 8080 < file_to_send

# 채팅
# 서버: nc -l 8080
# 클라이언트: nc server_ip 8080
```

---

## 네트워크 트래픽

### tcpdump - 패킷 캡처

```bash
# 기본 캡처
$ sudo tcpdump

# 특정 인터페이스
$ sudo tcpdump -i eth0

# 패킷 수 제한
$ sudo tcpdump -c 10

# 파일로 저장
$ sudo tcpdump -w capture.pcap

# 파일 읽기
$ sudo tcpdump -r capture.pcap

# 특정 호스트
$ sudo tcpdump host 192.168.1.100

# 특정 포트
$ sudo tcpdump port 80
$ sudo tcpdump port 80 or port 443

# 네트워크
$ sudo tcpdump net 192.168.1.0/24

# 프로토콜
$ sudo tcpdump icmp
$ sudo tcpdump tcp
$ sudo tcpdump udp

# 복합 필터
$ sudo tcpdump 'tcp port 80 and src 192.168.1.100'

# HTTP 요청
$ sudo tcpdump -A 'tcp port 80 and (((ip[2:2] - ((ip[0]&0xf)<<2)) - ((tcp[12]&0xf0)>>2)) != 0)'

# DNS 쿼리
$ sudo tcpdump -i eth0 udp port 53

# 자세한 출력
$ sudo tcpdump -v
$ sudo tcpdump -vv
$ sudo tcpdump -vvv

# ASCII 출력
$ sudo tcpdump -A

# 16진수 출력
$ sudo tcpdump -X

# 타임스탬프
$ sudo tcpdump -tt
```

### iftop - 실시간 대역폭 모니터링

```bash
# 설치
$ sudo apt install iftop

# 기본 실행
$ sudo iftop

# 특정 인터페이스
$ sudo iftop -i eth0

# 포트 표시
$ sudo iftop -P

# 대역폭 단위
$ sudo iftop -B  # bytes/sec

# 필터
$ sudo iftop -f "port 80"

# 내부 명령어:
# h: 도움말
# n: DNS 해석 토글
# s: 출발지 표시 토글
# d: 목적지 표시 토글
# p: 포트 표시 토글
# t: 표시 모드 변경
# q: 종료
```

### nethogs - 프로세스별 대역폭

```bash
# 설치
$ sudo apt install nethogs

# 기본 실행
$ sudo nethogs

# 특정 인터페이스
$ sudo nethogs eth0

# 여러 인터페이스
$ sudo nethogs eth0 wlan0

# 업데이트 간격
$ sudo nethogs -d 5  # 5초
```

### nmap - 네트워크 스캔

```bash
# 설치
$ sudo apt install nmap

# 기본 스캔
$ nmap 192.168.1.100

# 포트 스캔
$ nmap -p 80,443 192.168.1.100
$ nmap -p 1-65535 192.168.1.100

# 서비스 버전 감지
$ nmap -sV 192.168.1.100

# OS 감지
$ sudo nmap -O 192.168.1.100

# 빠른 스캔
$ nmap -F 192.168.1.100

# 네트워크 전체 스캔
$ nmap 192.168.1.0/24

# Ping 스캔 (호스트 발견)
$ nmap -sn 192.168.1.0/24

# TCP SYN 스캔
$ sudo nmap -sS 192.168.1.100

# UDP 스캔
$ sudo nmap -sU 192.168.1.100

# 공격적 스캔
$ sudo nmap -A 192.168.1.100

# 스크립트 스캔
$ nmap --script=vuln 192.168.1.100

# 출력 저장
$ nmap -oN output.txt 192.168.1.100
$ nmap -oX output.xml 192.168.1.100
```

---

## 원격 접속

### ssh - Secure Shell

```bash
# 기본 연결
$ ssh user@hostname

# 포트 지정
$ ssh -p 2222 user@hostname

# 키 파일 지정
$ ssh -i ~/.ssh/id_rsa user@hostname

# X11 포워딩
$ ssh -X user@hostname

# 압축
$ ssh -C user@hostname

# verbose 모드
$ ssh -v user@hostname

# 명령 실행 후 종료
$ ssh user@hostname 'ls -la'

# SSH 터널링 (로컬 포트 포워딩)
$ ssh -L 8080:localhost:80 user@hostname

# 리모트 포트 포워딩
$ ssh -R 8080:localhost:80 user@hostname

# 동적 포트 포워딩 (SOCKS 프록시)
$ ssh -D 1080 user@hostname

# SSH 키 생성
$ ssh-keygen -t rsa -b 4096 -C "your_email@example.com"

# 공개키 복사
$ ssh-copy-id user@hostname

# SSH 설정 파일 (~/.ssh/config)
$ cat ~/.ssh/config
Host myserver
    HostName example.com
    User username
    Port 2222
    IdentityFile ~/.ssh/id_rsa

$ ssh myserver  # 위 설정 사용
```

### scp - SSH 파일 복사

```bash
# 파일 업로드
$ scp file.txt user@hostname:/remote/path/

# 파일 다운로드
$ scp user@hostname:/remote/file.txt /local/path/

# 디렉토리 복사
$ scp -r directory/ user@hostname:/remote/path/

# 포트 지정
$ scp -P 2222 file.txt user@hostname:/path/

# 압축
$ scp -C large_file.txt user@hostname:/path/

# 대역폭 제한 (KB/s)
$ scp -l 1000 file.txt user@hostname:/path/

# 여러 파일
$ scp file1.txt file2.txt user@hostname:/path/

# 진행 상황 숨김
$ scp -q file.txt user@hostname:/path/

# 원본 타임스탬프 보존
$ scp -p file.txt user@hostname:/path/
```

### rsync - 동기화

```bash
# 기본 동기화
$ rsync -av source/ destination/

# SSH를 통한 원격 동기화
$ rsync -av source/ user@hostname:/remote/path/

# 진행 상황 표시
$ rsync -av --progress source/ dest/

# 삭제된 파일도 동기화
$ rsync -av --delete source/ dest/

# 제외
$ rsync -av --exclude='*.log' source/ dest/
$ rsync -av --exclude-from=exclude.txt source/ dest/

# 드라이 런 (테스트)
$ rsync -avn source/ dest/

# 압축
$ rsync -avz source/ user@hostname:/path/

# 대역폭 제한 (KB/s)
$ rsync -av --bwlimit=1000 source/ dest/

# 부분 전송 (재개 가능)
$ rsync -avP source/ dest/

# 백업 디렉토리 생성
$ rsync -av --backup --backup-dir=/backup source/ dest/

# 특정 파일만
$ rsync -av --include='*.txt' --exclude='*' source/ dest/

# 실전 백업 예제
$ rsync -avz --delete --exclude='.git' \
  ~/projects/ user@backup:/backups/projects/
```

---

## 파일 전송

### wget - 파일 다운로드

```bash
# 기본 다운로드
$ wget https://example.com/file.zip

# 다른 이름으로 저장
$ wget -O newname.zip https://example.com/file.zip

# 재개
$ wget -c https://example.com/large_file.iso

# 백그라운드
$ wget -b https://example.com/file.zip

# 속도 제한 (KB/s)
$ wget --limit-rate=200k https://example.com/file.zip

# 여러 파일 (파일에서 읽기)
$ wget -i urls.txt

# 재귀 다운로드 (웹사이트 미러링)
$ wget -r -np -k https://example.com/

# 사용자 에이전트 지정
$ wget --user-agent="Mozilla/5.0" https://example.com/

# 인증
$ wget --user=username --password=password https://example.com/

# FTP 다운로드
$ wget ftp://ftp.example.com/file.tar.gz

# 프록시
$ wget -e use_proxy=yes -e http_proxy=proxy:8080 https://example.com/

# 재시도
$ wget --tries=10 https://example.com/file.zip

# 타임아웃
$ wget --timeout=60 https://example.com/file.zip
```

### curl - 다목적 전송 도구

```bash
# 기본 다운로드 (출력)
$ curl https://example.com

# 파일로 저장
$ curl -O https://example.com/file.zip
$ curl -o newname.zip https://example.com/file.zip

# 헤더 보기
$ curl -I https://example.com

# 재개
$ curl -C - -O https://example.com/large_file.iso

# POST 요청
$ curl -X POST -d "param1=value1&param2=value2" https://api.example.com/

# JSON 데이터
$ curl -X POST -H "Content-Type: application/json" \
  -d '{"key":"value"}' https://api.example.com/

# 파일 업로드
$ curl -F "file=@/path/to/file.txt" https://example.com/upload

# 인증
$ curl -u username:password https://example.com/

# Bearer 토큰
$ curl -H "Authorization: Bearer TOKEN" https://api.example.com/

# 쿠키
$ curl -b cookies.txt https://example.com/
$ curl -c cookies.txt https://example.com/  # 쿠키 저장

# 리다이렉트 따라가기
$ curl -L https://example.com/

# 진행 상황 표시
$ curl -# -O https://example.com/file.zip

# 조용한 모드
$ curl -s https://example.com/ | grep "keyword"

# 프록시
$ curl -x proxy:8080 https://example.com/

# 타임아웃
$ curl --connect-timeout 10 --max-time 30 https://example.com/

# verbose 모드
$ curl -v https://example.com/

# DNS 서버 지정
$ curl --dns-servers 8.8.8.8 https://example.com/

# API 테스트 예제
$ curl -X GET -H "Accept: application/json" https://api.github.com/users/octocat
```

---

## 실전 예제

### 예제 1: 네트워크 문제 진단

```bash
# 1. 연결 확인
$ ping -c 4 8.8.8.8

# 2. DNS 확인
$ nslookup google.com

# 3. 라우팅 확인
$ traceroute google.com

# 4. 포트 확인
$ telnet example.com 80

# 5. 방화벽 확인
$ sudo iptables -L
```

### 예제 2: 웹 서버 헬스 체크

```bash
# HTTP 상태 코드 확인
$ curl -I -s https://example.com | head -1

# 응답 시간 측정
$ curl -o /dev/null -s -w 'Total: %{time_total}s\n' https://example.com

# 스크립트로 자동화
#!/bin/bash
while true; do
    status=$(curl -I -s https://example.com | head -1)
    echo "$(date): $status"
    sleep 60
done
```

### 예제 3: 대량 파일 전송

```bash
# 증분 백업
$ rsync -avz --delete \
  --exclude='node_modules' \
  --exclude='.git' \
  ~/project/ user@backup:/backups/project/

# 진행 상황 로깅
$ rsync -avz --progress ~/data/ user@backup:/data/ \
  2>&1 | tee rsync.log
```

---

## 요약

네트워크 명령어 핵심:

- **설정**: ip, ifconfig, nmcli
- **진단**: ping, traceroute, dig, netstat
- **트래픽**: tcpdump, iftop, nmap
- **원격**: ssh, scp, rsync
- **전송**: wget, curl

이 도구들을 마스터하면 네트워크 관리와 문제 해결이 훨씬 쉬워집니다.

---

[다음: 고급 명령어 →](advanced.md)

[← 시스템 관리 명령어로 돌아가기](system.md)

[← 목차로 돌아가기](../README.md)
