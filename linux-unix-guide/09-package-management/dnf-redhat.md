# DNF / YUM - Red Hat 패키지 관리

## 목차
- [DNF 개요](#dnf-개요)
- [패키지 검색 및 정보](#패키지-검색-및-정보)
- [패키지 설치 및 제거](#패키지-설치-및-제거)
- [시스템 업데이트](#시스템-업데이트)
- [저장소 관리](#저장소-관리)
- [RPM](#rpm)
- [패키지 그룹](#패키지-그룹)
- [실전 예제](#실전-예제)

---

## DNF 개요

### DNF vs YUM

```bash
# DNF (Dandified YUM):
# - Fedora 22+, RHEL 8+, CentOS 8+의 기본
# - YUM의 차세대 버전
# - 더 빠르고 메모리 효율적
# - 의존성 해결 개선

# YUM (Yellowdog Updater Modified):
# - RHEL 7, CentOS 7 이하
# - 여전히 많이 사용됨
# - DNF와 명령어 호환

# 대부분의 명령어는 동일
$ dnf install package
$ yum install package  # RHEL 7
```

---

## 패키지 검색 및 정보

### 패키지 검색

```bash
# 패키지 검색
$ dnf search nginx
$ dnf search "web server"

# 정확한 이름만
$ dnf list nginx

# 모든 패키지 목록
$ dnf list all
$ dnf list available  # 설치 가능한
$ dnf list installed  # 설치된
$ dnf list updates    # 업데이트 가능한

# 와일드카드
$ dnf list 'httpd*'
$ dnf list '*python3*'

# 파일 제공 패키지 찾기
$ dnf provides /usr/sbin/nginx
$ dnf provides '*/nginx.conf'
$ dnf whatprovides nginx

# 패키지 정보
$ dnf info nginx
$ dnf info installed nginx
```

### 패키지 상세 정보

```bash
# 패키지 정보
$ dnf info nginx
Name         : nginx
Version      : 1.20.1
Release      : 14.el9
Architecture : x86_64
Size         : 1.0 M
Source       : nginx-1.20.1-14.el9.src.rpm
Repository   : @System
From repo    : appstream
Summary      : A high performance web server
URL          : http://nginx.org/
License      : BSD
Description  : Nginx is a web server...

# 의존성 확인
$ dnf deplist nginx
$ dnf repoquery --requires nginx

# 역의존성
$ dnf repoquery --whatrequires nginx

# 파일 목록
$ dnf repoquery -l nginx
$ rpm -ql nginx  # 설치된 패키지

# 변경 이력
$ dnf updateinfo list
$ dnf updateinfo nginx
```

---

## 패키지 설치 및 제거

### 설치

```bash
# 패키지 설치
$ sudo dnf install nginx
$ sudo dnf install httpd mariadb-server php

# 확인 없이
$ sudo dnf install -y nginx

# 특정 버전
$ sudo dnf install nginx-1.20.1

# 다운로드만
$ sudo dnf install --downloadonly nginx
$ sudo dnf download nginx

# 로컬 RPM 설치
$ sudo dnf install ./package.rpm
$ sudo dnf localinstall package.rpm

# 재설치
$ sudo dnf reinstall nginx

# 다운그레이드
$ sudo dnf downgrade nginx
```

### 제거

```bash
# 패키지 제거
$ sudo dnf remove nginx

# 의존성도 함께 제거
$ sudo dnf autoremove nginx

# 불필요한 패키지 정리
$ sudo dnf autoremove

# 설정 파일 유지하며 제거 (기본동작)
# RPM은 .rpmsave로 백업

# 캐시 정리
$ sudo dnf clean packages  # 패키지 캐시
$ sudo dnf clean metadata  # 메타데이터
$ sudo dnf clean all       # 모두

# 만료된 캐시
$ sudo dnf makecache --refresh
```

---

## 시스템 업데이트

### 업데이트 및 업그레이드

```bash
# 메타데이터 업데이트
$ sudo dnf check-update

# 업데이트 가능한 패키지 확인
$ dnf list updates
$ dnf updateinfo list

# 모든 패키지 업데이트
$ sudo dnf update
$ sudo dnf upgrade  # 동일

# 특정 패키지만
$ sudo dnf update nginx
$ sudo dnf update httpd mariadb-server

# 보안 업데이트만
$ sudo dnf update --security
$ sudo dnf updateinfo list security

# 최소 업데이트
$ sudo dnf update-minimal --security

# 버그픽스 업데이트
$ sudo dnf update --bugfix

# 시뮬레이션
$ sudo dnf update --assumeno

# 커널 업데이트
$ sudo dnf update kernel
$ sudo dnf install kernel  # 새 커널 추가

# 오래된 커널 제거
$ sudo dnf remove --oldinstallonly
$ sudo dnf remove $(dnf repoquery --installonly --latest-limit=-2 -q)
```

### 업데이트 제외

```bash
# 특정 패키지 제외
$ sudo dnf update --exclude=kernel*
$ sudo dnf update -x kernel* -x nvidia*

# 영구 제외 설정
$ sudo vi /etc/dnf/dnf.conf
[main]
excludepkgs=kernel* nvidia*

# 또는
$ sudo vi /etc/yum.repos.d/repo.repo
[repo]
exclude=package1 package2

# 보호된 패키지 확인
$ cat /etc/dnf/protected.d/*.conf
```

### versionlock (버전 고정)

```bash
# versionlock 플러그인 설치
$ sudo dnf install 'dnf-command(versionlock)'

# 현재 버전 고정
$ sudo dnf versionlock add nginx
$ sudo dnf versionlock nginx-1.20.1

# 고정 목록
$ dnf versionlock list

# 고정 해제
$ sudo dnf versionlock delete nginx

# 모두 해제
$ sudo dnf versionlock clear

# 고정된 패키지는 업데이트 안 됨
$ sudo dnf update  # nginx는 제외됨
```

---

## 저장소 관리

### 저장소 목록

```bash
# 활성화된 저장소
$ dnf repolist
$ dnf repolist enabled

# 모든 저장소 (비활성화 포함)
$ dnf repolist all
$ dnf repolist disabled

# 저장소 정보
$ dnf repoinfo
$ dnf repoinfo epel

# 저장소 ID 목록
$ dnf repolist -v
```

### 저장소 추가

```bash
# EPEL (Extra Packages for Enterprise Linux)
$ sudo dnf install epel-release  # RHEL 8+
$ sudo yum install epel-release  # RHEL 7

# RPM Fusion (Fedora)
$ sudo dnf install \
  https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm \
  https://download1.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm

# 저장소 파일 생성
$ sudo vi /etc/yum.repos.d/custom.repo
[custom-repo]
name=Custom Repository
baseurl=https://repo.example.com/rhel/$releasever/$basearch/
enabled=1
gpgcheck=1
gpgkey=https://repo.example.com/RPM-GPG-KEY

# URL에서 저장소 추가
$ sudo dnf config-manager --add-repo https://example.com/repo.repo

# 저장소 활성화/비활성화
$ sudo dnf config-manager --enable repo-id
$ sudo dnf config-manager --disable repo-id

# 특정 저장소에서만 설치
$ sudo dnf install --enablerepo=epel package
$ sudo dnf install --disablerepo=* --enablerepo=epel package
```

### GPG 키 관리

```bash
# GPG 키 가져오기
$ sudo rpm --import https://example.com/RPM-GPG-KEY

# 키 목록
$ rpm -q gpg-pubkey --qf '%{name}-%{version}-%{release} --> %{summary}\n'

# 키 정보
$ rpm -qi gpg-pubkey-<keyid>

# 키 제거
$ sudo rpm -e gpg-pubkey-<keyid>
```

### 저장소 우선순위

```bash
# priorities 플러그인 설치
$ sudo dnf install dnf-plugin-priorities

# 저장소 우선순위 설정
$ sudo vi /etc/yum.repos.d/repo.repo
[repo]
name=Repository
baseurl=https://example.com/repo
enabled=1
priority=1  # 낮을수록 높은 우선순위 (1-99)

# 기본 저장소: 1
# EPEL: 10
# 타사 저장소: 20-99
```

---

## RPM

### RPM 기본 명령어

```bash
# 패키지 설치
$ sudo rpm -ivh package.rpm
# i: install, v: verbose, h: hash (진행 표시)

# 업그레이드
$ sudo rpm -Uvh package.rpm  # 없으면 설치, 있으면 업그레이드
$ sudo rpm -Fvh package.rpm  # 있을 때만 업그레이드

# 제거
$ sudo rpm -e package

# 의존성 무시 (위험!)
$ sudo rpm -ivh --nodeps package.rpm

# 덮어쓰기
$ sudo rpm -ivh --force package.rpm

# 테스트 (실제 설치 안 함)
$ rpm -ivh --test package.rpm
```

### 패키지 조회

```bash
# 설치된 모든 패키지
$ rpm -qa
$ rpm -qa | grep nginx

# 패키지 정보
$ rpm -qi nginx
$ rpm -qip package.rpm  # 파일에서

# 파일 목록
$ rpm -ql nginx
$ rpm -qlp package.rpm  # 파일에서

# 설정 파일 목록
$ rpm -qc nginx

# 문서 목록
$ rpm -qd nginx

# 스크립트 확인
$ rpm -q --scripts nginx

# 변경 이력
$ rpm -q --changelog nginx | head -20

# 파일이 속한 패키지
$ rpm -qf /usr/sbin/nginx
$ rpm -qf $(which nginx)

# 의존성
$ rpm -qR nginx  # Requires
$ rpm -qpR package.rpm

# 제공하는 것
$ rpm -q --provides nginx

# 패키지 확인 (변경된 파일)
$ rpm -V nginx
$ rpm -Va  # 모든 패키지

# 확인 결과:
# S: Size
# M: Mode
# 5: MD5 checksum
# D: Device
# L: Link
# U: User
# G: Group
# T: Mtime
```

### RPM 빌드

```bash
# 소스 RPM 설치
$ rpm -ivh package.src.rpm

# rpmbuild 설정
$ mkdir -p ~/rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS}
$ echo '%_topdir %(echo $HOME)/rpmbuild' > ~/.rpmmacros

# SPEC 파일로 빌드
$ rpmbuild -ba package.spec

# 바이너리 RPM만
$ rpmbuild -bb package.spec

# 소스 RPM만
$ rpmbuild -bs package.spec

# 소스에서 재빌드
$ rpmbuild --rebuild package.src.rpm
```

---

## 패키지 그룹

### 그룹 관리

```bash
# 그룹 목록
$ dnf group list
$ dnf grouplist

# 숨겨진 그룹 포함
$ dnf group list --hidden

# 그룹 정보
$ dnf group info "Development Tools"
$ dnf groupinfo "Web Server"

# 그룹 설치
$ sudo dnf group install "Development Tools"
$ sudo dnf groupinstall "System Tools"

# 그룹 제거
$ sudo dnf group remove "Development Tools"
$ sudo dnf groupremove "Web Server"

# 그룹 업데이트
$ sudo dnf group upgrade "Virtualization Host"

# 환경 그룹 (큰 그룹)
$ dnf group list --environment
$ sudo dnf install @^minimal-environment
```

### 주요 그룹

```bash
# Development Tools
$ sudo dnf group install "Development Tools"
# gcc, make, autoconf, automake 등

# System Tools
$ sudo dnf group install "System Tools"

# Security Tools
$ sudo dnf group install "Security Tools"

# Virtualization
$ sudo dnf group install "Virtualization Host"
$ sudo dnf group install "Virtualization Client"

# Web Server
$ sudo dnf install @httpd
$ sudo dnf install @nginx

# Database Server
$ sudo dnf install @mariadb
$ sudo dnf install @postgresql

# File and Storage Server
$ sudo dnf install @file-server
```

---

## 히스토리

### 트랜잭션 히스토리

```bash
# 히스토리 목록
$ dnf history
$ dnf history list

# 상세 정보
$ dnf history info 5
$ dnf history info last

# 특정 패키지 히스토리
$ dnf history list nginx

# 트랜잭션 되돌리기
$ sudo dnf history undo 5
$ sudo dnf history undo last

# 트랜잭션 재실행
$ sudo dnf history redo 5

# 특정 시점으로 롤백
$ sudo dnf history rollback 5

# 히스토리 데이터베이스 정리
$ sudo dnf history prune
```

---

## 모듈 (Modules - RHEL 8+)

### 모듈 관리

```bash
# 모듈 목록
$ dnf module list
$ dnf module list nodejs

# 모듈 정보
$ dnf module info nodejs:14

# 모듈 활성화
$ sudo dnf module enable nodejs:14

# 모듈 설치
$ sudo dnf module install nodejs:14

# 또는 한 번에
$ sudo dnf module install nodejs:14/common

# 스트림 전환
$ sudo dnf module reset nodejs
$ sudo dnf module install nodejs:16

# 모듈 제거
$ sudo dnf module remove nodejs:14

# 모듈 비활성화
$ sudo dnf module disable nodejs
```

---

## 실전 예제

### LAMP 스택 설치

```bash
#!/bin/bash
# install-lamp.sh - LAMP Stack 설치

echo "Installing LAMP Stack..."

# Apache
sudo dnf install -y httpd
sudo systemctl enable httpd
sudo systemctl start httpd

# MariaDB
sudo dnf install -y mariadb-server
sudo systemctl enable mariadb
sudo systemctl start mariadb
sudo mysql_secure_installation

# PHP
sudo dnf install -y php php-mysqlnd php-fpm
sudo systemctl enable php-fpm
sudo systemctl start php-fpm

# PHP 모듈
sudo dnf install -y php-gd php-xml php-mbstring

# 방화벽
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload

echo "LAMP Stack installed successfully"
```

### 시스템 업데이트 스크립트

```bash
#!/bin/bash
# system-update.sh

LOG="/var/log/system-update.log"

echo "=== Update Started: $(date) ===" | tee -a "$LOG"

# 업데이트 확인
echo "Checking for updates..." | tee -a "$LOG"
sudo dnf check-update 2>&1 | tee -a "$LOG"

# 업데이트 적용
echo "Applying updates..." | tee -a "$LOG"
sudo dnf update -y 2>&1 | tee -a "$LOG"

# 자동 제거
echo "Removing unnecessary packages..." | tee -a "$LOG"
sudo dnf autoremove -y 2>&1 | tee -a "$LOG"

# 커널 정리
echo "Cleaning old kernels..." | tee -a "$LOG"
sudo dnf remove --oldinstallonly -y 2>&1 | tee -a "$LOG"

echo "=== Update Completed: $(date) ===" | tee -a "$LOG"

# 재부팅 필요 여부
if [ -f /var/run/reboot-required ]; then
    echo "*** System restart required ***" | tee -a "$LOG"
fi
```

---

## 문제 해결

### 공통 문제

```bash
# 1. 의존성 문제
$ sudo dnf clean all
$ sudo dnf makecache
$ sudo dnf update

# 2. GPG 키 오류
$ sudo rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-*
$ sudo rpm --import https://example.com/RPM-GPG-KEY

# 3. 손상된 캐시
$ sudo dnf clean all
$ sudo rm -rf /var/cache/dnf
$ sudo dnf makecache

# 4. 잠금 파일
$ sudo rm -f /var/run/dnf.pid
$ sudo rm -f /var/cache/dnf/*.lock

# 5. 데이터베이스 재구축
$ sudo rpm --rebuilddb

# 6. 패키지 확인
$ sudo dnf check
$ rpm -Va  # 모든 패키지 검증
```

### 디버깅

```bash
# Verbose 모드
$ sudo dnf -v install package
$ sudo dnf -vv install package

# 디버그 정보
$ sudo dnf --debuglevel=10 install package

# 트랜잭션 테스트
$ sudo dnf install --assumeno package

# 로그 확인
$ sudo tail -f /var/log/dnf.log
$ sudo journalctl -u dnf
```

---

## DNF 설정

### 설정 파일

```bash
# 메인 설정
$ sudo vi /etc/dnf/dnf.conf

[main]
gpgcheck=1
installonly_limit=3
clean_requirements_on_remove=True
best=True
skip_if_unavailable=True

# 유용한 옵션
keepcache=True          # 캐시 유지
deltarpm=True           # Delta RPM 사용
fastestmirror=True      # 빠른 미러 선택
max_parallel_downloads=10  # 병렬 다운로드

# 플러그인 설정
$ ls /etc/dnf/plugins/

# 보호된 패키지
$ cat /etc/dnf/protected.d/dnf.conf
```

---

## 요약

DNF/YUM 핵심:

1. **설치**: `dnf install`, `dnf remove`
2. **업데이트**: `dnf update`, `dnf check-update`
3. **검색**: `dnf search`, `dnf info`
4. **저장소**: `/etc/yum.repos.d/`, `dnf repolist`
5. **그룹**: `dnf group install`
6. **히스토리**: `dnf history`, `dnf history undo`

---

[다음: Pacman (Arch) →](pacman-arch.md)

[← APT/Debian으로 돌아가기](apt-debian.md)

[← 목차로 돌아가기](../README.md)
