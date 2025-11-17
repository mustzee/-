# 리눅스 배포판 가이드

## 목차
- [배포판이란?](#배포판이란)
- [주요 배포판 계열](#주요-배포판-계열)
- [배포판 선택 가이드](#배포판-선택-가이드)
- [주요 배포판 상세 분석](#주요-배포판-상세-분석)
- [특수 목적 배포판](#특수-목적-배포판)
- [배포판 비교표](#배포판-비교표)

---

## 배포판이란?

### 리눅스 vs 리눅스 배포판

**리눅스 (Linux):**
- Linus Torvalds가 개발한 **커널**만을 의미
- 하드웨어와 소프트웨어 사이의 인터페이스
- 단독으로는 사용자가 직접 사용할 수 없음

**리눅스 배포판 (Linux Distribution):**
```
┌────────────────────────────────────┐
│  Applications & Desktop Environment│  ← 사용자 애플리케이션
├────────────────────────────────────┤
│  Package Manager & Tools           │  ← 패키지 관리 시스템
├────────────────────────────────────┤
│  System Utilities (GNU Tools)      │  ← 시스템 도구
├────────────────────────────────────┤
│  Libraries & Dependencies          │  ← 라이브러리
├────────────────────────────────────┤
│  Init System (systemd, etc.)       │  ← 초기화 시스템
├────────────────────────────────────┤
│  Linux Kernel                      │  ← 리눅스 커널
├────────────────────────────────────┤
│  Hardware                          │  ← 하드웨어
└────────────────────────────────────┘
```

### 배포판의 구성 요소

1. **Linux Kernel** - 핵심 운영체제
2. **GNU Tools** - 기본 유틸리티 (bash, coreutils 등)
3. **Package Manager** - 소프트웨어 설치/관리 도구
4. **Init System** - 시스템 초기화 (systemd, SysVinit 등)
5. **Desktop Environment** - GUI 환경 (선택적)
6. **Applications** - 웹 브라우저, 오피스 등
7. **Documentation** - 매뉴얼, 가이드

---

## 주요 배포판 계열

### 1. Debian 계열

**특징:**
- .deb 패키지 형식
- APT/dpkg 패키지 관리자
- 안정성 중시
- 커뮤니티 주도

**계열도:**
```
Debian
  ├── Ubuntu
  │     ├── Linux Mint
  │     ├── Pop!_OS
  │     ├── elementary OS
  │     ├── Zorin OS
  │     └── KDE neon
  ├── Kali Linux
  ├── Parrot OS
  └── MX Linux
```

**패키지 관리:**
```bash
# APT 사용
sudo apt update
sudo apt install package-name
sudo apt remove package-name
sudo apt search keyword

# dpkg 직접 사용
sudo dpkg -i package.deb
dpkg -l  # 설치된 패키지 목록
```

### 2. Red Hat 계열

**특징:**
- .rpm 패키지 형식
- DNF/YUM 패키지 관리자
- 엔터프라이즈 중심
- 강력한 상업적 지원

**계열도:**
```
Red Hat Enterprise Linux (RHEL)
  ├── CentOS Stream
  ├── Rocky Linux
  ├── AlmaLinux
  ├── Oracle Linux
  └── Scientific Linux

Fedora
  └── RHEL (upstream)
```

**패키지 관리:**
```bash
# DNF 사용 (Fedora, RHEL 8+)
sudo dnf check-update
sudo dnf install package-name
sudo dnf remove package-name
sudo dnf search keyword

# YUM 사용 (RHEL 7, CentOS 7)
sudo yum update
sudo yum install package-name

# RPM 직접 사용
sudo rpm -ivh package.rpm
rpm -qa  # 설치된 패키지 목록
```

### 3. Arch 계열

**특징:**
- 롤링 릴리스 (Rolling Release)
- 최신 소프트웨어
- 사용자가 직접 구성
- Arch Wiki - 최고의 문서

**계열도:**
```
Arch Linux
  ├── Manjaro
  ├── EndeavourOS
  ├── ArcoLinux
  ├── Garuda Linux
  └── Artix Linux (systemd 제외)
```

**패키지 관리:**
```bash
# pacman 사용
sudo pacman -Syu  # 시스템 업데이트
sudo pacman -S package-name  # 패키지 설치
sudo pacman -R package-name  # 패키지 제거
sudo pacman -Ss keyword  # 패키지 검색

# AUR (Arch User Repository) - yay 사용
yay -S aur-package-name
yay -Syu  # 전체 업데이트 (AUR 포함)
```

### 4. SUSE 계열

**특징:**
- 유럽에서 인기
- YaST 관리 도구
- 엔터프라이즈 지원
- Btrfs 기본 파일시스템

**계열도:**
```
SUSE Linux Enterprise
  └── openSUSE Leap

openSUSE Tumbleweed (롤링 릴리스)
```

**패키지 관리:**
```bash
# zypper 사용
sudo zypper refresh
sudo zypper install package-name
sudo zypper remove package-name
sudo zypper search keyword

# YaST (GUI/TUI 관리 도구)
sudo yast
```

### 5. 독립 배포판

**Gentoo:**
- 소스 기반 배포판
- 모든 패키지를 컴파일
- 최대 커스터마이징
```bash
# emerge 사용
sudo emerge --sync
sudo emerge package-name
```

**Slackware:**
- 가장 오래된 현존 배포판 (1993년부터)
- 전통적인 유닉스 방식
- 단순함 추구

**Void Linux:**
- 독자적인 init 시스템 (runit)
- systemd를 사용하지 않음
- 롤링 릴리스

---

## 배포판 선택 가이드

### 사용 목적별 추천

#### 초보자용
```
┌─────────────────┬──────────────────────────────┐
│ Ubuntu          │ 가장 인기 있고 자료 많음     │
│ Linux Mint      │ Windows 사용자에게 친숙      │
│ Pop!_OS         │ 개발자 친화적, Nvidia 지원   │
│ Zorin OS        │ Windows/macOS와 유사한 UI    │
└─────────────────┴──────────────────────────────┘
```

**초보자가 Ubuntu를 선택해야 하는 이유:**
```bash
# 1. 방대한 커뮤니티 지원
- 구글 검색 시 가장 많은 해결책
- 포럼, 블로그, YouTube 튜토리얼 풍부

# 2. 소프트웨어 가용성
sudo apt install vlc
sudo apt install gimp
sudo apt install vscode

# 3. 하드웨어 호환성
- 대부분의 하드웨어 자동 인식
- 드라이버 자동 설치

# 4. 정기적인 릴리스
- 6개월마다 새 버전
- LTS (Long Term Support) 버전은 5년 지원
```

#### 개발자용
```
┌─────────────────┬──────────────────────────────┐
│ Ubuntu          │ 서버 환경과 동일, CI/CD 호환  │
│ Fedora          │ 최신 기술, 개발 도구 풍부     │
│ Arch Linux      │ 최신 패키지, 완전한 제어      │
│ Pop!_OS         │ 개발 환경 최적화             │
└─────────────────┴──────────────────────────────┘
```

**개발자가 Fedora를 선택하는 이유:**
```bash
# 최신 개발 도구
- 최신 커널
- 최신 GCC, LLVM
- 최신 언어 버전 (Python, Node.js, Go 등)

# Red Hat 생태계
- RHEL의 테스트베드
- SELinux 완벽 지원
- 엔터프라이즈 기술 선도

# 개발 환경
sudo dnf groupinstall "Development Tools"
sudo dnf install git vim emacs
```

#### 서버용
```
┌──────────────────┬──────────────────────────────┐
│ Ubuntu Server    │ 클라우드에서 가장 인기        │
│ RHEL/Rocky Linux │ 엔터프라이즈 표준             │
│ Debian           │ 안정성, 최소 리소스           │
│ Alpine Linux     │ 컨테이너용, 매우 경량         │
└──────────────────┴──────────────────────────────┘
```

**서버 환경별 선택:**

**클라우드 (AWS, GCP, Azure):**
```bash
# Ubuntu가 기본 선택인 이유
- 가장 많은 AMI/이미지
- cloud-init 완벽 지원
- 커뮤니티 지원 우수

# 예: AWS EC2
aws ec2 run-instances \
  --image-id ami-ubuntu-22.04 \
  --instance-type t3.medium
```

**엔터프라이즈:**
```bash
# RHEL/Rocky Linux 선택 이유
- 공식 상업 지원
- 장기 지원 (10년+)
- 인증 및 컴플라이언스
- 예측 가능한 업데이트 주기
```

**컨테이너:**
```dockerfile
# Alpine Linux - 5MB 크기
FROM alpine:latest
RUN apk add --no-cache python3

# vs Ubuntu - 77MB
FROM ubuntu:22.04
RUN apt-get update && apt-get install -y python3
```

#### 보안/침투 테스트용
```
┌─────────────────┬──────────────────────────────┐
│ Kali Linux      │ 가장 인기, 도구 600+          │
│ Parrot Security │ 경량, 익명성 중시             │
│ BlackArch       │ Arch 기반, 도구 2500+         │
└─────────────────┴──────────────────────────────┘
```

**Kali Linux 예제:**
```bash
# 사전 설치된 보안 도구
nmap -sV target.com
wireshark
metasploit-framework
burpsuite
john
hashcat

# 카테고리별 도구 설치
sudo apt install kali-tools-web
sudo apt install kali-tools-wireless
sudo apt install kali-tools-forensics
```

#### 프라이버시/익명성 중시
```
┌─────────────────┬──────────────────────────────┐
│ Tails           │ Tor 기반, 흔적 남기지 않음    │
│ Whonix          │ Tor 격리, 강력한 익명성       │
│ Qubes OS        │ 보안 격리, 가상화 기반        │
└─────────────────┴──────────────────────────────┘
```

#### 경량/구형 하드웨어
```
┌─────────────────┬──────────────────────────────┐
│ Lubuntu         │ LXQt 데스크톱, 매우 가벼움    │
│ Puppy Linux     │ 512MB RAM에서도 동작          │
│ AntiX           │ systemd 없음, 초경량          │
│ Tiny Core Linux │ 16MB 크기!                    │
└─────────────────┴──────────────────────────────┘
```

---

## 주요 배포판 상세 분석

### Ubuntu

**개요:**
- 첫 릴리스: 2004년 10월
- 개발사: Canonical Ltd.
- 기반: Debian
- 철학: "Linux for Human Beings"

**버전 체계:**
```
Ubuntu 22.04 LTS
       │  │  └─ LTS (Long Term Support) - 5년 지원
       │  └─── 4월 릴리스
       └────── 2022년
```

**릴리스 주기:**
```
2022.04 (LTS) ─────────────────> 2027.04 지원 종료
2022.10       ──────> 2023.07 지원 종료
2023.04       ──────> 2024.01 지원 종료
2023.10       ──────> 2024.07 지원 종료
2024.04 (LTS) ─────────────────> 2029.04 지원 종료
```

**공식 flavor:**
```bash
# Desktop Environments 별 배포판
Kubuntu        # KDE Plasma
Xubuntu        # Xfce
Lubuntu        # LXQt
Ubuntu MATE    # MATE
Ubuntu Budgie  # Budgie
Ubuntu Studio  # 멀티미디어 제작
Ubuntu Kylin   # 중국 사용자용
```

**장점:**
- ✅ 가장 많은 사용자 커뮤니티
- ✅ 풍부한 문서와 튜토리얼
- ✅ 하드웨어 호환성 우수
- ✅ PPA를 통한 쉬운 소프트웨어 추가
- ✅ Snap 패키지 지원

**단점:**
- ❌ Snap 강제 (논란)
- ❌ Canonical의 독자적 결정 (Unity, Mir 등)
- ❌ 일부 블로트웨어

**실습 예제:**
```bash
# 1. 시스템 정보 확인
lsb_release -a
# Output:
# Distributor ID: Ubuntu
# Description:    Ubuntu 22.04.3 LTS
# Release:        22.04
# Codename:       jammy

# 2. PPA 추가 (예: 최신 Git)
sudo add-apt-repository ppa:git-core/ppa
sudo apt update
sudo apt install git

# 3. Snap 패키지 설치
sudo snap install code --classic  # VS Code
sudo snap install spotify

# 4. 데스크탑 환경 변경
sudo apt install kubuntu-desktop  # KDE Plasma 설치
# 로그인 시 DE 선택 가능
```

### Fedora

**개요:**
- 첫 릴리스: 2003년 11월
- 스폰서: Red Hat
- RHEL의 upstream
- 최신 기술 테스트베드

**버전 체계:**
```
Fedora 39
       └─ 버전 번호 (6개월마다 증가)

지원 기간: 약 13개월 (2개 버전)
```

**Fedora Spins:**
```bash
# Desktop Environments
Fedora KDE Plasma
Fedora Xfce
Fedora LXQt
Fedora Cinnamon
Fedora MATE

# 특수 목적
Fedora Server
Fedora IoT
Fedora CoreOS
```

**장점:**
- ✅ 최신 소프트웨어
- ✅ Red Hat 지원
- ✅ SELinux 완벽 통합
- ✅ 혁신적 기술 선도
- ✅ Wayland, PipeWire, systemd 등

**단점:**
- ❌ 짧은 지원 기간
- ❌ 잦은 업그레이드 필요
- ❌ 일부 드라이버 issue (NVIDIA)

**실습 예제:**
```bash
# 1. 시스템 정보
cat /etc/fedora-release
# Fedora release 39 (Thirty Nine)

# 2. 개발 도구 설치
sudo dnf groupinstall "Development Tools"
sudo dnf groupinstall "C Development Tools and Libraries"

# 3. RPM Fusion 저장소 추가 (멀티미디어 코덱)
sudo dnf install \
  https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm

# 4. Flatpak 사용
flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
flatpak install flathub org.gimp.GIMP

# 5. Fedora 버전 업그레이드
sudo dnf upgrade --refresh
sudo dnf install dnf-plugin-system-upgrade
sudo dnf system-upgrade download --releasever=39
sudo dnf system-upgrade reboot
```

### Debian

**개요:**
- 첫 릴리스: 1993년 9월
- 완전한 커뮤니티 프로젝트
- 가장 오래된 현존 배포판 중 하나
- "Universal Operating System"

**버전 체계:**
```
Debian 12 "bookworm"
       │    └─ Toy Story 캐릭터 코드명
       └────── 버전 번호

릴리스: 약 2년마다
지원: 5년 (LTS는 추가 지원)
```

**Debian 코드명 역사:**
```
Debian 6   - Squeeze (2011)
Debian 7   - Wheezy (2013)
Debian 8   - Jessie (2015)
Debian 9   - Stretch (2017)
Debian 10  - Buster (2019)
Debian 11  - Bullseye (2021)
Debian 12  - Bookworm (2023)
Debian 13  - Trixie (개발 중)
```

**브랜치:**
```
Stable     - 안정 릴리스 (프로덕션용)
Testing    - 다음 릴리스 준비
Unstable   - Sid (항상 불안정, 개발용)
```

**장점:**
- ✅ 매우 안정적
- ✅ 방대한 패키지 저장소 (59,000+)
- ✅ 다양한 아키텍처 지원
- ✅ 순수 FOSS (Free and Open Source Software)
- ✅ 커뮤니티 주도

**단점:**
- ❌ 오래된 소프트웨어 (Stable)
- ❌ 초보자에게 어려움
- ❌ 설치 시 non-free 드라이버 별도 설정

**실습 예제:**
```bash
# 1. 버전 확인
cat /etc/debian_version
# 12.4

cat /etc/os-release
# PRETTY_NAME="Debian GNU/Linux 12 (bookworm)"

# 2. 소스 목록 확인
cat /etc/apt/sources.list
# deb http://deb.debian.org/debian/ bookworm main
# deb-src http://deb.debian.org/debian/ bookworm main

# 3. contrib, non-free 저장소 추가
sudo nano /etc/apt/sources.list
# deb http://deb.debian.org/debian/ bookworm main contrib non-free non-free-firmware

# 4. backports 사용 (최신 패키지)
echo "deb http://deb.debian.org/debian bookworm-backports main" | \
  sudo tee /etc/apt/sources.list.d/backports.list
sudo apt update
sudo apt install -t bookworm-backports package-name

# 5. Testing으로 업그레이드 (주의!)
sudo sed -i 's/bookworm/testing/g' /etc/apt/sources.list
sudo apt update
sudo apt full-upgrade
```

### Arch Linux

**개요:**
- 첫 릴리스: 2002년 3월
- KISS 원칙 (Keep It Simple, Stupid)
- 롤링 릴리스
- DIY (Do It Yourself) 철학

**철학:**
```
1. Simplicity (단순성)
   - 불필요한 추가 없이 upstream 소프트웨어 유지

2. Modernity (현대성)
   - 항상 최신 소프트웨어

3. Pragmatism (실용성)
   - 이데올로기보다 실용성

4. User Centrality (사용자 중심)
   - 사용자가 시스템 완전 제어

5. Versatility (다용성)
   - 다양한 용도로 사용 가능
```

**Arch Way:**
```
"Arch Linux defines simplicity as without unnecessary
additions or modifications. It ships software as
released by the original developers (upstream) with
minimal distribution-specific (downstream) changes."
```

**장점:**
- ✅ 최신 소프트웨어 (bleeding edge)
- ✅ 완전한 커스터마이징
- ✅ Arch Wiki - 세계 최고의 문서
- ✅ AUR (Arch User Repository)
- ✅ 롤링 릴리스 (재설치 불필요)

**단점:**
- ❌ 가파른 학습 곡선
- ❌ 수동 설치 과정
- ❌ 업데이트 시 깨질 수 있음
- ❌ 초보자에게 비추천

**설치 과정 (간략):**
```bash
# 1. 디스크 파티셔닝
fdisk /dev/sda
mkfs.ext4 /dev/sda1
mount /dev/sda1 /mnt

# 2. 기본 시스템 설치
pacstrap /mnt base linux linux-firmware

# 3. fstab 생성
genfstab -U /mnt >> /mnt/etc/fstab

# 4. chroot
arch-chroot /mnt

# 5. 시스템 설정
ln -sf /usr/share/zoneinfo/Asia/Seoul /etc/localtime
hwclock --systohc
echo "archlinux" > /etc/hostname

# 6. 부트로더 설치
pacman -S grub
grub-install /dev/sda
grub-mkconfig -o /boot/grub/grub.cfg

# 7. 재부팅
exit
reboot
```

**일상 사용:**
```bash
# 시스템 전체 업데이트
sudo pacman -Syu

# AUR helper (yay) 설치
git clone https://aur.archlinux.org/yay.git
cd yay
makepkg -si

# AUR 패키지 설치
yay -S google-chrome
yay -S visual-studio-code-bin
yay -S spotify

# 패키지 정보
pacman -Si package-name  # 저장소
yay -Si aur-package     # AUR

# 파일이 어느 패키지에 속하는지
pacman -Qo /usr/bin/ls
```

### Linux Mint

**개요:**
- 첫 릴리스: 2006년
- 기반: Ubuntu (및 Debian)
- Windows 사용자를 위한 쉬운 전환

**에디션:**
```
Cinnamon - 전통적인 데스크탑 (Windows 유사)
MATE     - 경량, 안정적
Xfce     - 매우 경량
```

**장점:**
- ✅ Windows 사용자에게 친숙
- ✅ 멀티미디어 코덱 기본 포함
- ✅ 안정성 중시
- ✅ 초보자 친화적

**독특한 도구:**
```bash
# Timeshift - 시스템 스냅샷
sudo timeshift --create
sudo timeshift --restore

# Update Manager - 안전한 업데이트
mintupdate

# Driver Manager
sudo mint-drivers

# Software Manager - GUI 소프트웨어 센터
```

---

## 특수 목적 배포판

### 보안/침투 테스트

**Kali Linux:**
```bash
# 사전 설치된 도구 카테고리
01. Information Gathering (정보 수집)
    - nmap, whois, dnsenum, fierce

02. Vulnerability Analysis (취약점 분석)
    - nikto, OpenVAS, sqlmap

03. Web Applications (웹 애플리케이션)
    - burpsuite, w3af, wpscan

04. Password Attacks (비밀번호 공격)
    - john, hashcat, hydra, medusa

05. Wireless Attacks (무선 공격)
    - aircrack-ng, reaver, wifite

# 메타패키지 설치
sudo apt install kali-linux-default   # 기본 도구
sudo apt install kali-linux-large     # 확장 도구
sudo apt install kali-linux-everything # 모든 도구
```

### 프라이버시/익명성

**Tails (The Amnesic Incognito Live System):**
```
특징:
- Live USB로만 실행
- 모든 연결이 Tor를 통해 라우팅
- 메모리에만 실행, 재부팅 시 모든 흔적 삭제
- 암호화된 영구 스토리지 옵션

사용 사례:
- 저널리스트
- 활동가
- 고위험 환경의 사용자
```

**Whonix:**
```
구조:
┌────────────────┐
│ Whonix Workstation │  ← 실제 작업
│ (Isolated)         │
└────────┬───────────┘
         │ 모든 트래픽
         ↓
┌────────────────┐
│ Whonix Gateway │  ← Tor Gateway
│ (Tor Router)   │
└────────┬───────────┘
         │ Tor 네트워크
         ↓
   [Internet]
```

### 교육용

**Ubuntu Education Edition:**
- 교육 소프트웨어 기본 포함
- GCompris, TuxMath, TuxPaint 등

**Edubuntu:**
- GNOME 환경
- 학교용 최적화

### 멀티미디어 제작

**Ubuntu Studio:**
```bash
# 사전 설치된 소프트웨어
Audio:
- Ardour (DAW)
- Audacity
- Hydrogen (드럼 머신)

Video:
- Kdenlive
- Blender
- OBS Studio

Graphics:
- GIMP
- Inkscape
- Krita
```

**AV Linux:**
- 음악 제작 특화
- 저지연 커널

### 과학/연구

**Scientific Linux:**
- 과학 연구용
- CERN, Fermilab 사용

**Bio-Linux:**
- 생물정보학 도구

---

## 배포판 비교표

### 데스크탑 사용

| 배포판 | 난이도 | 안정성 | 최신성 | 커뮤니티 | 추천 대상 |
|--------|--------|--------|--------|----------|-----------|
| Ubuntu | ⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 초보자 |
| Linux Mint | ⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | Windows 전환자 |
| Fedora | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 개발자 |
| Arch | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 고급 사용자 |
| Manjaro | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | Arch 입문 |
| Pop!_OS | ⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | 개발자, 게이머 |

### 서버 사용

| 배포판 | 안정성 | 지원 기간 | 엔터프라이즈 | 클라우드 | 컨테이너 |
|--------|--------|-----------|--------------|----------|----------|
| RHEL | ⭐⭐⭐⭐⭐ | 10년+ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Rocky Linux | ⭐⭐⭐⭐⭐ | 10년 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Ubuntu Server | ⭐⭐⭐⭐ | 5년 (LTS) | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Debian | ⭐⭐⭐⭐⭐ | 5년+ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Alpine | ⭐⭐⭐ | 2년 | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

### 패키지 수 비교

```
Debian:     59,000+
Ubuntu:     50,000+
Arch (AUR): 80,000+ (공식 + AUR)
Fedora:     30,000+
openSUSE:   35,000+
```

---

## 실전 조언

### 첫 리눅스 선택하기

**절대 초보자:**
```bash
1순위: Linux Mint (Cinnamon)
2순위: Ubuntu
3순위: Pop!_OS
```

**Windows에서 온 사용자:**
```bash
1순위: Linux Mint
2순위: Zorin OS
3순위: Ubuntu
```

**macOS에서 온 사용자:**
```bash
1순위: elementary OS
2순위: Ubuntu
3순위: Pop!_OS
```

**개발자:**
```bash
1순위: Ubuntu (서버 환경과 동일)
2순위: Fedora (최신 도구)
3순위: Arch (완전한 제어)
```

**게이머:**
```bash
1순위: Pop!_OS (Nvidia 최적화)
2순위: Ubuntu
3순위: Manjaro
```

### 듀얼 부팅 vs 가상 머신

**듀얼 부팅:**
```
장점:
✅ 네이티브 성능
✅ 하드웨어 완전 활용
✅ 진정한 리눅스 경험

단점:
❌ 재부팅 필요
❌ 파티션 관리 복잡
❌ 설치 시 위험 (데이터 손실 가능)
```

**가상 머신:**
```
장점:
✅ 안전 (호스트 OS 영향 없음)
✅ 스냅샷 가능
✅ 동시 실행
✅ 쉬운 삭제/재설치

단점:
❌ 성능 저하
❌ 하드웨어 제한적 지원
❌ 리소스 분할
```

**추천:**
```bash
# 1단계: 가상 머신으로 시작 (2-4주)
VirtualBox 또는 VMware
→ 리눅스 익숙해지기

# 2단계: Live USB 사용 (1-2주)
→ 실제 하드웨어 테스트

# 3단계: 듀얼 부팅 또는 완전 전환
→ 본격적 사용
```

---

## 참고 자료

### 배포판 선택 도구
- [DistroWatch](https://distrowatch.com/) - 배포판 정보와 랭킹
- [DistroChooser](https://distrochooser.de/) - 대화형 배포판 추천

### 공식 사이트
- [Ubuntu](https://ubuntu.com/)
- [Fedora](https://getfedora.org/)
- [Debian](https://www.debian.org/)
- [Arch Linux](https://archlinux.org/)
- [Linux Mint](https://linuxmint.com/)

---

[다음: 유닉스/리눅스 철학 →](philosophy.md)

[← 이전: 유닉스의 역사](history.md)

[← 목차로 돌아가기](../README.md)
