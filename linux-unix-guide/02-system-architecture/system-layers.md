# 시스템 계층 구조

## 목차
- [계층 구조 개요](#계층-구조-개요)
- [하드웨어 계층](#하드웨어-계층)
- [커널 계층](#커널-계층)
- [시스템 콜 인터페이스](#시스템-콜-인터페이스)
- [라이브러리 계층](#라이브러리-계층)
- [유틸리티 계층](#유틸리티-계층)
- [애플리케이션 계층](#애플리케이션-계층)
- [계층 간 통신](#계층-간-통신)

---

## 계층 구조 개요

리눅스/유닉스는 명확한 계층 구조를 가진 모놀리식 커널 기반의 운영체제입니다. 각 계층은 명확한 역할과 책임을 가지며, 하위 계층의 서비스를 사용하여 상위 계층에 기능을 제공합니다.

### 전체 시스템 계층

```
┌─────────────────────────────────────────┐
│         사용자 애플리케이션              │  ← User Space
│  (Firefox, vim, gcc, bash, etc.)        │
├─────────────────────────────────────────┤
│         시스템 유틸리티                  │
│  (ls, cp, mv, systemctl, etc.)          │
├─────────────────────────────────────────┤
│         라이브러리                       │
│  (glibc, libpthread, libssl, etc.)      │
├─────────────────────────────────────────┤
│      시스템 콜 인터페이스 (API)          │
│  (open, read, write, fork, etc.)        │
╞═════════════════════════════════════════╡  ← 커널/유저 경계
│          리눅스 커널                     │  ← Kernel Space
│  ┌─────────────────────────────────┐    │
│  │   프로세스 관리   │  메모리 관리 │    │
│  ├─────────────────────────────────┤    │
│  │  파일시스템  │  네트워크 스택   │    │
│  ├─────────────────────────────────┤    │
│  │      디바이스 드라이버           │    │
│  └─────────────────────────────────┘    │
├─────────────────────────────────────────┤
│           하드웨어                       │
│  (CPU, Memory, Disk, Network, etc.)     │
└─────────────────────────────────────────┘
```

### 권한 레벨 (Protection Rings)

현대 CPU는 권한 레벨을 통해 시스템 보호를 제공합니다:

```
Ring 0 (최고 권한)  ← 커널 모드
  ↑
Ring 1            ← (일반적으로 사용 안 함)
  ↑
Ring 2            ← (일반적으로 사용 안 함)
  ↑
Ring 3 (최저 권한)  ← 사용자 모드
```

**x86-64 아키텍처에서의 실제 사용:**

```bash
# 현재 CPU 모드 확인 (간접적)
$ cat /proc/cpuinfo | grep -i "model name"
model name : Intel(R) Core(TM) i7-9750H CPU @ 2.60GHz

# 커널 모드와 사용자 모드 시간 확인
$ cat /proc/stat | grep "^cpu "
cpu  123456 789 234567 8901234 5678 0 1234 0 0 0
#    user   nice system idle    iowait irq softirq steal

# 프로세스별 CPU 사용 모드
$ ps aux | head -5
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root         1  0.0  0.0 169404 13524 ?        Ss   10:30   0:02 /sbin/init
root         2  0.0  0.0      0     0 ?        S    10:30   0:00 [kthreadd]

# 시스템 콜 추적으로 모드 전환 관찰
$ strace -c ls
% time     seconds  usecs/call     calls    errors syscall
------ ----------- ----------- --------- --------- ----------------
 35.71    0.000050          50         1           execve
 21.43    0.000030          10         3           mmap
 14.29    0.000020          10         2           openat
```

---

## 하드웨어 계층

### 물리적 구성 요소

**1. 중앙처리장치 (CPU):**

```bash
# CPU 정보 확인
$ lscpu
Architecture:            x86_64
  CPU op-mode(s):        32-bit, 64-bit
  Address sizes:         39 bits physical, 48 bits virtual
  Byte Order:            Little Endian
CPU(s):                  12
  On-line CPU(s) list:   0-11
Vendor ID:               GenuineIntel
  Model name:            Intel(R) Core(TM) i7-9750H CPU @ 2.60GHz
    CPU family:          6
    Model:               158
    Thread(s) per core:  2
    Core(s) per socket:  6
    Socket(s):           1
    Stepping:            10
    CPU max MHz:         4500.0000
    CPU min MHz:         800.0000

# CPU 캐시 정보
$ lscpu | grep cache
L1d cache:               192 KiB (6 instances)
L1i cache:               192 KiB (6 instances)
L2 cache:                1.5 MiB (6 instances)
L3 cache:                12 MiB (1 instance)

# 실시간 CPU 사용률
$ mpstat 1 3
Linux 5.15.0-78-generic (hostname)      11/17/2024      _x86_64_        (12 CPU)

12:45:23 PM  CPU    %usr   %nice    %sys %iowait    %irq   %soft  %steal  %guest  %gnice   %idle
12:45:24 PM  all    5.32    0.00    2.15    0.43    0.00    0.22    0.00    0.00    0.00   91.88
```

**2. 메모리 (RAM):**

```bash
# 메모리 정보
$ free -h
               total        used        free      shared  buff/cache   available
Mem:            15Gi       3.2Gi       8.5Gi       324Mi       3.8Gi        11Gi
Swap:          4.0Gi          0B       4.0Gi

# 상세 메모리 정보
$ cat /proc/meminfo | head -20
MemTotal:       16384000 kB
MemFree:         8912340 kB
MemAvailable:   12234560 kB
Buffers:          456789 kB
Cached:          3234567 kB
SwapCached:            0 kB
Active:          5678901 kB
Inactive:        2345678 kB

# DIMM 정보
$ sudo dmidecode -t memory | grep -A 16 "Memory Device"
Memory Device
    Total Width: 64 bits
    Data Width: 64 bits
    Size: 8192 MB
    Form Factor: SODIMM
    Type: DDR4
    Speed: 2667 MT/s
```

**3. 저장 장치:**

```bash
# 블록 디바이스 목록
$ lsblk
NAME                      MAJ:MIN RM   SIZE RO TYPE MOUNTPOINT
sda                         8:0    0 465.8G  0 disk
├─sda1                      8:1    0   512M  0 part /boot/efi
└─sda2                      8:2    0 465.3G  0 part
  ├─ubuntu--vg-root       253:0    0 400.0G  0 lvm  /
  └─ubuntu--vg-swap_1     253:1    0   4.0G  0 lvm  [SWAP]
nvme0n1                   259:0    0 953.9G  0 disk
└─nvme0n1p1               259:1    0 953.9G  0 part /home

# 디스크 상세 정보
$ sudo hdparm -I /dev/sda | head -30
ATA device, with non-removable media
    Model Number:       Samsung SSD 870 EVO 500GB
    Serial Number:      S5XXXXXXXXXXX
    Firmware Revision:  SVT02B6Q
    Transport:          Serial, ATA8-AST, SATA 1.0a, SATA II Extensions

# 디스크 성능 테스트
$ sudo hdparm -tT /dev/sda
/dev/sda:
 Timing cached reads:   24576 MB in  2.00 seconds = 12301.23 MB/sec
 Timing buffered disk reads: 1500 MB in  3.00 seconds = 499.85 MB/sec

# I/O 통계
$ iostat -x 1 3
Device            r/s     w/s     rkB/s     wkB/s   rrqm/s   wrqm/s  %util
sda              5.23   12.45    234.56    567.89     0.12     2.34  12.45
nvme0n1         23.45   45.67   1234.56   2345.67     1.23     5.67  45.67
```

**4. 네트워크 인터페이스:**

```bash
# 네트워크 인터페이스 목록
$ ip link show
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP
    link/ether 52:54:00:12:34:56 brd ff:ff:ff:ff:ff:ff
3: wlan0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP
    link/ether a4:c3:f0:12:34:56 brd ff:ff:ff:ff:ff:ff

# 네트워크 카드 정보
$ lspci | grep -i network
02:00.0 Network controller: Intel Corporation Wi-Fi 6 AX200
03:00.0 Ethernet controller: Realtek Semiconductor Co., Ltd. RTL8111/8168/8411

# 드라이버 정보
$ ethtool -i eth0
driver: r8169
version: 5.15.0-78-generic
firmware-version: rtl8168h-2_0.0.2 02/26/15
```

**5. 주변 장치:**

```bash
# 모든 PCI 장치
$ lspci
00:00.0 Host bridge: Intel Corporation 8th Gen Core Processor
00:02.0 VGA compatible controller: Intel Corporation UHD Graphics 630
00:14.0 USB controller: Intel Corporation Cannon Lake USB 3.1
00:1f.3 Audio device: Intel Corporation Cannon Lake PCH cAVS

# USB 장치
$ lsusb
Bus 002 Device 001: ID 1d6b:0003 Linux Foundation 3.0 root hub
Bus 001 Device 003: ID 046d:c52b Logitech, Inc. Unifying Receiver
Bus 001 Device 002: ID 8087:0aaa Intel Corp. Bluetooth wireless

# 입력 장치
$ ls /dev/input/
by-id  by-path  event0  event1  event2  mice  mouse0
```

### 하드웨어 추상화

```bash
# /sys 파일시스템을 통한 하드웨어 접근
$ ls /sys/class/
backlight  block  dmi  graphics  input  leds  mem  net  power_supply  rtc  thermal

# 블록 디바이스 정보
$ cat /sys/block/sda/size
976773168  # 섹터 수

$ cat /sys/block/sda/queue/scheduler
[mq-deadline] none

# 네트워크 인터페이스 상태
$ cat /sys/class/net/eth0/operstate
up

$ cat /sys/class/net/eth0/speed
1000  # Mbps

# CPU 주파수 조절
$ cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor
powersave

$ cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq
2600000  # kHz
```

---

## 커널 계층

### 커널의 핵심 서브시스템

**1. 프로세스 관리:**

```bash
# 프로세스 정보는 /proc를 통해 접근
$ ls /proc/1/
attr        cmdline    environ   limits    mountinfo   personality  stat     wchan
autogroup   comm       exe       loginuid  mounts      projid_map   statm
auxv        coredump   fd        map_files net         root         status
cgroup      cpuset     fdinfo    maps      ns          schedstat    syscall
clear_refs  cwd        gid_map   mem       numa_maps   sessionid    task
```

**프로세스 상태 확인:**

```bash
# 프로세스 상태
$ cat /proc/1/status | head -20
Name:   systemd
Umask:  0000
State:  S (sleeping)
Tgid:   1
Ngid:   0
Pid:    1
PPid:   0
TracerPid:      0
Uid:    0       0       0       0
Gid:    0       0       0       0
FDSize: 256
Groups:
VmPeak:   169404 kB
VmSize:   169404 kB
VmLck:         0 kB
VmPin:         0 kB
VmHWM:     13524 kB
VmRSS:     13524 kB
```

**2. 메모리 관리:**

```bash
# 가상 메모리 통계
$ cat /proc/vmstat | head -20
nr_free_pages 2228085
nr_zone_inactive_anon 123456
nr_zone_active_anon 234567
nr_zone_inactive_file 345678
nr_zone_active_file 456789
nr_zone_unevictable 0
nr_zone_write_pending 123

# 메모리 매핑
$ cat /proc/self/maps | head -10
55d8a1234000-55d8a1256000 r--p 00000000 08:02 12345   /usr/bin/cat
55d8a1256000-55d8a1278000 r-xp 00022000 08:02 12345   /usr/bin/cat
55d8a1278000-55d8a1289000 r--p 00044000 08:02 12345   /usr/bin/cat
55d8a1289000-55d8a128a000 r--p 00054000 08:02 12345   /usr/bin/cat
55d8a128a000-55d8a128b000 rw-p 00055000 08:02 12345   /usr/bin/cat

# Swap 사용 상황
$ cat /proc/swaps
Filename                                Type            Size    Used    Priority
/dev/dm-1                               partition       4194300 0       -2

# 메모리 압박 상황 모니터링
$ cat /proc/pressure/memory
some avg10=0.00 avg60=0.00 avg300=0.00 total=123456
full avg10=0.00 avg60=0.00 avg300=0.00 total=0
```

**3. 파일시스템:**

```bash
# 지원되는 파일시스템
$ cat /proc/filesystems
nodev   sysfs
nodev   tmpfs
nodev   bdev
nodev   proc
nodev   cgroup
nodev   cgroup2
        ext4
        ext3
        ext2
        vfat
        xfs
        btrfs

# 마운트된 파일시스템
$ cat /proc/mounts | head -5
sysfs /sys sysfs rw,nosuid,nodev,noexec,relatime 0 0
proc /proc proc rw,nosuid,nodev,noexec,relatime 0 0
udev /dev devtmpfs rw,nosuid,relatime,size=8158812k 0 0
devpts /dev/pts devpts rw,nosuid,noexec,relatime 0 0
tmpfs /run tmpfs rw,nosuid,nodev,noexec,relatime,size=1638404k 0 0

# 파일시스템 통계
$ cat /proc/sys/fs/file-nr
4832    0       9223372036854775807
# 할당된 파일 핸들 | 사용 중 | 최대값

# inode 사용량
$ cat /proc/sys/fs/inode-nr
234567  123456
# 할당된 inode | 사용 가능한 inode
```

**4. 네트워크 스택:**

```bash
# 네트워크 통계
$ cat /proc/net/dev
Inter-|   Receive                                                |  Transmit
 face |bytes    packets errs drop fifo frame compressed multicast|bytes    packets
  eth0: 12345678  234567    0    0    0     0          0     12345 9876543  123456
    lo: 9876543   123456    0    0    0     0          0         0 9876543  123456

# TCP 연결
$ cat /proc/net/tcp | head -5
  sl  local_address rem_address   st tx_queue rx_queue tr tm->when retrnsmt
   0: 0100007F:1F90 00000000:0000 0A 00000000:00000000 00:00000000 00000000
   1: 00000000:0016 00000000:0000 0A 00000000:00000000 00:00000000 00000000

# 라우팅 테이블
$ cat /proc/net/route
Iface   Destination     Gateway         Flags   RefCnt  Use     Metric  Mask
eth0    00000000        0101A8C0        0003    0       0       100     00000000
eth0    0001A8C0        00000000        0001    0       0       100     00FFFFFF

# ARP 캐시
$ cat /proc/net/arp
IP address       HW type     Flags       HW address            Mask     Device
192.168.1.1      0x1         0x2         aa:bb:cc:dd:ee:ff     *        eth0
```

**5. 디바이스 드라이버:**

```bash
# 로드된 모듈 (드라이버)
$ cat /proc/modules | head -10
nvidia_uvm 1150976 0 - Live 0xffffffffc0a1b000
nvidia_drm 69632 4 - Live 0xffffffffc0a08000
nvidia_modeset 1224704 6 nvidia_drm, Live 0xffffffffc08c4000
nvidia 40960000 280 nvidia_uvm,nvidia_modeset, Live 0xffffffffc0000000

# 인터럽트 통계
$ cat /proc/interrupts | head -10
            CPU0       CPU1       CPU2       CPU3
   0:         34          0          0          0   IO-APIC   2-edge      timer
   1:          0          0          5          0   IO-APIC   1-edge      i8042
   8:          0          0          0          1   IO-APIC   8-edge      rtc0
   9:          0       1234          0          0   IO-APIC   9-fasteoi   acpi

# DMA 채널
$ cat /proc/dma
 4: cascade
```

### 커널 파라미터 조정

```bash
# 모든 커널 파라미터 확인
$ sysctl -a | head -20
abi.vsyscall32 = 1
debug.exception-trace = 1
debug.kprobes-optimization = 1
dev.cdrom.autoclose = 1
dev.cdrom.autoeject = 0
dev.cdrom.check_media = 0

# 특정 파라미터 확인
$ sysctl kernel.hostname
kernel.hostname = myserver

# 파라미터 변경 (일시적)
$ sudo sysctl -w net.ipv4.ip_forward=1
net.ipv4.ip_forward = 1

# 파라미터 변경 (영구적)
$ sudo vi /etc/sysctl.conf
net.ipv4.ip_forward = 1
vm.swappiness = 10
fs.file-max = 65535

$ sudo sysctl -p  # 적용
```

**유용한 커널 파라미터 예제:**

```bash
# 네트워크 최적화
net.core.rmem_max = 134217728
net.core.wmem_max = 134217728
net.ipv4.tcp_rmem = 4096 87380 67108864
net.ipv4.tcp_wmem = 4096 65536 67108864
net.ipv4.tcp_congestion_control = bbr
net.core.default_qdisc = fq

# 보안 강화
kernel.dmesg_restrict = 1
kernel.kptr_restrict = 2
net.ipv4.conf.all.rp_filter = 1
net.ipv4.conf.all.accept_source_route = 0

# 성능 튜닝
vm.swappiness = 10
vm.dirty_ratio = 15
vm.dirty_background_ratio = 5
fs.file-max = 2097152
```

---

## 시스템 콜 인터페이스

시스템 콜은 사용자 공간과 커널 공간을 연결하는 유일한 인터페이스입니다.

### 주요 시스템 콜 카테고리

**1. 프로세스 제어:**

```c
// fork() - 새 프로세스 생성
#include <unistd.h>
#include <stdio.h>

int main() {
    pid_t pid = fork();

    if (pid == 0) {
        printf("자식 프로세스: PID = %d\n", getpid());
    } else if (pid > 0) {
        printf("부모 프로세스: PID = %d, 자식 PID = %d\n", getpid(), pid);
    } else {
        perror("fork 실패");
    }

    return 0;
}
```

```bash
# 실행 추적
$ strace -e trace=process ./fork_example
execve("./fork_example", ["./fork_example"], 0x7ffc...) = 0
clone(child_stack=NULL, flags=CLONE_CHILD_CLEARTID|CLONE_CHILD_SETTID|SIGCHLD...) = 12345
부모 프로세스: PID = 12344, 자식 PID = 12345
자식 프로세스: PID = 12345
```

**2. 파일 작업:**

```c
// open, read, write, close
#include <fcntl.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>

int main() {
    // 파일 열기
    int fd = open("/tmp/test.txt", O_WRONLY | O_CREAT | O_TRUNC, 0644);
    if (fd == -1) {
        perror("open");
        return 1;
    }

    // 쓰기
    const char *text = "Hello, System Call!\n";
    ssize_t written = write(fd, text, strlen(text));
    printf("Written %zd bytes\n", written);

    // 닫기
    close(fd);

    // 읽기
    fd = open("/tmp/test.txt", O_RDONLY);
    char buffer[100];
    ssize_t read_bytes = read(fd, buffer, sizeof(buffer) - 1);
    buffer[read_bytes] = '\0';
    printf("Read: %s", buffer);
    close(fd);

    return 0;
}
```

```bash
# 시스템 콜 추적
$ strace -e trace=open,read,write,close ./file_example
openat(AT_FDCWD, "/tmp/test.txt", O_WRONLY|O_CREAT|O_TRUNC, 0644) = 3
write(3, "Hello, System Call!\n", 20)   = 20
close(3)                                = 0
openat(AT_FDCWD, "/tmp/test.txt", O_RDONLY) = 3
read(3, "Hello, System Call!\n", 99)   = 20
close(3)                                = 0
```

**3. 메모리 관리:**

```c
// mmap - 메모리 매핑
#include <sys/mman.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>

int main() {
    int fd = open("/tmp/mapped.txt", O_RDWR | O_CREAT, 0644);

    // 파일 크기 설정
    ftruncate(fd, 4096);

    // 메모리에 매핑
    char *mapped = mmap(NULL, 4096, PROT_READ | PROT_WRITE,
                        MAP_SHARED, fd, 0);

    if (mapped == MAP_FAILED) {
        perror("mmap");
        return 1;
    }

    // 메모리에 직접 쓰기 (파일에 자동 반영)
    strcpy(mapped, "Memory-mapped file!");

    // 동기화
    msync(mapped, 4096, MS_SYNC);

    // 언매핑
    munmap(mapped, 4096);
    close(fd);

    return 0;
}
```

**4. 프로세스 간 통신 (IPC):**

```c
// pipe - 파이프 생성
#include <unistd.h>
#include <stdio.h>
#include <string.h>

int main() {
    int pipefd[2];
    char buffer[100];

    // 파이프 생성
    if (pipe(pipefd) == -1) {
        perror("pipe");
        return 1;
    }

    pid_t pid = fork();

    if (pid == 0) {
        // 자식: 읽기
        close(pipefd[1]);  // 쓰기 끝 닫기
        read(pipefd[0], buffer, sizeof(buffer));
        printf("자식이 받음: %s\n", buffer);
        close(pipefd[0]);
    } else {
        // 부모: 쓰기
        close(pipefd[0]);  // 읽기 끝 닫기
        const char *msg = "Hello from parent!";
        write(pipefd[1], msg, strlen(msg) + 1);
        close(pipefd[1]);
    }

    return 0;
}
```

### 시스템 콜 추적 및 분석

```bash
# 프로그램의 모든 시스템 콜 추적
$ strace ls /home
execve("/usr/bin/ls", ["ls", "/home"], 0x7ffc...) = 0
brk(NULL)                               = 0x55d8a1234000
access("/etc/ld.so.preload", R_OK)      = -1 ENOENT
openat(AT_FDCWD, "/etc/ld.so.cache", O_RDONLY|O_CLOEXEC) = 3
...

# 시스템 콜 통계
$ strace -c ls /home > /dev/null
% time     seconds  usecs/call     calls    errors syscall
------ ----------- ----------- --------- --------- ----------------
 35.29    0.000060          20         3           openat
 17.65    0.000030          30         1           execve
 11.76    0.000020          10         2           fstat
 11.76    0.000020          20         1           write
  5.88    0.000010          10         1           read

# 특정 시스템 콜만 추적
$ strace -e trace=open,openat ls
openat(AT_FDCWD, "/etc/ld.so.cache", O_RDONLY|O_CLOEXEC) = 3
openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libselinux.so.1", O_RDONLY|O_CLOEXEC) = 3

# 시간 측정
$ strace -T ls 2>&1 | grep write
write(1, "file1\nfile2\n", 12)          = 12 <0.000034>

# 여러 프로세스 추적
$ strace -f bash -c "ls | wc -l"
```

---

## 라이브러리 계층

### C 표준 라이브러리 (glibc)

**라이브러리의 역할:**

```
1. 시스템 콜 래핑 (Wrapping)
   - 사용하기 쉬운 함수 제공
   - 에러 처리
   - 버퍼링 최적화

2. 유틸리티 함수
   - 문자열 처리
   - 수학 연산
   - 메모리 관리

3. 표준화
   - POSIX 준수
   - 이식성 보장
```

**라이브러리 확인:**

```bash
# 시스템의 glibc 버전
$ ldd --version
ldd (Ubuntu GLIBC 2.35-0ubuntu3.4) 2.35

# 프로그램이 사용하는 라이브러리
$ ldd /usr/bin/ls
    linux-vdso.so.1 (0x00007ffd...)
    libselinux.so.1 => /lib/x86_64-linux-gnu/libselinux.so.1
    libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6
    libpcre2-8.so.0 => /lib/x86_64-linux-gnu/libpcre2-8.so.0
    /lib64/ld-linux-x86-64.so.2

# 라이브러리 경로 확인
$ ldconfig -p | grep libc.so.6
    libc.so.6 (libc6,x86-64) => /lib/x86_64-linux-gnu/libc.so.6

# 라이브러리 정보
$ objdump -p /usr/bin/ls | grep NEEDED
  NEEDED               libselinux.so.1
  NEEDED               libc.so.6
```

**라이브러리 함수 vs 시스템 콜:**

```c
// 라이브러리 함수 (버퍼링 포함)
#include <stdio.h>
FILE *fp = fopen("/tmp/test.txt", "w");
fprintf(fp, "Hello\n");  // 버퍼에 저장
fclose(fp);              // 버퍼 플러시 및 close() 시스템 콜

// 직접 시스템 콜 (버퍼링 없음)
#include <fcntl.h>
#include <unistd.h>
int fd = open("/tmp/test.txt", O_WRONLY | O_CREAT);
write(fd, "Hello\n", 6);  // 즉시 커널로
close(fd);
```

**동적 링킹 vs 정적 링킹:**

```bash
# 동적 링킹 (기본)
$ gcc -o dynamic program.c
$ ls -lh dynamic
-rwxr-xr-x 1 user user 16K Nov 17 13:00 dynamic
$ ldd dynamic
    linux-vdso.so.1
    libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6

# 정적 링킹
$ gcc -static -o static program.c
$ ls -lh static
-rwxr-xr-x 1 user user 872K Nov 17 13:01 static
$ ldd static
    not a dynamic executable

# 크기 비교
$ size dynamic
   text    data     bss     dec     hex filename
   1234     568      16    1818     71a dynamic

$ size static
   text    data     bss     dec     hex filename
 789012   23456   45678  858146   d1862 static
```

---

## 유틸리티 계층

### GNU 핵심 유틸리티 (coreutils)

```bash
# coreutils 패키지의 프로그램들
$ dpkg -L coreutils | grep '/bin/' | head -20
/usr/bin/[
/usr/bin/b2sum
/usr/bin/base32
/usr/bin/base64
/usr/bin/basename
/usr/bin/cat
/usr/bin/chcon
/usr/bin/chgrp
/usr/bin/chmod
/usr/bin/chown
/usr/bin/chroot
/usr/bin/cksum
/usr/bin/comm
/usr/bin/cp
/usr/bin/csplit
/usr/bin/cut
/usr/bin/date
/usr/bin/dd
/usr/bin/df
/usr/bin/dir
```

**카테고리별 유틸리티:**

```bash
# 파일 작업
ls, cp, mv, rm, mkdir, rmdir, ln, touch

# 텍스트 처리
cat, tac, head, tail, cut, paste, sort, uniq, tr, wc

# 시스템 정보
uname, hostname, uptime, who, whoami, id, groups

# 파일시스템
df, du, mount, umount, sync

# 프로세스
ps, top, kill, nice, renice

# 네트워크
ping, netstat, ss, ip, ifconfig(deprecated)
```

---

## 애플리케이션 계층

### 사용자 애플리케이션

```
데스크탑 애플리케이션
├─ 웹 브라우저 (Firefox, Chrome)
├─ 오피스 (LibreOffice)
├─ 개발 도구 (VSCode, IntelliJ)
└─ 미디어 (VLC, GIMP)

서버 애플리케이션
├─ 웹 서버 (Apache, Nginx)
├─ 데이터베이스 (MySQL, PostgreSQL)
├─ 메시징 (RabbitMQ, Kafka)
└─ 컨테이너 (Docker, Podman)

개발 도구
├─ 컴파일러 (GCC, Clang)
├─ 빌드 시스템 (Make, CMake)
├─ 버전 관리 (Git, SVN)
└─ 디버거 (GDB, LLDB)
```

---

## 계층 간 통신

### 데이터 흐름 예제: 파일 읽기

```
1. 애플리케이션 계층
   Python 코드: f = open('/etc/passwd', 'r')
        ↓
2. 라이브러리 계층
   glibc: fopen() 함수
        ↓
3. 시스템 콜 인터페이스
   open() 시스템 콜 (syscall number: 2)
        ↓
4. 커널 계층
   VFS (Virtual File System)
        ↓
   ext4 파일시스템 드라이버
        ↓
   블록 디바이스 드라이버
        ↓
5. 하드웨어 계층
   디스크에서 데이터 읽기
```

**실제 추적:**

```bash
# Python 스크립트
$ cat test.py
with open('/etc/passwd', 'r') as f:
    lines = f.readlines()
    print(f"Read {len(lines)} lines")

# strace로 추적
$ strace -e trace=openat,read,close python3 test.py
openat(AT_FDCWD, "/etc/passwd", O_RDONLY|O_CLOEXEC) = 3
read(3, "root:x:0:0:root:/root:/bin/bash\n"..., 4096) = 2345
read(3, "", 4096)                       = 0
close(3)                                = 0
Read 45 lines
```

---

## 요약

리눅스 시스템의 계층 구조:

1. **하드웨어**: 물리적 자원
2. **커널**: 자원 관리 및 추상화
3. **시스템 콜**: 커널-유저 인터페이스
4. **라이브러리**: 편리한 API 제공
5. **유틸리티**: 기본 도구
6. **애플리케이션**: 최종 사용자 프로그램

각 계층은 명확한 책임을 가지며, 하위 계층의 복잡성을 숨기고 상위 계층에 추상화된 인터페이스를 제공합니다.

---

[다음: 파일시스템 구조 →](../03-filesystem/structure.md)

[← 부팅 프로세스로 돌아가기](boot-process.md)

[← 목차로 돌아가기](../README.md)
