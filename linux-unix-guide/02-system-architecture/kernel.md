# 커널의 이해

## 목차
- [커널이란?](#커널이란)
- [커널의 역할](#커널의-역할)
- [커널 아키텍처](#커널-아키텍처)
- [커널 vs 유저 스페이스](#커널-vs-유저-스페이스)
- [시스템 콜](#시스템-콜)
- [커널 모듈](#커널-모듈)
- [커널 버전 관리](#커널-버전-관리)
- [실습 예제](#실습-예제)

---

## 커널이란?

### 정의

**커널(Kernel)**은 운영체제의 핵심으로, 하드웨어와 소프트웨어 사이의 인터페이스 역할을 합니다.

```
┌─────────────────────────────────────┐
│      User Applications              │  사용자 애플리케이션
│  (Firefox, LibreOffice, etc.)       │
├─────────────────────────────────────┤
│      System Libraries               │  시스템 라이브러리
│  (glibc, libssl, etc.)              │
├─────────────────────────────────────┤
│      System Call Interface          │  시스템 콜 인터페이스
╞═════════════════════════════════════╡  ← 커널 경계
│                                     │
│          Linux Kernel               │  리눅스 커널
│                                     │
│  ┌──────────────────────────────┐  │
│  │  Process Scheduler           │  │  프로세스 스케줄러
│  ├──────────────────────────────┤  │
│  │  Memory Management           │  │  메모리 관리
│  ├──────────────────────────────┤  │
│  │  Virtual File System (VFS)   │  │  가상 파일시스템
│  ├──────────────────────────────┤  │
│  │  Network Stack               │  │  네트워크 스택
│  ├──────────────────────────────┤  │
│  │  Device Drivers              │  │  디바이스 드라이버
│  └──────────────────────────────┘  │
├─────────────────────────────────────┤
│         Hardware                    │  하드웨어
│  (CPU, Memory, Disk, Network)       │
└─────────────────────────────────────┘
```

### 커널의 종류

**1. 모놀리식 커널 (Monolithic Kernel)**
- Linux, Unix, BSD
- 모든 기능이 커널 공간에서 실행
- 빠른 성능
- 한 부분의 버그가 전체 시스템 다운 가능

```
┌───────────────────────────┐
│    Kernel Space           │
│  ┌─────────────────────┐  │
│  │  All OS Services    │  │
│  │  - Process Mgmt     │  │
│  │  - Memory Mgmt      │  │
│  │  - File System      │  │
│  │  - Network Stack    │  │
│  │  - Device Drivers   │  │
│  └─────────────────────┘  │
└───────────────────────────┘
```

**2. 마이크로커널 (Microkernel)**
- Minix, QNX, L4
- 최소 기능만 커널에, 나머지는 유저 스페이스
- 안정적 (격리성)
- 상대적으로 느림 (컨텍스트 스위칭)

```
┌───────────────────────────┐
│    User Space             │
│  ┌─────────────────────┐  │
│  │  File System        │  │
│  │  Device Drivers     │  │
│  │  Network Stack      │  │
│  └─────────────────────┘  │
├───────────────────────────┤
│    Kernel Space           │
│  ┌─────────────────────┐  │
│  │  IPC                │  │
│  │  Basic Memory Mgmt  │  │
│  │  Basic Scheduling   │  │
│  └─────────────────────┘  │
└───────────────────────────┘
```

**3. 하이브리드 커널**
- Windows NT, macOS (XNU)
- 모놀리식과 마이크로커널의 장점 결합

---

## 커널의 역할

### 1. 프로세스 관리 (Process Management)

**역할:**
- 프로세스 생성, 실행, 종료
- CPU 스케줄링
- 멀티태스킹

**주요 개념:**
```bash
# 프로세스 확인
ps aux
# USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
# root         1  0.0  0.1 169644 13532 ?        Ss   10:00   0:01 /sbin/init
# root         2  0.0  0.0      0     0 ?        S    10:00   0:00 [kthreadd]

# PID 1: init (또는 systemd) - 모든 프로세스의 부모
# PID 2: kthreadd - 커널 스레드의 부모
```

**프로세스 상태:**
```
R (Running)     : 실행 중 또는 실행 대기
S (Sleeping)    : 대기 중 (인터럽트 가능)
D (Disk Sleep)  : 디스크 I/O 대기 (인터럽트 불가)
T (Stopped)     : 정지됨
Z (Zombie)      : 종료되었지만 부모가 정리 안 함
```

**CPU 스케줄러:**
```bash
# CFS (Completely Fair Scheduler) - 리눅스 기본 스케줄러
# 모든 프로세스에게 공정한 CPU 시간 할당

# 실시간 스케줄러
chrt -f 99 /path/to/realtime/app  # FIFO 스케줄러
chrt -r 50 /path/to/app           # Round-Robin 스케줄러
```

### 2. 메모리 관리 (Memory Management)

**역할:**
- 물리 메모리 할당
- 가상 메모리 관리
- 페이징과 스와핑

**가상 메모리:**
```
프로세스의 가상 주소 공간

0xFFFFFFFF ┌──────────────┐
           │   Kernel     │  1GB (커널 공간)
0xC0000000 ├──────────────┤
           │    Stack     │  ↓ 아래로 성장
           │              │
           │     ...      │
           │              │
           │     Heap     │  ↑ 위로 성장
           ├──────────────┤
           │     BSS      │  초기화 안 된 데이터
           ├──────────────┤
           │     Data     │  초기화된 데이터
           ├──────────────┤
           │     Text     │  프로그램 코드
0x00000000 └──────────────┘
```

**메모리 정보 확인:**
```bash
# 전체 메모리 현황
free -h
#               total        used        free      shared  buff/cache   available
# Mem:           15Gi       4.2Gi       8.1Gi       324Mi       3.3Gi        10Gi
# Swap:         2.0Gi          0B       2.0Gi

# 프로세스별 메모리 사용
ps aux --sort=-%mem | head -10

# 메모리 맵 확인
cat /proc/self/maps
# 00400000-00452000 r-xp 00000000 08:01 1234  /bin/bash
# 00651000-00652000 r--p 00051000 08:01 1234  /bin/bash
# 00652000-0065b000 rw-p 00052000 08:01 1234  /bin/bash
```

**페이지 폴트:**
```bash
# Minor page fault: 메모리에 있지만 페이지 테이블에 없음
# Major page fault: 디스크에서 로드 필요

# 페이지 폴트 통계
ps -o min_flt,maj_flt,cmd -p $$
# MINFL  MAJFL CMD
#  2345     12 bash
```

### 3. 파일 시스템 관리

**VFS (Virtual File System):**
- 다양한 파일시스템에 대한 추상화 계층
- 일관된 인터페이스 제공

```
┌────────────────────────────────────┐
│   User Space Applications          │
│   (open, read, write, close)       │
├────────────────────────────────────┤
│   VFS Layer                        │
│   (추상화 인터페이스)              │
├────┬───────┬────────┬──────────────┤
│ext4│ XFS   │ Btrfs  │ NFS  │ tmpfs│
└────┴───────┴────────┴──────────────┘
```

**파일시스템 정보:**
```bash
# 마운트된 파일시스템
mount | column -t
# /dev/sda1  on  /       type  ext4   (rw,relatime)
# tmpfs      on  /run    type  tmpfs  (rw,nosuid,nodev)
# /dev/sdb1  on  /data   type  xfs    (rw,relatime)

# 파일시스템 타입 확인
df -T
# Filesystem     Type      Size  Used Avail Use% Mounted on
# /dev/sda1      ext4      100G   45G   50G  48% /
# tmpfs          tmpfs     7.8G  1.5G  6.3G  20% /run

# VFS 통계
cat /proc/filesystems
# nodev   sysfs
# nodev   tmpfs
#         ext4
#         xfs
```

### 4. 디바이스 드라이버 관리

**역할:**
- 하드웨어와 통신
- 디바이스 추상화

**디바이스 파일:**
```bash
# /dev 디렉토리의 디바이스 파일
ls -l /dev/sd*
# brw-rw---- 1 root disk 8, 0 Jan 17 10:00 /dev/sda
# brw-rw---- 1 root disk 8, 1 Jan 17 10:00 /dev/sda1
# brw-rw---- 1 root disk 8, 2 Jan 17 10:00 /dev/sda2

# b: 블록 디바이스 (디스크)
# c: 문자 디바이스 (키보드, 마우스)
# 8, 0: 주 번호(major), 부 번호(minor)

# 문자 디바이스 예제
ls -l /dev/tty*
# crw--w---- 1 root tty 4, 0 Jan 17 10:00 /dev/tty0
# crw--w---- 1 user tty 4, 1 Jan 17 10:30 /dev/tty1

# 특수 디바이스
ls -l /dev/null /dev/zero /dev/random
# crw-rw-rw- 1 root root 1, 3 Jan 17 10:00 /dev/null
# crw-rw-rw- 1 root root 1, 5 Jan 17 10:00 /dev/zero
# crw-rw-rw- 1 root root 1, 8 Jan 17 10:00 /dev/random
```

### 5. 네트워크 스택

**TCP/IP 스택:**
```
┌──────────────────┐
│  Application     │  HTTP, FTP, SSH
├──────────────────┤
│  Transport       │  TCP, UDP
├──────────────────┤
│  Network         │  IP, ICMP
├──────────────────┤
│  Data Link       │  Ethernet, WiFi
├──────────────────┤
│  Physical        │  하드웨어
└──────────────────┘
```

**네트워크 정보:**
```bash
# 네트워크 인터페이스
ip link show
# 1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue
# 2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500

# 소켓 통계
ss -s
# Total: 1234 (kernel 1500)
# TCP:   567 (estab 123, closed 234, orphaned 0, synrecv 0, timewait 100)

# 네트워크 통계
netstat -i
# Iface      MTU    RX-OK RX-ERR RX-DRP RX-OVR    TX-OK TX-ERR TX-DRP TX-OVR Flg
# eth0      1500  1234567      0      0 0       9876543      0      0      0 BMRU
# lo       65536    45678      0      0 0         45678      0      0      0 LRU
```

---

## 커널 vs 유저 스페이스

### 권한 레벨

**CPU 보호 링:**
```
┌─────────────────┐
│   Ring 3        │  User Mode (가장 낮은 권한)
│   User Space    │  - 애플리케이션 실행
│                 │  - 제한된 명령어만 실행
├─────────────────┤
│   Ring 0        │  Kernel Mode (최고 권한)
│   Kernel Space  │  - 하드웨어 직접 접근
│                 │  - 모든 명령어 실행
└─────────────────┘
```

### 메모리 분리

```bash
# 커널 메모리와 유저 메모리는 분리됨
cat /proc/1/maps | head -5
# 유저 스페이스 메모리

cat /proc/kallsyms | head -5
# 커널 심볼 주소 (커널 공간)
# 0000000000000000 A irq_stack_union
# 0000000000000000 A __per_cpu_start
```

### 권한 확인

```bash
# 현재 실행 모드 확인 (간접적)
# 유저 프로세스
ps aux | grep $$

# 커널 스레드 (대괄호로 표시)
ps aux | grep '\[.*\]'
# root         2  0.0  0.0      0     0 ?        S    10:00   0:00 [kthreadd]
# root         3  0.0  0.0      0     0 ?        I<   10:00   0:00 [rcu_gp]
```

---

## 시스템 콜

### 시스템 콜이란?

유저 스페이스에서 커널 서비스를 요청하는 인터페이스입니다.

**플로우:**
```
1. 애플리케이션: read() 함수 호출
        ↓
2. C 라이브러리 (glibc): 시스템 콜 래퍼
        ↓
3. CPU 인터럽트 발생 (software interrupt)
        ↓
4. User Mode → Kernel Mode 전환
        ↓
5. 커널: 시스템 콜 핸들러 실행
        ↓
6. 하드웨어 접근 (디스크, 네트워크 등)
        ↓
7. Kernel Mode → User Mode 전환
        ↓
8. 결과 반환
```

### 시스템 콜 종류

**프로세스 제어:**
```c
fork()    // 새 프로세스 생성
exec()    // 프로그램 실행
exit()    // 프로세스 종료
wait()    // 자식 프로세스 대기
kill()    // 시그널 전송
```

**파일 관리:**
```c
open()    // 파일 열기
read()    // 읽기
write()   // 쓰기
close()   // 닫기
lseek()   // 파일 포인터 이동
stat()    // 파일 정보
```

**디렉토리 관리:**
```c
mkdir()   // 디렉토리 생성
rmdir()   // 디렉토리 삭제
opendir() // 디렉토리 열기
readdir() // 디렉토리 읽기
```

**네트워킹:**
```c
socket()  // 소켓 생성
bind()    // 주소 바인딩
listen()  // 연결 대기
accept()  // 연결 수락
send()    // 데이터 전송
recv()    // 데이터 수신
```

### 시스템 콜 추적

```bash
# strace - 시스템 콜 추적 도구
strace ls
# execve("/usr/bin/ls", ["ls"], 0x7ffe...) = 0
# brk(NULL)                               = 0x55f0...
# access("/etc/ld.so.preload", R_OK)      = -1 ENOENT
# openat(AT_FDCWD, "/etc/ld.so.cache", O_RDONLY) = 3
# fstat(3, {st_mode=S_IFREG|0644, st_size=123456, ...}) = 0
# ...

# 특정 시스템 콜만 추적
strace -e open,read ls

# 시스템 콜 통계
strace -c ls
# % time     seconds  usecs/call     calls    errors syscall
# ------ ----------- ----------- --------- --------- ----------------
#  35.71    0.000050           5        10           read
#  28.57    0.000040           4        10           write
#  21.43    0.000030           3        10           openat
#  14.29    0.000020           2        10           close
# ------ ----------- ----------- --------- --------- ----------------
# 100.00    0.000140                    40           total
```

**실전 예제:**
```c
// simple_read.c
#include <fcntl.h>
#include <unistd.h>
#include <stdio.h>

int main() {
    int fd = open("test.txt", O_RDONLY);  // 시스템 콜
    if (fd == -1) {
        perror("open");
        return 1;
    }

    char buffer[100];
    ssize_t bytes = read(fd, buffer, sizeof(buffer));  // 시스템 콜
    if (bytes == -1) {
        perror("read");
        close(fd);
        return 1;
    }

    write(1, buffer, bytes);  // 시스템 콜 (stdout에 쓰기)
    close(fd);  // 시스템 콜
    return 0;
}
```

```bash
# 컴파일 및 실행
gcc -o simple_read simple_read.c
echo "Hello, Kernel!" > test.txt

# 시스템 콜 추적
strace ./simple_read
# open("test.txt", O_RDONLY)        = 3
# read(3, "Hello, Kernel!\n", 100)  = 15
# write(1, "Hello, Kernel!\n", 15)  = 15
# close(3)                          = 0
```

---

## 커널 모듈

### 커널 모듈이란?

커널 모듈은 동적으로 로드/언로드할 수 있는 커널 코드입니다. 재부팅 없이 커널 기능을 추가/제거할 수 있습니다.

**장점:**
- ✅ 재부팅 불필요
- ✅ 메모리 절약 (필요할 때만 로드)
- ✅ 커널 크기 감소

### 모듈 관리 명령어

```bash
# 로드된 모듈 확인
lsmod
# Module                  Size  Used by
# nvidia              20971520  45
# bluetooth            716800  5 btrtl,btintel,btbcm
# nf_conntrack         212992  3 nf_nat,nf_conntrack_netlink
# ext4                 921600  2

# 모듈 정보 확인
modinfo bluetooth
# filename:       /lib/modules/5.15.0/kernel/net/bluetooth/bluetooth.ko
# license:        GPL
# version:        2.22
# description:    Bluetooth subsystem core
# author:         Marcel Holtmann <marcel@holtmann.org>

# 모듈 로드
sudo modprobe bluetooth

# 모듈 언로드
sudo modprobe -r bluetooth

# 강제 언로드 (사용 중이어도)
sudo rmmod -f bluetooth

# 모듈 매개변수와 함께 로드
sudo modprobe module_name param1=value1 param2=value2
```

### 모듈 의존성

```bash
# 모듈 의존성 확인
modprobe --show-depends bluetooth
# insmod /lib/modules/.../kernel/net/bluetooth/bluetooth.ko
# insmod /lib/modules/.../kernel/drivers/bluetooth/btrtl.ko
# insmod /lib/modules/.../kernel/drivers/bluetooth/btintel.ko

# 의존성 데이터베이스
cat /lib/modules/$(uname -r)/modules.dep | grep bluetooth
# kernel/net/bluetooth/bluetooth.ko:
# kernel/drivers/bluetooth/btusb.ko: kernel/net/bluetooth/bluetooth.ko
```

### 부팅 시 자동 로드

```bash
# /etc/modules-load.d/에 설정 파일 생성
echo "bluetooth" | sudo tee /etc/modules-load.d/bluetooth.conf

# 또는 /etc/modules에 추가 (Debian/Ubuntu)
echo "bluetooth" | sudo tee -a /etc/modules
```

---

## 커널 버전 관리

### 버전 체계

**리눅스 커널 버전:**
```
6.7.2
│ │ └─ Patch level (버그 수정)
│ └─── Minor version
└───── Major version

예:
6.7.2   - 현재 안정 버전
6.8-rc1 - 6.8 릴리스 후보 1
6.7     - 6.7 안정 버전
```

### 커널 확인

```bash
# 커널 버전 확인
uname -r
# 5.15.0-91-generic

# 상세 정보
uname -a
# Linux hostname 5.15.0-91-generic #101-Ubuntu SMP x86_64 GNU/Linux

# 커널 빌드 정보
cat /proc/version
# Linux version 5.15.0-91-generic (buildd@lcy02-amd64-012)
# (gcc (Ubuntu 11.3.0-1ubuntu1~22.04) 11.3.0, GNU ld 2.38)

# 컴파일 시간
cat /proc/version_signature
# Ubuntu 5.15.0-91.101-generic 5.15.131
```

### 커널 업데이트

**Ubuntu/Debian:**
```bash
# 사용 가능한 커널 확인
apt search linux-image | grep $(uname -r | cut -d- -f1)

# 최신 커널 설치
sudo apt update
sudo apt install linux-image-generic

# 특정 버전 설치
sudo apt install linux-image-5.15.0-92-generic

# 재부팅
sudo reboot

# 재부팅 후 확인
uname -r
```

**Fedora/RHEL:**
```bash
# 커널 업데이트
sudo dnf update kernel

# 특정 버전 설치
sudo dnf install kernel-6.7.2

# 재부팅
sudo reboot
```

### 이전 커널 제거

```bash
# 설치된 커널 목록
dpkg -l | grep linux-image

# 이전 커널 제거 (Ubuntu/Debian)
sudo apt remove linux-image-5.15.0-90-generic

# 자동 정리
sudo apt autoremove

# Fedora/RHEL
sudo dnf remove kernel-old-version
```

---

## 실습 예제

### 1. 커널 정보 탐색

```bash
# /proc/sys를 통한 커널 매개변수 확인
ls /proc/sys/kernel/
# hostname  osrelease  ostype  panic  ...

# 특정 매개변수 확인
cat /proc/sys/kernel/hostname
cat /proc/sys/kernel/osrelease

# 동적 변경 (재부팅 후 초기화됨)
echo "new-hostname" | sudo tee /proc/sys/kernel/hostname

# 영구 변경
echo "kernel.hostname = new-hostname" | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
```

### 2. 커널 로그 확인

```bash
# dmesg - 커널 링 버퍼
dmesg | less

# 최근 10줄
dmesg | tail -10

# 특정 레벨만
dmesg --level=err,warn

# 실시간 모니터링
dmesg -w

# 부팅 메시지만
dmesg | grep -i boot
```

### 3. 커널 파라미터 튜닝

```bash
# 네트워크 버퍼 크기 확인
sysctl net.core.rmem_max
sysctl net.core.wmem_max

# 변경
sudo sysctl -w net.core.rmem_max=134217728
sudo sysctl -w net.core.wmem_max=134217728

# 영구 변경
echo "net.core.rmem_max = 134217728" | sudo tee -a /etc/sysctl.conf
echo "net.core.wmem_max = 134217728" | sudo tee -a /etc/sysctl.conf
sudo sysctl -p

# 모든 설정 확인
sysctl -a | less
```

### 4. 커널 컴파일 (고급)

```bash
# 소스 다운로드
wget https://cdn.kernel.org/pub/linux/kernel/v6.x/linux-6.7.2.tar.xz
tar -xf linux-6.7.2.tar.xz
cd linux-6.7.2

# 빌드 도구 설치
sudo apt install build-essential libncurses-dev bison flex \
                 libssl-dev libelf-dev

# 현재 커널 설정 복사
cp /boot/config-$(uname -r) .config

# 메뉴 설정
make menuconfig

# 컴파일 (멀티코어 활용)
make -j$(nproc)

# 모듈 컴파일
make modules

# 설치
sudo make modules_install
sudo make install

# GRUB 업데이트
sudo update-grub

# 재부팅
sudo reboot
```

---

## 참고 자료

### 공식 문서
- [Linux Kernel Documentation](https://www.kernel.org/doc/)
- [The Linux Kernel Archives](https://www.kernel.org/)

### 책
- "Linux Kernel Development" - Robert Love
- "Understanding the Linux Kernel" - Daniel P. Bovet
- "Linux Device Drivers" - Jonathan Corbet

### 온라인 리소스
- [LWN.net](https://lwn.net/) - Linux 커널 뉴스
- [KernelNewbies](https://kernelnewbies.org/) - 커널 개발 입문

---

[다음: 부팅 프로세스 →](boot-process.md)

[← 목차로 돌아가기](../README.md)
