# 리눅스 부팅 프로세스

## 목차
- [부팅 프로세스 개요](#부팅-프로세스-개요)
- [1단계: BIOS/UEFI](#1단계-biosuefi)
- [2단계: 부트로더 (GRUB)](#2단계-부트로더-grub)
- [3단계: 커널 초기화](#3단계-커널-초기화)
- [4단계: init/systemd](#4단계-initsystemd)
- [5단계: 런레벨/타겟](#5단계-런레벨타겟)
- [부팅 문제 해결](#부팅-문제-해결)
- [부팅 최적화](#부팅-최적화)

---

## 부팅 프로세스 개요

리눅스 시스템이 전원을 켜고 사용 가능한 상태가 되기까지의 전체 과정을 이해하는 것은 시스템 관리의 핵심입니다.

### 전체 부팅 단계

```
전원 ON
   ↓
┌─────────────────────────────────────────┐
│ 1. BIOS/UEFI POST (Power-On Self Test) │
│    - 하드웨어 체크                       │
│    - 부팅 장치 선택                      │
└─────────────────────────────────────────┘
   ↓
┌─────────────────────────────────────────┐
│ 2. 부트로더 (GRUB/GRUB2)                │
│    - MBR/GPT 읽기                        │
│    - 커널 선택                           │
│    - 커널 및 initramfs 로드              │
└─────────────────────────────────────────┘
   ↓
┌─────────────────────────────────────────┐
│ 3. 커널 초기화                           │
│    - 압축 해제                           │
│    - 하드웨어 감지                       │
│    - 루트 파일시스템 마운트              │
└─────────────────────────────────────────┘
   ↓
┌─────────────────────────────────────────┐
│ 4. init 프로세스 (PID 1)                │
│    - SysVinit / Upstart / systemd       │
│    - 시스템 서비스 시작                  │
└─────────────────────────────────────────┘
   ↓
┌─────────────────────────────────────────┐
│ 5. 런레벨/타겟 도달                      │
│    - 다중 사용자 모드                    │
│    - 그래픽 로그인                       │
└─────────────────────────────────────────┘
   ↓
로그인 프롬프트
```

### 부팅 시간 측정

```bash
# 전체 부팅 시간 확인
$ systemd-analyze
Startup finished in 4.271s (firmware) + 2.456s (loader) + 3.845s (kernel) + 5.234s (userspace) = 15.806s

# 각 서비스별 시간 확인
$ systemd-analyze blame
     2.845s NetworkManager-wait-online.service
     1.234s plymouth-quit-wait.service
     0.987s systemd-logind.service
     0.765s accounts-daemon.service
     0.543s gdm.service

# 중요 경로 분석
$ systemd-analyze critical-chain
The time when unit became active or started is printed after the "@" character.
The time the unit took to start is printed after the "+" character.

graphical.target @5.234s
└─multi-user.target @5.234s
  └─networking.service @3.456s +1.778s
    └─network-pre.target @3.445s
```

---

## 1단계: BIOS/UEFI

### BIOS (Basic Input/Output System)

**전통적인 BIOS 부팅:**

```
1. POST (Power-On Self Test) 실행
   - CPU 체크
   - 메모리 테스트
   - 주변 장치 확인

2. 부팅 장치 순서 확인
   - BIOS 설정에서 지정한 순서
   - 예: HDD → USB → CD-ROM

3. MBR (Master Boot Record) 읽기
   - 디스크의 첫 512바이트
   - 부트로더 코드 (446바이트)
   - 파티션 테이블 (64바이트)
   - 부트 시그니처 (2바이트: 0x55AA)
```

**MBR 구조 확인:**

```bash
# MBR 내용 보기 (주의: 읽기 전용으로)
$ sudo dd if=/dev/sda bs=512 count=1 | hexdump -C
00000000  eb 63 90 00 00 00 00 00  00 00 00 00 00 00 00 00  |.c..............|
...
000001b0  00 00 00 00 00 00 00 00  80 20 21 00 83 fe ff ff  |......... !.....|
000001c0  01 00 00 00 ff ff ff ff  00 00 00 00 00 00 00 00  |................|
...
000001f0  00 00 00 00 00 00 00 00  00 00 00 00 00 00 55 aa  |..............U.|

# 파티션 테이블 확인
$ sudo fdisk -l /dev/sda
Disk /dev/sda: 500 GB
Device     Boot   Start       End   Sectors  Size Id Type
/dev/sda1  *       2048   1050623   1048576  512M 83 Linux
/dev/sda2       1050624 976773119 975722496  465G 8e Linux LVM
```

### UEFI (Unified Extensible Firmware Interface)

**UEFI의 장점:**

```
1. GPT (GUID Partition Table) 지원
   - 2TB 이상 디스크 지원
   - 최대 128개 파티션
   - 파티션 테이블 백업

2. Secure Boot
   - 서명된 부트로더만 실행
   - 루트킷 방지

3. 빠른 부팅
   - 하드웨어 초기화 최적화

4. 그래픽 인터페이스
   - 마우스 사용 가능
   - 고해상도 지원
```

**UEFI 부팅 확인:**

```bash
# UEFI 모드로 부팅했는지 확인
$ [ -d /sys/firmware/efi ] && echo "UEFI" || echo "BIOS"
UEFI

# EFI 변수 확인
$ efibootmgr
BootCurrent: 0001
Timeout: 1 seconds
BootOrder: 0001,0000,0002
Boot0000* ubuntu
Boot0001* Windows Boot Manager
Boot0002* USB Drive

# EFI 시스템 파티션 확인
$ df -h /boot/efi
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1       511M   5.3M  506M   2% /boot/efi

# EFI 파티션 내용 확인
$ ls -R /boot/efi/EFI/
/boot/efi/EFI/:
ubuntu  Microsoft  BOOT

/boot/efi/EFI/ubuntu/:
grub.cfg  grubx64.efi  shimx64.efi
```

**GPT 파티션 테이블 확인:**

```bash
# GPT 정보 보기
$ sudo gdisk -l /dev/sda
GPT fdisk (gdisk) version 1.0.5

Partition table scan:
  MBR: protective
  BSD: not present
  APM: not present
  GPT: present

Number  Start (sector)    End (sector)  Size       Code  Name
   1            2048         1050623   512.0 MiB   EF00  EFI System
   2         1050624       976773119   465.3 GiB   8E00  Linux LVM

# parted로 확인
$ sudo parted /dev/sda print
Model: ATA Samsung SSD 870 (scsi)
Disk /dev/sda: 500GB
Sector size (logical/physical): 512B/512B
Partition Table: gpt

Number  Start   End    Size    File system  Name         Flags
 1      1049kB  538MB  537MB   fat32        EFI System   boot, esp
 2      538MB   500GB  500GB                Linux LVM    lvm
```

---

## 2단계: 부트로더 (GRUB)

### GRUB2 (GRand Unified Bootloader version 2)

**GRUB의 역할:**

```
1. 멀티부팅 관리
   - 여러 OS 선택
   - 여러 커널 버전 선택

2. 커널 파라미터 전달
   - 부팅 옵션 설정
   - 복구 모드 진입

3. 파일시스템 이해
   - ext4, xfs, btrfs 등 읽기 가능
   - 커널 이미지 로드
```

**GRUB 설정 파일:**

```bash
# 메인 설정 파일 (수동 편집 금지!)
$ cat /boot/grub/grub.cfg
# 이 파일은 자동 생성됨. 직접 편집하지 말 것!
# 대신 /etc/default/grub 및 /etc/grub.d/* 수정

# 실제 편집할 파일
$ cat /etc/default/grub
GRUB_DEFAULT=0
GRUB_TIMEOUT=5
GRUB_DISTRIBUTOR=`lsb_release -i -s 2> /dev/null || echo Debian`
GRUB_CMDLINE_LINUX_DEFAULT="quiet splash"
GRUB_CMDLINE_LINUX=""

# 변경 후 GRUB 업데이트
$ sudo update-grub
# 또는
$ sudo grub-mkconfig -o /boot/grub/grub.cfg
```

**GRUB 부팅 메뉴 커스터마이징:**

```bash
# 기본 부팅 항목 변경 (0부터 시작)
$ sudo vi /etc/default/grub
GRUB_DEFAULT=2  # 3번째 항목으로 부팅

# 이름으로 지정
GRUB_DEFAULT="Advanced options for Ubuntu>Ubuntu, with Linux 5.15.0-78"

# 저장된 마지막 선택 사용
GRUB_DEFAULT=saved
GRUB_SAVEDEFAULT=true

# 타임아웃 설정 (초)
GRUB_TIMEOUT=10  # 10초 대기
GRUB_TIMEOUT=0   # 즉시 부팅
GRUB_TIMEOUT=-1  # 수동 선택까지 대기

# 부팅 파라미터 추가
GRUB_CMDLINE_LINUX_DEFAULT="quiet splash nomodeset"

# 적용
$ sudo update-grub
```

**커널 부팅 파라미터 예제:**

```bash
# 싱글 유저 모드 (복구 모드)
GRUB_CMDLINE_LINUX="single"
# 또는
GRUB_CMDLINE_LINUX="1"

# 텍스트 모드로 부팅
GRUB_CMDLINE_LINUX="text systemd.unit=multi-user.target"

# 디버그 모드
GRUB_CMDLINE_LINUX="debug ignore_loglevel"

# 그래픽 카드 문제 해결
GRUB_CMDLINE_LINUX="nomodeset"

# 메모리 제한
GRUB_CMDLINE_LINUX="mem=4G"

# IOMMU 활성화 (가상화)
GRUB_CMDLINE_LINUX="intel_iommu=on"
# 또는 AMD
GRUB_CMDLINE_LINUX="amd_iommu=on"
```

**GRUB 복구:**

```bash
# GRUB 재설치 (Live USB에서)
$ sudo mount /dev/sda2 /mnt
$ sudo mount /dev/sda1 /mnt/boot/efi
$ sudo mount --bind /dev /mnt/dev
$ sudo mount --bind /proc /mnt/proc
$ sudo mount --bind /sys /mnt/sys
$ sudo chroot /mnt
$ grub-install /dev/sda
$ update-grub
$ exit

# 또는 boot-repair 도구 사용
$ sudo add-apt-repository ppa:yannubuntu/boot-repair
$ sudo apt update
$ sudo apt install boot-repair
$ boot-repair
```

**GRUB 부팅 시 편집:**

```
1. GRUB 메뉴에서 'e' 키 누르기
2. linux 라인 찾기:
   linux /boot/vmlinuz-5.15.0-78-generic root=UUID=xxx ro quiet splash

3. 파라미터 수정:
   linux /boot/vmlinuz-5.15.0-78-generic root=UUID=xxx ro single

4. Ctrl+X 또는 F10으로 부팅
```

---

## 3단계: 커널 초기화

### 커널 로드 과정

**initramfs (Initial RAM File System):**

```bash
# initramfs 파일 확인
$ ls -lh /boot/initrd.img-*
-rw-r--r-- 1 root root 85M Nov 15 10:23 /boot/initrd.img-5.15.0-78-generic
-rw-r--r-- 1 root root 84M Oct 20 14:56 /boot/initrd.img-5.15.0-76-generic

# initramfs 내용 확인
$ lsinitramfs /boot/initrd.img-$(uname -r) | head -20
.
kernel
kernel/x86
kernel/x86/microcode
kernel/x86/microcode/GenuineIntel.bin
scripts
scripts/functions
scripts/init-top
scripts/init-premount
scripts/local-top
scripts/local-premount

# 압축 해제하여 확인
$ mkdir /tmp/initrd
$ cd /tmp/initrd
$ unmkinitramfs /boot/initrd.img-$(uname -r) .
$ ls
main  early
$ ls main/
bin  conf  etc  init  lib  lib64  run  scripts  usr

# init 스크립트 확인
$ cat main/init | head -30
#!/bin/sh
# initramfs의 메인 초기화 스크립트
```

**커널 초기화 메시지 확인:**

```bash
# 부팅 메시지 보기
$ dmesg | head -50
[    0.000000] Linux version 5.15.0-78-generic (buildd@lcy02-amd64-026)
[    0.000000] Command line: BOOT_IMAGE=/boot/vmlinuz-5.15.0-78-generic root=UUID=xxx ro quiet splash
[    0.000000] KERNEL supported cpus:
[    0.000000]   Intel GenuineIntel
[    0.000000]   AMD AuthenticAMD
[    0.000000] x86/fpu: Supporting XSAVE feature 0x001: 'x87 floating point registers'
[    0.001000] ACPI: Early table checksum verification disabled
[    0.002000] ACPI: RSDP 0x00000000000F0490 000024 (v02 ALASKA)

# 특정 하드웨어 초기화 확인
$ dmesg | grep -i "disk\|storage\|sata"
[    1.234567] ata1: SATA max UDMA/133 abar m2048@0xf7f00000 port 0xf7f00100
[    1.234890] ata1: SATA link up 6.0 Gbps (SStatus 133 SControl 300)
[    1.345678] ata1.00: ATA-9: Samsung SSD 870 EVO 500GB, SVT02B6Q

# 메모리 초기화
$ dmesg | grep -i memory
[    0.000000] Memory: 16384MB RAM
[    0.001000] e820: BIOS-provided physical RAM map:

# 네트워크 인터페이스
$ dmesg | grep -i eth
[    2.456789] e1000e 0000:00:1f.6 eth0: registered PHC clock
[    2.567890] e1000e 0000:00:1f.6 eno1: renamed from eth0
```

**커널 모듈 로드:**

```bash
# 로드된 모듈 확인
$ lsmod
Module                  Size  Used by
nvidia_uvm           1150976  0
nvidia_drm             69632  4
nvidia_modeset       1224704  6 nvidia_drm
nvidia              40960000  280 nvidia_uvm,nvidia_modeset

# 모듈 정보 확인
$ modinfo nvidia | head -15
filename:       /lib/modules/5.15.0-78-generic/updates/dkms/nvidia.ko
firmware:       nvidia/530.41.03/gsp.bin
version:        530.41.03
supported:      external
license:        NVIDIA

# 모듈 수동 로드
$ sudo modprobe module_name

# 모듈 제거
$ sudo modprobe -r module_name

# 부팅 시 자동 로드 설정
$ echo "module_name" | sudo tee -a /etc/modules
```

**루트 파일시스템 마운트:**

```bash
# 현재 마운트된 루트 확인
$ mount | grep " / "
/dev/mapper/ubuntu--vg-root on / type ext4 (rw,relatime,errors=remount-ro)

# fstab 확인
$ cat /etc/fstab
# <file system> <mount point>   <type>  <options>       <dump>  <pass>
UUID=xxx-xxx  /               ext4    errors=remount-ro 0       1
UUID=yyy-yyy  /boot/efi       vfat    umask=0077      0       1

# UUID 확인
$ sudo blkid
/dev/sda1: UUID="XXXX-XXXX" TYPE="vfat" PARTUUID="..."
/dev/sda2: UUID="yyyy..." TYPE="LVM2_member" PARTUUID="..."
```

---

## 4단계: init/systemd

### systemd - 현대적 init 시스템

**systemd의 특징:**

```
1. 병렬 서비스 시작 - 빠른 부팅
2. On-demand 서비스 시작
3. 의존성 기반 서비스 제어
4. 스냅샷 및 시스템 상태 복원
5. 통합 로깅 (journald)
6. 타이머 기반 작업 (cron 대체 가능)
```

**systemd 기본 명령:**

```bash
# systemd 버전 확인
$ systemctl --version
systemd 249 (249.11-0ubuntu3.9)
+PAM +AUDIT +SELINUX +APPARMOR +IMA +SMACK +SECCOMP +GCRYPT

# 시스템 상태 확인
$ systemctl status
● hostname
    State: running
     Jobs: 0 queued
   Failed: 0 units
    Since: Mon 2024-11-17 10:30:45 KST; 2h 15min ago

# 서비스 관리
$ sudo systemctl start nginx
$ sudo systemctl stop nginx
$ sudo systemctl restart nginx
$ sudo systemctl reload nginx  # 설정만 재로드

# 서비스 상태 확인
$ systemctl status nginx
● nginx.service - A high performance web server
     Loaded: loaded (/lib/systemd/system/nginx.service; enabled; vendor preset: enabled)
     Active: active (running) since Mon 2024-11-17 10:35:12 KST; 2h 10min ago
       Docs: man:nginx(8)
   Main PID: 1234 (nginx)
      Tasks: 5 (limit: 18842)
     Memory: 7.2M
        CPU: 142ms
     CGroup: /system.slice/nginx.service
             ├─1234 nginx: master process /usr/sbin/nginx
             └─1235 nginx: worker process

# 부팅 시 자동 시작
$ sudo systemctl enable nginx
Created symlink /etc/systemd/system/multi-user.target.wants/nginx.service → /lib/systemd/system/nginx.service

$ sudo systemctl disable nginx
Removed /etc/systemd/system/multi-user.target.wants/nginx.service
```

**서비스 의존성 확인:**

```bash
# 의존성 트리
$ systemctl list-dependencies nginx
nginx.service
● ├─system.slice
● ├─network.target
● │ ├─NetworkManager.service
● │ └─systemd-networkd.service
● └─sysinit.target

# 역방향 의존성 (어떤 서비스가 이것에 의존하는가)
$ systemctl list-dependencies --reverse nginx

# 특정 서비스가 필요로 하는 것들
$ systemctl show nginx -p Requires -p Wants -p After -p Before
Requires=sysinit.target system.slice
Wants=network.target
After=network.target sysinit.target
Before=
```

**서비스 유닛 파일 작성:**

```bash
# 커스텀 서비스 생성
$ sudo vi /etc/systemd/system/myapp.service

[Unit]
Description=My Custom Application
After=network.target
Wants=network-online.target
Documentation=https://example.com/docs

[Service]
Type=simple
User=myuser
Group=mygroup
WorkingDirectory=/opt/myapp
ExecStartPre=/bin/sh -c 'echo "Starting myapp..." | systemd-cat'
ExecStart=/opt/myapp/bin/myapp --config /etc/myapp/config.yml
ExecReload=/bin/kill -HUP $MAINPID
Restart=on-failure
RestartSec=5s
StandardOutput=journal
StandardError=journal
SyslogIdentifier=myapp

# 환경변수 설정
Environment="NODE_ENV=production"
Environment="PORT=8080"
EnvironmentFile=/etc/myapp/environment

# 리소스 제한
LimitNOFILE=65535
MemoryLimit=512M
CPUQuota=50%

[Install]
WantedBy=multi-user.target

# 리로드 및 시작
$ sudo systemctl daemon-reload
$ sudo systemctl start myapp
$ sudo systemctl enable myapp
```

**타이머 유닛 (cron 대체):**

```bash
# 타이머 유닛 파일
$ sudo vi /etc/systemd/system/mybackup.timer

[Unit]
Description=Daily Backup Timer
Requires=mybackup.service

[Timer]
OnCalendar=daily
OnCalendar=*-*-* 02:00:00
Persistent=true
Unit=mybackup.service

[Install]
WantedBy=timers.target

# 서비스 유닛 파일
$ sudo vi /etc/systemd/system/mybackup.service

[Unit]
Description=Backup Service

[Service]
Type=oneshot
ExecStart=/usr/local/bin/backup.sh
User=backup
StandardOutput=journal

# 활성화
$ sudo systemctl daemon-reload
$ sudo systemctl enable mybackup.timer
$ sudo systemctl start mybackup.timer

# 타이머 확인
$ systemctl list-timers
NEXT                        LEFT          LAST                        PASSED  UNIT
Mon 2024-11-18 02:00:00 KST 13h left      Sun 2024-11-17 02:00:00 KST 10h ago mybackup.timer
```

### 레거시 SysVinit

**SysVinit의 런레벨:**

```bash
# 런레벨 확인 (systemd에서도 호환 명령)
$ runlevel
N 5

# 런레벨 변경
$ sudo init 3  # 텍스트 모드
$ sudo init 5  # 그래픽 모드

# 런레벨 의미:
0 - 시스템 종료
1 - 싱글 유저 모드 (복구)
2 - 다중 사용자, 네트워킹 없음
3 - 다중 사용자, 텍스트 모드
4 - 사용 안 함 (사용자 정의)
5 - 다중 사용자, 그래픽 모드
6 - 재부팅
```

---

## 5단계: 런레벨/타겟

### systemd 타겟

**타겟 = 런레벨의 systemd 버전:**

```bash
# 현재 타겟 확인
$ systemctl get-default
graphical.target

# 모든 타겟 확인
$ systemctl list-units --type=target
UNIT                   LOAD   ACTIVE SUB    DESCRIPTION
basic.target           loaded active active Basic System
cryptsetup.target      loaded active active Local Encrypted Volumes
getty.target           loaded active active Login Prompts
graphical.target       loaded active active Graphical Interface
local-fs.target        loaded active active Local File Systems
multi-user.target      loaded active active Multi-User System
network.target         loaded active active Network
paths.target           loaded active active Paths
remote-fs.target       loaded active active Remote File Systems
slices.target          loaded active active Slices
sockets.target         loaded active active Sockets
sysinit.target         loaded active active System Initialization
timers.target          loaded active active Timers

# 기본 타겟 변경
$ sudo systemctl set-default multi-user.target  # 텍스트 모드
$ sudo systemctl set-default graphical.target   # 그래픽 모드

# 타겟으로 전환 (재부팅 없이)
$ sudo systemctl isolate multi-user.target
$ sudo systemctl isolate graphical.target
```

**주요 타겟 대응표:**

| SysV 런레벨 | systemd 타겟 | 용도 |
|------------|--------------|------|
| 0 | poweroff.target | 시스템 종료 |
| 1, s | rescue.target | 싱글 유저 모드 |
| 2, 3, 4 | multi-user.target | 텍스트 다중 사용자 |
| 5 | graphical.target | 그래픽 다중 사용자 |
| 6 | reboot.target | 재부팅 |

**타겟 의존성 확인:**

```bash
# graphical.target의 의존성
$ systemctl list-dependencies graphical.target
graphical.target
● ├─accounts-daemon.service
● ├─gdm.service
● ├─systemd-update-utmp-runlevel.service
● ├─udisks2.service
● └─multi-user.target
●   ├─anacron.service
●   ├─avahi-daemon.service
●   ├─cron.service
```

---

## 부팅 문제 해결

### 복구 모드 진입

**GRUB에서 복구 모드:**

```
1. GRUB 메뉴에서 "Advanced options" 선택
2. "recovery mode" 커널 선택
3. 복구 메뉴에서 옵션 선택:
   - resume: 정상 부팅 계속
   - clean: 디스크 공간 정리
   - dpkg: 패키지 복구
   - fsck: 파일시스템 검사
   - grub: GRUB 업데이트
   - network: 네트워킹 활성화
   - root: 루트 쉘
```

**싱글 유저 모드 (init 1):**

```bash
# GRUB에서 'e' 눌러 편집
# linux 라인 끝에 추가:
single
# 또는
1
# 또는
systemd.unit=rescue.target

# 부팅 후:
$ whoami
root

# 파일시스템은 읽기 전용으로 마운트됨
$ mount -o remount,rw /

# 비밀번호 재설정
$ passwd username

# 재부팅
$ reboot
```

### 부팅 로그 분석

```bash
# journalctl로 부팅 로그 확인
$ journalctl -b
# -b: 현재 부팅
# -b -1: 이전 부팅
# -b -2: 그 전 부팅

# 특정 부팅의 로그
$ journalctl --list-boots
-2 3e3c... Mon 2024-11-15 09:23:45 KST—Mon 2024-11-15 18:45:12 KST
-1 8d2a... Tue 2024-11-16 08:15:23 KST—Tue 2024-11-16 22:30:45 KST
 0 f4b1... Mon 2024-11-17 10:30:45 KST—Mon 2024-11-17 12:45:23 KST

# 부팅 에러만 확인
$ journalctl -b -p err
Nov 17 10:30:52 hostname kernel: [drm:intel_cpu_fifo_underrun_irq_handler] *ERROR*

# 특정 서비스의 부팅 로그
$ journalctl -b -u nginx

# 커널 메시지만
$ journalctl -b -k

# 시간 범위 지정
$ journalctl --since "2024-11-17 10:00:00" --until "2024-11-17 11:00:00"
```

### 일반적인 부팅 문제

**1. 파일시스템 손상:**

```bash
# Live USB로 부팅 후 fsck 실행
$ sudo fsck /dev/sda2
fsck from util-linux 2.37.2
e2fsck 1.46.5 (30-Dec-2021)
/dev/sda2: clean, 234567/12345678 files, 8901234/49382716 blocks

# 강제 검사
$ sudo fsck -f /dev/sda2

# 자동 복구 시도
$ sudo fsck -y /dev/sda2

# 심각한 손상
$ sudo fsck -b 8193 /dev/sda2  # 대체 슈퍼블록 사용
```

**2. GRUB 손상:**

```bash
# 위에서 설명한 GRUB 복구 과정 수행
# 또는 간단하게:
$ sudo grub-install /dev/sda
$ sudo update-grub
```

**3. initramfs 문제:**

```bash
# initramfs 재생성
$ sudo update-initramfs -u -k all

# 특정 커널만
$ sudo update-initramfs -u -k 5.15.0-78-generic

# 디버그 정보와 함께
$ sudo update-initramfs -u -v -k all
```

**4. 커널 패닉:**

```bash
# 이전 커널로 부팅 (GRUB에서 선택)
# 문제되는 커널 제거
$ sudo apt remove linux-image-5.15.0-78-generic

# 커널 파라미터 추가 (GRUB 편집)
# 그래픽 드라이버 문제
nomodeset

# ACPI 문제
acpi=off
noapic

# 커널 디버깅
debug ignore_loglevel
```

**5. 서비스 시작 실패:**

```bash
# 실패한 서비스 확인
$ systemctl --failed
  UNIT                    LOAD   ACTIVE SUB    DESCRIPTION
● network-manager.service loaded failed failed Network Manager

# 상세 로그
$ systemctl status network-manager
$ journalctl -xe -u network-manager

# 서비스 비활성화하고 부팅
$ sudo systemctl mask problematic.service
```

---

## 부팅 최적화

### 부팅 시간 단축

**1. 불필요한 서비스 비활성화:**

```bash
# 느린 서비스 찾기
$ systemd-analyze blame | head -20

# 불필요한 서비스 비활성화
$ sudo systemctl disable bluetooth.service
$ sudo systemctl disable cups.service
$ sudo systemctl disable ModemManager.service

# 네트워크 대기 비활성화
$ sudo systemctl disable NetworkManager-wait-online.service
```

**2. 병렬화 증가:**

```bash
# /etc/systemd/system.conf 편집
$ sudo vi /etc/systemd/system.conf

[Manager]
DefaultTimeoutStartSec=30s
DefaultTimeoutStopSec=15s

# 재부팅 적용
$ sudo systemctl daemon-reload
```

**3. 파일시스템 최적화:**

```bash
# /etc/fstab에서 noatime 옵션 추가
UUID=xxx  /  ext4  defaults,noatime  0  1

# 재마운트
$ sudo mount -o remount /
```

**4. GRUB 타임아웃 단축:**

```bash
$ sudo vi /etc/default/grub
GRUB_TIMEOUT=2  # 5초 → 2초

$ sudo update-grub
```

**5. 프리로드 사용:**

```bash
# preload 설치 (자주 사용하는 프로그램 미리 로드)
$ sudo apt install preload
$ sudo systemctl enable preload
```

### 부팅 프로세스 모니터링

```bash
# 시각화된 부팅 차트 생성
$ systemd-analyze plot > boot.svg

# SVG 파일을 브라우저에서 열기
$ firefox boot.svg

# 중요 경로의 시간
$ systemd-analyze critical-chain graphical.target

# 모든 유닛의 시간
$ systemd-analyze time
```

---

## 실전 예제

### 예제 1: 부팅 시 자동 마운트

```bash
# NFS 공유를 부팅 시 자동 마운트
$ sudo vi /etc/fstab
192.168.1.100:/share  /mnt/nfs  nfs  defaults,_netdev  0  0

# _netdev: 네트워크가 준비된 후 마운트
```

### 예제 2: 커스텀 부팅 스크립트

```bash
# rc.local 스타일 스크립트 (systemd)
$ sudo vi /etc/systemd/system/my-startup.service

[Unit]
Description=My Startup Script
After=network.target

[Service]
Type=oneshot
ExecStart=/usr/local/bin/my-startup.sh
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target

# 스크립트 생성
$ sudo vi /usr/local/bin/my-startup.sh
#!/bin/bash
# 시작 시 실행할 명령들
echo "System started at $(date)" >> /var/log/startup.log
/usr/local/bin/check-services.sh

$ sudo chmod +x /usr/local/bin/my-startup.sh

# 활성화
$ sudo systemctl daemon-reload
$ sudo systemctl enable my-startup.service
```

### 예제 3: 응급 복구

```bash
# 루트 비밀번호를 잊어버렸을 때
1. GRUB에서 'e' 눌러 편집
2. linux 라인에서 "ro quiet splash" 찾기
3. "rw init=/bin/bash"로 변경
4. Ctrl+X로 부팅
5. 쉘에서:
   $ passwd root
   $ exec /sbin/init
```

---

## 요약

리눅스 부팅 프로세스의 5단계:

1. **BIOS/UEFI**: 하드웨어 초기화, 부팅 장치 선택
2. **부트로더**: 커널 로드, 파라미터 전달
3. **커널**: 시스템 초기화, 드라이버 로드
4. **init/systemd**: 서비스 관리, 시스템 구성
5. **타겟/런레벨**: 최종 시스템 상태 도달

각 단계를 이해하면 부팅 문제를 효과적으로 해결하고 시스템을 최적화할 수 있습니다.

---

[다음: 시스템 계층 구조 →](system-layers.md)

[← 커널 구조로 돌아가기](kernel.md)

[← 목차로 돌아가기](../README.md)
