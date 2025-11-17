# Vagrant 완전정복 가이드

## 목차
1. [Vagrant 소개](#vagrant-소개)
2. [설치 및 환경 설정](#설치-및-환경-설정)
3. [핵심 개념](#핵심-개념)
4. [기본 명령어](#기본-명령어)
5. [Vagrantfile 완전 분석](#vagrantfile-완전-분석)
6. [네트워킹 구성](#네트워킹-구성)
7. [프로비저닝](#프로비저닝)
8. [멀티 머신 환경](#멀티-머신-환경)
9. [플러그인 시스템](#플러그인-시스템)
10. [고급 설정](#고급-설정)
11. [트러블슈팅](#트러블슈팅)
12. [베스트 프랙티스](#베스트-프랙티스)
13. [실전 예제](#실전-예제)

---

## Vagrant 소개

### Vagrant란?
Vagrant는 가상 머신 환경을 코드로 관리할 수 있게 해주는 오픈소스 도구입니다. HashiCorp에서 개발하였으며, 개발 환경의 구축과 배포를 자동화하여 "내 컴퓨터에서는 되는데..."라는 문제를 해결합니다.

### 주요 특징
- **환경 일관성**: 모든 개발자가 동일한 환경에서 작업
- **간편한 설정**: 간단한 텍스트 파일(Vagrantfile)로 환경 정의
- **다양한 Provider 지원**: VirtualBox, VMware, Hyper-V, Docker 등
- **프로비저닝 지원**: Shell, Ansible, Chef, Puppet 등
- **포터블**: 환경 설정을 코드로 공유

### 사용 사례
- 로컬 개발 환경 구축
- CI/CD 파이프라인 테스트 환경
- 프로덕션 환경 미러링
- 멀티 OS 테스트 환경
- 마이크로서비스 개발 환경

---

## 설치 및 환경 설정

### 사전 요구사항
1. **가상화 소프트웨어 (Provider)**
   - VirtualBox (권장, 무료)
   - VMware Workstation/Fusion
   - Hyper-V (Windows Pro 이상)
   - Docker
   - Parallels Desktop (macOS)

### 설치 방법

#### Windows
```powershell
# Chocolatey 사용
choco install vagrant

# 또는 공식 웹사이트에서 다운로드
# https://www.vagrantup.com/downloads
```

#### macOS
```bash
# Homebrew 사용
brew install vagrant

# 또는 공식 웹사이트에서 다운로드
```

#### Linux (Ubuntu/Debian)
```bash
# 공식 저장소 추가
wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update && sudo apt install vagrant
```

#### Linux (RHEL/CentOS)
```bash
sudo yum install -y yum-utils
sudo yum-config-manager --add-repo https://rpm.releases.hashicorp.com/RHEL/hashicorp.repo
sudo yum -y install vagrant
```

### VirtualBox 설치 (권장 Provider)

#### Windows/macOS
공식 웹사이트에서 다운로드: https://www.virtualbox.org/

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install virtualbox
```

### 설치 확인
```bash
vagrant --version
# 출력 예: Vagrant 2.4.0

vboxmanage --version
# 출력 예: 7.0.12r159484
```

---

## 핵심 개념

### 1. Box
Box는 Vagrant가 사용하는 패키지 형식으로, 미리 구성된 가상 머신 이미지입니다.

**Box 검색**
```bash
# Vagrant Cloud에서 검색
vagrant box search ubuntu

# 웹 브라우저에서 검색
# https://app.vagrantup.com/boxes/search
```

**Box 추가**
```bash
# 공식 Ubuntu 20.04 Box
vagrant box add ubuntu/focal64

# 특정 버전 지정
vagrant box add ubuntu/focal64 --box-version 20230607.0.0

# 로컬 Box 파일 추가
vagrant box add mybox ./path/to/box.box
```

**Box 관리**
```bash
# 설치된 Box 목록
vagrant box list

# Box 업데이트
vagrant box update

# Box 제거
vagrant box remove ubuntu/focal64

# 오래된 버전 제거
vagrant box prune
```

### 2. Vagrantfile
프로젝트의 환경 설정을 정의하는 Ruby 기반 설정 파일입니다.

**기본 구조**
```ruby
Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/focal64"
end
```

### 3. Provider
가상 머신을 실제로 실행하는 백엔드 시스템입니다.

- **VirtualBox**: 기본 Provider, 크로스 플랫폼, 무료
- **VMware**: 고성능, 상용
- **Hyper-V**: Windows 네이티브
- **Docker**: 컨테이너 기반
- **AWS, Azure, GCP**: 클라우드 Provider

### 4. Provisioner
가상 머신을 자동으로 구성하는 도구입니다.

- Shell 스크립트
- Ansible
- Chef
- Puppet
- Docker
- Salt

### 5. Synced Folders
호스트와 게스트 간 파일 공유 메커니즘입니다.

---

## 기본 명령어

### 프로젝트 초기화
```bash
# 새 Vagrantfile 생성
vagrant init

# 특정 Box로 초기화
vagrant init ubuntu/focal64

# 최소 Vagrantfile 생성
vagrant init -m ubuntu/focal64
```

### VM 라이프사이클 관리

#### 시작 및 생성
```bash
# VM 시작 (처음이면 생성)
vagrant up

# 특정 Provider 지정
vagrant up --provider=virtualbox
vagrant up --provider=vmware_desktop

# 프로비저닝 없이 시작
vagrant up --no-provision

# 병렬 시작 (멀티 머신)
vagrant up --parallel
```

#### 연결
```bash
# SSH 접속
vagrant ssh

# 특정 VM에 접속 (멀티 머신)
vagrant ssh vm-name

# SSH 설정 확인
vagrant ssh-config

# SSH 키 출력
vagrant ssh-config > ssh-config
ssh -F ssh-config default
```

#### 중지 및 재시작
```bash
# VM 일시 정지 (메모리 상태 저장)
vagrant suspend

# 일시 정지된 VM 재개
vagrant resume

# VM 종료 (Graceful shutdown)
vagrant halt

# 강제 종료
vagrant halt --force

# VM 재시작
vagrant reload

# 설정 변경 후 재시작 + 프로비저닝
vagrant reload --provision
```

#### 삭제
```bash
# VM 완전 삭제
vagrant destroy

# 확인 없이 삭제
vagrant destroy -f

# 특정 VM만 삭제
vagrant destroy vm-name
```

### 상태 확인
```bash
# VM 상태 확인
vagrant status

# 모든 Vagrant VM 상태 (전역)
vagrant global-status

# 캐시된 전역 상태 정리
vagrant global-status --prune
```

### 프로비저닝
```bash
# 프로비저닝 실행
vagrant provision

# 특정 프로비저너만 실행
vagrant provision --provision-with shell,ansible
```

### 스냅샷 관리
```bash
# 스냅샷 생성
vagrant snapshot save snapshot-name

# 스냅샷 목록
vagrant snapshot list

# 스냅샷 복원
vagrant snapshot restore snapshot-name

# 스냅샷 삭제
vagrant snapshot delete snapshot-name

# 현재 상태로 스냅샷 푸시 (임시)
vagrant snapshot push

# 마지막 푸시된 스냅샷 복원
vagrant snapshot pop
```

### 플러그인 관리
```bash
# 플러그인 설치
vagrant plugin install vagrant-vbguest

# 플러그인 목록
vagrant plugin list

# 플러그인 업데이트
vagrant plugin update
vagrant plugin update vagrant-vbguest

# 플러그인 제거
vagrant plugin uninstall vagrant-vbguest
```

### 기타 유용한 명령어
```bash
# Vagrantfile 문법 검증
vagrant validate

# 포트 포워딩 정보
vagrant port

# SSH 명령어 실행
vagrant ssh -c "ls -la /vagrant"

# RDP 연결 (Windows VM)
vagrant rdp

# WinRM 실행 (Windows VM)
vagrant winrm -c "ipconfig"
```

---

## Vagrantfile 완전 분석

### 기본 구조
```ruby
# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrant API 버전 (2가 최신)
Vagrant.configure("2") do |config|
  # 설정 내용
end
```

### VM 기본 설정

#### Box 설정
```ruby
Vagrant.configure("2") do |config|
  # Box 이름
  config.vm.box = "ubuntu/focal64"

  # Box 버전
  config.vm.box_version = ">= 20230607.0.0"

  # Box URL (사설 Box)
  config.vm.box_url = "https://example.com/boxes/mybox.box"

  # Box 다운로드 체크섬
  config.vm.box_download_checksum = "abc123..."
  config.vm.box_download_checksum_type = "sha256"

  # Box 업데이트 확인 비활성화
  config.vm.box_check_update = false
end
```

#### 호스트명 설정
```ruby
config.vm.hostname = "myapp-dev"
```

#### Provider 특정 설정

**VirtualBox**
```ruby
config.vm.provider "virtualbox" do |vb|
  # VM 이름
  vb.name = "my-project-vm"

  # GUI 모드 활성화
  vb.gui = true

  # 메모리 (MB)
  vb.memory = "2048"

  # CPU 코어 수
  vb.cpus = 2

  # 비디오 메모리 (MB)
  vb.customize ["modifyvm", :id, "--vram", "128"]

  # 클립보드 공유
  vb.customize ["modifyvm", :id, "--clipboard", "bidirectional"]

  # 드래그 앤 드롭
  vb.customize ["modifyvm", :id, "--draganddrop", "bidirectional"]

  # 네트워크 성능 향상
  vb.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
  vb.customize ["modifyvm", :id, "--natdnsproxy1", "on"]

  # 디스크 I/O 캐시
  vb.customize ["storagectl", :id, "--name", "SATA Controller", "--hostiocache", "on"]

  # USB 지원
  vb.customize ["modifyvm", :id, "--usb", "on"]
  vb.customize ["modifyvm", :id, "--usbehci", "on"]

  # 링크된 클론 사용 (빠른 생성)
  vb.linked_clone = true
end
```

**VMware**
```ruby
config.vm.provider "vmware_desktop" do |vmware|
  vmware.vmx["memsize"] = "2048"
  vmware.vmx["numvcpus"] = "2"
  vmware.gui = true
end
```

**Hyper-V**
```ruby
config.vm.provider "hyperv" do |h|
  h.memory = 2048
  h.cpus = 2
  h.enable_virtualization_extensions = true
  h.linked_clone = true
end
```

**Docker**
```ruby
config.vm.provider "docker" do |d|
  d.image = "ubuntu:20.04"
  d.has_ssh = true
  d.remains_running = true
end
```

---

## 네트워킹 구성

### 1. 포트 포워딩 (Forwarded Port)
호스트의 포트를 게스트 포트로 매핑합니다.

```ruby
config.vm.network "forwarded_port", guest: 80, host: 8080

# 여러 포트 포워딩
config.vm.network "forwarded_port", guest: 80, host: 8080
config.vm.network "forwarded_port", guest: 443, host: 8443
config.vm.network "forwarded_port", guest: 3000, host: 3000

# 프로토콜 지정
config.vm.network "forwarded_port", guest: 53, host: 5353, protocol: "udp"

# 자동 수정 비활성화 (포트 충돌 시)
config.vm.network "forwarded_port", guest: 80, host: 8080, auto_correct: false

# 특정 IP만 접근 허용
config.vm.network "forwarded_port", guest: 80, host: 8080, host_ip: "127.0.0.1"

# ID 지정 (삭제/수정 용이)
config.vm.network "forwarded_port", guest: 80, host: 8080, id: "web"
```

### 2. 프라이빗 네트워크 (Private Network)
호스트-게스트 간 또는 게스트-게스트 간 통신을 위한 내부 네트워크입니다.

```ruby
# DHCP 사용
config.vm.network "private_network", type: "dhcp"

# 고정 IP
config.vm.network "private_network", ip: "192.168.50.4"

# 서브넷 마스크 지정
config.vm.network "private_network", ip: "192.168.50.4", netmask: "255.255.255.0"

# 네트워크 이름 지정 (VirtualBox)
config.vm.network "private_network", ip: "192.168.50.4", virtualbox__intnet: "mynetwork"

# IPv6
config.vm.network "private_network", ip: "fde4:8dba:82e1::c4"
```

### 3. 퍼블릭 네트워크 (Public Network)
브리지 모드로 외부 네트워크에 직접 연결합니다.

```ruby
# DHCP 사용
config.vm.network "public_network"

# 고정 IP
config.vm.network "public_network", ip: "192.168.1.100"

# 브리지 어댑터 지정
config.vm.network "public_network", bridge: "en0: Wi-Fi (AirPort)"

# 자동 설정
config.vm.network "public_network", auto_config: false
```

### 네트워킹 고급 설정

```ruby
# MAC 주소 지정
config.vm.network "private_network", ip: "192.168.50.4", mac: "5CA1AB1E0001"

# 멀티 어댑터
config.vm.network "private_network", ip: "192.168.50.4"
config.vm.network "private_network", ip: "192.168.51.4"

# 어댑터 타입 (VirtualBox)
config.vm.network "private_network", ip: "192.168.50.4",
  virtualbox__adapter_type: "82545EM"
```

---

## 프로비저닝

프로비저닝은 VM을 자동으로 구성하는 프로세스입니다.

### 1. Shell 프로비저닝

#### 인라인 스크립트
```ruby
config.vm.provision "shell", inline: <<-SHELL
  apt-get update
  apt-get install -y apache2
  systemctl start apache2
  systemctl enable apache2
SHELL
```

#### 외부 스크립트 파일
```ruby
config.vm.provision "shell", path: "scripts/setup.sh"

# 인자 전달
config.vm.provision "shell", path: "scripts/setup.sh", args: ["arg1", "arg2"]

# URL에서 다운로드
config.vm.provision "shell", path: "https://example.com/setup.sh"
```

#### 권한 및 실행 옵션
```ruby
# 일반 사용자로 실행 (기본은 root)
config.vm.provision "shell", inline: "echo Hello", privileged: false

# 재시작 후 실행
config.vm.provision "shell", inline: "echo Hello", run: "always"

# 프로비저닝 이름
config.vm.provision "shell", name: "Install Apache", inline: <<-SHELL
  apt-get install -y apache2
SHELL

# 환경 변수 설정
config.vm.provision "shell", inline: "echo $MESSAGE", env: {"MESSAGE" => "Hello World"}

# 재부팅
config.vm.provision "shell", inline: "echo Rebooting", reboot: true
```

#### 실전 예제: LAMP 스택 설치
```ruby
$script = <<-SCRIPT
#!/bin/bash

# 시스템 업데이트
apt-get update
apt-get upgrade -y

# Apache 설치
apt-get install -y apache2

# MySQL 설치
debconf-set-selections <<< 'mysql-server mysql-server/root_password password root'
debconf-set-selections <<< 'mysql-server mysql-server/root_password_again password root'
apt-get install -y mysql-server

# PHP 설치
apt-get install -y php libapache2-mod-php php-mysql

# Apache 재시작
systemctl restart apache2

# 방화벽 설정
ufw allow 80/tcp
ufw allow 443/tcp

echo "LAMP stack installed successfully!"
SCRIPT

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/focal64"
  config.vm.network "forwarded_port", guest: 80, host: 8080
  config.vm.provision "shell", inline: $script
end
```

### 2. Ansible 프로비저닝

```ruby
config.vm.provision "ansible" do |ansible|
  # Playbook 지정
  ansible.playbook = "playbooks/site.yml"

  # 인벤토리 파일
  ansible.inventory_path = "inventory/hosts"

  # 그룹 지정
  ansible.groups = {
    "webservers" => ["web1", "web2"],
    "dbservers" => ["db1"],
    "all_groups:children" => ["webservers", "dbservers"]
  }

  # 변수 전달
  ansible.extra_vars = {
    nginx_port: 8080,
    db_name: "myapp"
  }

  # Verbose 출력
  ansible.verbose = "v"

  # 제한 (limit)
  ansible.limit = "webservers"

  # 태그
  ansible.tags = ["install", "configure"]

  # Raw arguments
  ansible.raw_arguments = ["--check"]
end
```

#### Ansible Local (게스트에서 실행)
```ruby
config.vm.provision "ansible_local" do |ansible|
  ansible.playbook = "playbook.yml"
  ansible.install = true
  ansible.install_mode = "pip"
  ansible.version = "2.9.0"
end
```

### 3. Docker 프로비저닝

```ruby
# Docker 설치
config.vm.provision "docker"

# 이미지 pull
config.vm.provision "docker" do |d|
  d.pull_images "ubuntu"
  d.pull_images "nginx"
  d.pull_images "postgres:13"
end

# 컨테이너 실행
config.vm.provision "docker" do |d|
  d.run "nginx",
    image: "nginx",
    args: "-p 80:80 -v /vagrant/html:/usr/share/nginx/html"

  d.run "app",
    image: "myapp:latest",
    args: "-p 3000:3000",
    daemonize: true
end

# Docker Compose
config.vm.provision "docker_compose" do |dc|
  dc.yml = "/vagrant/docker-compose.yml"
  dc.compose_version = "1.29.2"
  dc.run = "always"
end
```

### 4. Chef 프로비저닝

```ruby
config.vm.provision "chef_solo" do |chef|
  chef.cookbooks_path = "cookbooks"
  chef.roles_path = "roles"
  chef.data_bags_path = "data_bags"

  chef.add_recipe "apache"
  chef.add_recipe "mysql::server"

  chef.add_role "web"

  chef.json = {
    mysql: {
      server_root_password: "rootpass"
    }
  }
end
```

### 5. Puppet 프로비저닝

```ruby
config.vm.provision "puppet" do |puppet|
  puppet.manifests_path = "manifests"
  puppet.manifest_file = "site.pp"
  puppet.module_path = "modules"

  puppet.options = "--verbose --debug"
end
```

### 6. File 프로비저닝

```ruby
# 파일 복사
config.vm.provision "file", source: "~/myapp/config.yml", destination: "/home/vagrant/config.yml"

# 디렉토리 복사
config.vm.provision "file", source: "~/myapp/data", destination: "/home/vagrant/data"
```

### 프로비저닝 실행 제어

```ruby
# 최초 vagrant up 시에만 실행 (기본값)
config.vm.provision "shell", inline: "echo once", run: "once"

# 항상 실행
config.vm.provision "shell", inline: "echo always", run: "always"

# 명시적으로 실행되지 않음
config.vm.provision "shell", inline: "echo never", run: "never"

# 조건부 프로비저닝
if ENV['RAILS_ENV'] == 'production'
  config.vm.provision "shell", inline: "echo production"
end
```

---

## 멀티 머신 환경

하나의 Vagrantfile에서 여러 VM을 정의하고 관리할 수 있습니다.

### 기본 멀티 머신 구성

```ruby
Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/focal64"

  # 웹 서버
  config.vm.define "web" do |web|
    web.vm.hostname = "web-server"
    web.vm.network "private_network", ip: "192.168.50.10"
    web.vm.provider "virtualbox" do |vb|
      vb.memory = "1024"
    end
    web.vm.provision "shell", inline: <<-SHELL
      apt-get update
      apt-get install -y nginx
    SHELL
  end

  # 데이터베이스 서버
  config.vm.define "db" do |db|
    db.vm.hostname = "db-server"
    db.vm.network "private_network", ip: "192.168.50.11"
    db.vm.provider "virtualbox" do |vb|
      vb.memory = "2048"
    end
    db.vm.provision "shell", inline: <<-SHELL
      apt-get update
      apt-get install -y mysql-server
    SHELL
  end
end
```

### 멀티 머신 명령어

```bash
# 모든 VM 시작
vagrant up

# 특정 VM만 시작
vagrant up web
vagrant up db

# 특정 VM SSH 접속
vagrant ssh web
vagrant ssh db

# 특정 VM 재시작
vagrant reload web

# 특정 VM 삭제
vagrant destroy db
```

### 루프를 이용한 멀티 머신 생성

```ruby
Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/focal64"

  # 웹 서버 3대
  (1..3).each do |i|
    config.vm.define "web#{i}" do |node|
      node.vm.hostname = "web#{i}"
      node.vm.network "private_network", ip: "192.168.50.#{10+i}"
      node.vm.provider "virtualbox" do |vb|
        vb.memory = "1024"
        vb.cpus = 1
      end
    end
  end
end
```

### 복잡한 멀티 머신 예제: 마이크로서비스 환경

```ruby
Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/focal64"

  # 공통 설정
  config.vm.provider "virtualbox" do |vb|
    vb.linked_clone = true
  end

  # 서버 정의
  servers = {
    "loadbalancer" => { ip: "192.168.50.10", memory: 512, cpus: 1 },
    "web1" => { ip: "192.168.50.11", memory: 1024, cpus: 2 },
    "web2" => { ip: "192.168.50.12", memory: 1024, cpus: 2 },
    "api1" => { ip: "192.168.50.21", memory: 1024, cpus: 2 },
    "api2" => { ip: "192.168.50.22", memory: 1024, cpus: 2 },
    "db-master" => { ip: "192.168.50.30", memory: 2048, cpus: 2 },
    "db-slave" => { ip: "192.168.50.31", memory: 2048, cpus: 2 },
    "cache" => { ip: "192.168.50.40", memory: 1024, cpus: 1 },
    "queue" => { ip: "192.168.50.41", memory: 1024, cpus: 1 }
  }

  servers.each do |name, conf|
    config.vm.define name do |node|
      node.vm.hostname = name
      node.vm.network "private_network", ip: conf[:ip]

      node.vm.provider "virtualbox" do |vb|
        vb.name = "myapp-#{name}"
        vb.memory = conf[:memory]
        vb.cpus = conf[:cpus]
      end

      # 역할별 프로비저닝
      case name
      when "loadbalancer"
        node.vm.provision "shell", path: "scripts/setup-nginx-lb.sh"
      when /^web/
        node.vm.provision "shell", path: "scripts/setup-web.sh"
      when /^api/
        node.vm.provision "shell", path: "scripts/setup-api.sh"
      when "db-master", "db-slave"
        node.vm.provision "shell", path: "scripts/setup-mysql.sh"
      when "cache"
        node.vm.provision "shell", path: "scripts/setup-redis.sh"
      when "queue"
        node.vm.provision "shell", path: "scripts/setup-rabbitmq.sh"
      end
    end
  end

  # 마지막 VM에서만 전체 설정 완료
  config.vm.define "queue", primary: true do |node|
    node.vm.provision "shell", inline: <<-SHELL
      echo "All servers are up and running!"
    SHELL
  end
end
```

### Primary VM 설정

```ruby
# web을 기본 VM으로 설정
config.vm.define "web", primary: true do |web|
  # 설정...
end

# vagrant ssh 시 primary VM에 자동 접속
# vagrant up 시 primary VM 먼저 시작
```

### Autostart 제어

```ruby
# 자동 시작 비활성화
config.vm.define "db", autostart: false do |db|
  # 이 VM은 vagrant up으로 자동 시작되지 않음
  # vagrant up db로 명시적으로 시작해야 함
end
```

---

## 플러그인 시스템

Vagrant의 기능을 확장하는 플러그인을 사용할 수 있습니다.

### 유용한 플러그인

#### 1. vagrant-vbguest
VirtualBox Guest Additions를 자동으로 업데이트합니다.

```bash
# 설치
vagrant plugin install vagrant-vbguest

# 비활성화 (Vagrantfile)
config.vbguest.auto_update = false
```

#### 2. vagrant-hostmanager
호스트와 게스트의 hosts 파일을 자동 관리합니다.

```bash
vagrant plugin install vagrant-hostmanager
```

```ruby
config.hostmanager.enabled = true
config.hostmanager.manage_host = true
config.hostmanager.manage_guest = true
config.hostmanager.ignore_private_ip = false

config.vm.define "web" do |web|
  web.vm.hostname = "web.example.com"
  web.vm.network "private_network", ip: "192.168.50.10"
  web.hostmanager.aliases = %w(www.example.com)
end
```

#### 3. vagrant-cachier
패키지 다운로드를 캐시하여 프로비저닝 속도 향상합니다.

```bash
vagrant plugin install vagrant-cachier
```

```ruby
if Vagrant.has_plugin?("vagrant-cachier")
  config.cache.scope = :box
  # 또는 :machine (머신별 캐시)
end
```

#### 4. vagrant-disksize
디스크 크기를 조정합니다.

```bash
vagrant plugin install vagrant-disksize
```

```ruby
config.disksize.size = '50GB'
```

#### 5. vagrant-env
.env 파일에서 환경 변수를 로드합니다.

```bash
vagrant plugin install vagrant-env
```

```ruby
config.env.enable
```

#### 6. vagrant-reload
프로비저닝 중 VM 재부팅을 허용합니다.

```bash
vagrant plugin install vagrant-reload
```

```ruby
config.vm.provision :shell, inline: "echo Install kernel updates"
config.vm.provision :reload
config.vm.provision :shell, inline: "echo Continue provisioning"
```

#### 7. vagrant-aws
AWS EC2에서 Vagrant를 사용합니다.

```bash
vagrant plugin install vagrant-aws
```

```ruby
config.vm.provider :aws do |aws, override|
  aws.access_key_id = ENV['AWS_ACCESS_KEY']
  aws.secret_access_key = ENV['AWS_SECRET_KEY']
  aws.keypair_name = "mykeypair"

  aws.ami = "ami-12345678"
  aws.instance_type = "t2.micro"
  aws.region = "us-east-1"

  override.ssh.username = "ubuntu"
  override.ssh.private_key_path = "~/.ssh/mykey.pem"
end
```

#### 8. vagrant-docker-compose
Docker Compose를 쉽게 사용합니다.

```bash
vagrant plugin install vagrant-docker-compose
```

### 플러그인 의존성 자동 설치

```ruby
# Vagrantfile에서 플러그인 자동 설치
required_plugins = %w(vagrant-vbguest vagrant-hostmanager)
plugins_to_install = required_plugins.select { |plugin| not Vagrant.has_plugin? plugin }

if not plugins_to_install.empty?
  puts "Installing plugins: #{plugins_to_install.join(' ')}"
  if system "vagrant plugin install #{plugins_to_install.join(' ')}"
    exec "vagrant #{ARGV.join(' ')}"
  else
    abort "Installation of one or more plugins has failed. Aborting."
  end
end
```

---

## 고급 설정

### Synced Folders (공유 폴더)

#### 기본 Synced Folder
```ruby
# 기본 공유 (/vagrant)
# 프로젝트 디렉토리가 자동으로 /vagrant에 마운트됨

# 추가 공유 폴더
config.vm.synced_folder "src/", "/srv/website"

# 호스트 절대 경로
config.vm.synced_folder "/Users/john/data", "/guest/data"

# 옵션
config.vm.synced_folder ".", "/vagrant",
  owner: "www-data",
  group: "www-data",
  mount_options: ["dmode=775", "fmode=664"]
```

#### Synced Folder 타입

**NFS (성능 향상, macOS/Linux)**
```ruby
config.vm.synced_folder ".", "/vagrant",
  type: "nfs",
  nfs_udp: false,
  nfs_version: 4

# NFS 설정 (macOS/Linux 호스트)
config.vm.network "private_network", ip: "192.168.50.4"
```

**SMB (Windows)**
```ruby
config.vm.synced_folder ".", "/vagrant",
  type: "smb",
  smb_username: ENV['USERNAME'],
  smb_password: ENV['PASSWORD']
```

**RSync**
```ruby
config.vm.synced_folder ".", "/vagrant",
  type: "rsync",
  rsync__exclude: [".git/", "node_modules/"],
  rsync__args: ["--verbose", "--archive", "--delete", "-z"],
  rsync__auto: true

# rsync 자동 동기화 (별도 터미널)
# vagrant rsync-auto
```

**VirtualBox Shared Folders**
```ruby
config.vm.synced_folder ".", "/vagrant",
  type: "virtualbox",
  SharedFoldersEnableSymlinksCreate: false
```

#### Synced Folder 비활성화
```ruby
# 기본 /vagrant 공유 비활성화
config.vm.synced_folder ".", "/vagrant", disabled: true
```

### SSH 설정

```ruby
# SSH 설정
config.ssh.username = "vagrant"
config.ssh.password = "vagrant"
config.ssh.host = "127.0.0.1"
config.ssh.port = 2222

# SSH 키 경로
config.ssh.private_key_path = ["~/.ssh/id_rsa", "~/.vagrant.d/insecure_private_key"]

# SSH 포워드 에이전트
config.ssh.forward_agent = true

# X11 포워딩
config.ssh.forward_x11 = true

# Keep alive
config.ssh.keep_alive = true

# Shell
config.ssh.shell = "bash -l"

# 연결 타임아웃
config.ssh.connect_timeout = 30

# 추가 옵션
config.ssh.extra_args = ["-Y"]

# Compression
config.ssh.compression = true
```

### 디스크 추가 (VirtualBox)

```ruby
config.vm.provider "virtualbox" do |vb|
  # 두 번째 디스크 추가 (10GB)
  disk = './secondDisk.vdi'
  unless File.exist?(disk)
    vb.customize ['createhd', '--filename', disk, '--size', 10 * 1024]
  end
  vb.customize ['storageattach', :id,
                '--storagectl', 'SATA Controller',
                '--port', 1,
                '--device', 0,
                '--type', 'hdd',
                '--medium', disk]
end
```

### 환경 변수 사용

```ruby
# 환경 변수 확인
if ENV['VAGRANT_ENV'] == 'production'
  config.vm.box = "ubuntu/focal64"
  config.vm.network "private_network", ip: "192.168.50.10"
else
  config.vm.box = "ubuntu/bionic64"
  config.vm.network "private_network", ip: "192.168.60.10"
end

# 환경 변수로 설정 전달
config.vm.provision "shell", env: {
  "DATABASE_URL" => ENV['DATABASE_URL'],
  "API_KEY" => ENV['API_KEY']
}, inline: <<-SHELL
  echo $DATABASE_URL > /etc/myapp/database_url
SHELL
```

### 외부 파일에서 설정 로드

```ruby
# YAML 설정 로드
require 'yaml'
settings = YAML.load_file 'config.yml'

Vagrant.configure("2") do |config|
  config.vm.box = settings['box']
  config.vm.network "private_network", ip: settings['ip']

  config.vm.provider "virtualbox" do |vb|
    vb.memory = settings['memory']
    vb.cpus = settings['cpus']
  end
end
```

**config.yml**
```yaml
box: ubuntu/focal64
ip: 192.168.50.10
memory: 2048
cpus: 2
```

### 트리거 (Triggers)

```ruby
# before/after 트리거
config.trigger.before :up do |trigger|
  trigger.name = "Before Up"
  trigger.info = "Starting VM setup..."
  trigger.run = {inline: "echo Starting..."}
end

config.trigger.after :up do |trigger|
  trigger.name = "After Up"
  trigger.info = "VM is ready!"
  trigger.run = {inline: "echo VM is ready at http://192.168.50.10"}
end

# 특정 VM에만 적용
config.vm.define "web" do |web|
  web.trigger.before :destroy do |trigger|
    trigger.warn = "You are about to destroy the web server!"
    trigger.run = {inline: "bash scripts/backup.sh"}
  end
end

# 호스트에서 명령 실행
config.trigger.after :up do |trigger|
  trigger.run = {inline: "open http://localhost:8080"}
end

# 게스트에서 명령 실행
config.trigger.after :provision do |trigger|
  trigger.run_remote = {inline: "systemctl restart nginx"}
end

# 조건부 트리거
config.trigger.before :halt do |trigger|
  trigger.ruby do |env, machine|
    puts "Halting #{machine.name}..."
  end
end
```

### WinRM (Windows VM)

```ruby
config.vm.box = "gusztavvargadr/windows-server"

config.vm.communicator = "winrm"
config.winrm.username = "vagrant"
config.winrm.password = "vagrant"

config.vm.provision "shell", inline: <<-SHELL
  # PowerShell 스크립트
  Write-Host "Installing IIS..."
  Install-WindowsFeature -name Web-Server -IncludeManagementTools
SHELL
```

---

## 트러블슈팅

### 일반적인 문제와 해결 방법

#### 1. "Vagrant was unable to mount VirtualBox shared folders"

**원인**: Guest Additions 버전 불일치

**해결 방법**:
```bash
# vagrant-vbguest 플러그인 설치
vagrant plugin install vagrant-vbguest

# VM 재시작
vagrant reload
```

또는 Vagrantfile에:
```ruby
config.vbguest.auto_update = true
```

#### 2. "The box you're attempting to add doesn't support the provider"

**원인**: Provider가 Box를 지원하지 않음

**해결 방법**:
```bash
# Provider 확인
vagrant box list

# 올바른 Provider Box 다운로드
vagrant box add ubuntu/focal64 --provider virtualbox
```

#### 3. "Port collision"

**원인**: 포트가 이미 사용 중

**해결 방법**:
```ruby
# 자동 수정 활성화
config.vm.network "forwarded_port", guest: 80, host: 8080, auto_correct: true

# 또는 다른 포트 사용
config.vm.network "forwarded_port", guest: 80, host: 8090
```

#### 4. "Authentication failure"

**원인**: SSH 키 문제

**해결 방법**:
```bash
# SSH 디버그 모드
vagrant ssh -- -v

# 또는 Vagrantfile에서
config.ssh.insert_key = false
```

#### 5. NFS 마운트 실패 (macOS/Linux)

**원인**: NFS 설정 문제

**해결 방법**:
```bash
# macOS
sudo nano /etc/exports
# 파일 확인 후 저장

# nfsd 재시작
sudo nfsd restart

# Linux
sudo apt-get install nfs-kernel-server
sudo systemctl restart nfs-kernel-server
```

#### 6. "VT-x is not available" 또는 "AMD-V is disabled"

**원인**: BIOS에서 가상화가 비활성화됨

**해결 방법**:
- BIOS/UEFI 설정에 들어가서 Intel VT-x 또는 AMD-V 활성화
- Hyper-V와 VirtualBox 충돌 (Windows)

```powershell
# Windows: Hyper-V 비활성화
bcdedit /set hypervisorlaunchtype off
# 재부팅 필요
```

#### 7. 느린 성능

**해결 방법**:
```ruby
# NFS 사용 (macOS/Linux)
config.vm.synced_folder ".", "/vagrant", type: "nfs"

# Linked clone 사용
config.vm.provider "virtualbox" do |vb|
  vb.linked_clone = true
end

# 메모리/CPU 증가
config.vm.provider "virtualbox" do |vb|
  vb.memory = "4096"
  vb.cpus = 4
end

# I/O APIC 활성화
config.vm.provider "virtualbox" do |vb|
  vb.customize ["modifyvm", :id, "--ioapic", "on"]
end
```

#### 8. "Kernel driver not installed"

**원인**: VirtualBox 커널 모듈 문제

**해결 방법**:
```bash
# macOS
sudo "/Library/Application Support/VirtualBox/LaunchDaemons/VirtualBoxStartup.sh" restart

# Linux
sudo modprobe vboxdrv
sudo systemctl restart vboxdrv
```

#### 9. Windows에서 심볼릭 링크 문제

**해결 방법**:
```ruby
config.vm.provider "virtualbox" do |vb|
  vb.customize ["setextradata", :id, "VBoxInternal2/SharedFoldersEnableSymlinksCreate/v-root", "1"]
end
```

관리자 권한으로 실행:
```powershell
fsutil behavior set SymlinkEvaluation L2L:1 R2R:1 L2R:1 R2L:1
```

### 디버깅

```bash
# Vagrant 디버그 로그
VAGRANT_LOG=debug vagrant up

# Provider별 디버그
VAGRANT_LOG=debug vagrant up --provider=virtualbox

# 특정 명령어 디버그
VAGRANT_LOG=info vagrant ssh
```

### 상태 복구

```bash
# Vagrant 상태 리셋
vagrant destroy -f
vagrant box update
vagrant up

# 전역 상태 정리
vagrant global-status --prune

# VirtualBox VM 수동 제거
vboxmanage list vms
vboxmanage unregistervm <vm-name> --delete
```

---

## 베스트 프랙티스

### 1. Vagrantfile 버전 관리

```ruby
# Git에 포함
# .gitignore
.vagrant/
*.box

# Vagrantfile은 Git에 커밋
```

### 2. 민감 정보 관리

```ruby
# 환경 변수 사용
config.vm.provision "shell", env: {
  "DB_PASSWORD" => ENV['DB_PASSWORD']
}

# .env 파일 사용 (vagrant-env)
# .gitignore에 .env 추가
```

### 3. 프로비저닝 멱등성

프로비저닝 스크립트는 여러 번 실행해도 같은 결과를 보장해야 합니다.

```bash
# 나쁜 예
echo "export PATH=\$PATH:/opt/bin" >> ~/.bashrc

# 좋은 예
if ! grep -q "/opt/bin" ~/.bashrc; then
  echo "export PATH=\$PATH:/opt/bin" >> ~/.bashrc
fi
```

### 4. 캐시 활용

```ruby
# vagrant-cachier 플러그인
if Vagrant.has_plugin?("vagrant-cachier")
  config.cache.scope = :box
end

# apt 캐시 유지
config.vm.provision "shell", inline: <<-SHELL
  apt-get update
  apt-get install -y --no-install-recommends package-name
SHELL
```

### 5. 리소스 최적화

```ruby
# Linked clone 사용
config.vm.provider "virtualbox" do |vb|
  vb.linked_clone = true
end

# 필요한 리소스만 할당
config.vm.provider "virtualbox" do |vb|
  vb.memory = "1024"
  vb.cpus = 2
end
```

### 6. 문서화

```ruby
# Vagrantfile에 주석 추가
Vagrant.configure("2") do |config|
  # Ubuntu 20.04 LTS 사용
  config.vm.box = "ubuntu/focal64"

  # 웹 서버 포트 포워딩 (호스트:8080 -> 게스트:80)
  config.vm.network "forwarded_port", guest: 80, host: 8080

  # LAMP 스택 설치
  config.vm.provision "shell", path: "scripts/install-lamp.sh"
end
```

**README.md** 작성:
```markdown
# 프로젝트명

## 개발 환경 설정

### 필요 사항
- Vagrant 2.3+
- VirtualBox 7.0+

### 시작하기
\`\`\`bash
vagrant up
vagrant ssh
\`\`\`

### 접속 정보
- 웹: http://localhost:8080
- MySQL: localhost:3306 (root/root)
```

### 7. 네이밍 컨벤션

```ruby
# 명확한 VM 이름
config.vm.define "myapp-web-server" do |web|
  web.vm.hostname = "web.myapp.local"
end

# Provider VM 이름
config.vm.provider "virtualbox" do |vb|
  vb.name = "myapp-web-#{Time.now.to_i}"
end
```

### 8. 스크립트 분리

```
project/
├── Vagrantfile
├── scripts/
│   ├── bootstrap.sh
│   ├── install-nginx.sh
│   ├── install-mysql.sh
│   └── configure-app.sh
├── ansible/
│   ├── playbook.yml
│   └── roles/
└── README.md
```

### 9. 조건부 설정

```ruby
# 개발/프로덕션 환경 분리
ENV['VAGRANT_ENV'] ||= 'development'

if ENV['VAGRANT_ENV'] == 'production'
  config.vm.provider "virtualbox" do |vb|
    vb.memory = "4096"
    vb.cpus = 4
  end
else
  config.vm.provider "virtualbox" do |vb|
    vb.memory = "2048"
    vb.cpus = 2
  end
end
```

### 10. 정기적인 유지보수

```bash
# Box 업데이트
vagrant box update

# 오래된 Box 버전 정리
vagrant box prune

# 플러그인 업데이트
vagrant plugin update

# 사용하지 않는 VM 정리
vagrant global-status --prune
```

---

## 실전 예제

### 예제 1: Node.js 개발 환경

**Vagrantfile**
```ruby
Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/focal64"
  config.vm.hostname = "nodejs-dev"

  config.vm.network "forwarded_port", guest: 3000, host: 3000
  config.vm.network "private_network", ip: "192.168.50.10"

  config.vm.provider "virtualbox" do |vb|
    vb.name = "nodejs-dev"
    vb.memory = "2048"
    vb.cpus = 2
    vb.linked_clone = true
  end

  config.vm.synced_folder ".", "/vagrant", type: "nfs"

  config.vm.provision "shell", inline: <<-SHELL
    # 시스템 업데이트
    apt-get update
    apt-get upgrade -y

    # Node.js 설치 (NodeSource)
    curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
    apt-get install -y nodejs

    # 개발 도구
    apt-get install -y build-essential git

    # 글로벌 패키지
    npm install -g pm2 nodemon

    # 프로젝트 의존성
    cd /vagrant
    if [ -f package.json ]; then
      npm install
    fi

    echo "Node.js $(node --version) installed"
    echo "npm $(npm --version) installed"
  SHELL
end
```

### 예제 2: Django 개발 환경

**Vagrantfile**
```ruby
Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/focal64"
  config.vm.hostname = "django-dev"

  config.vm.network "forwarded_port", guest: 8000, host: 8000
  config.vm.network "private_network", ip: "192.168.50.20"

  config.vm.provider "virtualbox" do |vb|
    vb.memory = "2048"
    vb.cpus = 2
  end

  config.vm.provision "shell", inline: <<-SHELL
    # Python 3 및 pip
    apt-get update
    apt-get install -y python3 python3-pip python3-venv

    # PostgreSQL
    apt-get install -y postgresql postgresql-contrib libpq-dev

    # PostgreSQL 설정
    sudo -u postgres psql -c "CREATE DATABASE djangodb;"
    sudo -u postgres psql -c "CREATE USER djangouser WITH PASSWORD 'django123';"
    sudo -u postgres psql -c "ALTER ROLE djangouser SET client_encoding TO 'utf8';"
    sudo -u postgres psql -c "ALTER ROLE djangouser SET default_transaction_isolation TO 'read committed';"
    sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE djangodb TO djangouser;"

    # 가상 환경 및 의존성
    cd /vagrant
    python3 -m venv venv
    source venv/bin/activate

    if [ -f requirements.txt ]; then
      pip install -r requirements.txt
    else
      pip install django psycopg2-binary
    fi
  SHELL

  # 항상 실행: Django 서버 시작
  config.vm.provision "shell", run: "always", inline: <<-SHELL
    cd /vagrant
    source venv/bin/activate
    python manage.py runserver 0.0.0.0:8000 &
  SHELL
end
```

### 예제 3: Docker 개발 환경

**Vagrantfile**
```ruby
Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/focal64"
  config.vm.hostname = "docker-dev"

  config.vm.network "private_network", ip: "192.168.50.30"

  config.vm.provider "virtualbox" do |vb|
    vb.memory = "4096"
    vb.cpus = 2
  end

  # Docker 설치
  config.vm.provision "docker"

  # Docker Compose 설치
  config.vm.provision "shell", inline: <<-SHELL
    curl -L "https://github.com/docker/compose/releases/download/v2.23.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose

    # vagrant 사용자를 docker 그룹에 추가
    usermod -aG docker vagrant
  SHELL

  # Docker Compose로 서비스 시작
  config.vm.provision "docker_compose",
    yml: "/vagrant/docker-compose.yml",
    run: "always"
end
```

**docker-compose.yml**
```yaml
version: '3.8'
services:
  web:
    image: nginx:latest
    ports:
      - "80:80"
    volumes:
      - ./html:/usr/share/nginx/html

  db:
    image: postgres:13
    environment:
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: myapp
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:
```

### 예제 4: Kubernetes 클러스터 (k3s)

**Vagrantfile**
```ruby
# -*- mode: ruby -*-
# vi: set ft=ruby :

MASTER_COUNT = 1
WORKER_COUNT = 2

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/focal64"

  config.vm.provider "virtualbox" do |vb|
    vb.linked_clone = true
  end

  # 마스터 노드
  (1..MASTER_COUNT).each do |i|
    config.vm.define "k8s-master-#{i}" do |master|
      master.vm.hostname = "k8s-master-#{i}"
      master.vm.network "private_network", ip: "192.168.50.#{10+i}"

      master.vm.provider "virtualbox" do |vb|
        vb.name = "k8s-master-#{i}"
        vb.memory = "2048"
        vb.cpus = 2
      end

      master.vm.provision "shell", path: "scripts/install-k3s-master.sh"
    end
  end

  # 워커 노드
  (1..WORKER_COUNT).each do |i|
    config.vm.define "k8s-worker-#{i}" do |worker|
      worker.vm.hostname = "k8s-worker-#{i}"
      worker.vm.network "private_network", ip: "192.168.50.#{20+i}"

      worker.vm.provider "virtualbox" do |vb|
        vb.name = "k8s-worker-#{i}"
        vb.memory = "1024"
        vb.cpus = 1
      end

      worker.vm.provision "shell", path: "scripts/install-k3s-worker.sh"
    end
  end
end
```

**scripts/install-k3s-master.sh**
```bash
#!/bin/bash

# k3s 마스터 설치
curl -sfL https://get.k3s.io | sh -s - --write-kubeconfig-mode 644

# 토큰 저장
sudo cat /var/lib/rancher/k3s/server/node-token > /vagrant/node-token

# kubeconfig 복사
mkdir -p /home/vagrant/.kube
sudo cp /etc/rancher/k3s/k3s.yaml /home/vagrant/.kube/config
sudo chown vagrant:vagrant /home/vagrant/.kube/config

echo "Master node ready!"
kubectl get nodes
```

**scripts/install-k3s-worker.sh**
```bash
#!/bin/bash

# 토큰 읽기
K3S_TOKEN=$(cat /vagrant/node-token)
K3S_URL="https://192.168.50.11:6443"

# k3s 워커 설치
curl -sfL https://get.k3s.io | K3S_URL=$K3S_URL K3S_TOKEN=$K3S_TOKEN sh -

echo "Worker node joined!"
```

### 예제 5: WordPress 개발 환경 (Ansible 프로비저닝)

**Vagrantfile**
```ruby
Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/focal64"
  config.vm.hostname = "wordpress-dev"

  config.vm.network "forwarded_port", guest: 80, host: 8080
  config.vm.network "private_network", ip: "192.168.50.40"

  config.vm.provider "virtualbox" do |vb|
    vb.memory = "2048"
    vb.cpus = 2
  end

  config.vm.provision "ansible_local" do |ansible|
    ansible.playbook = "playbook.yml"
    ansible.verbose = true
    ansible.install = true
    ansible.install_mode = "pip"
  end
end
```

**playbook.yml**
```yaml
---
- hosts: all
  become: yes
  vars:
    mysql_root_password: root
    wordpress_db_name: wordpress
    wordpress_db_user: wpuser
    wordpress_db_password: wppass

  tasks:
    - name: Update apt cache
      apt:
        update_cache: yes
        cache_valid_time: 3600

    - name: Install LAMP stack
      apt:
        name:
          - apache2
          - mysql-server
          - php
          - php-mysql
          - php-curl
          - php-gd
          - php-mbstring
          - php-xml
          - php-xmlrpc
          - php-soap
          - php-intl
          - php-zip
          - python3-pymysql
        state: present

    - name: Start Apache
      service:
        name: apache2
        state: started
        enabled: yes

    - name: Start MySQL
      service:
        name: mysql
        state: started
        enabled: yes

    - name: Create WordPress database
      mysql_db:
        name: "{{ wordpress_db_name }}"
        state: present
        login_unix_socket: /var/run/mysqld/mysqld.sock

    - name: Create WordPress user
      mysql_user:
        name: "{{ wordpress_db_user }}"
        password: "{{ wordpress_db_password }}"
        priv: "{{ wordpress_db_name }}.*:ALL"
        state: present
        login_unix_socket: /var/run/mysqld/mysqld.sock

    - name: Download WordPress
      get_url:
        url: https://wordpress.org/latest.tar.gz
        dest: /tmp/wordpress.tar.gz

    - name: Extract WordPress
      unarchive:
        src: /tmp/wordpress.tar.gz
        dest: /var/www/html
        remote_src: yes
        creates: /var/www/html/wordpress

    - name: Set permissions
      file:
        path: /var/www/html/wordpress
        owner: www-data
        group: www-data
        recurse: yes

    - name: Configure wp-config.php
      template:
        src: wp-config.php.j2
        dest: /var/www/html/wordpress/wp-config.php
        owner: www-data
        group: www-data
```

**templates/wp-config.php.j2**
```php
<?php
define('DB_NAME', '{{ wordpress_db_name }}');
define('DB_USER', '{{ wordpress_db_user }}');
define('DB_PASSWORD', '{{ wordpress_db_password }}');
define('DB_HOST', 'localhost');
define('DB_CHARSET', 'utf8');
define('DB_COLLATE', '');

// Salt keys (production에서는 https://api.wordpress.org/secret-key/1.1/salt/ 사용)
define('AUTH_KEY',         'put your unique phrase here');
define('SECURE_AUTH_KEY',  'put your unique phrase here');
define('LOGGED_IN_KEY',    'put your unique phrase here');
define('NONCE_KEY',        'put your unique phrase here');
define('AUTH_SALT',        'put your unique phrase here');
define('SECURE_AUTH_SALT', 'put your unique phrase here');
define('LOGGED_IN_SALT',   'put your unique phrase here');
define('NONCE_SALT',       'put your unique phrase here');

$table_prefix = 'wp_';
define('WP_DEBUG', true);

if ( !defined('ABSPATH') )
    define('ABSPATH', dirname(__FILE__) . '/');

require_once(ABSPATH . 'wp-settings.php');
```

---

## 추가 리소스

### 공식 문서
- Vagrant 공식 사이트: https://www.vagrantup.com
- Vagrant 문서: https://developer.hashicorp.com/vagrant/docs
- Vagrant Cloud: https://app.vagrantup.com/boxes/search

### 커뮤니티
- GitHub: https://github.com/hashicorp/vagrant
- 토론 포럼: https://discuss.hashicorp.com/c/vagrant

### Box 찾기
- Vagrant Cloud: https://app.vagrantup.com/boxes/search
- Bento Boxes (Chef): https://app.vagrantup.com/bento
- Generic Boxes: https://app.vagrantup.com/generic

### 유용한 도구
- Packer: Box 이미지 생성 도구
- Vagrant Manager: GUI 관리 도구 (macOS/Windows)

---

## 부록

### A. 자주 사용하는 명령어 치트시트

```bash
# 초기화 및 시작
vagrant init <box>          # Vagrantfile 생성
vagrant up                  # VM 시작/생성
vagrant ssh                 # SSH 접속
vagrant halt                # VM 종료
vagrant reload              # VM 재시작
vagrant destroy             # VM 삭제

# 상태
vagrant status              # VM 상태
vagrant global-status       # 모든 VM 상태

# Box 관리
vagrant box add <name>      # Box 추가
vagrant box list            # Box 목록
vagrant box update          # Box 업데이트
vagrant box remove <name>   # Box 제거

# 프로비저닝
vagrant provision           # 프로비저닝 실행
vagrant reload --provision  # 재시작 + 프로비저닝

# 스냅샷
vagrant snapshot save <name>    # 스냅샷 저장
vagrant snapshot list           # 스냅샷 목록
vagrant snapshot restore <name> # 스냅샷 복원

# 플러그인
vagrant plugin install <name>   # 플러그인 설치
vagrant plugin list             # 플러그인 목록
```

### B. Vagrantfile 템플릿

**최소 구성**
```ruby
Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/focal64"
end
```

**표준 구성**
```ruby
Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/focal64"
  config.vm.network "private_network", ip: "192.168.50.4"

  config.vm.provider "virtualbox" do |vb|
    vb.memory = "2048"
    vb.cpus = 2
  end

  config.vm.provision "shell", inline: <<-SHELL
    apt-get update
    apt-get install -y nginx
  SHELL
end
```

### C. 환경별 설정 예제

**개발 환경**
```ruby
# 메모리: 적당히
# 프로비저닝: 빠르게 (Shell)
# 네트워크: Private
```

**스테이징 환경**
```ruby
# 메모리: 프로덕션과 유사
# 프로비저닝: Ansible/Chef
# 네트워크: Public (제한적)
```

**프로덕션 미러**
```ruby
# 메모리: 프로덕션과 동일
# 프로비저닝: 프로덕션 스크립트
# 네트워크: 격리된 네트워크
```

---

## 맺음말

이 가이드는 Vagrant의 기본부터 고급 기능까지 모든 것을 다루었습니다. Vagrant를 효과적으로 사용하면:

1. **개발 환경 일관성** - "내 컴퓨터에서는 되는데" 문제 해결
2. **빠른 온보딩** - 신규 팀원이 몇 분 만에 환경 구축
3. **실험 안전성** - 언제든 초기 상태로 복원 가능
4. **인프라 코드화** - 버전 관리 가능한 환경 설정

Vagrant를 마스터하여 더 효율적인 개발 워크플로우를 구축하세요!

---

**버전**: 1.0
**최종 업데이트**: 2025-11-17
**작성자**: Claude AI
**라이선스**: MIT
