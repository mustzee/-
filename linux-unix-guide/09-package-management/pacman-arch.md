# Pacman (Arch Linux)

## 목차
- [소개](#소개)
- [기본 작업](#기본-작업)
- [패키지 검색 및 정보](#패키지-검색-및-정보)
- [시스템 업데이트](#시스템-업데이트)
- [패키지 그룹](#패키지-그룹)
- [캐시 관리](#캐시-관리)
- [AUR (Arch User Repository)](#aur-arch-user-repository)
- [Pacman 설정](#pacman-설정)
- [문제 해결](#문제-해결)
- [고급 기능](#고급-기능)
- [실전 예제](#실전-예제)

---

## 소개

Pacman은 Arch Linux의 공식 패키지 관리자입니다. 간단하고 빠르며 강력한 기능을 제공합니다.

### Pacman 특징

```bash
# Pacman의 주요 특징:
# 1. 이진 패키지 시스템
# 2. 간단한 PKGBUILD 빌드 시스템
# 3. 쉬운 패키지 관리
# 4. 빠른 속도
# 5. AUR 지원 (yay, paru 등 헬퍼 사용)

# 패키지 데이터베이스
$ ls /var/lib/pacman/sync/
core.db  extra.db  community.db  multilib.db

# 설정 파일
$ cat /etc/pacman.conf

# 미러 서버 목록
$ cat /etc/pacman.d/mirrorlist
```

### 기본 문법

```bash
# 일반 형식
pacman <operation> [options] [targets]

# 주요 작업 (Operations):
# -S, --sync      : 패키지 동기화/설치
# -R, --remove    : 패키지 제거
# -Q, --query     : 패키지 정보 쿼리
# -U, --upgrade   : 패키지 업그레이드
# -F, --files     : 파일 데이터베이스 쿼리
# -D, --database  : 데이터베이스 수정

# 주요 옵션:
# -y, --refresh   : 데이터베이스 새로고침
# -u, --sysupgrade: 시스템 업그레이드
# -s, --search    : 패키지 검색
# -i, --info      : 패키지 정보 표시
```

---

## 기본 작업

### 패키지 설치

```bash
# 단일 패키지 설치
$ sudo pacman -S nginx
resolving dependencies...
looking for conflicting packages...

Packages (1) nginx-1.24.0-1

Total Installed Size:  1.58 MiB

:: Proceed with installation? [Y/n] y

# 여러 패키지 동시 설치
$ sudo pacman -S vim git curl wget
$ sudo pacman -S python python-pip python-virtualenv

# 확인 없이 설치
$ sudo pacman -S --noconfirm htop

# 패키지만 다운로드 (설치 안 함)
$ sudo pacman -Sw package

# 의존성 무시하고 설치 (권장하지 않음)
$ sudo pacman -Sd package

# 그룹으로 설치
$ sudo pacman -S gnome
:: There are 66 members in group gnome:
:: Repository extra
   1) baobab  2) cheese  3) eog  4) epiphany  ...

# 그룹에서 선택 설치
Enter a selection (default=all): 1 2 5 10

# 로컬 패키지 설치 (.pkg.tar.zst)
$ sudo pacman -U /path/to/package.pkg.tar.zst

# URL에서 직접 설치
$ sudo pacman -U https://example.com/package.pkg.tar.zst

# 설치 시 의존성도 함께
$ sudo pacman -S package --needed  # 이미 설치된 것은 스킵
```

### 패키지 제거

```bash
# 패키지 제거 (의존성 유지)
$ sudo pacman -R package

# 패키지 및 의존성 제거
$ sudo pacman -Rs package

# 패키지, 의존성, 설정 파일 모두 제거
$ sudo pacman -Rns package

# 여러 패키지 제거
$ sudo pacman -Rs package1 package2 package3

# 강제 제거 (권장하지 않음)
$ sudo pacman -Rdd package

# 제거 전 확인
$ sudo pacman -R package
checking dependencies...

Packages (1) package-1.0-1

Total Removed Size:  5.00 MiB

:: Do you want to remove these packages? [Y/n]

# 사용하지 않는 의존성 제거 (orphans)
$ sudo pacman -Rns $(pacman -Qtdq)

# orphan 패키지 찾기
$ pacman -Qtdq
lib32-glibc
lib32-gcc-libs

# 백업 파일도 함께 제거 (-n)
$ sudo pacman -Rn package
```

### 패키지 업그레이드

```bash
# 데이터베이스 새로고침
$ sudo pacman -Sy

# 시스템 전체 업그레이드
$ sudo pacman -Syu
:: Synchronizing package databases...
 core is up to date
 extra is up to date
 community is up to date
:: Starting full system upgrade...
resolving dependencies...
looking for conflicting packages...

Packages (42) linux-6.5.9-1  systemd-254.5-1  ...

# 데이터베이스 새로고침 후 업그레이드 (권장)
$ sudo pacman -Syyu  # 강제 새로고침

# 다운그레이드 허용 업그레이드
$ sudo pacman -Suu

# 특정 패키지만 업그레이드
$ sudo pacman -S package

# 무시 패키지 설정 후 업그레이드
$ sudo pacman -Syu --ignore package1,package2
```

---

## 패키지 검색 및 정보

### 패키지 검색

```bash
# 저장소에서 검색
$ pacman -Ss nginx
extra/nginx 1.24.0-1
    Lightweight HTTP server and IMAP/POP3 proxy server

# 정규식 검색
$ pacman -Ss ^python-
$ pacman -Ss 'web.*server'

# 설치된 패키지 검색
$ pacman -Qs nginx

# 대소문자 구분 없이
$ pacman -Ss --ignorecase NGINX

# 그룹 검색
$ pacman -Sg
$ pacman -Sg gnome
$ pacman -Sg | grep -i desktop

# 파일 소유자 찾기
$ pacman -Qo /usr/bin/vim
/usr/bin/vim is owned by vim 9.0.2046-1

# 파일 검색 (데이터베이스 업데이트 필요)
$ sudo pacman -Fy  # 파일 데이터베이스 업데이트
$ pacman -Fl package  # 패키지 내 파일 목록
$ pacman -Fx filename  # 파일 이름으로 검색
```

### 패키지 정보

```bash
# 저장소 패키지 정보
$ pacman -Si nginx
Repository      : extra
Name            : nginx
Version         : 1.24.0-1
Description     : Lightweight HTTP server
Architecture    : x86_64
URL             : https://nginx.org
Licenses        : custom
Groups          : None
Provides        : None
Depends On      : pcre2  zlib  openssl  ...
Optional Deps   : None
Conflicts With  : None
Replaces        : None
Download Size   : 584.00 KiB
Installed Size  : 1.58 MiB

# 설치된 패키지 정보
$ pacman -Qi nginx

# 자세한 정보 (-ii)
$ pacman -Sii package
$ pacman -Qii package

# 패키지 의존성 확인
$ pactree package
package
├─dependency1
│ └─subdependency
└─dependency2

# 역 의존성 (누가 이 패키지를 필요로 하는가)
$ pactree -r package

# 패키지 파일 목록
$ pacman -Ql package
package /usr/
package /usr/bin/
package /usr/bin/executable
package /usr/share/doc/

# 백업 파일 확인
$ pacman -Qii package | grep Backup

# 패키지 크기
$ pacman -Qi package | grep Size
```

### 패키지 나열

```bash
# 모든 설치된 패키지
$ pacman -Q
bash 5.2.015-3
coreutils 9.4-2
...

# 명시적으로 설치된 패키지 (사용자가 직접)
$ pacman -Qe

# 의존성으로 설치된 패키지
$ pacman -Qd

# 사용하지 않는 패키지 (orphans)
$ pacman -Qdt

# 외부 패키지 (AUR 등)
$ pacman -Qm

# 공식 저장소 패키지
$ pacman -Qn

# 업데이트 가능한 패키지
$ pacman -Qu
linux 6.5.8-1 -> 6.5.9-1
systemd 254.4-1 -> 254.5-1

# 날짜순 정렬
$ expac -HM '%l\t%n' | sort -h | tail -20

# 크기순 정렬
$ expac -H M '%m\t%n' | sort -h | tail -20
```

---

## 시스템 업데이트

### 부분 업그레이드 방지

```bash
# 올바른 방법 (항상 이것 사용)
$ sudo pacman -Syu

# 잘못된 방법 (절대 사용하지 말 것)
# sudo pacman -Sy package  # 부분 업그레이드 위험
# sudo pacman -Su          # 데이터베이스 동기화 없이 업그레이드

# 특정 패키지 무시
$ sudo vi /etc/pacman.conf
IgnorePkg = linux linux-headers

# 또는 명령줄에서
$ sudo pacman -Syu --ignore linux,linux-headers

# 특정 그룹 무시
IgnoreGroup = gnome
```

### 안전한 업데이트 절차

```bash
# 1. Arch 뉴스 확인
$ curl https://archlinux.org/feeds/news/ | grep -E '<title>|<pubDate>'

# 2. 미러 업데이트
$ sudo reflector --country Korea,Japan --age 12 --protocol https \
  --sort rate --save /etc/pacman.d/mirrorlist

# 3. 데이터베이스 동기화
$ sudo pacman -Sy

# 4. keyring 업데이트
$ sudo pacman -S archlinux-keyring

# 5. 시스템 업그레이드
$ sudo pacman -Syu

# 6. 재부팅 필요 확인
$ uname -r  # 커널 버전 확인
$ pacman -Q linux  # 설치된 커널 버전
```

### 다운그레이드

```bash
# 캐시에서 이전 버전 설치
$ sudo pacman -U /var/cache/pacman/pkg/package-old-version.pkg.tar.zst

# downgrade 도구 사용 (AUR)
$ yay -S downgrade
$ sudo downgrade package

# Arch Linux Archive (ALA) 사용
$ sudo vi /etc/pacman.conf
# [core] 저장소를 다음으로 변경:
# Server = https://archive.archlinux.org/repos/2024/01/15/$repo/os/$arch

$ sudo pacman -Syu  # 해당 날짜 버전으로 다운그레이드
```

---

## 패키지 그룹

### 그룹 관리

```bash
# 사용 가능한 그룹 목록
$ pacman -Sg
base
base-devel
gnome
kde-applications
...

# 그룹 내용 확인
$ pacman -Sg gnome
gnome baobab
gnome cheese
gnome eog
...

# 그룹 전체 설치
$ sudo pacman -S gnome

# 그룹 일부 설치
$ sudo pacman -S gnome
Enter a selection (default=all): 1-10 15 20

# 그룹에 속한 설치된 패키지
$ pacman -Qg gnome

# 그룹 제거
$ sudo pacman -Rs gnome

# 특정 패키지가 속한 그룹 찾기
$ pacman -Qi package | grep Groups
```

### 유용한 그룹

```bash
# 개발 도구
$ sudo pacman -S base-devel
# gcc, make, autoconf, automake 등 포함

# 멀티미디어
$ sudo pacman -S gnome-extra
$ sudo pacman -S kde-multimedia

# 그래픽
$ sudo pacman -S xorg
$ sudo pacman -S xorg-apps

# 폰트
$ sudo pacman -S ttf-liberation
$ sudo pacman -S noto-fonts noto-fonts-cjk noto-fonts-emoji
```

---

## 캐시 관리

### 캐시 디렉토리

```bash
# 캐시 위치
$ ls /var/cache/pacman/pkg/
package-1.0-1-x86_64.pkg.tar.zst
package-1.1-1-x86_64.pkg.tar.zst
...

# 캐시 크기 확인
$ du -sh /var/cache/pacman/pkg/
2.5G    /var/cache/pacman/pkg/

# 패키지 개수
$ ls /var/cache/pacman/pkg/ | wc -l
1247

# 가장 큰 패키지들
$ ls -lhS /var/cache/pacman/pkg/ | head -20
```

### 캐시 정리

```bash
# 모든 캐시 제거
$ sudo pacman -Scc
:: Do you want to remove ALL files from cache? [y/N] y

# 설치되지 않은 패키지만 제거
$ sudo pacman -Sc

# paccache 사용 (더 안전)
$ sudo pacman -S pacman-contrib

# 최근 3개 버전만 유지
$ paccache -r
$ paccache -rk3  # 3개 버전 유지

# 미설치 패키지 캐시 제거
$ paccache -ruk0

# 드라이런 (실제 삭제 안 함)
$ paccache -dk3

# 자동화 (systemd timer)
$ sudo systemctl enable paccache.timer
$ sudo systemctl start paccache.timer

# 타이머 확인
$ systemctl status paccache.timer
```

### 캐시 복원

```bash
# 캐시에서 패키지 재설치
$ sudo pacman -U /var/cache/pacman/pkg/package-version.pkg.tar.zst

# 모든 캐시 패키지 목록
$ ls /var/cache/pacman/pkg/*.pkg.tar.zst | less

# 특정 패키지의 모든 버전
$ ls /var/cache/pacman/pkg/nginx-*.pkg.tar.zst
```

---

## AUR (Arch User Repository)

### AUR 소개

```bash
# AUR은 사용자가 제공하는 패키지 저장소
# 공식 저장소에 없는 소프트웨어 제공
# PKGBUILD 스크립트로 소스에서 빌드

# AUR 웹사이트
# https://aur.archlinux.org/

# AUR 헬퍼 없이 수동 설치
$ git clone https://aur.archlinux.org/package-name.git
$ cd package-name
$ less PKGBUILD  # 내용 확인 (보안)
$ makepkg -si
# -s: 의존성 설치
# -i: 빌드 후 설치
```

### yay 설치 및 사용

```bash
# yay 설치 (가장 인기있는 AUR 헬퍼)
$ sudo pacman -S --needed git base-devel
$ git clone https://aur.archlinux.org/yay.git
$ cd yay
$ makepkg -si

# yay 사용법 (pacman과 유사)
# 패키지 검색
$ yay -Ss package

# 패키지 설치
$ yay -S package
$ yay -S google-chrome

# 시스템 업데이트 (공식 + AUR)
$ yay -Syu

# AUR 패키지만 업데이트
$ yay -Sua

# 패키지 정보
$ yay -Si package

# 제거
$ yay -Rs package

# orphans 제거
$ yay -Yc

# 설치된 AUR 패키지
$ yay -Qm

# 통계
$ yay -Ps
```

### paru (yay 대안)

```bash
# paru 설치
$ yay -S paru

# 또는 수동 설치
$ git clone https://aur.archlinux.org/paru.git
$ cd paru
$ makepkg -si

# paru 사용법
$ paru -Syu  # 시스템 업데이트
$ paru -S package  # 설치
$ paru -Rs package  # 제거

# paru의 장점
# - Rust로 작성 (빠름)
# - 개선된 PKGBUILD 검토
# - 더 나은 의존성 처리
```

### AUR 패키지 빌드

```bash
# 수동 빌드 과정
$ git clone https://aur.archlinux.org/package.git
$ cd package

# PKGBUILD 검토 (중요!)
$ less PKGBUILD
$ cat .SRCINFO

# 의존성 설치
$ makepkg -s

# 패키지 빌드
$ makepkg

# 빌드 및 설치
$ makepkg -si

# 정리
$ makepkg -c  # 빌드 파일 정리

# GPG 키 가져오기 (필요시)
$ gpg --recv-keys KEY_ID

# 체크섬 건너뛰기 (권장하지 않음)
$ makepkg --skipinteg
```

---

## Pacman 설정

### /etc/pacman.conf

```bash
# 설정 파일 편집
$ sudo vi /etc/pacman.conf

# 주요 설정 옵션
[options]
# Architecture = auto
# HoldPkg = pacman glibc
# IgnorePkg = package1 package2
# IgnoreGroup = gnome
# NoUpgrade = /etc/passwd /etc/group
# NoExtract = usr/share/man/* usr/share/doc/*

# 컬러 출력 활성화
Color

# 진행바 표시
ILoveCandy  # Pac-Man 스타일

# 병렬 다운로드
ParallelDownloads = 5

# VerbosePkgLists
VerbosePkgLists

# 저장소 설정
[core]
Include = /etc/pacman.d/mirrorlist

[extra]
Include = /etc/pacman.d/mirrorlist

[community]
Include = /etc/pacman.d/mirrorlist

[multilib]  # 32비트 지원
Include = /etc/pacman.d/mirrorlist

# 사용자 저장소 추가
[custom]
SigLevel = Optional TrustAll
Server = file:///home/user/packages
```

### 미러 관리

```bash
# 미러 목록 확인
$ cat /etc/pacman.d/mirrorlist
Server = https://mirror.example.com/archlinux/$repo/os/$arch

# reflector로 미러 업데이트
$ sudo pacman -S reflector

# 가장 빠른 미러 찾기
$ sudo reflector --latest 20 --protocol https --sort rate \
  --save /etc/pacman.d/mirrorlist

# 특정 국가 미러
$ sudo reflector --country 'South Korea,Japan' --age 12 \
  --protocol https --sort rate --save /etc/pacman.d/mirrorlist

# 자동화
$ sudo vi /etc/xdg/reflector/reflector.conf
--save /etc/pacman.d/mirrorlist
--country Korea,Japan
--protocol https
--latest 10
--sort rate

# reflector 서비스 활성화
$ sudo systemctl enable reflector.service
$ sudo systemctl start reflector.service

# 타이머로 주기적 업데이트
$ sudo systemctl enable reflector.timer
```

### 서명 검증

```bash
# GPG 키 관리
$ sudo pacman-key --init
$ sudo pacman-key --populate archlinux

# 키 목록
$ pacman-key --list-keys

# 키 새로고침
$ sudo pacman-key --refresh-keys

# 특정 키 추가
$ sudo pacman-key --recv-keys KEY_ID
$ sudo pacman-key --lsign-key KEY_ID

# 서명 레벨 설정 (pacman.conf)
SigLevel = Required DatabaseOptional
# Required: 서명 필수
# Optional: 서명 선택
# TrustAll: 모든 서명 신뢰
```

---

## 문제 해결

### 일반 문제

```bash
# 1. "failed to commit transaction (conflicting files)"
$ sudo pacman -S package
error: failed to commit transaction (conflicting files)
package: /usr/bin/file exists in filesystem

# 해결: 충돌 파일 덮어쓰기 (주의)
$ sudo pacman -S --overwrite /usr/bin/file package

# 2. "invalid or corrupted package"
# 캐시 정리 후 재시도
$ sudo rm /var/cache/pacman/pkg/package-*.pkg.tar.zst
$ sudo pacman -Sy package

# 3. "failed to update core (unable to lock database)"
$ sudo rm /var/lib/pacman/db.lck

# 4. "error: failed to init transaction (unable to lock database)"
# 다른 pacman 프로세스 확인
$ ps aux | grep pacman
$ sudo kill -9 PID
$ sudo rm /var/lib/pacman/db.lck

# 5. GPG 서명 오류
$ sudo pacman -S archlinux-keyring
$ sudo pacman-key --populate archlinux
$ sudo pacman-key --refresh-keys

# 6. 미러 오류
$ sudo reflector --latest 20 --sort rate \
  --save /etc/pacman.d/mirrorlist
$ sudo pacman -Syyu
```

### 손상된 데이터베이스 복구

```bash
# 데이터베이스 동기화
$ sudo pacman -Syyu

# 데이터베이스 재생성
$ sudo rm -rf /var/lib/pacman/sync/*
$ sudo pacman -Sy

# 로컬 데이터베이스 문제
$ sudo pacman -Dk  # 확인
$ sudo pacman -Syyu

# 완전 복구
$ sudo mv /var/lib/pacman/local /var/lib/pacman/local.bak
$ sudo pacman -Syyu
$ sudo pacman -S $(pacman -Qq)
```

### 의존성 문제

```bash
# 깨진 의존성 찾기
$ pacman -Qk  # 모든 패키지 파일 확인
$ pacman -Qkk  # 철저한 확인

# 특정 패키지 확인
$ pacman -Qk package

# 의존성 재설치
$ sudo pacman -S $(pacman -Qnq)  # 공식 저장소 패키지
$ yay -S $(pacman -Qmq)  # AUR 패키지

# 강제 재설치
$ sudo pacman -S --overwrite '*' package
```

---

## 고급 기능

### 패키지 쿼리

```bash
# 암묵적 의존성 찾기
$ comm -23 <(pacman -Qeq | sort) <(pacman -Qmq | sort)

# 사용하지 않는 패키지 (orphans)
$ pacman -Qtdq

# 가장 큰 패키지들
$ expac -H M '%m\t%n' | sort -h | tail -20
1104.00 MiB     linux-firmware
589.00 MiB      texlive-core
412.00 MiB      libreoffice-fresh

# 최근 설치된 패키지
$ expac --timefmt='%Y-%m-%d %T' '%l\t%n' | sort | tail -20

# 사용하지 않는 의존성 자동 제거 스크립트
$ cat > /usr/local/bin/remove-orphans.sh << 'EOF'
#!/bin/bash
orphans=$(pacman -Qtdq)
if [ -n "$orphans" ]; then
    echo "Removing orphans:"
    echo "$orphans"
    sudo pacman -Rns $orphans
else
    echo "No orphans found."
fi
EOF
$ chmod +x /usr/local/bin/remove-orphans.sh
```

### Hook 시스템

```bash
# Hook 위치
$ ls /usr/share/libalpm/hooks/

# 사용자 hook 디렉토리
$ sudo mkdir -p /etc/pacman.d/hooks/

# 예제: 커널 업데이트 시 알림
$ sudo vi /etc/pacman.d/hooks/kernel-update.hook
[Trigger]
Operation = Upgrade
Type = Package
Target = linux

[Action]
Description = Kernel updated - reboot recommended
When = PostTransaction
Exec = /usr/bin/echo "Kernel updated! Please reboot."

# 예제: 패키지 캐시 자동 정리
$ sudo vi /etc/pacman.d/hooks/clean-cache.hook
[Trigger]
Operation = Upgrade
Operation = Install
Operation = Remove
Type = Package
Target = *

[Action]
Description = Cleaning pacman cache...
When = PostTransaction
Exec = /usr/bin/paccache -rk2

# Hook 테스트
$ sudo pacman -S package
```

### 사용자 저장소

```bash
# 로컬 저장소 생성
$ mkdir ~/packages
$ cp *.pkg.tar.zst ~/packages/

# 데이터베이스 생성
$ cd ~/packages
$ repo-add custom.db.tar.gz *.pkg.tar.zst

# pacman.conf에 추가
$ sudo vi /etc/pacman.conf
[custom]
SigLevel = Optional TrustAll
Server = file:///home/user/packages

# 동기화
$ sudo pacman -Sy

# 설치
$ sudo pacman -S package-from-custom-repo
```

---

## 실전 예제

### 시스템 업데이트 스크립트

```bash
#!/bin/bash
# arch-update.sh

echo "=== Arch Linux System Update ==="
echo "Date: $(date)"
echo

# 1. Arch 뉴스 확인
echo "Latest Arch Linux News:"
curl -s https://archlinux.org/feeds/news/ | \
    grep -E '<title>|<pubDate>' | head -10
echo

# 2. 미러 업데이트
echo "Updating mirrorlist..."
sudo reflector --country Korea,Japan --age 12 \
    --protocol https --sort rate \
    --save /etc/pacman.d/mirrorlist

# 3. keyring 업데이트
echo "Updating keyring..."
sudo pacman -S --noconfirm archlinux-keyring

# 4. 시스템 업데이트
echo "Updating system..."
sudo pacman -Syu

# 5. AUR 업데이트
if command -v yay &> /dev/null; then
    echo "Updating AUR packages..."
    yay -Sua
fi

# 6. orphans 제거
orphans=$(pacman -Qtdq)
if [ -n "$orphans" ]; then
    echo "Removing orphaned packages:"
    echo "$orphans"
    sudo pacman -Rns $orphans
fi

# 7. 캐시 정리
echo "Cleaning cache..."
paccache -rk2

echo
echo "=== Update Complete ==="
```

### 패키지 백업 및 복원

```bash
# 백업 스크립트
#!/bin/bash
# backup-packages.sh

BACKUP_DIR="$HOME/pacman-backup"
DATE=$(date +%Y%m%d)

mkdir -p "$BACKUP_DIR"

# 패키지 목록
pacman -Qqe > "$BACKUP_DIR/pkglist-$DATE.txt"
pacman -Qqem > "$BACKUP_DIR/pkglist-aur-$DATE.txt"

# pacman 설정
cp /etc/pacman.conf "$BACKUP_DIR/pacman.conf-$DATE"
cp /etc/pacman.d/mirrorlist "$BACKUP_DIR/mirrorlist-$DATE"

echo "Backup created in $BACKUP_DIR"

# 복원 스크립트
#!/bin/bash
# restore-packages.sh

BACKUP_FILE="$1"

if [ ! -f "$BACKUP_FILE" ]; then
    echo "Usage: $0 <pkglist-file>"
    exit 1
fi

# 공식 저장소 패키지
pacman -Qqn > /tmp/repo-pkgs.txt
comm -12 <(sort "$BACKUP_FILE") <(sort /tmp/repo-pkgs.txt) | \
    sudo pacman -S --needed -

# AUR 패키지
if command -v yay &> /dev/null; then
    comm -13 <(sort /tmp/repo-pkgs.txt) <(sort "$BACKUP_FILE") | \
        yay -S --needed -
fi

echo "Restoration complete"
```

### 패키지 모니터링

```bash
# 크기 분석
#!/bin/bash
# package-size-report.sh

echo "=== Top 20 Largest Packages ==="
expac -H M '%m\t%n' | sort -h | tail -20

echo
echo "=== Total Installed Size ==="
expac -H M '%m' | awk '{s+=$1} END {print s " MiB"}'

echo
echo "=== Cache Size ==="
du -sh /var/cache/pacman/pkg/

echo
echo "=== Number of Installed Packages ==="
pacman -Q | wc -l
```

---

## 요약

Pacman 핵심 명령어:

1. **설치**: `pacman -S package`
2. **제거**: `pacman -Rs package`
3. **업데이트**: `pacman -Syu`
4. **검색**: `pacman -Ss keyword`
5. **정보**: `pacman -Si/Qi package`
6. **캐시 정리**: `paccache -r`
7. **AUR**: `yay -S package`

중요 팁:
- 항상 `pacman -Syu`로 업데이트 (부분 업그레이드 방지)
- 정기적으로 orphans 제거
- AUR 패키지는 PKGBUILD 확인 후 설치
- 미러 최적화로 다운로드 속도 향상

---

[다음: 소스에서 빌드 →](building-from-source.md)

[← DNF/YUM으로 돌아가기](dnf-redhat.md)

[← 목차로 돌아가기](../README.md)
