# 파일시스템 타입

## 목차
- [파일시스템 개요](#파일시스템-개요)
- [ext 시리즈 (ext2/3/4)](#ext-시리즈-ext234)
- [XFS](#xfs)
- [Btrfs](#btrfs)
- [ZFS](#zfs)
- [FAT/NTFS](#fatntfs)
- [특수 파일시스템](#특수-파일시스템)
- [파일시스템 비교](#파일시스템-비교)

---

## 파일시스템 개요

파일시스템은 저장 장치에 데이터를 구조화하고 관리하는 방법을 정의합니다.

### 파일시스템의 역할

```
1. 데이터 저장 및 조직화
   - 파일과 디렉토리 구조
   - 메타데이터 관리

2. 공간 관리
   - 블록 할당
   - 여유 공간 추적

3. 접근 제어
   - 권한 관리
   - 소유권 관리

4. 데이터 무결성
   - 저널링
   - 체크섬
```

### 현재 사용 중인 파일시스템 확인

```bash
# 마운트된 파일시스템 확인
$ df -T
Filesystem     Type     1K-blocks      Used Available Use% Mounted on
/dev/sda2      ext4     487206912 128901856 333502384  28% /
/dev/sda1      vfat        523248      5324    517924   2% /boot/efi
tmpfs          tmpfs      1638404       123   1638281   1% /run
/dev/nvme0n1p1 xfs      999320576 456789012 542531564  46% /home

# 지원되는 파일시스템 목록
$ cat /proc/filesystems
nodev   sysfs
nodev   tmpfs
nodev   bdev
nodev   proc
        ext4
        ext3
        ext2
        vfat
        xfs
        btrfs
        ntfs

# 블록 디바이스의 파일시스템 타입
$ lsblk -f
NAME   FSTYPE LABEL UUID                                 MOUNTPOINT
sda
├─sda1 vfat         ABCD-1234                            /boot/efi
└─sda2 ext4         12345678-1234-1234-1234-123456789abc /
nvme0n1
└─nvme0n1p1 xfs    56789abc-5678-5678-5678-56789abcdef0 /home
```

---

## ext 시리즈 (ext2/3/4)

리눅스의 전통적인 파일시스템으로, Extended Filesystem의 약자입니다.

### ext2 (Second Extended Filesystem)

**특징:**
```
- 저널링 없음
- 간단하고 안정적
- USB 드라이브에 적합
- 최대 파일 크기: 2TB (4KB 블록 시)
- 최대 파일시스템 크기: 32TB
```

**ext2 생성:**
```bash
# ext2 파일시스템 생성
$ sudo mkfs.ext2 /dev/sdb1
mke2fs 1.46.5 (30-Dec-2021)
Creating filesystem with 26214400 4k blocks and 6553600 inodes
Filesystem UUID: 12345678-1234-1234-1234-123456789abc
Superblock backups stored on blocks:
    32768, 98304, 163840, 229376, 294912, 819200, 884736

# 블록 크기 지정
$ sudo mkfs.ext2 -b 4096 /dev/sdb1

# 레이블 지정
$ sudo mkfs.ext2 -L "MyData" /dev/sdb1

# inode 수 지정
$ sudo mkfs.ext2 -N 10000000 /dev/sdb1
```

### ext3 (Third Extended Filesystem)

**특징:**
```
- ext2 + 저널링
- 충돌 후 빠른 복구
- ext2와 호환
- 온라인 파일시스템 성장 지원
```

**저널링 모드:**
```bash
# journal (기본) - 메타데이터 + 데이터 저널링 (가장 안전, 느림)
$ sudo tune2fs -o journal_data /dev/sdb1

# ordered (권장) - 메타데이터만 저널링, 데이터는 순서 보장
$ sudo tune2fs -o journal_data_ordered /dev/sdb1

# writeback - 메타데이터만 저널링 (가장 빠름, 덜 안전)
$ sudo tune2fs -o journal_data_writeback /dev/sdb1

# 현재 설정 확인
$ sudo tune2fs -l /dev/sdb1 | grep "mount options"
Default mount options:    user_xattr acl
```

**ext3 생성 및 변환:**
```bash
# 새로운 ext3 생성
$ sudo mkfs.ext3 /dev/sdb1

# ext2를 ext3로 변환 (저널 추가)
$ sudo tune2fs -j /dev/sdb1

# ext3를 ext2로 변환 (저널 제거)
$ sudo tune2fs -O ^has_journal /dev/sdb1
```

### ext4 (Fourth Extended Filesystem)

**특징:**
```
- 현대 리눅스의 기본 파일시스템
- 최대 파일 크기: 16TB
- 최대 파일시스템 크기: 1EB (엑사바이트)
- 향상된 성능
- Extent 기반 할당
- 지연 할당
- 저널 체크섬
- 빠른 fsck
```

**ext4 생성:**
```bash
# 기본 ext4 생성
$ sudo mkfs.ext4 /dev/sdb1
mke2fs 1.46.5 (30-Dec-2021)
Creating filesystem with 26214400 4k blocks and 6553600 inodes
Filesystem UUID: abcdef01-2345-6789-abcd-ef0123456789
Superblock backups stored on blocks:
    32768, 98304, 163840, 229376, 294912, 819200, 884736

Allocating group tables: done
Writing inode tables: done
Creating journal (131072 blocks): done
Writing superblocks and filesystem accounting information: done

# SSD 최적화
$ sudo mkfs.ext4 -E discard /dev/sdb1

# 대용량 파일용 (4KB 블록, extent 크기 증가)
$ sudo mkfs.ext4 -E stride=32,stripe-width=64 /dev/sdb1
```

**ext4 최적화:**
```bash
# 예약 블록 비율 변경 (기본 5%)
$ sudo tune2fs -m 1 /dev/sdb1  # 1%로 변경

# 마지막 마운트 시간 업데이트 비활성화 (SSD 수명 연장)
$ sudo tune2fs -o noatime /dev/sdb1

# 파일시스템 레이블 변경
$ sudo tune2fs -L "NewLabel" /dev/sdb1

# 파일시스템 UUID 변경
$ sudo tune2fs -U random /dev/sdb1

# 파일시스템 정보 확인
$ sudo tune2fs -l /dev/sdb1
Filesystem volume name:   <none>
Last mounted on:          /mnt
Filesystem UUID:          abcdef01-2345-6789-abcd-ef0123456789
Filesystem magic number:  0xEF53
Filesystem revision #:    1 (dynamic)
Filesystem features:      has_journal ext_attr resize_inode dir_index
Block count:              26214400
Reserved block count:     1310720
Free blocks:              25678945
Free inodes:              6553589
First block:              0
Block size:               4096
Inode size:               256
Journal size:             128M
```

**ext4 온라인 리사이즈:**
```bash
# 파일시스템 확장 (파티션 먼저 확장 필요)
$ sudo resize2fs /dev/sdb1
resize2fs 1.46.5 (30-Dec-2021)
Filesystem at /dev/sdb1 is mounted on /mnt; on-line resizing required
Performing an on-line resize of /dev/sdb1 to 52428800 (4k) blocks.
The filesystem on /dev/sdb1 is now 52428800 (4k) blocks long.

# 특정 크기로 축소 (언마운트 필요)
$ sudo umount /dev/sdb1
$ sudo e2fsck -f /dev/sdb1
$ sudo resize2fs /dev/sdb1 100G
```

---

## XFS

고성능 저널링 파일시스템으로, SGI에서 개발했습니다.

### XFS 특징

```
- 대용량 파일 및 파일시스템 지원
- 최대 파일 크기: 8EB
- 최대 파일시스템 크기: 8EB
- 우수한 병렬 I/O 성능
- 온라인 확장 (축소는 불가)
- 지연 할당
- RHEL/CentOS의 기본 파일시스템
```

### XFS 생성 및 관리

```bash
# XFS 생성
$ sudo mkfs.xfs /dev/sdb1
meta-data=/dev/sdb1              isize=512    agcount=4, agsize=6553600 blks
data     =                       bsize=4096   blocks=26214400, imaxpct=25
naming   =version 2              bsize=4096   ascii-ci=0
log      =internal log           bsize=4096   blocks=12800, version=2
realtime =none                   extsz=4096   blocks=0, rtextents=0

# 레이블 지정
$ sudo mkfs.xfs -L "DataDrive" /dev/sdb1

# SSD 최적화
$ sudo mkfs.xfs -K /dev/sdb1

# 블록 크기 지정
$ sudo mkfs.xfs -b size=4096 /dev/sdb1

# RAID 최적화 (stripe unit 64K, stripe width 4 disks)
$ sudo mkfs.xfs -d su=64k,sw=4 /dev/md0
```

**XFS 정보 확인:**
```bash
# 파일시스템 정보
$ sudo xfs_info /dev/sdb1
meta-data=/dev/sdb1              isize=512    agcount=4, agsize=6553600 blks
         =                       sectsz=512   attr=2, projid32bit=1
data     =                       bsize=4096   blocks=26214400, imaxpct=25
         =                       sunit=0      swidth=0 blks
naming   =version 2              bsize=4096   ascii-ci=0 ftype=1
log      =internal               bsize=4096   blocks=12800, version=2
realtime =none                   extsz=4096   blocks=0, rtextents=0

# 또는 마운트된 경로로
$ sudo xfs_info /mnt
```

**XFS 확장:**
```bash
# 온라인 확장 (파티션 먼저 확장 필요)
$ sudo xfs_growfs /mnt
data blocks changed from 26214400 to 52428800

# 또는 디바이스로
$ sudo xfs_growfs /dev/sdb1
```

**XFS 복구:**
```bash
# 파일시스템 검사 (언마운트 상태)
$ sudo xfs_repair /dev/sdb1

# 체크만 (수정 안 함)
$ sudo xfs_repair -n /dev/sdb1

# 로그 초기화 (손상된 경우)
$ sudo xfs_repair -L /dev/sdb1
```

**XFS 백업 및 복원:**
```bash
# XFS 전용 백업 (파일시스템 레벨)
$ sudo xfsdump -f /backup/sdb1.dump /dev/sdb1

# 증분 백업 (레벨 1)
$ sudo xfsdump -l 1 -f /backup/sdb1_inc.dump /dev/sdb1

# 복원
$ sudo xfsrestore -f /backup/sdb1.dump /mnt/restore

# 복원 전 내용 확인
$ sudo xfsrestore -t -f /backup/sdb1.dump
```

---

## Btrfs

차세대 리눅스 파일시스템으로, B-tree 파일시스템입니다.

### Btrfs 특징

```
- Copy-on-Write (CoW)
- 스냅샷 및 복제
- 서브볼륨
- 온라인 리사이즈 (확장/축소)
- 내장 RAID 지원
- 압축 (zlib, lzo, zstd)
- 데이터 및 메타데이터 체크섬
- 자체 복구
```

### Btrfs 생성

```bash
# 기본 Btrfs 생성
$ sudo mkfs.btrfs /dev/sdb1
btrfs-progs v5.16.2
See http://btrfs.wiki.kernel.org for more information.

Label:              (null)
UUID:               12345678-1234-1234-1234-123456789abc
Node size:          16384
Sector size:        4096
Filesystem size:    100.00GiB
Block group profiles:
  Data:             single            8.00MiB
  Metadata:         DUP               1.00GiB
  System:           DUP               8.00MiB

# 레이블 지정
$ sudo mkfs.btrfs -L "BtrfsData" /dev/sdb1

# 다중 디바이스 (RAID1)
$ sudo mkfs.btrfs -m raid1 -d raid1 /dev/sdb1 /dev/sdc1

# 압축 활성화
$ sudo mount -o compress=zstd /dev/sdb1 /mnt

# /etc/fstab에 추가
/dev/sdb1  /mnt  btrfs  defaults,compress=zstd,noatime  0  0
```

### Btrfs 서브볼륨

```bash
# 서브볼륨 생성
$ sudo btrfs subvolume create /mnt/@home
$ sudo btrfs subvolume create /mnt/@var
$ sudo btrfs subvolume create /mnt/@snapshots

# 서브볼륨 목록
$ sudo btrfs subvolume list /mnt
ID 256 gen 8 top level 5 path @home
ID 257 gen 9 top level 5 path @var
ID 258 gen 10 top level 5 path @snapshots

# 서브볼륨 마운트
$ sudo mount -o subvol=@home /dev/sdb1 /home
$ sudo mount -o subvol=@var /dev/sdb1 /var

# 서브볼륨 삭제
$ sudo btrfs subvolume delete /mnt/@old
```

### Btrfs 스냅샷

```bash
# 읽기/쓰기 스냅샷 생성
$ sudo btrfs subvolume snapshot /mnt/@home /mnt/@snapshots/home_$(date +%Y%m%d)

# 읽기 전용 스냅샷
$ sudo btrfs subvolume snapshot -r /mnt/@home /mnt/@snapshots/home_ro_$(date +%Y%m%d)

# 스냅샷 복원
$ sudo mv /mnt/@home /mnt/@home_broken
$ sudo btrfs subvolume snapshot /mnt/@snapshots/home_20241117 /mnt/@home

# 스냅샷 삭제
$ sudo btrfs subvolume delete /mnt/@snapshots/home_20241110
```

### Btrfs 용량 관리

```bash
# 파일시스템 사용량
$ sudo btrfs filesystem usage /mnt
Overall:
    Device size:                 100.00GiB
    Device allocated:             12.02GiB
    Device unallocated:           87.98GiB
    Device missing:                  0.00B
    Used:                          5.23GiB
    Free (estimated):             94.00GiB

# 밸런스 실행 (공간 재배치)
$ sudo btrfs balance start /mnt

# 특정 사용률 이상만 밸런스
$ sudo btrfs balance start -dusage=50 /mnt

# 스크럽 (데이터 검증 및 복구)
$ sudo btrfs scrub start /mnt

# 스크럽 상태 확인
$ sudo btrfs scrub status /mnt

# 온라인 리사이즈
$ sudo btrfs filesystem resize +10G /mnt  # 10GB 확장
$ sudo btrfs filesystem resize -5G /mnt   # 5GB 축소
$ sudo btrfs filesystem resize max /mnt   # 최대로 확장
```

---

## ZFS

원래 Solaris용으로 개발된 고급 파일시스템입니다.

### ZFS 특징

```
- 128비트 파일시스템
- 통합 볼륨 관리
- Copy-on-Write
- 스냅샷 및 클론
- 압축 및 중복 제거
- 자체 복구
- RAID-Z (소프트웨어 RAID)
- 캐싱 (ARC, L2ARC)
```

### ZFS 설치 (Ubuntu)

```bash
# ZFS 설치
$ sudo apt install zfsutils-linux

# 커널 모듈 확인
$ lsmod | grep zfs
zfs                  4395008  6
zunicode              331776  1 zfs
zzstd                 495616  1 zfs
zlua                  180224  1 zfs
zavl                   16384  1 zfs
```

### ZFS 풀 생성

```bash
# 단일 디스크 풀
$ sudo zpool create mypool /dev/sdb

# 미러 (RAID1)
$ sudo zpool create mypool mirror /dev/sdb /dev/sdc

# RAID-Z (RAID5 유사)
$ sudo zpool create mypool raidz /dev/sdb /dev/sdc /dev/sdd

# RAID-Z2 (RAID6 유사)
$ sudo zpool create mypool raidz2 /dev/sdb /dev/sdc /dev/sdd /dev/sde

# 풀 상태 확인
$ sudo zpool status
  pool: mypool
 state: ONLINE
  scan: none requested
config:

    NAME        STATE     READ WRITE CKSUM
    mypool      ONLINE       0     0     0
      raidz1-0  ONLINE       0     0     0
        sdb     ONLINE       0     0     0
        sdc     ONLINE       0     0     0
        sdd     ONLINE       0     0     0

# 풀 용량 확인
$ sudo zpool list
NAME     SIZE  ALLOC   FREE  CKPOINT  EXPANDSZ   FRAG    CAP  DEDUP  HEALTH
mypool   279G  12.3G   267G        -         -     2%     4%  1.00x  ONLINE
```

### ZFS 데이터셋

```bash
# 데이터셋 생성
$ sudo zfs create mypool/home
$ sudo zfs create mypool/var
$ sudo zfs create mypool/data

# 데이터셋 목록
$ sudo zfs list
NAME           USED  AVAIL  REFER  MOUNTPOINT
mypool         156K   256G    24K  /mypool
mypool/home     24K   256G    24K  /mypool/home
mypool/var      24K   256G    24K  /mypool/var
mypool/data     24K   256G    24K  /mypool/data

# 마운트 포인트 변경
$ sudo zfs set mountpoint=/home mypool/home

# 압축 활성화
$ sudo zfs set compression=lz4 mypool/home

# 중복 제거 활성화 (RAM 많이 필요)
$ sudo zfs set dedup=on mypool/data

# 쿼터 설정
$ sudo zfs set quota=50G mypool/home
```

### ZFS 스냅샷

```bash
# 스냅샷 생성
$ sudo zfs snapshot mypool/home@backup_$(date +%Y%m%d)

# 스냅샷 목록
$ sudo zfs list -t snapshot
NAME                              USED  AVAIL  REFER  MOUNTPOINT
mypool/home@backup_20241117        0B      -  1.2G  -
mypool/home@backup_20241110      123M      -  1.1G  -

# 스냅샷 복원
$ sudo zfs rollback mypool/home@backup_20241117

# 스냅샷에서 클론 생성
$ sudo zfs clone mypool/home@backup_20241117 mypool/home_clone

# 스냅샷 삭제
$ sudo zfs destroy mypool/home@backup_20241110
```

---

## FAT/NTFS

Windows와의 호환성을 위한 파일시스템입니다.

### FAT32

```bash
# FAT32 생성 (32GB 이하 권장)
$ sudo mkfs.vfat /dev/sdb1

# 또는
$ sudo mkfs.fat -F 32 /dev/sdb1

# 레이블 지정
$ sudo mkfs.vfat -n "USB_DRIVE" /dev/sdb1

# 마운트
$ sudo mount -t vfat /dev/sdb1 /mnt

# 한글 파일명 지원
$ sudo mount -t vfat -o iocharset=utf8 /dev/sdb1 /mnt
```

### exFAT

```bash
# exFAT 도구 설치
$ sudo apt install exfat-fuse exfat-utils

# exFAT 생성
$ sudo mkfs.exfat /dev/sdb1

# 레이블 지정
$ sudo mkfs.exfat -n "EXTERNAL" /dev/sdb1

# 마운트
$ sudo mount -t exfat /dev/sdb1 /mnt
```

### NTFS

```bash
# NTFS 도구 설치
$ sudo apt install ntfs-3g

# NTFS 생성
$ sudo mkfs.ntfs /dev/sdb1

# 빠른 포맷
$ sudo mkfs.ntfs -f /dev/sdb1

# 레이블 지정
$ sudo mkfs.ntfs -L "Windows_Disk" /dev/sdb1

# 읽기/쓰기 마운트
$ sudo mount -t ntfs-3g /dev/sdb1 /mnt

# 권한 옵션과 함께 마운트
$ sudo mount -t ntfs-3g -o uid=1000,gid=1000,dmask=022,fmask=133 /dev/sdb1 /mnt
```

---

## 특수 파일시스템

### tmpfs (메모리 기반)

```bash
# tmpfs 생성 (RAM 디스크)
$ sudo mount -t tmpfs -o size=512M tmpfs /mnt/ramdisk

# /etc/fstab에 추가
tmpfs  /mnt/ramdisk  tmpfs  defaults,size=512M,mode=1777  0  0

# 사용 확인
$ df -h /mnt/ramdisk
Filesystem      Size  Used Avail Use% Mounted on
tmpfs           512M  123K  512M   1% /mnt/ramdisk
```

### procfs

```bash
# 프로세스 정보 파일시스템
$ mount | grep proc
proc on /proc type proc (rw,nosuid,nodev,noexec,relatime)

# 프로세스 정보 읽기
$ cat /proc/cpuinfo | head -10
$ cat /proc/meminfo
$ cat /proc/1/cmdline
```

### sysfs

```bash
# 시스템 정보 파일시스템
$ mount | grep sysfs
sysfs on /sys type sysfs (rw,nosuid,nodev,noexec,relatime)

# 하드웨어 정보
$ cat /sys/block/sda/size
$ cat /sys/class/net/eth0/address
```

### NFS (Network File System)

```bash
# NFS 클라이언트 설치
$ sudo apt install nfs-common

# NFS 마운트
$ sudo mount -t nfs 192.168.1.100:/share /mnt/nfs

# /etc/fstab에 추가
192.168.1.100:/share  /mnt/nfs  nfs  defaults,_netdev  0  0

# NFS 옵션
$ sudo mount -t nfs -o rw,sync,hard,intr 192.168.1.100:/share /mnt/nfs
```

### FUSE (Filesystem in Userspace)

```bash
# SSHFS - SSH를 통한 원격 파일시스템
$ sudo apt install sshfs

$ sshfs user@remote:/path /mnt/remote
$ fusermount -u /mnt/remote  # 언마운트

# EncFS - 암호화 파일시스템
$ sudo apt install encfs

$ encfs ~/.encrypted ~/Private
$ fusermount -u ~/Private
```

---

## 파일시스템 비교

### 성능 비교

| 파일시스템 | 최대 파일 | 최대 FS | 저널링 | 스냅샷 | 압축 | 주 용도 |
|----------|---------|---------|--------|--------|------|---------|
| ext4 | 16TB | 1EB | O | X | X | 범용 |
| XFS | 8EB | 8EB | O | X | X | 대용량, 고성능 |
| Btrfs | 16EB | 16EB | O | O | O | 서버, NAS |
| ZFS | 16EB | 256 quintillion | O | O | O | 엔터프라이즈 |
| NTFS | 16EB | 16EB | O | X | O | Windows 호환 |
| FAT32 | 4GB | 2TB | X | X | X | USB, 호환성 |

### 선택 가이드

```bash
# 일반적인 데스크탑/서버
→ ext4 (안정적, 검증됨)

# 대용량 파일 (비디오, DB)
→ XFS (우수한 성능)

# 스냅샷, 백업이 중요한 경우
→ Btrfs, ZFS (CoW, 스냅샷)

# RAID 및 데이터 무결성이 중요
→ ZFS (자체 복구, RAID-Z)

# USB, 외장 드라이브 (호환성)
→ exFAT, NTFS

# 부팅 파티션 (UEFI)
→ FAT32 (EFI 표준)
```

---

## 실전 예제

### 예제 1: 듀얼 부팅 시스템

```bash
# 파티션 레이아웃
/dev/sda1  512MB   FAT32   /boot/efi     # UEFI
/dev/sda2  100GB   ext4    /             # Linux 루트
/dev/sda3  200GB   NTFS    -             # Windows
/dev/sda4  8GB     swap    -             # Swap
/dev/sda5  200GB   ext4    /home         # Linux 홈
```

### 예제 2: 서버 구성

```bash
# 파티션 레이아웃
/dev/sda1  1GB     ext4    /boot
/dev/sda2  50GB    ext4    /
/dev/sdb1  1TB     XFS     /var          # 로그 및 데이터
/dev/sdc1  2TB     Btrfs   /backup       # 백업 (스냅샷)
```

### 예제 3: NAS 구성

```bash
# ZFS RAID-Z 구성
$ sudo zpool create storage raidz /dev/sd{b,c,d,e}
$ sudo zfs create storage/media
$ sudo zfs create storage/backups
$ sudo zfs set compression=lz4 storage
$ sudo zfs set quota=1T storage/media
```

---

## 요약

각 파일시스템의 특성을 이해하고 용도에 맞게 선택하는 것이 중요합니다:

- **ext4**: 안정적인 범용 파일시스템
- **XFS**: 고성능이 필요한 경우
- **Btrfs/ZFS**: 고급 기능 (스냅샷, CoW) 필요 시
- **FAT/NTFS**: 호환성이 중요한 경우

---

[다음: 파일시스템 작업 →](operations.md)

[← 파일시스템 구조로 돌아가기](structure.md)

[← 목차로 돌아가기](../README.md)
