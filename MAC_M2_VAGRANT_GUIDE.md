# Mac M2에서 VirtualBox와 Vagrant 실행 문제 해결 가이드

## 🚨 핵심 문제

**VirtualBox는 ARM 기반 프로세서(Apple Silicon M1/M2/M3)를 지원하지 않습니다.**

VirtualBox는 x86/x64 아키텍처 전용으로 설계되어 있으며, Apple Silicon의 ARM64 아키텍처와 호환되지 않습니다. 따라서 Mac M1/M2/M3에서는 근본적으로 실행이 불가능합니다.

## ✅ 해결 방법 (대안)

Mac M2 환경에서 Vagrant를 사용하려면 다른 가상화 제공자(provider)를 사용해야 합니다.

### 방법 1: VMware Desktop (추천 ⭐)

VMware는 Apple Silicon을 공식 지원합니다.

```bash
# VMware Fusion 13+ 설치 (무료 개인 라이선스 사용 가능)
# https://www.vmware.com/products/fusion.html 에서 다운로드

# Vagrant VMware 플러그인 설치
vagrant plugin install vagrant-vmware-desktop

# Vagrantfile에서 provider 지정
vagrant up --provider=vmware_desktop
```

**Vagrantfile 예시:**
```ruby
Vagrant.configure("2") do |config|
  config.vm.box = "bento/ubuntu-22.04-arm64"  # ARM64 박스 사용 필수

  config.vm.provider "vmware_desktop" do |v|
    v.memory = "2048"
    v.cpus = 2
  end
end
```

**장점:**
- ✅ Apple Silicon 네이티브 지원
- ✅ 우수한 성능
- ✅ 무료 개인 라이선스 제공
- ✅ Vagrant 플러그인 공식 지원

**주의사항:**
- ARM64 호환 박스(box)를 사용해야 합니다 (예: `bento/ubuntu-22.04-arm64`)

### 방법 2: Parallels Desktop

Parallels는 Mac에 최적화된 상용 가상화 솔루션입니다.

```bash
# Parallels Desktop 18+ 설치 (유료)
# https://www.parallels.com/products/desktop/ 에서 구매

# Vagrant Parallels 플러그인 설치
vagrant plugin install vagrant-parallels

# 실행
vagrant up --provider=parallels
```

**Vagrantfile 예시:**
```ruby
Vagrant.configure("2") do |config|
  config.vm.box = "bento/ubuntu-22.04-arm64"

  config.vm.provider "parallels" do |prl|
    prl.memory = "2048"
    prl.cpus = 2
  end
end
```

**장점:**
- ✅ Mac에 최적화된 성능
- ✅ ARM64 네이티브 지원
- ✅ 우수한 사용자 경험

**단점:**
- ❌ 유료 라이선스 필요

### 방법 3: QEMU (UTM 또는 직접 사용)

QEMU는 오픈소스 가상화 솔루션입니다.

#### UTM 사용 (GUI 인터페이스)
```bash
# Homebrew로 설치
brew install --cask utm

# Vagrant QEMU 플러그인
vagrant plugin install vagrant-qemu
```

#### libvirt 사용
```bash
# libvirt 설치
brew install libvirt

# Vagrant libvirt 플러그인
vagrant plugin install vagrant-libvirt

# 실행
vagrant up --provider=libvirt
```

**장점:**
- ✅ 완전 무료 오픈소스
- ✅ ARM64 지원

**단점:**
- ❌ 설정이 복잡함
- ❌ 성능이 상대적으로 낮음
- ❌ Vagrant 통합이 불완전할 수 있음

### 방법 4: Docker (가벼운 컨테이너 기반)

전체 VM이 필요 없다면 Docker가 가장 효율적입니다.

```bash
# Docker Desktop for Mac 설치 (Apple Silicon 지원)
brew install --cask docker

# Vagrant Docker provider는 기본 내장
vagrant up --provider=docker
```

**Vagrantfile 예시:**
```ruby
Vagrant.configure("2") do |config|
  config.vm.provider "docker" do |d|
    d.image = "ubuntu:22.04"
    d.has_ssh = true
  end
end
```

**장점:**
- ✅ 매우 빠른 실행 속도
- ✅ 낮은 리소스 사용
- ✅ Apple Silicon 네이티브 지원

**단점:**
- ❌ 전체 VM이 아닌 컨테이너 (커널 공유)
- ❌ 일부 시스템 레벨 기능 제한

### 방법 5: 클라우드 Provider (AWS, Azure, etc.)

로컬 VM이 필요 없다면 클라우드 환경 사용:

```bash
# AWS 예시
vagrant plugin install vagrant-aws

# Vagrantfile에서 클라우드 설정
```

## 📊 방법 비교표

| 방법 | 비용 | 성능 | 설정 난이도 | ARM64 지원 | 추천도 |
|------|------|------|------------|-----------|--------|
| **VMware Desktop** | 무료(개인) | ⭐⭐⭐⭐⭐ | 쉬움 | ✅ | ⭐⭐⭐⭐⭐ |
| **Parallels** | 유료 | ⭐⭐⭐⭐⭐ | 쉬움 | ✅ | ⭐⭐⭐⭐ |
| **QEMU/UTM** | 무료 | ⭐⭐⭐ | 어려움 | ✅ | ⭐⭐⭐ |
| **Docker** | 무료 | ⭐⭐⭐⭐⭐ | 쉬움 | ✅ | ⭐⭐⭐⭐⭐ |
| **클라우드** | 사용량 기반 | ⭐⭐⭐⭐ | 보통 | ✅ | ⭐⭐⭐ |

