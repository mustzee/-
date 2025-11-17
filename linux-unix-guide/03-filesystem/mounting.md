# 파일시스템 마운팅

## 목차
- [마운팅 개념](#마운팅-개념)
- [mount 명령어](#mount-명령어)
- [umount 명령어](#umount-명령어)
- [/etc/fstab 설정](#etcfstab-설정)
- [자동 마운팅](#자동-마운팅)
- [네트워크 파일시스템](#네트워크-파일시스템)
- [루프백 디바이스](#루프백-디바이스)

---

## 마운팅 개념

리눅스에서는 모든 저장 장치를 파일시스템 트리의 특정 지점에 "마운트"하여 접근합니다.

### 마운팅이란?

```
저장 장치(파티션) → 디렉토리(마운트 포인트)로 연결

예시:
/dev/sdb1 (USB 드라이브) → /mnt/usb (마운트 포인트)

마운트 전:
/mnt/usb/ (빈 디렉토리)

마운트 후:
/mnt/usb/ (USB 드라이브의 내용)
```

### 현재 마운트 확인

```bash
# 모든 마운트 포인트 확인
$ mount
sysfs on /sys type sysfs (rw,nosuid,nodev,noexec,relatime)
proc on /proc type proc (rw,nosuid,nodev,noexec,relatime)
udev on /dev type devtmpfs (rw,nosuid,relatime,size=8158812k)
/dev/sda2 on / type ext4 (rw,relatime,errors=remount-ro)
/dev/sda1 on /boot/efi type vfat (rw,relatime,fmask=0077,dmask=0077)

# 깔끔한 출력
$ mount | column -t

# 특정 타입만 확인
$ mount -t ext4

# df로 확인
$ df -h
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda2       465G  123G  320G  28% /
/dev/sda1       511M  5.3M  506M   2% /boot/efi

# findmnt로 확인 (트리 형태)
$ findmnt
TARGET                SOURCE     FSTYPE  OPTIONS
/                     /dev/sda2  ext4    rw,relatime,errors=remount-ro
├─/sys                sysfs      sysfs   rw,nosuid,nodev,noexec
├─/proc               proc       proc    rw,nosuid,nodev,noexec
├─/dev                udev       devtmpfs rw,nosuid,relatime
└─/boot/efi           /dev/sda1  vfat    rw,relatime

# 특정 디바이스 확인
$ findmnt /dev/sdb1
TARGET SOURCE    FSTYPE OPTIONS
/mnt   /dev/sdb1 ext4   rw,relatime
```

---

## mount 명령어

### 기본 마운팅

```bash
# 기본 마운트
$ sudo mount /dev/sdb1 /mnt
# 파일시스템 타입 자동 감지

# 파일시스템 타입 지정
$ sudo mount -t ext4 /dev/sdb1 /mnt
$ sudo mount -t vfat /dev/sdb1 /mnt
$ sudo mount -t ntfs-3g /dev/sdb1 /mnt
$ sudo mount -t xfs /dev/sdb1 /mnt

# 읽기 전용 마운트
$ sudo mount -o ro /dev/sdb1 /mnt

# 읽기/쓰기 마운트
$ sudo mount -o rw /dev/sdb1 /mnt

# 여러 옵션 결합
$ sudo mount -o rw,noexec,nosuid /dev/sdb1 /mnt
```

### 마운트 옵션

```bash
# rw / ro - 읽기/쓰기 또는 읽기 전용
$ sudo mount -o ro /dev/sdb1 /mnt

# noexec - 실행 파일 실행 금지
$ sudo mount -o noexec /dev/sdb1 /mnt

# nosuid - SUID 비트 무시
$ sudo mount -o nosuid /dev/sdb1 /mnt

# nodev - 디바이스 파일 무시
$ sudo mount -o nodev /dev/sdb1 /mnt

# noatime - 접근 시간 업데이트 안 함 (성능 향상)
$ sudo mount -o noatime /dev/sdb1 /mnt

# nodiratime - 디렉토리 접근 시간 업데이트 안 함
$ sudo mount -o nodiratime /dev/sdb1 /mnt

# relatime - 상대적으로 접근 시간 업데이트 (기본값, 절충안)
$ sudo mount -o relatime /dev/sdb1 /mnt

# sync - 동기 I/O (안전하지만 느림)
$ sudo mount -o sync /dev/sdb1 /mnt

# async - 비동기 I/O (빠르지만 덜 안전, 기본값)
$ sudo mount -o async /dev/sdb1 /mnt

# user - 일반 사용자도 마운트 가능
$ sudo mount -o user /dev/sdb1 /mnt

# users - 일반 사용자가 마운트/언마운트 가능
$ sudo mount -o users /dev/sdb1 /mnt

# uid, gid - 소유자 지정 (FAT, NTFS 등)
$ sudo mount -o uid=1000,gid=1000 /dev/sdb1 /mnt

# umask - 권한 마스크 (FAT, NTFS 등)
$ sudo mount -o umask=022 /dev/sdb1 /mnt

# 파일과 디렉토리 권한 따로 지정
$ sudo mount -o fmask=133,dmask=022 /dev/sdb1 /mnt
```

### UUID 또는 레이블로 마운트

```bash
# UUID 확인
$ sudo blkid /dev/sdb1
/dev/sdb1: UUID="12345678-1234-1234-1234-123456789abc" TYPE="ext4"

# UUID로 마운트
$ sudo mount UUID=12345678-1234-1234-1234-123456789abc /mnt

# 레이블 확인
$ sudo blkid /dev/sdb1
/dev/sdb1: LABEL="MyData" UUID="..." TYPE="ext4"

# 레이블로 마운트
$ sudo mount LABEL=MyData /mnt

# 레이블 설정
$ sudo e2label /dev/sdb1 "MyData"          # ext2/3/4
$ sudo xfs_admin -L "MyData" /dev/sdb1     # XFS
$ sudo fatlabel /dev/sdb1 "MyData"         # FAT
$ sudo ntfslabel /dev/sdb1 "MyData"        # NTFS
```

### 리마운트

```bash
# 마운트된 파일시스템 옵션 변경
$ sudo mount -o remount,rw /mnt

# 읽기 전용으로 변경
$ sudo mount -o remount,ro /mnt

# noexec 추가
$ sudo mount -o remount,noexec /mnt

# 루트 파일시스템 리마운트
$ sudo mount -o remount,rw /

# 모든 파일시스템 리마운트
$ sudo mount -a
```

### 바인드 마운트

```bash
# 디렉토리를 다른 위치에 마운트
$ sudo mount --bind /source/directory /target/directory

# 예: 홈 디렉토리를 chroot 환경에 연결
$ sudo mount --bind /home /mnt/chroot/home

# 읽기 전용 바인드 마운트
$ sudo mount --bind /source /target
$ sudo mount -o remount,ro,bind /target

# 바인드 마운트 확인
$ findmnt | grep bind
```

---

## umount 명령어

### 기본 언마운트

```bash
# 마운트 포인트로 언마운트
$ sudo umount /mnt

# 디바이스로 언마운트
$ sudo umount /dev/sdb1

# 강제 언마운트
$ sudo umount -f /mnt

# 지연 언마운트 (사용 중일 때)
$ sudo umount -l /mnt

# 모든 옵션 조합
$ sudo umount -fl /mnt
```

### 언마운트 문제 해결

```bash
# "device is busy" 오류 시

# 1. 어떤 프로세스가 사용 중인지 확인
$ sudo lsof /mnt
COMMAND  PID USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
bash    1234 user  cwd    DIR    8,1     4096    2 /mnt

$ sudo fuser -v /mnt
                     USER        PID ACCESS COMMAND
/mnt:                user       1234 ..c.. bash

# 2. 해당 프로세스 종료
$ sudo kill 1234

# 3. 또는 강제 종료
$ sudo fuser -km /mnt

# 4. 디렉토리에서 나오기
$ cd ~

# 5. 다시 언마운트 시도
$ sudo umount /mnt

# 마지막 수단: 지연 언마운트
$ sudo umount -l /mnt
```

---

## /etc/fstab 설정

/etc/fstab는 부팅 시 자동으로 마운트할 파일시스템을 정의합니다.

### fstab 형식

```bash
$ cat /etc/fstab
# <device>  <mount point>  <type>  <options>  <dump>  <pass>

# 예제
UUID=xxx-xxx  /              ext4    errors=remount-ro  0  1
UUID=yyy-yyy  /boot/efi      vfat    umask=0077         0  1
UUID=zzz-zzz  /home          ext4    defaults           0  2
UUID=aaa-aaa  none           swap    sw                 0  0
```

### 필드 설명

```
1. <device>
   - /dev/sdb1, UUID=..., LABEL=..., PARTUUID=...

2. <mount point>
   - 마운트 위치
   - swap의 경우 "none"

3. <type>
   - ext4, xfs, vfat, ntfs, swap, nfs 등

4. <options>
   - defaults, rw, ro, noexec, noatime 등

5. <dump>
   - 0: dump 백업 안 함
   - 1: dump 백업 수행

6. <pass>
   - 0: fsck 체크 안 함
   - 1: 루트 파일시스템 (먼저 체크)
   - 2: 다른 파일시스템 (나중에 체크)
```

### fstab 예제

```bash
# 기본 ext4 파티션
UUID=12345678-1234-1234-1234-123456789abc  /data  ext4  defaults  0  2

# 성능 최적화
UUID=12345678-1234-1234-1234-123456789abc  /data  ext4  defaults,noatime,nodiratime  0  2

# USB 드라이브 (사용자 마운트 허용)
UUID=ABCD-1234  /media/usb  vfat  users,noauto,umask=000  0  0

# NTFS 파티션
UUID=12345678ABCD  /mnt/windows  ntfs-3g  defaults,uid=1000,gid=1000,umask=022  0  0

# Swap
UUID=aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee  none  swap  sw  0  0

# NFS 마운트
192.168.1.100:/share  /mnt/nfs  nfs  defaults,_netdev  0  0

# tmpfs (RAM 디스크)
tmpfs  /tmp  tmpfs  defaults,size=2G,mode=1777  0  0

# 바인드 마운트
/home/user/data  /var/www/html  none  bind  0  0
```

### fstab 테스트

```bash
# fstab 문법 확인
$ sudo mount -a
# 오류가 없으면 OK

# 특정 마운트 포인트만 마운트
$ sudo mount /data

# 자세한 출력
$ sudo mount -av

# 언마운트
$ sudo umount -a
# 주의: 루트와 중요 파일시스템은 언마운트 안 됨

# fstab 백업
$ sudo cp /etc/fstab /etc/fstab.backup

# 잘못된 fstab으로 부팅 실패 시 복구
# 1. 부팅 시 GRUB에서 'e' 눌러 편집
# 2. linux 라인에 "single" 또는 "1" 추가
# 3. 부팅 후:
$ sudo mount -o remount,rw /
$ sudo vi /etc/fstab  # 수정
$ reboot
```

---

## 자동 마운팅

### systemd .mount 유닛

```bash
# systemd 마운트 유닛 생성
$ sudo vi /etc/systemd/system/mnt-data.mount

[Unit]
Description=Data Partition
After=local-fs-pre.target

[Mount]
What=/dev/disk/by-uuid/12345678-1234-1234-1234-123456789abc
Where=/mnt/data
Type=ext4
Options=defaults,noatime

[Install]
WantedBy=multi-user.target

# 활성화
$ sudo systemctl daemon-reload
$ sudo systemctl enable mnt-data.mount
$ sudo systemctl start mnt-data.mount

# 상태 확인
$ sudo systemctl status mnt-data.mount
```

### systemd .automount (필요 시 마운트)

```bash
$ sudo vi /etc/systemd/system/mnt-data.automount

[Unit]
Description=Automount Data Partition

[Automount]
Where=/mnt/data
TimeoutIdleSec=60

[Install]
WantedBy=multi-user.target

# 활성화
$ sudo systemctl enable mnt-data.automount
$ sudo systemctl start mnt-data.automount

# 접근 시 자동 마운트, 60초 미사용 시 자동 언마운트
```

### autofs

```bash
# autofs 설치
$ sudo apt install autofs

# 마스터 설정 파일
$ sudo vi /etc/auto.master
/mnt/auto  /etc/auto.misc  --timeout=60

# 마운트 정의
$ sudo vi /etc/auto.misc
usb  -fstype=vfat,rw,uid=1000  :/dev/sdb1
data  -fstype=ext4  :/dev/disk/by-label/DATA

# 서비스 재시작
$ sudo systemctl restart autofs

# 접근 시 자동 마운트
$ ls /mnt/auto/usb
# 자동으로 /dev/sdb1이 마운트됨
```

### udev 규칙 (USB 자동 마운트)

```bash
# udev 규칙 생성
$ sudo vi /etc/udev/rules.d/99-usb-automount.rules

# USB 드라이브 삽입 시 자동 마운트
ACTION=="add", KERNEL=="sd[a-z][0-9]", SUBSYSTEM=="block", \
  RUN+="/usr/local/bin/usb-mount.sh %k"

ACTION=="remove", KERNEL=="sd[a-z][0-9]", SUBSYSTEM=="block", \
  RUN+="/usr/local/bin/usb-umount.sh %k"

# 마운트 스크립트
$ sudo vi /usr/local/bin/usb-mount.sh
#!/bin/bash
DEVICE=$1
MOUNT_POINT="/media/usb_$DEVICE"

mkdir -p "$MOUNT_POINT"
mount "/dev/$DEVICE" "$MOUNT_POINT"

$ sudo chmod +x /usr/local/bin/usb-mount.sh

# udev 재로드
$ sudo udevadm control --reload-rules
```

---

## 네트워크 파일시스템

### NFS (Network File System)

```bash
# NFS 클라이언트 설치
$ sudo apt install nfs-common

# NFS 공유 확인
$ showmount -e 192.168.1.100
Export list for 192.168.1.100:
/share      *
/data       192.168.1.0/24

# NFS 마운트
$ sudo mount -t nfs 192.168.1.100:/share /mnt/nfs

# NFSv4 마운트
$ sudo mount -t nfs4 192.168.1.100:/share /mnt/nfs

# 옵션과 함께 마운트
$ sudo mount -t nfs -o rw,sync,hard,intr 192.168.1.100:/share /mnt/nfs

# /etc/fstab에 추가
192.168.1.100:/share  /mnt/nfs  nfs  defaults,_netdev,rw,soft,intr  0  0
# _netdev: 네트워크 준비 후 마운트

# NFS 마운트 상태 확인
$ nfsstat -m
```

### CIFS/SMB (Windows 공유)

```bash
# CIFS 도구 설치
$ sudo apt install cifs-utils

# Windows/Samba 공유 마운트
$ sudo mount -t cifs //192.168.1.100/share /mnt/windows \
  -o username=user,password=pass

# 자격 증명 파일 사용 (보안)
$ sudo vi /root/.smbcredentials
username=user
password=pass
domain=WORKGROUP

$ sudo chmod 600 /root/.smbcredentials

$ sudo mount -t cifs //192.168.1.100/share /mnt/windows \
  -o credentials=/root/.smbcredentials,uid=1000,gid=1000

# /etc/fstab에 추가
//192.168.1.100/share  /mnt/windows  cifs  credentials=/root/.smbcredentials,uid=1000,gid=1000,_netdev  0  0
```

### SSHFS

```bash
# SSHFS 설치
$ sudo apt install sshfs

# SSH를 통한 원격 파일시스템 마운트
$ sshfs user@remote.server.com:/path /mnt/remote

# 포트 지정
$ sshfs -p 2222 user@remote.server.com:/path /mnt/remote

# 옵션과 함께
$ sshfs user@remote.server.com:/path /mnt/remote \
  -o allow_other,default_permissions,uid=1000,gid=1000

# 언마운트
$ fusermount -u /mnt/remote

# /etc/fstab에 추가
sshfs#user@remote:/path  /mnt/remote  fuse  delay_connect,_netdev,user,idmap=user,transform_symlinks,identityfile=/home/user/.ssh/id_rsa  0  0
```

---

## 루프백 디바이스

### ISO 파일 마운트

```bash
# ISO 파일을 루프백으로 마운트
$ sudo mount -o loop ubuntu.iso /mnt/iso

# 또는 명시적으로
$ sudo mount -t iso9660 -o loop ubuntu.iso /mnt/iso

# 읽기 전용으로 자동 마운트됨
$ mount | grep iso
/home/user/ubuntu.iso on /mnt/iso type iso9660 (ro,relatime,nojoliet,check=s,map=n,blocksize=2048)

# 언마운트
$ sudo umount /mnt/iso
```

### 디스크 이미지 마운트

```bash
# 디스크 이미지 생성
$ dd if=/dev/zero of=disk.img bs=1M count=100
100+0 records in
100+0 records out
104857600 bytes (105 MB) copied

# 파일시스템 생성
$ sudo mkfs.ext4 disk.img

# 루프백 디바이스로 마운트
$ sudo mount -o loop disk.img /mnt/loop

# 또는 losetup 사용
$ sudo losetup -f
/dev/loop0

$ sudo losetup /dev/loop0 disk.img
$ sudo mount /dev/loop0 /mnt/loop

# 언마운트 및 루프백 해제
$ sudo umount /mnt/loop
$ sudo losetup -d /dev/loop0

# 모든 루프백 디바이스 확인
$ losetup -a
```

### 파티션이 있는 이미지 마운트

```bash
# 파티션 정보 확인
$ fdisk -l disk.img
Disk disk.img: 10 GiB
Units: sectors of 1 * 512 = 512 bytes

Device     Boot Start      End  Sectors Size Id Type
disk.img1        2048  2099199  2097152   1G 83 Linux
disk.img2     2099200 20971519 18872320   9G 83 Linux

# 오프셋 계산
# 시작 섹터 * 섹터 크기 = 2048 * 512 = 1048576

# 특정 파티션 마운트
$ sudo mount -o loop,offset=1048576 disk.img /mnt/partition1

# 또는 losetup의 파티션 스캔
$ sudo losetup -fP disk.img
$ lsblk
NAME      MAJ:MIN RM SIZE RO TYPE MOUNTPOINT
loop0       7:0    0  10G  0 loop
├─loop0p1 259:0    0   1G  0 loop
└─loop0p2 259:1    0   9G  0 loop

$ sudo mount /dev/loop0p1 /mnt/partition1
```

---

## 실전 예제

### 예제 1: USB 드라이브 자동 마운트

```bash
# /etc/fstab 설정
UUID=XXXX-XXXX  /media/usb  vfat  users,noauto,umask=000,uid=1000,gid=1000  0  0

# 사용자가 마운트 가능
$ mount /media/usb
$ umount /media/usb
```

### 예제 2: 원격 백업 마운트

```bash
# SSH 키 설정
$ ssh-copy-id backup@backup.server.com

# SSHFS 마운트
$ mkdir ~/backup
$ sshfs backup@backup.server.com:/backups ~/backup

# 백업 수행
$ rsync -av /important/data/ ~/backup/daily/

# 언마운트
$ fusermount -u ~/backup
```

### 예제 3: 암호화된 파일시스템

```bash
# LUKS 암호화 볼륨 마운트
$ sudo cryptsetup luksOpen /dev/sdb1 encrypted_volume

# 파일시스템 마운트
$ sudo mount /dev/mapper/encrypted_volume /mnt/encrypted

# 사용 후 정리
$ sudo umount /mnt/encrypted
$ sudo cryptsetup luksClose encrypted_volume
```

---

## 요약

파일시스템 마운팅의 핵심:

1. **mount**: 파일시스템 연결
2. **umount**: 파일시스템 분리
3. **/etc/fstab**: 영구적 마운트 설정
4. **자동 마운트**: systemd, autofs, udev
5. **네트워크**: NFS, CIFS, SSHFS

올바른 마운트/언마운트는 데이터 무결성과 시스템 안정성에 중요합니다.

---

[다음: 기본 명령어 →](../04-commands/basic.md)

[← 파일시스템 작업으로 돌아가기](operations.md)

[← 목차로 돌아가기](../README.md)
