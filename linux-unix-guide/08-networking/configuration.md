# 네트워크 설정

## 목차
- [네트워크 기본 개념](#네트워크-기본-개념)
- [ip 명령어](#ip-명령어)
- [ifconfig (레거시)](#ifconfig-레거시)
- [NetworkManager](#networkmanager)
- [netplan (Ubuntu)](#netplan-ubuntu)
- [systemd-networkd](#systemd-networkd)
- [실전 예제](#실전 예제)

---

## 네트워크 기본 개념

### 네트워크 인터페이스

```bash
# 네트워크 인터페이스 유형:
# - lo: 루프백 (127.0.0.1)
# - eth0, eth1: 이더넷
# - wlan0, wlan1: 무선
# - enp0s3: Predictable Network Interface Names
# - br0: 브리지
# - docker0: Docker 브리지

# 인터페이스 이름 규칙 (Systemd):
# en: 이더넷
# wl: 무선 LAN
# ww: 무선 WAN (WWAN)
# p<slot>: PCI 슬롯
# s<slot>: hotplug 슬롯
# 예: enp0s3 = 이더넷, PCI버스 0, 슬롯 3
```

### IP 주소 기초

```bash
# IPv4 클래스:
# Class A: 10.0.0.0/8 (10.0.0.0 - 10.255.255.255)
# Class B: 172.16.0.0/12 (172.16.0.0 - 172.31.255.255)
# Class C: 192.168.0.0/16 (192.168.0.0 - 192.168.255.255)

# CIDR 표기법:
# /24 = 255.255.255.0 (256 주소)
# /16 = 255.255.0.0 (65536 주소)
# /8 = 255.0.0.0 (16777216 주소)

# 특수 주소:
# 127.0.0.1: 루프백
# 0.0.0.0: 모든 인터페이스
# 255.255.255.255: 브로드캐스트
```

---

## ip 명령어

### 인터페이스 관리

```bash
# 모든 인터페이스 보기
$ ip link show
$ ip link
$ ip l

# 특정 인터페이스
$ ip link show eth0
$ ip l show dev eth0

# 간단한 정보만
$ ip -brief link
$ ip -br l
lo               UNKNOWN        00:00:00:00:00:00 <LOOPBACK,UP,LOWER_UP>
eth0             UP             08:00:27:xx:xx:xx <BROADCAST,MULTICAST,UP,LOWER_UP>

# 통계 정보
$ ip -s link
$ ip -s -s link  # 더 자세히

# 인터페이스 활성화
$ sudo ip link set eth0 up

# 인터페이스 비활성화
$ sudo ip link set eth0 down

# MTU 설정
$ sudo ip link set eth0 mtu 9000

# MAC 주소 변경
$ sudo ip link set eth0 address 00:11:22:33:44:55

# 프로미스큐어스 모드
$ sudo ip link set eth0 promisc on
$ sudo ip link set eth0 promisc off

# 멀티캐스트
$ sudo ip link set eth0 multicast on
```

### IP 주소 관리

```bash
# 모든 IP 주소 보기
$ ip address show
$ ip addr
$ ip a

# 특정 인터페이스
$ ip addr show eth0
$ ip a show dev eth0

# 간단히
$ ip -brief address
$ ip -br a
lo               UNKNOWN        127.0.0.1/8 ::1/128
eth0             UP             192.168.1.100/24 fe80::a00:27ff:fexx:xxxx/64

# IPv4만
$ ip -4 addr

# IPv6만
$ ip -6 addr

# IP 주소 추가
$ sudo ip addr add 192.168.1.100/24 dev eth0

# 브로드캐스트 지정
$ sudo ip addr add 192.168.1.100/24 broadcast 192.168.1.255 dev eth0

# 보조 IP 추가
$ sudo ip addr add 192.168.1.101/24 dev eth0

# IP 주소 삭제
$ sudo ip addr del 192.168.1.100/24 dev eth0

# 모든 IP 삭제
$ sudo ip addr flush dev eth0
$ sudo ip addr flush dev eth0 scope global  # global만

# 라벨 지정
$ sudo ip addr add 192.168.1.100/24 dev eth0 label eth0:0
$ ip addr show dev eth0
```

### 라우팅 관리

```bash
# 라우팅 테이블 보기
$ ip route show
$ ip route
$ ip r
default via 192.168.1.1 dev eth0 proto dhcp src 192.168.1.100 metric 100
192.168.1.0/24 dev eth0 proto kernel scope link src 192.168.1.100

# IPv4만
$ ip -4 route

# IPv6만
$ ip -6 route

# 특정 목적지 라우트
$ ip route get 8.8.8.8
8.8.8.8 via 192.168.1.1 dev eth0 src 192.168.1.100 uid 1000
    cache

# 기본 게이트웨이 추가
$ sudo ip route add default via 192.168.1.1
$ sudo ip route add default via 192.168.1.1 dev eth0

# 특정 네트워크 라우트 추가
$ sudo ip route add 10.0.0.0/8 via 192.168.1.254
$ sudo ip route add 172.16.0.0/12 via 192.168.1.254 dev eth0

# 메트릭 지정
$ sudo ip route add default via 192.168.1.1 metric 100

# 라우트 삭제
$ sudo ip route del default via 192.168.1.1
$ sudo ip route del 10.0.0.0/8

# 모든 라우트 삭제
$ sudo ip route flush table main

# 특정 인터페이스 라우트만 삭제
$ sudo ip route flush dev eth0
```

### 네이버 (ARP) 관리

```bash
# ARP 테이블 보기
$ ip neigh show
$ ip neigh
$ ip n
192.168.1.1 dev eth0 lladdr 00:11:22:33:44:55 REACHABLE
192.168.1.50 dev eth0 lladdr aa:bb:cc:dd:ee:ff STALE

# 특정 인터페이스
$ ip neigh show dev eth0

# ARP 엔트리 추가
$ sudo ip neigh add 192.168.1.200 lladdr 00:11:22:33:44:55 dev eth0

# ARP 엔트리 삭제
$ sudo ip neigh del 192.168.1.200 dev eth0

# ARP 캐시 클리어
$ sudo ip neigh flush dev eth0
$ sudo ip neigh flush all
```

### 네임스페이스

```bash
# 네트워크 네임스페이스 목록
$ ip netns list

# 네임스페이스 생성
$ sudo ip netns add test_ns

# 네임스페이스에서 명령 실행
$ sudo ip netns exec test_ns ip addr

# 네임스페이스 삭제
$ sudo ip netns del test_ns

# veth 페어 생성
$ sudo ip link add veth0 type veth peer name veth1

# veth를 네임스페이스로 이동
$ sudo ip link set veth1 netns test_ns

# 네임스페이스 내부에서 설정
$ sudo ip netns exec test_ns ip addr add 10.0.0.1/24 dev veth1
$ sudo ip netns exec test_ns ip link set veth1 up
```

---

## ifconfig (레거시)

### 기본 사용법

```bash
# 모든 인터페이스
$ ifconfig
eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.1.100  netmask 255.255.255.0  broadcast 192.168.1.255
        inet6 fe80::a00:27ff:fexx:xxxx  prefixlen 64  scopeid 0x20<link>
        ether 08:00:27:xx:xx:xx  txqueuelen 1000  (Ethernet)
        RX packets 12345  bytes 1234567 (1.2 MB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 6789  bytes 678901 (678.9 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

# 특정 인터페이스
$ ifconfig eth0

# 비활성 인터페이스 포함
$ ifconfig -a

# IP 주소 설정
$ sudo ifconfig eth0 192.168.1.100
$ sudo ifconfig eth0 192.168.1.100 netmask 255.255.255.0

# 브로드캐스트 설정
$ sudo ifconfig eth0 192.168.1.100 netmask 255.255.255.0 broadcast 192.168.1.255

# 인터페이스 활성화/비활성화
$ sudo ifconfig eth0 up
$ sudo ifconfig eth0 down

# MTU 설정
$ sudo ifconfig eth0 mtu 9000

# 프로미스큐어스 모드
$ sudo ifconfig eth0 promisc
$ sudo ifconfig eth0 -promisc

# 보조 IP (alias)
$ sudo ifconfig eth0:0 192.168.1.101 netmask 255.255.255.0
$ sudo ifconfig eth0:1 192.168.1.102 netmask 255.255.255.0

# 삭제
$ sudo ifconfig eth0:0 down
```

### route 명령어

```bash
# 라우팅 테이블
$ route -n
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
0.0.0.0         192.168.1.1     0.0.0.0         UG    100    0        0 eth0
192.168.1.0     0.0.0.0         255.255.255.0   U     0      0        0 eth0

# 기본 게이트웨이 추가
$ sudo route add default gw 192.168.1.1
$ sudo route add default gw 192.168.1.1 eth0

# 네트워크 라우트 추가
$ sudo route add -net 10.0.0.0/8 gw 192.168.1.254
$ sudo route add -net 10.0.0.0 netmask 255.0.0.0 gw 192.168.1.254

# 호스트 라우트 추가
$ sudo route add -host 192.168.1.200 gw 192.168.1.254

# 라우트 삭제
$ sudo route del default gw 192.168.1.1
$ sudo route del -net 10.0.0.0/8
```

---

## NetworkManager

### nmcli 명령어

```bash
# 일반 상태
$ nmcli general status
STATE      CONNECTIVITY  WIFI-HW  WIFI     WWAN-HW  WWAN
connected  full          enabled  enabled  enabled  enabled

# 네트워크 연결 상태
$ nmcli networking
enabled

# 활성화/비활성화
$ nmcli networking off
$ nmcli networking on

# 연결 목록
$ nmcli connection show
$ nmcli con show
NAME                UUID                                  TYPE      DEVICE
Wired connection 1  a1b2c3d4-e5f6-7890-abcd-ef1234567890  ethernet  eth0
WiFi-Home           b2c3d4e5-f6a7-8901-bcde-fa2345678901  wifi      wlan0

# 활성 연결만
$ nmcli connection show --active
$ nmcli con show -a

# 연결 세부정보
$ nmcli connection show "Wired connection 1"
$ nmcli con show eth0

# 장치 목록
$ nmcli device status
$ nmcli dev status
DEVICE  TYPE      STATE      CONNECTION
eth0    ethernet  connected  Wired connection 1
wlan0   wifi      connected  WiFi-Home
lo      loopback  unmanaged  --

# 장치 세부정보
$ nmcli device show eth0
$ nmcli dev show eth0

# WiFi 스캔
$ nmcli device wifi list
$ nmcli dev wifi list
IN-USE  SSID          MODE   CHAN  RATE        SIGNAL  BARS  SECURITY
*       WiFi-Home     Infra  6     130 Mbit/s  85      ▂▄▆█  WPA2
        Office-WiFi   Infra  11    54 Mbit/s   45      ▂▄__  WPA2

# WiFi 재스캔
$ nmcli device wifi rescan
```

### 연결 관리

```bash
# 새 유선 연결 (DHCP)
$ nmcli connection add type ethernet con-name eth0-dhcp ifname eth0

# 새 유선 연결 (고정 IP)
$ nmcli connection add type ethernet con-name eth0-static ifname eth0 \
  ip4 192.168.1.100/24 gw4 192.168.1.1

# DNS 추가
$ nmcli connection modify eth0-static ipv4.dns "8.8.8.8 8.8.4.4"

# 추가 IP 주소
$ nmcli connection modify eth0-static +ipv4.addresses 192.168.1.101/24

# 자동 연결 설정
$ nmcli connection modify eth0-static connection.autoconnect yes

# WiFi 연결
$ nmcli device wifi connect WiFi-SSID password "wifi-password"
$ nmcli dev wifi connect WiFi-SSID password "wifi-password" name MyWiFi

# 숨겨진 WiFi
$ nmcli dev wifi connect WiFi-SSID password "wifi-password" hidden yes

# 연결 활성화
$ nmcli connection up eth0-static
$ nmcli con up id eth0-static

# 연결 비활성화
$ nmcli connection down eth0-static

# 연결 삭제
$ nmcli connection delete eth0-static

# 연결 수정
$ nmcli connection modify eth0-static ipv4.addresses 192.168.1.200/24
$ nmcli connection modify eth0-static ipv4.gateway 192.168.1.1
$ nmcli connection modify eth0-static ipv4.dns "8.8.8.8 1.1.1.1"
$ nmcli connection modify eth0-static ipv4.method manual

# DHCP로 변경
$ nmcli connection modify eth0-static ipv4.method auto

# 연결 재로드
$ nmcli connection reload

# 장치 재연결
$ nmcli device reapply eth0
$ nmcli device disconnect eth0
$ nmcli device connect eth0
```

### 인터랙티브 편집

```bash
# 연결 편집
$ nmcli connection edit eth0-static

# 또는 새 연결 생성
$ nmcli connection edit type ethernet con-name new-conn

# 인터랙티브 모드에서:
nmcli> print
nmcli> set ipv4.addresses 192.168.1.100/24
nmcli> set ipv4.gateway 192.168.1.1
nmcli> set ipv4.dns 8.8.8.8 8.8.4.4
nmcli> set ipv4.method manual
nmcli> save
nmcli> activate
nmcli> quit
```

---

## netplan (Ubuntu)

### Netplan 설정

```bash
# 설정 파일 위치
$ ls /etc/netplan/
01-netcfg.yaml

# 설정 예제 - DHCP
$ sudo vi /etc/netplan/01-netcfg.yaml
network:
  version: 2
  renderer: networkd
  ethernets:
    eth0:
      dhcp4: true

# 고정 IP
network:
  version: 2
  renderer: networkd
  ethernets:
    eth0:
      addresses:
        - 192.168.1.100/24
      gateway4: 192.168.1.1
      nameservers:
        addresses:
          - 8.8.8.8
          - 8.8.4.4

# 여러 인터페이스
network:
  version: 2
  renderer: networkd
  ethernets:
    eth0:
      addresses: [192.168.1.100/24]
      gateway4: 192.168.1.1
      nameservers:
        addresses: [8.8.8.8, 8.8.4.4]
    eth1:
      dhcp4: yes

# 고급 설정
network:
  version: 2
  renderer: networkd
  ethernets:
    eth0:
      addresses:
        - 192.168.1.100/24
        - 192.168.1.101/24  # 추가 IP
      gateway4: 192.168.1.1
      nameservers:
        addresses: [8.8.8.8, 1.1.1.1]
        search: [example.com, local]
      routes:
        - to: 10.0.0.0/8
          via: 192.168.1.254
          metric: 100
      mtu: 9000
      optional: true

# WiFi 설정
network:
  version: 2
  renderer: networkd
  wifis:
    wlan0:
      access-points:
        "WiFi-SSID":
          password: "wifi-password"
      dhcp4: yes

# 설정 확인
$ sudo netplan generate

# 테스트 (120초 후 자동 롤백)
$ sudo netplan try

# 적용
$ sudo netplan apply

# 디버그 모드
$ sudo netplan --debug apply

# 현재 설정 보기
$ sudo netplan get
```

### NetworkManager 렌더러

```bash
# NetworkManager 사용
network:
  version: 2
  renderer: NetworkManager
  ethernets:
    eth0:
      dhcp4: true

# 적용 후 nmcli 사용 가능
```

---

## systemd-networkd

### 설정 파일

```bash
# 설정 파일 위치
# /etc/systemd/network/
# /run/systemd/network/
# /lib/systemd/network/

# 파일 이름 규칙: ##-name.network
# 번호 순서로 처리됨

# DHCP 예제
$ sudo vi /etc/systemd/network/20-wired.network
[Match]
Name=eth0

[Network]
DHCP=yes

# 고정 IP
$ sudo vi /etc/systemd/network/20-wired.network
[Match]
Name=eth0

[Network]
Address=192.168.1.100/24
Gateway=192.168.1.1
DNS=8.8.8.8
DNS=8.8.4.4

# 여러 인터페이스 매칭
[Match]
Name=eth* en*

# 고급 설정
[Match]
Name=eth0

[Network]
Address=192.168.1.100/24
Address=192.168.1.101/24
Gateway=192.168.1.1
DNS=8.8.8.8
DNS=1.1.1.1
Domains=example.com

[Route]
Destination=10.0.0.0/8
Gateway=192.168.1.254
Metric=100

# VLAN
[NetDev]
Name=vlan10
Kind=vlan

[VLAN]
Id=10

# Bridge
[NetDev]
Name=br0
Kind=bridge

# 서비스 관리
$ sudo systemctl enable systemd-networkd
$ sudo systemctl start systemd-networkd
$ sudo systemctl restart systemd-networkd
$ sudo systemctl status systemd-networkd

# 네트워크 상태
$ networkctl
$ networkctl status
$ networkctl status eth0

# 재설정
$ sudo networkctl reload
$ sudo networkctl reconfigure eth0
```

---

## 실전 예제

### 예제 1: 네트워크 설정 백업 및 복원

```bash
# IP 명령어 백업
#!/bin/bash
BACKUP_FILE="/root/network-backup-$(date +%Y%m%d).sh"

{
    echo "#!/bin/bash"
    echo "# Network configuration backup - $(date)"
    echo

    ip addr show | grep -E "inet |inet6 " | \
    while read -r line; do
        echo "# $line"
    done

    echo
    ip route show | while read -r line; do
        echo "ip route add $line 2>/dev/null || true"
    done
} > "$BACKUP_FILE"

chmod +x "$BACKUP_FILE"
```

### 예제 2: 네트워크 진단 스크립트

```bash
#!/bin/bash
# network_diag.sh

echo "=== Network Diagnostic ==="
echo

echo "1. Network Interfaces:"
ip -br addr
echo

echo "2. Default Gateway:"
ip route | grep default
echo

echo "3. DNS Servers:"
cat /etc/resolv.conf | grep nameserver
echo

echo "4. Internet Connectivity:"
ping -c 3 8.8.8.8 > /dev/null 2>&1 && echo "OK" || echo "FAILED"
echo

echo "5. DNS Resolution:"
nslookup google.com > /dev/null 2>&1 && echo "OK" || echo "FAILED"
echo

echo "6. Active Connections:"
ss -tuln | grep LISTEN
```

---

## 문제 해결

### 인터페이스가 안 올라올 때

```bash
# 상태 확인
$ ip link show eth0
$ nmcli device status

# 드라이버 확인
$ lspci -k | grep -A 3 Ethernet
$ ethtool -i eth0

# 수동으로 올리기
$ sudo ip link set eth0 up
$ sudo ifconfig eth0 up

# NetworkManager 재시작
$ sudo systemctl restart NetworkManager
```

### IP가 안 잡힐 때

```bash
# DHCP 갱신
$ sudo dhclient -r eth0  # 릴리스
$ sudo dhclient eth0     # 요청

# 또는
$ sudo nmcli connection down eth0
$ sudo nmcli connection up eth0

# 로그 확인
$ journalctl -u NetworkManager -f
$ journalctl -u systemd-networkd -f
```

---

## 요약

네트워크 설정 도구:

1. **ip** - 현대적인 표준 도구
2. **nmcli** - NetworkManager CLI
3. **netplan** - Ubuntu 선언적 설정
4. **systemd-networkd** - Systemd 네트워크 관리

---

[다음: 네트워크 진단 →](diagnostics.md)

[← 시스템 모니터링으로 돌아가기](../06-processes/monitoring.md)

[← 목차로 돌아가기](../README.md)