## 🎯 시나리오별 추천

### 1. 개발/테스트 환경 (일반적인 경우)
→ **VMware Desktop** 또는 **Docker** 사용

### 2. 완전한 VM 환경 필요 + 예산 있음
→ **Parallels Desktop** 사용

### 3. 완전 무료 솔루션 원함
→ **Docker** (가벼운 워크로드) 또는 **QEMU/UTM** (완전한 VM)

### 4. 마이크로서비스/컨테이너 기반 개발
→ **Docker** 사용

## 🔧 기존 VirtualBox Vagrantfile 마이그레이션

기존 VirtualBox용 Vagrantfile이 있다면:

**Before (VirtualBox):**
```ruby
Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/focal64"  # x86_64 박스

  config.vm.provider "virtualbox" do |vb|
    vb.memory = "2048"
    vb.cpus = 2
  end
end
```

**After (VMware - Mac M2):**
```ruby
Vagrant.configure("2") do |config|
  config.vm.box = "bento/ubuntu-22.04-arm64"  # ARM64 박스로 변경!

  config.vm.provider "vmware_desktop" do |v|
    v.memory = "2048"
    v.cpus = 2
  end

  # 또는 Docker provider 추가
  config.vm.provider "docker" do |d|
    d.image = "ubuntu:22.04"
    d.has_ssh = true
  end
end
```

## 📦 ARM64 호환 Vagrant Box 찾기

```bash
# Vagrant Cloud에서 ARM64 박스 검색
vagrant box search ubuntu arm64

# 인기 ARM64 박스
- bento/ubuntu-22.04-arm64
- bento/ubuntu-20.04-arm64
- starboard/ubuntu-arm64-20.04
```

## ❌ 피해야 할 해결 방법

1. **Rosetta를 통한 VirtualBox 실행 시도**
   - 불가능합니다. VirtualBox는 커널 확장이 필요하며 Rosetta는 이를 변환할 수 없습니다.

2. **x86 에뮬레이션으로 VirtualBox 실행**
   - 커널 레벨 드라이버를 에뮬레이션할 수 없으므로 작동하지 않습니다.

3. **구버전 VirtualBox 설치 시도**
   - 어떤 버전의 VirtualBox도 Apple Silicon을 지원하지 않습니다.

## 🔍 현재 시스템 확인

Mac이 M1/M2/M3인지 확인:

```bash
# CPU 아키텍처 확인
uname -m
# 출력: arm64 → Apple Silicon (M1/M2/M3)
# 출력: x86_64 → Intel Mac (VirtualBox 사용 가능)

# 상세 정보
sysctl -n machdep.cpu.brand_string
```

## 💡 빠른 시작 가이드

**Docker를 사용한 가장 빠른 해결 방법:**

```bash
# 1. Docker Desktop 설치
brew install --cask docker

# 2. 간단한 Vagrantfile 생성
cat > Vagrantfile <<EOF
Vagrant.configure("2") do |config|
  config.vm.provider "docker" do |d|
    d.image = "ubuntu:22.04"
    d.has_ssh = true
  end

  config.vm.provision "shell", inline: <<-SHELL
    apt-get update
    apt-get install -y build-essential
  SHELL
end
EOF

# 3. 실행
vagrant up --provider=docker

# 4. SSH 접속
vagrant ssh
```

## 🆘 추가 도움말

### Vagrant 박스 목록 관리
```bash
# 설치된 박스 확인
vagrant box list

# 기존 x86 박스 제거
vagrant box remove ubuntu/focal64

# ARM64 박스 추가
vagrant box add bento/ubuntu-22.04-arm64
```

### Provider 기본값 설정
```bash
# 환경 변수로 기본 provider 설정
export VAGRANT_DEFAULT_PROVIDER=vmware_desktop

# 또는 ~/.zshrc나 ~/.bashrc에 추가
echo 'export VAGRANT_DEFAULT_PROVIDER=vmware_desktop' >> ~/.zshrc
```

## 📚 참고 자료

- [VMware Fusion for Mac](https://www.vmware.com/products/fusion.html)
- [Parallels Desktop](https://www.parallels.com/products/desktop/)
- [Vagrant VMware Plugin](https://www.vagrantup.com/docs/providers/vmware)
- [Vagrant Parallels Plugin](https://parallels.github.io/vagrant-parallels/)
- [Docker Desktop for Mac](https://docs.docker.com/desktop/mac/install/)
- [UTM for Mac](https://mac.getutm.app/)

## 📌 요약

Mac M2에서는:
- ❌ **VirtualBox 사용 불가능** (ARM 미지원)
- ✅ **VMware Desktop 사용** (무료, 추천)
- ✅ **Docker 사용** (가볍고 빠름, 추천)
- ✅ **Parallels 사용** (유료이지만 훌륭함)
- ✅ **QEMU/UTM 사용** (무료 오픈소스)

대부분의 경우 **VMware Desktop (개인 무료)** 또는 **Docker**로 전환하는 것이 가장 좋은 해결책입니다.
