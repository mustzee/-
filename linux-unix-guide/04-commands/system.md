# 시스템 관리 명령어

## 목차
- [프로세스 관리](#프로세스-관리)
- [사용자 및 그룹 관리](#사용자-및-그룹-관리)
- [디스크 관리](#디스크-관리)
- [시스템 모니터링](#시스템-모니터링)
- [패키지 관리](#패키지-관리)

---

## 프로세스 관리

### ps - 프로세스 목록

```bash
# 현재 터미널의 프로세스
$ ps
  PID TTY          TIME CMD
 1234 pts/0    00:00:00 bash
 5678 pts/0    00:00:00 ps

# 모든 프로세스
$ ps aux
$ ps -ef

# 프로세스 트리
$ ps auxf
$ ps -ejH
$ pstree

# 특정 사용자
$ ps -u username

# 특정 프로세스
$ ps -p 1234

# 메모리 사용량 순
$ ps aux --sort=-%mem | head

# CPU 사용량 순
$ ps aux --sort=-%cpu | head

# 특정 명령어
$ ps aux | grep nginx

# 자세한 정보
$ ps -eo pid,ppid,cmd,%mem,%cpu --sort=-%cpu

# 실시간 업데이트
$ watch -n 1 'ps aux --sort=-%cpu | head -20'
```

### top - 실시간 프로세스 모니터

```bash
# 기본 실행
$ top

# 내부 명령어:
# h: 도움말
# k: 프로세스 종료
# r: 우선순위 변경
# M: 메모리 사용량 정렬
# P: CPU 사용량 정렬
# q: 종료

# 특정 사용자만
$ top -u username

# 업데이트 간격 지정
$ top -d 5  # 5초마다

# 배치 모드 (스크립트용)
$ top -b -n 1 > top_output.txt

# htop (더 나은 대안)
$ sudo apt install htop
$ htop
```

### kill - 프로세스 종료

```bash
# 기본 종료 (SIGTERM)
$ kill 1234

# 강제 종료 (SIGKILL)
$ kill -9 1234
$ kill -KILL 1234

# 재시작 신호 (SIGHUP)
$ kill -1 1234
$ kill -HUP 1234

# 모든 시그널 목록
$ kill -l

# 프로세스 이름으로 종료
$ killall nginx
$ killall -9 firefox

# 패턴으로 종료
$ pkill -f "python.*script"

# 사용자의 모든 프로세스
$ pkill -u username

# 확인 후 종료
$ pgrep nginx  # PID 확인
$ kill $(pgrep nginx)
```

### systemctl - 서비스 관리

```bash
# 서비스 시작/중지/재시작
$ sudo systemctl start nginx
$ sudo systemctl stop nginx
$ sudo systemctl restart nginx
$ sudo systemctl reload nginx

# 서비스 상태
$ systemctl status nginx

# 부팅 시 자동 시작
$ sudo systemctl enable nginx
$ sudo systemctl disable nginx

# 마스크 (시작 완전 금지)
$ sudo systemctl mask nginx
$ sudo systemctl unmask nginx

# 모든 서비스 목록
$ systemctl list-units --type=service
$ systemctl list-units --state=running

# 실패한 서비스
$ systemctl --failed

# 부팅 시 시작되는 서비스
$ systemctl list-unit-files --state=enabled

# 서비스 의존성
$ systemctl list-dependencies nginx

# 서비스 로그
$ journalctl -u nginx
$ journalctl -u nginx -f  # 실시간
```

---

## 사용자 및 그룹 관리

### useradd / usermod / userdel

```bash
# 사용자 추가
$ sudo useradd alice
$ sudo useradd -m -s /bin/bash alice  # 홈 디렉토리 + 쉘

# 비밀번호 설정
$ sudo passwd alice

# 사용자 정보 수정
$ sudo usermod -c "Alice Smith" alice  # 전체 이름
$ sudo usermod -s /bin/zsh alice       # 쉘 변경
$ sudo usermod -d /new/home alice      # 홈 디렉토리

# 그룹 추가
$ sudo usermod -aG sudo alice          # sudo 그룹에 추가
$ sudo usermod -aG docker,www-data alice

# 사용자 잠금/해제
$ sudo usermod -L alice  # 잠금
$ sudo usermod -U alice  # 해제

# 사용자 삭제
$ sudo userdel alice           # 사용자만
$ sudo userdel -r alice        # 홈 디렉토리도

# 사용자 정보 확인
$ id alice
$ finger alice
$ getent passwd alice
```

### groupadd / groupmod / groupdel

```bash
# 그룹 추가
$ sudo groupadd developers

# GID 지정
$ sudo groupadd -g 5000 developers

# 그룹 이름 변경
$ sudo groupmod -n newname oldname

# GID 변경
$ sudo groupmod -g 6000 developers

# 그룹 삭제
$ sudo groupdel developers

# 그룹 확인
$ getent group developers
$ groups username
```

### sudo - 관리자 권한 실행

```bash
# 명령어 실행
$ sudo command

# 특정 사용자로 실행
$ sudo -u alice command

# 쉘 시작
$ sudo -i  # root 로그인 쉘
$ sudo -s  # root 쉘

# 비밀번호 캐시 갱신
$ sudo -v

# 비밀번호 캐시 삭제
$ sudo -k

# 설정 편집
$ sudo visudo  # /etc/sudoers 안전하게 편집

# sudo 권한 부여 예제
$ sudo vi /etc/sudoers.d/alice
alice ALL=(ALL) NOPASSWD: /usr/bin/systemctl restart nginx
```

---

## 디스크 관리

### fdisk - 파티션 관리

```bash
# 파티션 목록
$ sudo fdisk -l

# 디스크 편집
$ sudo fdisk /dev/sdb
# 내부 명령어:
# n: 새 파티션
# d: 파티션 삭제
# p: 파티션 테이블 출력
# w: 저장하고 종료
# q: 저장 않고 종료

# 파티션 타입 변경
# t: 파티션 타입 변경
# L: 타입 코드 목록
```

### parted - 고급 파티션 관리

```bash
# 대화형 모드
$ sudo parted /dev/sdb

# 파티션 정보
$ sudo parted /dev/sdb print

# GPT 테이블 생성
$ sudo parted /dev/sdb mklabel gpt

# 파티션 생성
$ sudo parted /dev/sdb mkpart primary ext4 0% 100%

# 파티션 삭제
$ sudo parted /dev/sdb rm 1

# 크기 조정
$ sudo parted /dev/sdb resizepart 1 100GB
```

### mkfs - 파일시스템 생성

```bash
# ext4
$ sudo mkfs.ext4 /dev/sdb1

# XFS
$ sudo mkfs.xfs /dev/sdb1

# FAT32
$ sudo mkfs.vfat /dev/sdb1

# NTFS
$ sudo mkfs.ntfs /dev/sdb1

# 옵션 지정
$ sudo mkfs.ext4 -L "MyData" -m 1 /dev/sdb1
```

### lsblk - 블록 디바이스 목록

```bash
# 기본 출력
$ lsblk

# 파일시스템 정보 포함
$ lsblk -f

# 권한 정보
$ lsblk -m

# JSON 출력
$ lsblk -J

# 특정 디바이스
$ lsblk /dev/sda
```

### du / df - 디스크 사용량

```bash
# 파일시스템 사용량
$ df -h

# inode 사용량
$ df -i

# 특정 파일시스템
$ df -h /home

# 디렉토리 크기
$ du -sh /home/user

# 하위 디렉토리 포함
$ du -h --max-depth=1 /var

# 크기 순 정렬
$ du -sh /* | sort -hr

# 제외하고 계산
$ du -sh --exclude='*.log' /var

# 총합만
$ du -s /home/*

# ncdu (대화형)
$ sudo apt install ncdu
$ ncdu /home
```

---

## 시스템 모니터링

### free - 메모리 사용량

```bash
# 기본 출력
$ free

# 사람이 읽기 쉽게
$ free -h

# 계속 갱신
$ free -h -s 3  # 3초마다

# 총합 표시
$ free -ht

# 와이드 모드
$ free -w
```

### vmstat - 가상 메모리 통계

```bash
# 기본 출력
$ vmstat

# 1초마다, 10회
$ vmstat 1 10

# 메가바이트 단위
$ vmstat -S M

# 디스크 통계
$ vmstat -d

# 파티션 통계
$ vmstat -p /dev/sda1
```

### iostat - I/O 통계

```bash
# 설치
$ sudo apt install sysstat

# 기본 출력
$ iostat

# 확장 통계
$ iostat -x

# 1초마다
$ iostat -x 1

# 특정 디바이스
$ iostat -x sda

# 사람이 읽기 쉽게
$ iostat -h
```

### sar - 시스템 활동 리포트

```bash
# CPU 사용량
$ sar -u 1 5

# 메모리
$ sar -r 1 5

# 스왑
$ sar -S 1 5

# I/O
$ sar -b 1 5

# 네트워크
$ sar -n DEV 1 5

# 전날 로그
$ sar -f /var/log/sysstat/sa$(date -d yesterday +%d)
```

### dmesg - 커널 메시지

```bash
# 모든 메시지
$ dmesg

# 최근 메시지
$ dmesg | tail

# 실시간
$ dmesg -w

# 읽기 쉬운 타임스탬프
$ dmesg -T

# 레벨별 필터
$ dmesg -l err,warn

# 특정 facility
$ dmesg -f kern

# 검색
$ dmesg | grep -i usb
$ dmesg | grep -i error
```

---

## 패키지 관리

### apt (Debian/Ubuntu)

```bash
# 패키지 목록 업데이트
$ sudo apt update

# 업그레이드
$ sudo apt upgrade
$ sudo apt full-upgrade

# 패키지 설치
$ sudo apt install nginx

# 여러 패키지
$ sudo apt install nginx mysql-server php

# 패키지 제거
$ sudo apt remove nginx
$ sudo apt purge nginx  # 설정 파일도 삭제

# 자동 설치된 불필요한 패키지 제거
$ sudo apt autoremove

# 패키지 검색
$ apt search nginx
$ apt-cache search nginx

# 패키지 정보
$ apt show nginx
$ apt-cache show nginx

# 설치된 패키지 목록
$ apt list --installed
$ dpkg -l

# 특정 파일이 어느 패키지에 속하는지
$ dpkg -S /usr/bin/ls

# 패키지가 설치한 파일 목록
$ dpkg -L nginx

# 캐시 정리
$ sudo apt clean
$ sudo apt autoclean
```

### yum / dnf (RHEL/CentOS/Fedora)

```bash
# 패키지 목록 업데이트
$ sudo dnf update  # 또는 yum update

# 패키지 설치
$ sudo dnf install nginx

# 패키지 제거
$ sudo dnf remove nginx

# 패키지 검색
$ dnf search nginx

# 패키지 정보
$ dnf info nginx

# 그룹 설치
$ sudo dnf groupinstall "Development Tools"

# 히스토리
$ dnf history

# 캐시 정리
$ sudo dnf clean all
```

### snap

```bash
# 스냅 설치
$ sudo snap install package-name

# 클래식 스냅
$ sudo snap install --classic code

# 스냅 제거
$ sudo snap remove package-name

# 스냅 목록
$ snap list

# 스냅 검색
$ snap find package-name

# 스냅 업데이트
$ sudo snap refresh
$ sudo snap refresh package-name

# 스냅 정보
$ snap info package-name
```

---

## 실전 예제

### 예제 1: 메모리 부족 시 대처

```bash
# 메모리 사용량 확인
$ free -h

# 메모리 많이 사용하는 프로세스
$ ps aux --sort=-%mem | head -10

# 불필요한 프로세스 종료
$ sudo systemctl stop unnecessary-service

# 캐시 정리 (주의!)
$ sudo sync && sudo sysctl -w vm.drop_caches=3
```

### 예제 2: 디스크 공간 확보

```bash
# 디스크 사용량 확인
$ df -h

# 큰 디렉토리 찾기
$ sudo du -sh /* | sort -hr | head -10

# 큰 파일 찾기
$ sudo find / -type f -size +100M -exec ls -lh {} \; 2>/dev/null

# 로그 파일 정리
$ sudo journalctl --vacuum-time=7d
$ sudo find /var/log -type f -name "*.log" -mtime +30 -delete

# APT 캐시 정리
$ sudo apt clean && sudo apt autoremove
```

### 예제 3: 시스템 성능 분석

```bash
# CPU 부하 확인
$ uptime
$ top

# I/O 병목 확인
$ iostat -x 1 5

# 메모리 스왑 확인
$ vmstat 1 5

# 네트워크 트래픽
$ sar -n DEV 1 5

# 전체 시스템 리포트
$ sudo apt install sysstat
$ sar -A > system_report.txt
```

---

## 요약

시스템 관리의 핵심 명령어:

- **프로세스**: ps, top, kill, systemctl
- **사용자**: useradd, usermod, sudo
- **디스크**: fdisk, mkfs, df, du
- **모니터링**: free, vmstat, iostat, dmesg
- **패키지**: apt, dnf, snap

이 명령어들을 마스터하면 리눅스 시스템을 효과적으로 관리할 수 있습니다.

---

[다음: 네트워크 명령어 →](network.md)

[← 텍스트 처리 명령어로 돌아가기](text.md)

[← 목차로 돌아가기](../README.md)
