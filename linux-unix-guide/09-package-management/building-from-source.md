# 소스에서 빌드하기

## 목차
- [소개](#소개)
- [빌드 준비](#빌드-준비)
- [GNU Build System (Autotools)](#gnu-build-system-autotools)
- [CMake](#cmake)
- [Make](#make)
- [언어별 빌드 시스템](#언어별-빌드-시스템)
- [의존성 관리](#의존성-관리)
- [설치 및 제거](#설치-및-제거)
- [최적화 및 설정](#최적화-및-설정)
- [문제 해결](#문제-해결)
- [패키징](#패키징)
- [실전 예제](#실전-예제)

---

## 소개

소스 코드에서 직접 소프트웨어를 빌드하면 최신 버전 사용, 커스터마이징, 시스템 최적화 등의 장점이 있습니다.

### 소스 빌드가 필요한 경우

```bash
# 1. 최신 버전이 필요할 때
# 배포판 저장소에 없는 최신 기능 사용

# 2. 커스텀 설정이 필요할 때
# 특정 기능 활성화/비활성화

# 3. 최적화가 필요할 때
# CPU 최적화, 불필요한 기능 제거

# 4. 패치 적용이 필요할 때
# 버그 수정, 보안 패치 등

# 5. 학습 목적
# 소프트웨어 내부 구조 이해
```

### 빌드 프로세스 개요

```bash
# 일반적인 빌드 과정:

# 1. 소스 다운로드
wget https://example.com/software-1.0.tar.gz
tar xzf software-1.0.tar.gz
cd software-1.0

# 2. 설정 (configure)
./configure --prefix=/usr/local

# 3. 컴파일 (make)
make

# 4. 테스트 (선택사항)
make test

# 5. 설치 (install)
sudo make install

# 6. 정리
make clean
```

---

## 빌드 준비

### 필수 도구 설치

```bash
# Debian/Ubuntu
$ sudo apt update
$ sudo apt install build-essential
$ sudo apt install gcc g++ make autoconf automake libtool
$ sudo apt install pkg-config
$ sudo apt install git wget curl

# Red Hat/Fedora/CentOS
$ sudo dnf groupinstall "Development Tools"
$ sudo dnf install gcc gcc-c++ make autoconf automake libtool
$ sudo dnf install pkgconfig
$ sudo dnf install git wget curl

# Arch Linux
$ sudo pacman -S base-devel
$ sudo pacman -S gcc make autoconf automake libtool
$ sudo pacman -S pkgconf
$ sudo pacman -S git wget curl

# 도구 버전 확인
$ gcc --version
gcc (GCC) 13.2.1 20230801

$ make --version
GNU Make 4.4.1

$ autoconf --version
autoconf (GNU Autoconf) 2.71
```

### 빌드 환경 설정

```bash
# 빌드 디렉토리 생성
$ mkdir -p ~/build
$ mkdir -p ~/src
$ mkdir -p /usr/local/src  # 시스템 전체용 (root)

# 환경 변수 설정
$ export BUILD_DIR=~/build
$ export SRC_DIR=~/src
$ export PREFIX=/usr/local

# .bashrc에 추가
$ vi ~/.bashrc
export BUILD_DIR=~/build
export SRC_DIR=~/src
export PREFIX=/usr/local
export PATH=$PREFIX/bin:$PATH
export LD_LIBRARY_PATH=$PREFIX/lib:$LD_LIBRARY_PATH
export PKG_CONFIG_PATH=$PREFIX/lib/pkgconfig:$PKG_CONFIG_PATH

# 적용
$ source ~/.bashrc

# 빌드 로그 디렉토리
$ mkdir -p ~/build-logs
```

### 소스 코드 다운로드

```bash
# tarball 다운로드
$ wget https://example.com/software-1.0.tar.gz
$ wget https://example.com/software-1.0.tar.gz.asc  # GPG 서명

# 체크섬 확인
$ sha256sum software-1.0.tar.gz
$ md5sum software-1.0.tar.gz

# GPG 서명 확인
$ gpg --verify software-1.0.tar.gz.asc software-1.0.tar.gz

# 압축 해제
$ tar xzf software-1.0.tar.gz  # .tar.gz
$ tar xjf software-1.0.tar.bz2  # .tar.bz2
$ tar xJf software-1.0.tar.xz  # .tar.xz

# Git 저장소에서
$ git clone https://github.com/user/repo.git
$ cd repo
$ git checkout v1.0  # 특정 버전
$ git submodule update --init --recursive  # 서브모듈 포함

# 단일 브랜치만
$ git clone --depth=1 --branch=v1.0 https://github.com/user/repo.git

# 소스 트리 확인
$ ls -la
configure  configure.ac  Makefile.am  src/  README  INSTALL
```

---

## GNU Build System (Autotools)

### configure 스크립트

```bash
# configure 도움말
$ ./configure --help
`configure' configures software 1.0 to adapt to many kinds of systems.

Usage: ./configure [OPTION]... [VAR=VALUE]...

Optional Features:
  --disable-option-checking  ignore unrecognized --enable/--with options
  --enable-shared[=PKGS]     build shared libraries
  --enable-static[=PKGS]     build static libraries
  --enable-debug             enable debugging
  ...

# 기본 configure
$ ./configure
checking for gcc... gcc
checking whether the C compiler works... yes
checking for library containing pthread_create... -lpthread
...
config.status: creating Makefile
config.status: creating config.h

# prefix 지정 (설치 위치)
$ ./configure --prefix=/usr/local
$ ./configure --prefix=$HOME/local  # 홈 디렉토리에

# 기능 활성화/비활성화
$ ./configure --enable-feature
$ ./configure --disable-feature
$ ./configure --enable-ssl --disable-debug

# 라이브러리 위치 지정
$ ./configure --with-library=/path/to/library
$ ./configure --without-library

# 예제: nginx 빌드
$ ./configure \
    --prefix=/usr/local/nginx \
    --with-http_ssl_module \
    --with-http_v2_module \
    --with-pcre \
    --without-http_autoindex_module
```

### configure.ac가 없는 경우

```bash
# autogen.sh가 있는 경우
$ ./autogen.sh

# bootstrap이 있는 경우
$ ./bootstrap

# 수동으로 autotools 실행
$ aclocal  # Makefile.am에서 매크로 수집
$ autoconf  # configure.ac에서 configure 생성
$ autoheader  # config.h.in 생성
$ automake --add-missing  # Makefile.in 생성

# 또는 한 번에
$ autoreconf -i
```

### Make 빌드

```bash
# 기본 빌드
$ make
gcc -c -o main.o main.c
gcc -c -o util.o util.c
gcc -o program main.o util.o

# 병렬 빌드 (빠름)
$ make -j$(nproc)  # CPU 코어 수만큼
$ make -j4  # 4개 작업 병렬

# 특정 타겟
$ make all
$ make install
$ make clean
$ make distclean  # configure 결과물도 삭제

# verbose 출력
$ make V=1
$ make VERBOSE=1

# 드라이런 (실제 실행 안 함)
$ make -n

# 빌드 로그 저장
$ make 2>&1 | tee build.log
```

### 테스트 및 설치

```bash
# 테스트 실행
$ make check
$ make test
$ make distcheck  # 배포 패키지 테스트

# 설치
$ sudo make install
# /usr/local/bin에 바이너리
# /usr/local/lib에 라이브러리
# /usr/local/share에 데이터 파일

# DESTDIR를 이용한 설치 (패키징용)
$ make DESTDIR=/tmp/install install

# 설치 미리보기
$ make -n install

# 제거
$ sudo make uninstall

# 정리
$ make clean  # 빌드 결과물 삭제
$ make distclean  # configure 결과물도 삭제
$ make maintainer-clean  # 모든 생성 파일 삭제
```

---

## CMake

### CMake 기본

```bash
# CMake 설치
$ sudo apt install cmake  # Debian/Ubuntu
$ sudo dnf install cmake  # Fedora
$ sudo pacman -S cmake  # Arch

# 버전 확인
$ cmake --version
cmake version 3.27.7

# out-of-source 빌드 (권장)
$ mkdir build
$ cd build
$ cmake ..
-- The C compiler identification is GNU 13.2.1
-- Configuring done
-- Generating done
-- Build files have been written to: /path/to/build

# 컴파일
$ make
$ make -j$(nproc)

# 설치
$ sudo make install

# 완전한 예제
$ git clone https://github.com/user/cmake-project.git
$ cd cmake-project
$ mkdir build && cd build
$ cmake .. -DCMAKE_INSTALL_PREFIX=/usr/local
$ make -j$(nproc)
$ sudo make install
```

### CMake 옵션

```bash
# 빌드 타입 지정
$ cmake .. -DCMAKE_BUILD_TYPE=Release
$ cmake .. -DCMAKE_BUILD_TYPE=Debug
$ cmake .. -DCMAKE_BUILD_TYPE=RelWithDebInfo

# 설치 경로 지정
$ cmake .. -DCMAKE_INSTALL_PREFIX=/usr/local
$ cmake .. -DCMAKE_INSTALL_PREFIX=$HOME/local

# 컴파일러 지정
$ cmake .. -DCMAKE_C_COMPILER=gcc-13
$ cmake .. -DCMAKE_CXX_COMPILER=g++-13
$ cmake .. -DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++

# 옵션 활성화/비활성화
$ cmake .. -DENABLE_FEATURE=ON
$ cmake .. -DENABLE_FEATURE=OFF
$ cmake .. -DBUILD_SHARED_LIBS=ON

# 여러 옵션
$ cmake .. \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX=/usr/local \
    -DENABLE_SSL=ON \
    -DENABLE_TESTS=OFF

# GUI 도구 (설치 필요)
$ cmake-gui ..
$ ccmake ..  # ncurses 기반

# 설정 확인
$ cmake -L ..  # 캐시 변수 목록
$ cmake -LAH ..  # 고급 옵션 포함
```

### CMake 프로젝트 빌드 예제

```bash
# OpenCV 빌드
$ git clone https://github.com/opencv/opencv.git
$ cd opencv
$ mkdir build && cd build
$ cmake .. \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX=/usr/local \
    -DWITH_CUDA=ON \
    -DWITH_GTK=ON \
    -DBUILD_EXAMPLES=OFF
$ make -j$(nproc)
$ sudo make install

# 설치 확인
$ pkg-config --modversion opencv4
$ ldconfig -p | grep opencv
```

### Ninja 빌드 시스템

```bash
# Ninja 설치
$ sudo apt install ninja-build

# CMake with Ninja
$ cmake .. -GNinja
$ ninja
$ ninja -j$(nproc)
$ sudo ninja install

# Ninja의 장점
# - Make보다 빠름
# - 더 나은 빌드 로그
# - 자동 병렬 빌드
```

---

## Make

### Makefile 기본

```bash
# 간단한 Makefile 예제
$ cat Makefile
CC = gcc
CFLAGS = -Wall -O2
TARGET = program
OBJS = main.o util.o

all: $(TARGET)

$(TARGET): $(OBJS)
	$(CC) $(CFLAGS) -o $@ $^

%.o: %.c
	$(CC) $(CFLAGS) -c $<

clean:
	rm -f $(TARGET) $(OBJS)

install:
	install -m 755 $(TARGET) /usr/local/bin

uninstall:
	rm -f /usr/local/bin/$(TARGET)

# 사용
$ make
$ make clean
$ sudo make install
```

### 복잡한 Makefile

```bash
# 실전 Makefile
$ cat Makefile
# 변수 정의
PREFIX ?= /usr/local
BINDIR = $(PREFIX)/bin
LIBDIR = $(PREFIX)/lib
INCLUDEDIR = $(PREFIX)/include

CC = gcc
CFLAGS = -Wall -Wextra -O2 -std=c11
LDFLAGS = -L$(LIBDIR)
LIBS = -lpthread -lm

# 소스 파일
SRCS = $(wildcard src/*.c)
OBJS = $(SRCS:.c=.o)
TARGET = myapp

# 타겟
.PHONY: all clean install uninstall test

all: $(TARGET)

$(TARGET): $(OBJS)
	$(CC) $(LDFLAGS) -o $@ $^ $(LIBS)

%.o: %.c
	$(CC) $(CFLAGS) -I$(INCLUDEDIR) -c $< -o $@

clean:
	rm -f $(TARGET) $(OBJS)

install: $(TARGET)
	install -d $(BINDIR)
	install -m 755 $(TARGET) $(BINDIR)

uninstall:
	rm -f $(BINDIR)/$(TARGET)

test: $(TARGET)
	./$(TARGET) --test

# 의존성 자동 생성
depend:
	$(CC) -MM $(SRCS) > .depend

-include .depend
```

### Make 고급 기능

```bash
# 조건부 컴파일
DEBUG ?= 0
ifeq ($(DEBUG),1)
    CFLAGS += -g -DDEBUG
else
    CFLAGS += -O2 -DNDEBUG
endif

# 사용
$ make DEBUG=1

# 플랫폼별 설정
UNAME_S := $(shell uname -s)
ifeq ($(UNAME_S),Linux)
    LIBS += -lrt
endif
ifeq ($(UNAME_S),Darwin)
    LIBS += -framework CoreFoundation
endif

# 함수 사용
SOURCES = $(shell find src -name '*.c')
INCLUDES = $(addprefix -I, $(wildcard include/*))

# 재귀 Make
.PHONY: subdirs
subdirs:
	$(MAKE) -C subdir1
	$(MAKE) -C subdir2
```

---

## 언어별 빌드 시스템

### Python

```bash
# setuptools 빌드
$ python3 setup.py build
$ python3 setup.py install  # 또는 sudo
$ python3 setup.py install --user  # 사용자 디렉토리에

# pip로 설치
$ pip install .
$ pip install -e .  # 개발 모드 (editable)

# 가상환경에서
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install .

# requirements 설치
$ pip install -r requirements.txt

# 빌드 의존성 포함
$ pip install -e ".[dev]"

# wheel 빌드
$ python3 setup.py bdist_wheel
$ pip install dist/package-1.0-py3-none-any.whl
```

### Rust

```bash
# Cargo 빌드
$ cargo build  # debug
$ cargo build --release  # optimized

# 실행
$ cargo run
$ cargo run --release

# 테스트
$ cargo test

# 설치
$ cargo install --path .
$ cargo install --path . --root /usr/local

# 의존성 업데이트
$ cargo update

# 정리
$ cargo clean
```

### Go

```bash
# Go 빌드
$ go build
$ go build -o myapp

# 최적화 빌드
$ go build -ldflags="-s -w" -o myapp

# 여러 플랫폼용
$ GOOS=linux GOARCH=amd64 go build -o myapp-linux
$ GOOS=windows GOARCH=amd64 go build -o myapp.exe
$ GOOS=darwin GOARCH=arm64 go build -o myapp-mac

# 설치
$ go install

# 의존성 관리
$ go mod init myapp
$ go mod tidy
$ go mod vendor
```

### Node.js

```bash
# npm 빌드
$ npm install  # 의존성 설치
$ npm run build  # 빌드 스크립트 실행

# 네이티브 모듈 빌드
$ npm install --build-from-source
$ npm rebuild

# node-gyp 수동 빌드
$ node-gyp configure
$ node-gyp build

# 전역 설치
$ npm install -g .
$ sudo npm install -g . --unsafe-perm
```

### Java

```bash
# Maven 빌드
$ mvn clean compile
$ mvn clean package
$ mvn clean install

# 테스트 스킵
$ mvn clean install -DskipTests

# Gradle 빌드
$ gradle build
$ gradle clean build
$ ./gradlew build  # wrapper 사용

# 설치
$ gradle install
$ gradle installDist
```

---

## 의존성 관리

### 의존성 확인

```bash
# configure 실패 시 의존성 확인
$ ./configure
checking for OpenSSL... no
configure: error: OpenSSL development files not found

# pkg-config로 확인
$ pkg-config --list-all | grep ssl
$ pkg-config --modversion openssl
$ pkg-config --cflags openssl
$ pkg-config --libs openssl

# 라이브러리 검색
$ ldconfig -p | grep ssl
$ find /usr -name "libssl.so*"

# 헤더 파일 검색
$ find /usr -name "openssl*.h"
```

### 의존성 설치

```bash
# Debian/Ubuntu - 개발 패키지
$ sudo apt install libssl-dev
$ sudo apt install libcurl4-openssl-dev
$ sudo apt install libpq-dev  # PostgreSQL
$ sudo apt install libmysqlclient-dev  # MySQL
$ sudo apt install libsqlite3-dev
$ sudo apt install zlib1g-dev
$ sudo apt install libxml2-dev
$ sudo apt install libxslt1-dev

# Red Hat/Fedora
$ sudo dnf install openssl-devel
$ sudo dnf install libcurl-devel
$ sudo dnf install postgresql-devel
$ sudo dnf install mysql-devel
$ sudo dnf install sqlite-devel
$ sudo dnf install zlib-devel

# Arch Linux
$ sudo pacman -S openssl
$ sudo pacman -S curl
$ sudo pacman -S postgresql-libs
$ sudo pacman -S mariadb-libs
$ sudo pacman -S sqlite
$ sudo pacman -S zlib
```

### 라이브러리 경로 설정

```bash
# LD_LIBRARY_PATH
$ export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH

# /etc/ld.so.conf.d/ 사용 (영구적)
$ sudo vi /etc/ld.so.conf.d/local.conf
/usr/local/lib
/opt/lib

$ sudo ldconfig  # 캐시 업데이트
$ ldconfig -p | grep library  # 확인

# PKG_CONFIG_PATH
$ export PKG_CONFIG_PATH=/usr/local/lib/pkgconfig:$PKG_CONFIG_PATH

# 프로그램 실행 시
$ LD_LIBRARY_PATH=/custom/path ./program
```

---

## 설치 및 제거

### 표준 설치

```bash
# 전형적인 설치 과정
$ ./configure --prefix=/usr/local
$ make -j$(nproc)
$ sudo make install

# 설치 파일 확인
$ make -n install  # 드라이런

# 로그 저장
$ sudo make install 2>&1 | tee install.log

# 설치된 파일 목록
$ cat install.log | grep -E '^(/usr|/opt)'
```

### checkinstall 사용

```bash
# checkinstall 설치
$ sudo apt install checkinstall  # Debian/Ubuntu

# 패키지로 설치
$ ./configure --prefix=/usr/local
$ make
$ sudo checkinstall
# .deb 또는 .rpm 패키지 생성 및 설치

# 나중에 제거 가능
$ sudo dpkg -r package
$ sudo rpm -e package

# 옵션
$ sudo checkinstall --pkgname=myapp \
                     --pkgversion=1.0 \
                     --pakdir=$PWD \
                     --default
```

### DESTDIR 활용

```bash
# 임시 디렉토리에 설치
$ make DESTDIR=/tmp/myapp install

# 설치된 파일 확인
$ find /tmp/myapp -type f

# tar 아카이브 생성
$ cd /tmp/myapp
$ tar czf ~/myapp-1.0.tar.gz .

# 다른 시스템에 설치
$ cd /
$ sudo tar xzf myapp-1.0.tar.gz
```

### 수동 제거

```bash
# 설치 로그 사용
$ cat install.log | grep -E '^(/usr|/opt)' > installed-files.txt

# 파일 제거 스크립트
$ cat > uninstall.sh << 'EOF'
#!/bin/bash
while read file; do
    if [ -f "$file" ]; then
        echo "Removing $file"
        sudo rm -f "$file"
    fi
done < installed-files.txt
EOF
$ chmod +x uninstall.sh
$ ./uninstall.sh

# 또는 xargs 사용
$ cat installed-files.txt | sudo xargs rm -f

# 빈 디렉토리 제거
$ sudo find /usr/local -type d -empty -delete
```

---

## 최적화 및 설정

### 컴파일러 최적화

```bash
# 최적화 레벨
$ ./configure CFLAGS="-O2"  # 기본
$ ./configure CFLAGS="-O3"  # 고급 최적화
$ ./configure CFLAGS="-Os"  # 크기 최적화
$ ./configure CFLAGS="-Ofast"  # 최대 속도 (표준 위반 가능)

# CPU 최적화
$ ./configure CFLAGS="-O3 -march=native"
$ ./configure CFLAGS="-O3 -march=x86-64-v3"

# 디버그 정보 제거
$ ./configure CFLAGS="-O2 -s"

# 링크 시간 최적화 (LTO)
$ ./configure CFLAGS="-O3 -flto" LDFLAGS="-flto"

# 프로파일 기반 최적화 (PGO)
# 1단계: 프로파일링 빌드
$ ./configure CFLAGS="-O2 -fprofile-generate"
$ make
$ ./program  # 실행하여 프로파일 생성

# 2단계: 최적화 빌드
$ make clean
$ ./configure CFLAGS="-O2 -fprofile-use"
$ make
```

### 정적 빌드

```bash
# 정적 라이브러리로 빌드
$ ./configure --enable-static --disable-shared
$ make LDFLAGS="-static"

# 부분 정적 빌드
$ make LDFLAGS="-Wl,-Bstatic -lssl -lcrypto -Wl,-Bdynamic"

# 의존성 확인
$ ldd program
	linux-vdso.so.1 (0x00007ffc...)
	libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6

# 완전 정적
$ ldd static-program
	not a dynamic executable
```

### 병렬 빌드

```bash
# CPU 코어 수 확인
$ nproc
8

# 병렬 빌드
$ make -j$(nproc)
$ make -j8

# 부하 제한
$ make -j$(nproc) -l$(nproc)

# distcc (분산 컴파일)
$ sudo apt install distcc

$ export CC="distcc gcc"
$ export CXX="distcc g++"
$ make -j20  # 원격 머신 코어 수 포함
```

---

## 문제 해결

### configure 오류

```bash
# 1. 의존성 누락
checking for library... no
configure: error: library not found

# 해결: 개발 패키지 설치
$ sudo apt install lib*-dev

# 2. 컴파일러 없음
configure: error: no acceptable C compiler found in $PATH

# 해결: 컴파일러 설치
$ sudo apt install build-essential

# 3. pkg-config 오류
configure: error: Package requirements not met

# 해결: PKG_CONFIG_PATH 설정
$ export PKG_CONFIG_PATH=/usr/local/lib/pkgconfig:$PKG_CONFIG_PATH

# 4. 권한 문제
$ ./configure --prefix=$HOME/local  # root 권한 불필요
```

### 컴파일 오류

```bash
# 1. 헤더 파일 없음
fatal error: header.h: No such file or directory

# 해결: include 경로 추가
$ make CFLAGS="-I/usr/local/include"

# 2. 라이브러리 링크 오류
undefined reference to 'function'

# 해결: 라이브러리 경로 추가
$ make LDFLAGS="-L/usr/local/lib -lmylib"

# 3. 메모리 부족
virtual memory exhausted: Cannot allocate memory

# 해결: 스왑 추가 또는 병렬 작업 줄이기
$ make -j2

# 4. 버전 충돌
$ ./configure CC=gcc-11 CXX=g++-11
```

### 실행 오류

```bash
# 1. 공유 라이브러리 없음
error while loading shared libraries: libfoo.so.1

# 해결: ldconfig 업데이트
$ sudo ldconfig
$ LD_LIBRARY_PATH=/usr/local/lib ./program

# 2. 권한 문제
$ sudo chown -R $USER:$USER /usr/local/bin/program
$ chmod +x /usr/local/bin/program

# 3. 디버깅
$ ldd program  # 의존성 확인
$ strace program  # 시스템 콜 추적
$ gdb program  # 디버거
```

---

## 패키징

### Debian 패키지 생성

```bash
# 기본 구조 생성
$ mkdir -p myapp-1.0/DEBIAN
$ mkdir -p myapp-1.0/usr/local/bin

# control 파일
$ cat > myapp-1.0/DEBIAN/control << EOF
Package: myapp
Version: 1.0
Section: utils
Priority: optional
Architecture: amd64
Maintainer: Your Name <email@example.com>
Description: My Application
 Long description here.
EOF

# 파일 복사
$ cp myapp myapp-1.0/usr/local/bin/

# 패키지 빌드
$ dpkg-deb --build myapp-1.0
$ dpkg-deb --build myapp-1.0 myapp-1.0-amd64.deb

# 설치
$ sudo dpkg -i myapp-1.0-amd64.deb
```

### RPM 패키지 생성

```bash
# rpmbuild 설치
$ sudo dnf install rpm-build rpmdevtools

# 디렉토리 구조 생성
$ rpmdev-setuptree
$ ls ~/rpmbuild/
BUILD  RPMS  SOURCES  SPECS  SRPMS

# spec 파일 생성
$ cat > ~/rpmbuild/SPECS/myapp.spec << EOF
Name: myapp
Version: 1.0
Release: 1%{?dist}
Summary: My Application
License: GPL
Source0: myapp-1.0.tar.gz

%description
My Application

%prep
%setup -q

%build
./configure --prefix=/usr
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

%files
/usr/bin/myapp

%changelog
* Mon Jan 01 2024 Your Name <email@example.com> - 1.0-1
- Initial package
EOF

# 빌드
$ rpmbuild -ba ~/rpmbuild/SPECS/myapp.spec

# 생성된 패키지
$ ls ~/rpmbuild/RPMS/x86_64/
myapp-1.0-1.el8.x86_64.rpm
```

### Arch PKGBUILD

```bash
# PKGBUILD 생성
$ cat > PKGBUILD << EOF
pkgname=myapp
pkgver=1.0
pkgrel=1
pkgdesc="My Application"
arch=('x86_64')
url="https://example.com"
license=('GPL')
depends=('glibc')
makedepends=('gcc' 'make')
source=("https://example.com/myapp-1.0.tar.gz")
sha256sums=('SKIP')

build() {
    cd "\$pkgname-\$pkgver"
    ./configure --prefix=/usr
    make
}

package() {
    cd "\$pkgname-\$pkgver"
    make DESTDIR="\$pkgdir" install
}
EOF

# 빌드
$ makepkg
$ makepkg -si  # 빌드 및 설치
```

---

## 실전 예제

### nginx 소스 빌드

```bash
# 의존성 설치
$ sudo apt install build-essential libpcre3-dev libssl-dev zlib1g-dev

# 소스 다운로드
$ wget http://nginx.org/download/nginx-1.24.0.tar.gz
$ tar xzf nginx-1.24.0.tar.gz
$ cd nginx-1.24.0

# configure
$ ./configure \
    --prefix=/usr/local/nginx \
    --sbin-path=/usr/local/sbin/nginx \
    --conf-path=/etc/nginx/nginx.conf \
    --pid-path=/var/run/nginx.pid \
    --with-http_ssl_module \
    --with-http_v2_module \
    --with-http_realip_module \
    --with-http_gzip_static_module

# 빌드 및 설치
$ make -j$(nproc)
$ sudo make install

# 확인
$ nginx -v
$ nginx -t
```

### Python 소스 빌드

```bash
# 의존성 설치
$ sudo apt install build-essential zlib1g-dev libncurses5-dev \
    libgdbm-dev libnss3-dev libssl-dev libreadline-dev \
    libffi-dev libsqlite3-dev wget libbz2-dev

# 다운로드
$ wget https://www.python.org/ftp/python/3.12.0/Python-3.12.0.tar.xz
$ tar xJf Python-3.12.0.tar.xz
$ cd Python-3.12.0

# configure (최적화)
$ ./configure \
    --prefix=/usr/local \
    --enable-optimizations \
    --with-lto \
    --enable-shared

# 빌드 (PGO)
$ make -j$(nproc)

# 테스트 (선택사항)
$ make test

# 설치
$ sudo make altinstall  # python3.12로 설치 (기존 버전 유지)

# 확인
$ python3.12 --version
$ which python3.12
```

### Redis 소스 빌드

```bash
# 다운로드
$ wget https://download.redis.io/redis-stable.tar.gz
$ tar xzf redis-stable.tar.gz
$ cd redis-stable

# 빌드 (Makefile 사용)
$ make -j$(nproc)
$ make test  # 테스트

# 설치
$ sudo make PREFIX=/usr/local install

# systemd 서비스 설치
$ sudo mkdir /etc/redis
$ sudo cp redis.conf /etc/redis/
$ sudo vi /etc/systemd/system/redis.service

# 확인
$ redis-server --version
$ redis-cli --version
```

---

## 요약

소스 빌드 핵심 단계:

1. **준비**: 빌드 도구 및 의존성 설치
2. **다운로드**: 소스 코드 획득 및 검증
3. **설정**: `./configure` 또는 `cmake`
4. **빌드**: `make` 또는 빌드 시스템 실행
5. **테스트**: `make test`
6. **설치**: `sudo make install`

주요 빌드 시스템:
- **Autotools**: `./configure && make && make install`
- **CMake**: `cmake .. && make && make install`
- **언어별**: setuptools, cargo, go build 등

최적화 팁:
- CPU 최적화: `-march=native`
- 병렬 빌드: `make -j$(nproc)`
- LTO: `-flto`

---

[← Pacman으로 돌아가기](pacman-arch.md)

[← 목차로 돌아가기](../README.md)
