# 네트워크 진단

## 목차
- [연결 테스트](#연결-테스트)
- [DNS 조회](#dns-조회)
- [라우트 추적](#라우트-추적)
- [포트 및 소켓](#포트-및-소켓)
- [패킷 캡처](#패킷-캡처)
- [네트워크 분석 도구](#네트워크-분석-도구)
- [실전 예제](#실전-예제)

---

## 연결 테스트

### ping - ICMP Echo

```bash
# 기본 ping
$ ping google.com
PING google.com (142.250.217.46): 56 data bytes
64 bytes from 142.250.217.46: icmp_seq=0 ttl=118 time=10.5 ms
64 bytes from 142.250.217.46: icmp_seq=1 ttl=118 time=11.2 ms
^C
--- google.com ping statistics ---
2 packets transmitted, 2 packets received, 0.0% packet loss
round-trip min/avg/max/stddev = 10.5/10.8/11.2/0.4 ms

# 횟수 지정
$ ping -c 4 8.8.8.8
$ ping -c 10 google.com

# 간격 지정 (초)
$ ping -i 0.5 8.8.8.8    # 0.5초마다
$ ping -i 2 8.8.8.8      # 2초마다

# 타임아웃
$ ping -W 2 8.8.8.8      # 2초 대기

# 패킷 크기
$ ping -s 1000 8.8.8.8   # 1000 바이트

# Flood ping (root 필요, 부하 테스트)
$ sudo ping -f 8.8.8.8

# TTL 설정
$ ping -t 64 8.8.8.8

# 인터페이스 지정
$ ping -I eth0 8.8.8.8
$ ping -I 192.168.1.100 8.8.8.8

# IPv6
$ ping6 google.com
$ ping -6 google.com

# 조용한 모드 (요약만)
$ ping -c 10 -q 8.8.8.8

# 타임스탬프
$ ping -D 8.8.8.8

# 오디오 알림 (응답 있을 때)
$ ping -a 8.8.8.8

# 브로드캐스트
$ ping -b 192.168.1.255

# 패턴 지정
$ ping -p ff 8.8.8.8     # 0xff 패턴

# MTU 경로 찾기
$ ping -M do -s 1472 8.8.8.8  # Don't fragment

# 빠른 연결 확인
$ ping -c 1 -W 1 8.8.8.8 > /dev/null 2>&1 && echo "UP" || echo "DOWN"
```

### arping - ARP Ping

```bash
# 설치
$ sudo apt install arping

# 로컬 네트워크에서 IP 확인
$ sudo arping 192.168.1.1
$ sudo arping -c 4 192.168.1.1

# 인터페이스 지정
$ sudo arping -I eth0 192.168.1.1

# 중복 IP 탐지
$ sudo arping -D -I eth0 192.168.1.100

# MAC 주소로 찾기
$ sudo arping -i eth0 00:11:22:33:44:55
```

### nc (netcat) - 포트 테스트

```bash
# TCP 포트 테스트
$ nc -zv 192.168.1.1 80
Connection to 192.168.1.1 80 port [tcp/http] succeeded!

# 포트 범위 스캔
$ nc -zv 192.168.1.1 20-80
$ nc -zv 192.168.1.1 1-1000

# UDP 테스트
$ nc -zuv 192.168.1.1 53

# 타임아웃 설정
$ nc -w 2 -zv 192.168.1.1 22

# 간단한 서버 시작
$ nc -l 8080

# 클라이언트 연결
$ nc localhost 8080

# 파일 전송 (서버)
$ nc -l 8080 > received_file

# 파일 전송 (클라이언트)
$ nc 192.168.1.100 8080 < file_to_send

# 채팅
# 서버: nc -l 8080
# 클라이언트: nc 192.168.1.100 8080

# 배너 그래빙
$ nc 192.168.1.1 22
$ nc 192.168.1.1 80
GET / HTTP/1.0

# 포트 포워딩
$ nc -l 8080 | nc remote.host 80
```

### telnet - 텔넷 테스트

```bash
# 포트 연결 테스트
$ telnet 192.168.1.1 80
$ telnet google.com 443

# HTTP 테스트
$ telnet www.example.com 80
Trying 93.184.216.34...
Connected to www.example.com.
Escape character is '^]'.
GET / HTTP/1.1
Host: www.example.com

# SMTP 테스트
$ telnet mail.example.com 25

# 타임아웃 후 종료
Ctrl+]
telnet> quit
```

### curl - HTTP 테스트

```bash
# 기본 요청
$ curl http://example.com
$ curl https://api.github.com

# 헤더 포함
$ curl -i http://example.com
$ curl -I http://example.com  # HEAD 요청

# 상세 출력
$ curl -v http://example.com
$ curl -vv http://example.com

# 응답 시간 측정
$ curl -w "@-" -o /dev/null -s http://example.com << 'EOF'
    time_namelookup:  %{time_namelookup}s\n
       time_connect:  %{time_connect}s\n
    time_appconnect:  %{time_appconnect}s\n
   time_pretransfer:  %{time_pretransfer}s\n
      time_redirect:  %{time_redirect}s\n
 time_starttransfer:  %{time_starttransfer}s\n
                    ----------\n
         time_total:  %{time_total}s\n
EOF

# 리다이렉트 따라가기
$ curl -L http://example.com

# HTTP 상태 코드만
$ curl -o /dev/null -s -w "%{http_code}\n" http://example.com

# POST 요청
$ curl -X POST -d "key=value" http://example.com/api

# JSON
$ curl -X POST -H "Content-Type: application/json" \
  -d '{"key":"value"}' http://example.com/api

# 파일 업로드
$ curl -F "file=@/path/to/file" http://example.com/upload

# 인증
$ curl -u username:password http://example.com/api
$ curl -H "Authorization: Bearer TOKEN" http://example.com/api

# 쿠키
$ curl -b cookies.txt http://example.com
$ curl -c cookies.txt http://example.com

# 프록시
$ curl -x http://proxy:8080 http://example.com

# 연결 테스트
$ curl -o /dev/null -s -w "Connect: %{time_connect}s\n" http://example.com
```

---

## DNS 조회

### dig - DNS 조회 도구

```bash
# 기본 조회
$ dig google.com
; <<>> DiG 9.18.1 <<>> google.com
;; QUESTION SECTION:
;google.com.                    IN      A

;; ANSWER SECTION:
google.com.             300     IN      A       142.250.217.46

# 짧은 답변
$ dig google.com +short
142.250.217.46

# 특정 레코드 타입
$ dig google.com A      # IPv4
$ dig google.com AAAA   # IPv6
$ dig google.com MX     # Mail
$ dig google.com NS     # Name Server
$ dig google.com TXT    # TXT 레코드
$ dig google.com SOA    # Start of Authority
$ dig google.com CNAME  # Canonical Name

# 특정 DNS 서버 사용
$ dig @8.8.8.8 google.com
$ dig @1.1.1.1 google.com

# 역방향 조회
$ dig -x 8.8.8.8
$ dig -x 142.250.217.46

# 추적 모드
$ dig google.com +trace

# 모든 레코드
$ dig google.com ANY

# 배치 조회
$ dig google.com facebook.com twitter.com

# TCP 사용
$ dig google.com +tcp

# DNSSEC 검증
$ dig google.com +dnssec

# 통계 표시
$ dig google.com +stats

# 상세 정보 없이
$ dig google.com +noall +answer

# 멀티라인 출력
$ dig google.com +multiline
```

### nslookup - DNS 조회

```bash
# 기본 조회
$ nslookup google.com
Server:         192.168.1.1
Address:        192.168.1.1#53

Non-authoritative answer:
Name:   google.com
Address: 142.250.217.46

# 특정 DNS 서버
$ nslookup google.com 8.8.8.8
$ nslookup google.com 1.1.1.1

# 레코드 타입 지정
$ nslookup -type=mx google.com
$ nslookup -type=ns google.com
$ nslookup -type=txt google.com

# 역방향 조회
$ nslookup 8.8.8.8

# 인터랙티브 모드
$ nslookup
> google.com
> set type=mx
> google.com
> set type=ns
> google.com
> exit
```

### host - 간단한 DNS 조회

```bash
# 기본 조회
$ host google.com
google.com has address 142.250.217.46
google.com has IPv6 address 2404:6800:4004:820::200e
google.com mail is handled by 10 smtp.google.com.

# IPv4만
$ host -t A google.com

# IPv6만
$ host -t AAAA google.com

# MX 레코드
$ host -t MX google.com

# NS 레코드
$ host -t NS google.com

# 모든 레코드
$ host -a google.com

# 역방향 조회
$ host 8.8.8.8

# 특정 DNS 서버
$ host google.com 8.8.8.8

# 상세 모드
$ host -v google.com
```

### 시스템 DNS 설정

```bash
# DNS 서버 확인
$ cat /etc/resolv.conf
nameserver 192.168.1.1
nameserver 8.8.8.8

# systemd-resolved
$ systemd-resolve --status
$ resolvectl status

# DNS 캐시 클리어
$ sudo systemd-resolve --flush-caches
$ sudo resolvectl flush-caches

# DNS 쿼리 통계
$ resolvectl statistics
```

---

## 라우트 추적

### traceroute - 경로 추적

```bash
# 기본 사용
$ traceroute google.com
traceroute to google.com (142.250.217.46), 30 hops max, 60 byte packets
 1  192.168.1.1 (192.168.1.1)  1.234 ms  1.123 ms  1.056 ms
 2  10.0.0.1 (10.0.0.1)  5.678 ms  5.567 ms  5.456 ms
 3  203.0.113.1 (203.0.113.1)  10.123 ms  10.012 ms  9.901 ms
...

# 최대 홉 수 지정
$ traceroute -m 20 google.com

# ICMP 대신 UDP 사용
$ traceroute -I google.com

# TCP 사용
$ traceroute -T google.com

# 특정 포트
$ traceroute -p 80 google.com

# 패킷 크기
$ traceroute -q 1 google.com  # 쿼리 1개만

# 대기 시간
$ traceroute -w 2 google.com  # 2초 대기

# 인터페이스 지정
$ traceroute -i eth0 google.com

# AS 번호 표시
$ traceroute -A google.com

# 숫자만 (호스트명 해석 안 함)
$ traceroute -n google.com

# IPv6
$ traceroute6 google.com
```

### tracepath - 단순한 경로 추적

```bash
# 기본 사용
$ tracepath google.com

# MTU 발견
$ tracepath -m 1500 google.com

# 포트 지정
$ tracepath google.com/80

# IPv6
$ tracepath6 google.com
```

### mtr - 실시간 traceroute

```bash
# 설치
$ sudo apt install mtr

# 기본 사용 (인터랙티브)
$ mtr google.com

# 리포트 모드
$ mtr --report google.com
$ mtr -r -c 100 google.com  # 100개 패킷

# 횟수 지정
$ mtr -c 50 google.com

# 간격 지정
$ mtr -i 0.5 google.com

# TCP 사용
$ mtr -T google.com

# 특정 포트
$ mtr -T -P 443 google.com

# CSV 출력
$ mtr --csv google.com

# JSON 출력
$ mtr --json google.com

# 양방향 (패킷 크기 표시)
$ mtr -b google.com

# AS 번호 표시
$ mtr -z google.com
```

---

## 포트 및 소켓

### ss - 소켓 통계

```bash
# 모든 소켓
$ ss -a

# TCP만
$ ss -t
$ ss -ta    # 모든 TCP (LISTEN 포함)

# UDP만
$ ss -u
$ ss -ua

# LISTEN 상태만
$ ss -l
$ ss -lt    # TCP LISTEN
$ ss -lu    # UDP LISTEN

# 프로세스 표시
$ ss -p
$ ss -ltp   # TCP LISTEN + 프로세스

# 숫자로 표시 (포트 번호)
$ ss -n
$ ss -ltn

# 확장 정보
$ ss -e
$ ss -ltpe

# 메모리 사용량
$ ss -m

# 타이머 정보
$ ss -o

# 통계
$ ss -s
Total: 245
TCP:   12 (estab 5, closed 2, orphaned 0, timewait 2)
...

# 특정 상태
$ ss state established
$ ss state listening
$ ss state time-wait

# 특정 포트
$ ss -ltn sport = :80
$ ss -ltn sport = :22
$ ss dst :443

# 포트 범위
$ ss sport \> :1024

# 특정 주소
$ ss dst 192.168.1.100
$ ss src 192.168.1.100

# 조합
$ ss -tan state established '( dport = :80 or dport = :443 )'

# IPv4만
$ ss -4

# IPv6만
$ ss -6

# 소켓별 상세 정보
$ ss -ti
```

### netstat (레거시)

```bash
# 모든 연결
$ netstat -a

# TCP
$ netstat -t
$ netstat -ta

# UDP
$ netstat -u
$ netstat -ua

# LISTEN
$ netstat -l
$ netstat -lt

# 프로세스 표시
$ netstat -p
$ netstat -ltp

# 숫자로
$ netstat -n
$ netstat -ltn

# 라우팅 테이블
$ netstat -r

# 인터페이스 통계
$ netstat -i

# 프로토콜 통계
$ netstat -s

# 지속적 업데이트
$ netstat -c

# 특정 프로그램
$ netstat -ap | grep ssh
$ netstat -ap | grep :80
```

### lsof - 열린 파일 (네트워크 포함)

```bash
# 모든 네트워크 파일
$ sudo lsof -i

# TCP만
$ sudo lsof -i tcp

# UDP만
$ sudo lsof -i udp

# 특정 포트
$ sudo lsof -i :80
$ sudo lsof -i :22
$ sudo lsof -i tcp:80

# 포트 범위
$ sudo lsof -i :1-1024

# 특정 호스트
$ sudo lsof -i @192.168.1.100

# LISTEN 상태
$ sudo lsof -i -sTCP:LISTEN

# ESTABLISHED 상태
$ sudo lsof -i -sTCP:ESTABLISHED

# IPv4만
$ sudo lsof -i4

# IPv6만
$ sudo lsof -i6

# 특정 프로세스
$ sudo lsof -i -p 1234

# 특정 사용자
$ sudo lsof -i -u username

# 조합
$ sudo lsof -i tcp:80 -sTCP:LISTEN
```

---

## 패킷 캡처

### tcpdump - 패킷 캡처

```bash
# 기본 캡처 (root 필요)
$ sudo tcpdump

# 특정 인터페이스
$ sudo tcpdump -i eth0
$ sudo tcpdump -i any  # 모든 인터페이스

# 패킷 수 제한
$ sudo tcpdump -c 100

# 호스트 필터
$ sudo tcpdump host 192.168.1.100
$ sudo tcpdump src 192.168.1.100
$ sudo tcpdump dst 192.168.1.100

# 포트 필터
$ sudo tcpdump port 80
$ sudo tcpdump port 22 or port 23
$ sudo tcpdump portrange 20-80

# 프로토콜
$ sudo tcpdump icmp
$ sudo tcpdump tcp
$ sudo tcpdump udp

# 네트워크
$ sudo tcpdump net 192.168.1.0/24
$ sudo tcpdump net 192.168.1.0 mask 255.255.255.0

# 파일로 저장
$ sudo tcpdump -w capture.pcap
$ sudo tcpdump -i eth0 -w capture.pcap -c 1000

# 파일 읽기
$ sudo tcpdump -r capture.pcap

# 상세 출력
$ sudo tcpdump -v
$ sudo tcpdump -vv
$ sudo tcpdump -vvv

# ASCII로 표시
$ sudo tcpdump -A

# 헥스와 ASCII
$ sudo tcpdump -X

# 타임스탬프
$ sudo tcpdump -tttt

# 패킷 크기
$ sudo tcpdump -s 0  # 전체 패킷
$ sudo tcpdump -s 100  # 100바이트만

# 조합 필터
$ sudo tcpdump -i eth0 'tcp port 80 and host 192.168.1.100'
$ sudo tcpdump 'tcp[tcpflags] & (tcp-syn) != 0'
$ sudo tcpdump 'tcp[13] & 2 != 0'  # SYN 패킷

# HTTP 트래픽
$ sudo tcpdump -i eth0 'tcp port 80 and (((ip[2:2] - ((ip[0]&0xf)<<2)) - ((tcp[12]&0xf0)>>2)) != 0)'

# DNS 쿼리
$ sudo tcpdump -i eth0 udp port 53

# 파일 크기 제한 (로테이션)
$ sudo tcpdump -i eth0 -w capture.pcap -C 100  # 100MB마다
$ sudo tcpdump -i eth0 -w capture.pcap -C 100 -W 10  # 10개 파일 유지

# 시간 제한
$ sudo tcpdump -i eth0 -G 3600 -w capture_%Y%m%d_%H%M%S.pcap
```

### wireshark / tshark

```bash
# tshark 설치
$ sudo apt install tshark

# 기본 캡처
$ sudo tshark -i eth0

# 패킷 수 제한
$ sudo tshark -i eth0 -c 100

# 파일 저장
$ sudo tshark -i eth0 -w capture.pcapng

# 파일 읽기
$ tshark -r capture.pcapng

# 필터
$ sudo tshark -i eth0 -f "port 80"
$ sudo tshark -i eth0 -f "host 192.168.1.100"

# 디스플레이 필터
$ tshark -r capture.pcapng -Y "http"
$ tshark -r capture.pcapng -Y "ip.addr == 192.168.1.100"

# 통계
$ tshark -r capture.pcapng -q -z io,stat,10

# 프로토콜 계층
$ tshark -r capture.pcapng -q -z io,phs

# 대화 통계
$ tshark -r capture.pcapng -q -z conv,ip
```

---

## 네트워크 분석 도구

### iftop - 실시간 대역폭 모니터

```bash
# 설치
$ sudo apt install iftop

# 기본 사용
$ sudo iftop

# 특정 인터페이스
$ sudo iftop -i eth0

# 포트 표시
$ sudo iftop -P

# 텍스트 모드
$ sudo iftop -t

# 네트워크 필터
$ sudo iftop -f "port 80"
```

### nethogs - 프로세스별 대역폭

```bash
# 설치
$ sudo apt install nethogs

# 기본 사용
$ sudo nethogs

# 특정 인터페이스
$ sudo nethogs eth0

# 업데이트 간격
$ sudo nethogs -d 5

# KB/s 단위
$ sudo nethogs -v 1
```

### iperf3 - 대역폭 테스트

```bash
# 설치
$ sudo apt install iperf3

# 서버 모드
$ iperf3 -s

# 클라이언트 (서버 IP로 테스트)
$ iperf3 -c 192.168.1.100

# UDP 테스트
$ iperf3 -c 192.168.1.100 -u

# 양방향 테스트
$ iperf3 -c 192.168.1.100 --bidir

# 10초간 테스트
$ iperf3 -c 192.168.1.100 -t 10

# 대역폭 제한
$ iperf3 -c 192.168.1.100 -b 10M

# 포트 지정
$ iperf3 -s -p 5555
$ iperf3 -c 192.168.1.100 -p 5555
```

---

## 실전 예제

### 예제 1: 종합 네트워크 진단

```bash
#!/bin/bash
# network_check.sh

echo "=== Network Diagnostic ==="
echo "Time: $(date)"
echo

echo "1. Network Interfaces:"
ip -br addr
echo

echo "2. Default Route:"
ip route | grep default
echo

echo "3. DNS Servers:"
cat /etc/resolv.conf | grep nameserver
echo

echo "4. Ping Gateway:"
GW=$(ip route | grep default | awk '{print $3}')
ping -c 3 -W 2 $GW
echo

echo "5. Ping Public DNS:"
ping -c 3 -W 2 8.8.8.8
echo

echo "6. DNS Resolution:"
dig +short google.com
echo

echo "7. HTTP Connectivity:"
curl -I -s -m 5 http://www.google.com | head -1
echo

echo "8. Listening Ports:"
ss -ltn
echo

echo "9. Active Connections:"
ss -tun | head -10
```

### 예제 2: 포트 스캐너

```bash
#!/bin/bash
# port_scan.sh

TARGET=$1
START_PORT=${2:-1}
END_PORT=${3:-1000}

if [ -z "$TARGET" ]; then
    echo "Usage: $0 <target> [start_port] [end_port]"
    exit 1
fi

echo "Scanning $TARGET from port $START_PORT to $END_PORT..."

for port in $(seq $START_PORT $END_PORT); do
    (echo > /dev/tcp/$TARGET/$port) 2>/dev/null && \
        echo "Port $port is open"
done
```

---

## 문제 해결

### 인터넷 연결 안 될 때

```bash
# 1단계: 인터페이스 확인
$ ip link show

# 2단계: IP 주소 확인
$ ip addr show

# 3단계: 게이트웨이 Ping
$ ping -c 3 $(ip route | grep default | awk '{print $3}')

# 4단계: 공인 IP Ping
$ ping -c 3 8.8.8.8

# 5단계: DNS 확인
$ dig google.com
```

---

## 요약

네트워크 진단 도구:

1. **연결 테스트**: ping, arping, nc, telnet
2. **DNS**: dig, nslookup, host
3. **경로**: traceroute, mtr
4. **소켓**: ss, netstat, lsof
5. **패킷**: tcpdump, tshark
6. **분석**: iftop, nethogs, iperf3

---

[다음: SSH →](ssh.md)

[← 네트워크 설정으로 돌아가기](configuration.md)

[← 목차로 돌아가기](../README.md)
