# APT / Debian 패키지 관리

## 목차
- [APT 개요](#apt-개요)
- [패키지 검색 및 정보](#패키지-검색-및-정보)
- [패키지 설치 및 제거](#패키지-설치-및-제거)
- [시스템 업데이트](#시스템-업데이트)
- [저장소 관리](#저장소-관리)
- [dpkg](#dpkg)
- [고급 사용법](#고급-사용법)
- [문제 해결](#문제-해결)

---

## APT 개요

### APT vs apt vs apt-get

```bash
# APT (Advanced Package Tool)
# - apt: 현대적인 사용자 친화적 인터페이스
# - apt-get: 전통적인 도구, 스크립트용
# - apt-cache: 패키지 정보 검색
# - aptitude: 텍스트 UI 제공

# apt 사용 권장 (Ubuntu 16.04+)
$ apt search package
$ apt install package
$ apt update

# apt-get (스크립트, 이전 버전)
$ apt-get update
$ apt-get install package
$ apt-cache search package
```

---

## 패키지 검색 및 정보

### 패키지 검색

```bash
# 패키지 검색
$ apt search nginx
$ apt search "web server"

# 정확한 이름
$ apt search ^nginx$

# 설명에서 검색
$ apt search --names-only nginx

# apt-cache로 (더 빠름)
$ apt-cache search nginx
$ apt-cache search --names-only nginx

# 정규식
$ apt-cache search '^python3-.*'
```

### 패키지 정보

```bash
# 패키지 상세 정보
$ apt show nginx
Package: nginx
Version: 1.18.0-6ubuntu14
Priority: optional
Section: web
...

# apt-cache로
$ apt-cache show nginx

# 모든 버전 정보
$ apt-cache showpkg nginx

# 간단한 정보
$ apt list nginx

# 의존성 확인
$ apt depends nginx
$ apt-cache depends nginx

# 역의존성 (이 패키지를 의존하는 패키지)
$ apt rdepends nginx
$ apt-cache rdepends nginx

# 패키지 정책 (버전, 우선순위)
$ apt policy nginx
$ apt-cache policy nginx

# 설치 가능한 버전
$ apt list nginx -a
$ apt-cache madison nginx
```

### 설치된 패키지 확인

```bash
# 설치된 모든 패키지
$ apt list --installed
$ dpkg -l

# 특정 패키지 설치 여부
$ apt list --installed | grep nginx
$ dpkg -l | grep nginx

# 패키지 파일 목록
$ dpkg -L nginx
$ dpkg -L nginx | grep bin

# 파일이 어느 패키지 소속인지
$ dpkg -S /usr/sbin/nginx
$ dpkg -S $(which nginx)

# 패키지 상태
$ dpkg -s nginx
$ dpkg --status nginx

# 업그레이드 가능한 패키지
$ apt list --upgradable
```

---

## 패키지 설치 및 제거

### 설치

```bash
# 패키지 설치
$ sudo apt install nginx
$ sudo apt install apache2 mysql-server php

# 특정 버전
$ sudo apt install nginx=1.18.0-6ubuntu14

# 여러 패키지
$ sudo apt install package1 package2 package3

# 확인 없이 설치 (스크립트용)
$ sudo apt install -y nginx
$ sudo DEBIAN_FRONTEND=noninteractive apt install -y package

# 추천 패키지 제외
$ sudo apt install --no-install-recommends package

# 제안 패키지도 설치
$ sudo apt install --install-suggests package

# 다운로드만 (설치 안 함)
$ sudo apt install --download-only nginx
$ sudo apt download nginx

# 시뮬레이션 (실제 설치 안 함)
$ sudo apt install --simulate nginx
$ sudo apt install -s nginx

# 로컬 .deb 파일 설치
$ sudo apt install ./package.deb
$ sudo dpkg -i package.deb
$ sudo apt install -f  # 의존성 해결

# 재설치
$ sudo apt reinstall nginx
```

### 제거

```bash
# 패키지 제거 (설정 파일 유지)
$ sudo apt remove nginx

# 완전 제거 (설정 파일 포함)
$ sudo apt purge nginx
$ sudo apt remove --purge nginx

# 여러 패키지
$ sudo apt remove package1 package2

# 자동 설치된 불필요한 패키지 제거
$ sudo apt autoremove

# Purge와 함께
$ sudo apt autoremove --purge

# 패키지와 설정 완전 삭제 후 자동 정리
$ sudo apt purge nginx
$ sudo apt autoremove

# 다운로드된 패키지 파일 삭제
$ sudo apt clean  # 모든 .deb 파일
$ sudo apt autoclean  # 오래된 것만
```

---

## 시스템 업데이트

### 업데이트 및 업그레이드

```bash
# 패키지 목록 업데이트
$ sudo apt update

# 설치된 패키지 업그레이드
$ sudo apt upgrade

# 전체 업그레이드 (의존성 처리 포함)
$ sudo apt full-upgrade
$ sudo apt dist-upgrade  # 이전 명령어

# 업데이트 + 업그레이드 (한 번에)
$ sudo apt update && sudo apt upgrade -y

# 특정 패키지만 업그레이드
$ sudo apt install --only-upgrade nginx

# 업그레이드 가능한 패키지 확인
$ apt list --upgradable

# 보류
$ sudo apt-mark hold package  # 업그레이드 방지
$ sudo apt-mark unhold package  # 보류 해제
$ apt-mark showhold  # 보류 목록

# 자동 설치 표시
$ sudo apt-mark auto package
$ sudo apt-mark manual package
$ apt-mark showauto
$ apt-mark showmanual
```

### 보안 업데이트

```bash
# Ubuntu에서 보안 업데이트만
$ sudo unattended-upgrade -d

# unattended-upgrades 설정
$ sudo apt install unattended-upgrades
$ sudo dpkg-reconfigure unattended-upgrades

# /etc/apt/apt.conf.d/50unattended-upgrades 편집
$ sudo vi /etc/apt/apt.conf.d/50unattended-upgrades

# 자동 업데이트 설정
Unattended-Upgrade::Allowed-Origins {
    "${distro_id}:${distro_codename}-security";
    "${distro_id}ESMApps:${distro_codename}-apps-security";
};

# 수동 실행
$ sudo unattended-upgrade --dry-run -d
$ sudo unattended-upgrade -d
```

---

## 저장소 관리

### sources.list

```bash
# 저장소 목록
$ cat /etc/apt/sources.list
$ ls /etc/apt/sources.list.d/

# Ubuntu 기본 저장소
deb http://archive.ubuntu.com/ubuntu/ focal main restricted
deb http://archive.ubuntu.com/ubuntu/ focal-updates main restricted
deb http://archive.ubuntu.com/ubuntu/ focal universe
deb http://archive.ubuntu.com/ubuntu/ focal-updates universe
deb http://archive.ubuntu.com/ubuntu/ focal multiverse
deb http://archive.ubuntu.com/ubuntu/ focal-updates multiverse
deb http://archive.ubuntu.com/ubuntu/ focal-backports main restricted universe multiverse
deb http://security.ubuntu.com/ubuntu/ focal-security main restricted
deb http://security.ubuntu.com/ubuntu/ focal-security universe
deb http://security.ubuntu.com/ubuntu/ focal-security multiverse

# 저장소 구성 요소:
# main: 공식 지원
# restricted: 제한적 라이선스
# universe: 커뮤니티 지원
# multiverse: 제한된 라이선스
```

### 저장소 추가

```bash
# add-apt-repository 사용 (권장)
$ sudo add-apt-repository "deb http://archive.canonical.com/ubuntu $(lsb_release -sc) partner"
$ sudo apt update

# PPA 추가 (Personal Package Archive)
$ sudo add-apt-repository ppa:user/ppa-name
$ sudo apt update

# PPA 제거
$ sudo add-apt-repository --remove ppa:user/ppa-name

# 수동으로 추가
$ echo "deb http://repository.url/ubuntu focal main" | sudo tee /etc/apt/sources.list.d/repo.list

# GPG 키 추가 (저장소 인증)
$ wget -qO - https://example.com/key.gpg | sudo apt-key add -
$ curl -fsSL https://example.com/key.gpg | sudo apt-key add -

# 새로운 방식 (apt-key deprecated)
$ curl -fsSL https://example.com/key.gpg | sudo gpg --dearmor -o /usr/share/keyrings/example.gpg
$ echo "deb [signed-by=/usr/share/keyrings/example.gpg] https://example.com/ubuntu focal main" | sudo tee /etc/apt/sources.list.d/example.list

# 저장소 비활성화
$ sudo add-apt-repository --disable ppa:user/ppa-name

# 저장소 목록 확인
$ apt-cache policy
```

### 예제: Docker 저장소 추가

```bash
# Docker 공식 저장소 추가 (Ubuntu)
$ sudo apt update
$ sudo apt install ca-certificates curl gnupg

# GPG 키 추가
$ sudo install -m 0755 -d /etc/apt/keyrings
$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
$ sudo chmod a+r /etc/apt/keyrings/docker.gpg

# 저장소 추가
$ echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

$ sudo apt update
$ sudo apt install docker-ce docker-ce-cli containerd.io
```

---

## dpkg

### dpkg 기본 명령어

```bash
# .deb 파일 설치
$ sudo dpkg -i package.deb

# 여러 파일 설치
$ sudo dpkg -i *.deb

# 패키지 제거
$ sudo dpkg -r package
$ sudo dpkg --remove package

# 설정 파일 포함 제거
$ sudo dpkg -P package
$ sudo dpkg --purge package

# 설치된 패키지 목록
$ dpkg -l
$ dpkg -l | grep nginx
$ dpkg -l 'python3-*'

# 패키지 상태
$ dpkg -s nginx
$ dpkg --status nginx

# 패키지 파일 목록
$ dpkg -L nginx
$ dpkg --listfiles nginx

# 파일 소속 패키지 찾기
$ dpkg -S /bin/ls
$ dpkg --search /usr/bin/python3

# 패키지 내용 확인 (설치 전)
$ dpkg -c package.deb
$ dpkg --contents package.deb

# 패키지 정보 (설치 전)
$ dpkg -I package.deb
$ dpkg --info package.deb

# 설치된 패키지를 .deb로 재패키징
$ dpkg-repack package
```

### dpkg 고급 사용

```bash
# 설정 스크립트 확인
$ dpkg -L nginx | grep -E '(preinst|postinst|prerm|postrm)'

# 패키지 확인 (무결성 검사)
$ sudo dpkg --verify nginx

# 설정 파일만 남은 패키지 목록
$ dpkg -l | grep '^rc'

# 설정 파일 제거
$ dpkg -l | grep '^rc' | awk '{print $2}' | sudo xargs dpkg --purge

# dpkg 데이터베이스 정보
$ dpkg --get-selections
$ dpkg --get-selections > package_list.txt

# 패키지 선택 복원
$ sudo dpkg --set-selections < package_list.txt
$ sudo apt-get dselect-upgrade

# 아키텍처 확인
$ dpkg --print-architecture
$ dpkg --print-foreign-architectures
```

---

## 고급 사용법

### 의존성 문제 해결

```bash
# 깨진 의존성 수정
$ sudo apt install -f
$ sudo apt --fix-broken install

# dpkg 설정 완료
$ sudo dpkg --configure -a

# 패키지 캐시 재구축
$ sudo apt clean
$ sudo apt update

# 전체 시스템 복구
$ sudo apt update
$ sudo apt install -f
$ sudo dpkg --configure -a
$ sudo apt full-upgrade
```

### 패키지 고정 (Pinning)

```bash
# /etc/apt/preferences.d/pin-example 생성
$ sudo vi /etc/apt/preferences.d/pin-example

# 특정 버전 고정
Package: nginx
Pin: version 1.18.0-*
Pin-Priority: 1001

# 특정 저장소 우선순위
Package: *
Pin: release o=Ubuntu
Pin-Priority: 500

Package: *
Pin: release o=LP-PPA-*
Pin-Priority: 600

# 우선순위:
# < 0: 절대 설치 안 함
# 0-99: 현재 버전보다 최신이어도 설치 안 함
# 100-499: 다른 소스가 없을 때만
# 500-989: 표준 우선순위
# 990-1000: 다운그레이드라도 설치
# > 1000: 경고 없이 다운그레이드
```

### 로그 및 히스토리

```bash
# APT 로그
$ cat /var/log/apt/history.log
$ cat /var/log/apt/term.log

# dpkg 로그
$ cat /var/log/dpkg.log

# 최근 설치된 패키지
$ grep " install " /var/log/dpkg.log
$ grep " install " /var/log/dpkg.log | tail -20

# 최근 제거된 패키지
$ grep " remove " /var/log/dpkg.log

# 날짜별 검색
$ grep "2024-11-17" /var/log/dpkg.log
```

### 다운로드 위치 및 캐시

```bash
# 패키지 다운로드 위치
$ ls /var/cache/apt/archives/

# 패키지 캐시 정리
$ sudo apt clean  # 모두 삭제
$ sudo apt autoclean  # 오래된 것만

# 디스크 사용량 확인
$ du -sh /var/cache/apt/archives/

# 패키지 다운로드 (설치 안 함)
$ sudo apt install --download-only nginx
$ apt download nginx

# 소스 코드 다운로드
$ apt source nginx
```

---

## 문제 해결

### 공통 문제

```bash
# 1. "Unable to locate package"
$ sudo apt update  # 패키지 목록 업데이트
$ apt search package  # 패키지 이름 확인

# 2. "404 Not Found" 오류
$ sudo vi /etc/apt/sources.list  # 저장소 URL 확인
$ sudo apt update

# 3. "GPG error"
$ sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys KEY_ID
$ sudo apt update

# 4. "dpkg was interrupted"
$ sudo dpkg --configure -a
$ sudo apt install -f

# 5. "Could not get lock"
$ sudo rm /var/lib/apt/lists/lock
$ sudo rm /var/cache/apt/archives/lock
$ sudo rm /var/lib/dpkg/lock*
$ sudo dpkg --configure -a
$ sudo apt update

# 6. 손상된 패키지 데이터베이스
$ sudo rm -rf /var/lib/apt/lists/*
$ sudo apt clean
$ sudo apt update

# 7. 의존성 지옥
$ sudo apt install -f
$ sudo apt autoremove
$ sudo apt clean && sudo apt update
$ sudo apt dist-upgrade
```

### 패키지 다운그레이드

```bash
# 이전 버전으로 다운그레이드
$ apt list -a package  # 사용 가능한 버전 확인
$ sudo apt install package=version

# 예제
$ apt list -a nginx
$ sudo apt install nginx=1.18.0-6ubuntu14

# 다운그레이드 후 고정
$ sudo apt-mark hold nginx
```

### APT 성능 향상

```bash
# 병렬 다운로드 활성화
$ sudo vi /etc/apt/apt.conf.d/99parallel-downloads
Acquire::Queue-Mode "host";
Acquire::http::Pipeline-Depth "5";

# 미러 선택 최적화 (Ubuntu)
$ sudo apt install apt-mirror-updater
$ sudo apt-mirror-updater

# apt-fast (비공식, 병렬 다운로드)
$ sudo add-apt-repository ppa:apt-fast/stable
$ sudo apt update
$ sudo apt install apt-fast
$ apt-fast install package  # apt 대신 사용
```

---

## 실전 스크립트

### 시스템 업데이트 스크립트

```bash
#!/bin/bash
# system-update.sh

LOG="/var/log/system-update.log"

echo "=== System Update Started: $(date) ===" | tee -a "$LOG"

# 업데이트
echo "Updating package lists..." | tee -a "$LOG"
sudo apt update 2>&1 | tee -a "$LOG"

# 업그레이드 가능한 패키지
echo "Upgradable packages:" | tee -a "$LOG"
apt list --upgradable 2>&1 | tee -a "$LOG"

# 업그레이드
echo "Upgrading packages..." | tee -a "$LOG"
sudo apt upgrade -y 2>&1 | tee -a "$LOG"

# 자동 제거
echo "Removing unnecessary packages..." | tee -a "$LOG"
sudo apt autoremove -y 2>&1 | tee -a "$LOG"

# 캐시 정리
echo "Cleaning cache..." | tee -a "$LOG"
sudo apt autoclean 2>&1 | tee -a "$LOG"

echo "=== System Update Completed: $(date) ===" | tee -a "$LOG"
```

### 패키지 백업 및 복원

```bash
# 설치된 패키지 목록 백업
$ dpkg --get-selections > package-backup.txt

# 복원
$ sudo dpkg --set-selections < package-backup.txt
$ sudo apt-get dselect-upgrade

# 더 나은 방법 (apt-clone)
$ sudo apt install apt-clone

# 백업
$ sudo apt-clone clone backup

# 복원
$ sudo apt-clone restore backup/apt-clone-state-hostname.tar.gz
```

---

## 요약

APT 핵심 명령어:

1. **검색**: `apt search`, `apt show`
2. **설치**: `apt install`, `apt remove`
3. **업데이트**: `apt update`, `apt upgrade`
4. **저장소**: `add-apt-repository`, `sources.list`
5. **dpkg**: `.deb` 파일 직접 관리

---

[다음: DNF/YUM (Red Hat) →](dnf-redhat.md)

[← 방화벽으로 돌아가기](../08-networking/firewall.md)

[← 목차로 돌아가기](../README.md)
