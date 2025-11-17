# 유닉스의 역사와 철학

## 목차
- [유닉스의 탄생 배경](#유닉스의-탄생-배경)
- [주요 발전 과정](#주요-발전-과정)
- [유닉스 전쟁 (Unix Wars)](#유닉스-전쟁-unix-wars)
- [리눅스의 등장](#리눅스의-등장)
- [현대의 유닉스/리눅스](#현대의-유닉스리눅스)
- [타임라인](#타임라인)

---

## 유닉스의 탄생 배경

### Multics 프로젝트의 실패

1960년대 후반, MIT, AT&T 벨 연구소, General Electric이 공동으로 **Multics**(Multiplexed Information and Computing Service) 프로젝트를 진행했습니다.

**Multics의 목표:**
- 다중 사용자 지원
- 시분할 시스템 (Time-sharing)
- 고수준의 보안
- 모듈화된 설계

**실패 원인:**
- 지나치게 복잡한 설계
- 느린 개발 속도
- 비용 초과
- 성능 목표 미달성

### 유닉스의 시작 (1969)

Multics 프로젝트에서 AT&T가 철수한 후, 벨 연구소의 **Ken Thompson**은 개인적으로 운영체제 개발을 시작했습니다.

**초기 개발 (1969년 여름):**
```
하드웨어: PDP-7 (Digital Equipment Corporation)
메모리: 8K words
스토리지: 디스크 없음 (테이프만)
언어: 어셈블리
```

**개발 동기:**
- Space Travel 게임을 더 나은 환경에서 실행하고 싶었음
- 파일 시스템 실험
- 간단하지만 강력한 OS 만들기

**초기 팀:**
- **Ken Thompson**: 주요 개발자
- **Dennis Ritchie**: 초기 협력자, 후에 C 언어 개발
- **Doug McIlroy**: 파이프 개념 제안
- **J.F. Ossanna**: 문서 도구 개발

### 이름의 유래

**"UNIX"** 라는 이름은 Brian Kernighan이 제안한 것으로, Multics에 대한 말장난입니다:
- **Multi**cs → **Uni**x
- 복잡함(Multi) → 단순함(Uni)
- 원래는 "UNICS" (Uniplexed Information and Computing Service)였으나 나중에 UNIX로 변경

---

## 주요 발전 과정

### 1세대: 어셈블리 시대 (1969-1972)

**1969년:**
- PDP-7에서 초기 유닉스 개발
- 파일 시스템, 프로세스 관리 구현
- 셸과 에디터 개발

**1970년:**
- PDP-11/20으로 포팅
- 문서 처리 시스템 roff 개발
- 처음으로 "UNIX"라는 이름 사용

**1971년:**
- 첫 번째 유닉스 매뉴얼 발행
- 파이프 개념 도입 (Doug McIlroy)
```bash
# 파이프의 혁신성 - 여러 프로그램을 연결
$ who | wc -l  # 로그인한 사용자 수 세기
```

### 2세대: C 언어와 이식성 (1973-1975)

**1972년:**
- Dennis Ritchie가 **C 언어** 개발
- B 언어의 후속작 (Ken Thompson의 B 언어 기반)

**1973년:**
- 🔥 **유닉스를 C로 재작성** - 운영체제 역사의 혁명
- 이식성(Portability) 확보
- 이전에는 어셈블리로 작성된 OS는 특정 하드웨어에 종속

**C로 재작성의 의미:**
```c
// 이전: 어셈블리 (하드웨어 종속적)
MOV AX, 1
INT 0x80

// 이후: C (이식 가능)
#include <stdio.h>
int main() {
    printf("Hello, World!\n");
    return 0;
}
```

**영향:**
- 다양한 하드웨어로 쉽게 포팅 가능
- 코드 가독성과 유지보수성 향상
- 개발 생산성 증대

### 3세대: 대학으로의 확산 (1975-1983)

**1975년: Version 6 (V6)**
- AT&T가 대학에 소스 코드와 함께 배포
- 라이선스 비용: $20,000 (교육 기관은 무료)
- 🎓 **UC Berkeley에서 도입**

**1977년: BSD (Berkeley Software Distribution)**
- Bill Joy가 주도
- Berkeley에서 개선된 버전 배포
- vi 에디터, C shell (csh) 추가

**1BSD (1977):**
```bash
# BSD의 주요 기여
- Pascal 컴파일러
- ex/vi 에디터
- C shell (csh)
```

**2BSD (1978):**
- vi 에디터 정식 포함
- 향상된 가상 메모리

**3BSD (1979):**
- VAX-11/780 지원
- 가상 메모리 시스템
- 성능 대폭 향상

**4BSD (1980):**
- 더욱 개선된 가상 메모리
- 새로운 신호 메커니즘

**4.2BSD (1983):**
- TCP/IP 네트워킹 스택 포함 🌐
- Fast File System (FFS)
- 인터넷 시대의 기반 마련

### 4세대: 상업화와 분열 (1983-1993)

**System III (1982):**
- AT&T의 첫 상업용 유닉스
- 여러 내부 버전 통합

**System V (1983):**
- AT&T의 주요 상업용 유닉스
- 많은 현대 유닉스의 기반
- STREAMS, RFS (Remote File System) 도입

**주요 상용 유닉스:**

| 제품 | 회사 | 기반 | 출시 |
|------|------|------|------|
| AIX | IBM | System V | 1986 |
| HP-UX | HP | System V | 1984 |
| Solaris | Sun | BSD + System V | 1992 |
| IRIX | SGI | System V | 1988 |
| Tru64 | DEC | BSD | 1992 |

---

## 유닉스 전쟁 (Unix Wars)

### 배경

1980년대, AT&T가 전화 사업 독점권을 잃으면서 컴퓨터 사업 진출이 가능해졌습니다. 이는 유닉스의 상업화를 의미했고, 여러 회사가 자신들의 유닉스 버전을 개발했습니다.

### 두 진영의 대립

**System V 진영 (AT&T 중심):**
- AT&T
- Sun Microsystems (초기)
- IBM
- HP

**BSD 진영 (Berkeley 중심):**
- UC Berkeley
- Sun Microsystems (후기)
- DEC
- SGI

### 표준화 노력

**POSIX (1988):**
- Portable Operating System Interface
- IEEE 1003.1 표준
- 유닉스 시스템 간 호환성 보장

```c
// POSIX 표준 API 예제
#include <unistd.h>
#include <fcntl.h>

int main() {
    // POSIX 표준 파일 작업
    int fd = open("/tmp/test.txt", O_RDWR | O_CREAT, 0644);
    write(fd, "Hello, POSIX!\n", 14);
    close(fd);
    return 0;
}
```

**Single UNIX Specification:**
- The Open Group에서 관리
- 유닉스 상표권 관리
- 호환성 인증

---

## 리눅스의 등장

### GNU 프로젝트의 시작 (1983)

**Richard Stallman의 비전:**
- 완전히 자유로운 유닉스 호환 OS
- Free Software Foundation (FSF) 설립
- GNU (GNU's Not Unix)

**GNU 프로젝트 성과 (1983-1991):**
```bash
# GNU 도구들
- GCC (GNU C Compiler)
- GNU Make
- GNU Emacs
- Bash (Bourne Again Shell)
- GNU Coreutils (ls, cp, mv, etc.)
- glibc (GNU C Library)
```

**부족한 부분:**
- 커널 (GNU Hurd)이 완성되지 않음
- OS로서 완전하지 않음

### 리눅스 커널의 탄생 (1991)

**Linus Torvalds (핀란드 헬싱키 대학교 학생):**

**1991년 4월:**
- Minix 사용 중 (교육용 유닉스, Andrew Tanenbaum 개발)
- Minix의 제한사항에 불만

**1991년 8월 25일 - 역사적인 발표:**
```
From: torvalds@klaava.Helsinki.FI (Linus Benedict Torvalds)
Newsgroups: comp.os.minix
Subject: What would you like to see most in minix?
Date: 25 Aug 91 20:57:08 GMT

Hello everybody out there using minix -

I'm doing a (free) operating system (just a hobby, won't be big and
professional like gnu) for 386(486) AT clones. This has been brewing
since april, and is starting to get ready. I'd like any feedback on
things people like/dislike in minix, as my OS resembles it somewhat
(same physical layout of the file-system (due to practical reasons)
among other things).
```

**1991년 9월 17일:**
- Linux 0.01 릴리스
- 10,239 줄의 코드
- 기본적인 기능만 제공

**1991년 10월 5일:**
- Linux 0.02 릴리스
- Bash, GCC 실행 가능
- 최초로 사용 가능한 버전

### 급속한 성장

**1992년:**
- Linux 0.95 릴리스
- X Window System 지원
- 네트워킹 기능 추가

**1994년:**
- Linux 1.0.0 릴리스 🎉
- 176,250 줄의 코드
- 안정적인 커널

**주요 코드 라인 수 변화:**
```
1991 (0.01):      10,239 줄
1994 (1.0.0):    176,250 줄
2001 (2.4.0):  2,396,000 줄
2011 (3.0):   14,647,000 줄
2020 (5.10):  28,000,000 줄
2024 (6.7):   35,000,000 줄
```

### GNU/Linux의 결합

**왜 "GNU/Linux"인가?**
- Linux: 커널
- GNU: 대부분의 유저랜드 도구

```
┌─────────────────────────────────┐
│    Applications                 │
├─────────────────────────────────┤
│    GNU Tools (ls, bash, gcc)    │
├─────────────────────────────────┤
│    GNU C Library (glibc)        │
├─────────────────────────────────┤
│    System Calls Interface       │
├─────────────────────────────────┤
│    Linux Kernel                 │
├─────────────────────────────────┤
│    Hardware                     │
└─────────────────────────────────┘
```

---

## 현대의 유닉스/리눅스

### 현존하는 유닉스 시스템

**오픈소스:**
- FreeBSD, OpenBSD, NetBSD
- illumos (Solaris 기반)
- macOS (Darwin 커널, BSD 기반)

**상용:**
- AIX (IBM, 여전히 활발)
- HP-UX (HP, 레거시 시스템)
- Solaris (Oracle, 유지보수 모드)

### 리눅스의 지배

**2024년 현재 리눅스 점유율:**

**서버 시장:**
- 웹 서버: ~70%
- 슈퍼컴퓨터: 100% (TOP 500 전부)
- 클라우드: ~90%
- 컨테이너: 거의 100%

**엔터프라이즈:**
```bash
# 주요 엔터프라이즈 리눅스
- Red Hat Enterprise Linux (RHEL)
- SUSE Linux Enterprise Server (SLES)
- Ubuntu Server
- Oracle Linux
```

**임베디드:**
- 스마트폰: Android (Linux 커널)
- IoT 디바이스
- 네트워크 장비
- 자동차 인포테인먼트 시스템

**데스크탑:**
- 약 2-3% (하지만 개발자들 사이에서 인기)
- 리눅스 데스크탑 사용자: 수천만 명

### 주요 영향력

**클라우드 컴퓨팅:**
```bash
# 주요 클라우드 제공자 모두 리눅스 기반
AWS EC2
Google Cloud Platform
Microsoft Azure (Linux 인스턴스 50% 이상)
```

**컨테이너 혁명:**
```bash
# Docker, Kubernetes 모두 리눅스 기반
docker run ubuntu
kubectl apply -f deployment.yaml
```

**DevOps와 자동화:**
```bash
# 현대 개발 도구의 표준 플랫폼
Ansible
Terraform
Jenkins
GitLab CI
```

---

## 타임라인

### 1969-1979: 탄생과 성장
```
1969  ─┬─ Ken Thompson, PDP-7에서 유닉스 개발 시작
1970  ─┼─ PDP-11로 포팅, "UNIX" 이름 사용
1971  ─┼─ 파이프 개념 도입
1972  ─┼─ C 언어 개발
1973  ─┼─ 유닉스를 C로 재작성
1975  ─┼─ V6 릴리스, 대학에 배포
1977  ─┼─ 1BSD 릴리스 (Bill Joy)
1979  ─┴─ V7 릴리스, 3BSD 릴리스
```

### 1980-1989: 상업화와 분열
```
1980  ─┬─ 4BSD 릴리스
1983  ─┼─ System V 릴리스, GNU 프로젝트 시작
1984  ─┼─ X Window System
1986  ─┼─ BSD Net/1, BSD Net/2
1988  ─┼─ POSIX 표준
1989  ─┴─ GNU GPL v1
```

### 1990-1999: 리눅스와 오픈소스
```
1991  ─┬─ Linux 0.01 릴리스
1992  ─┼─ 386BSD 릴리스
1993  ─┼─ FreeBSD, NetBSD 릴리스, Debian 설립
1994  ─┼─ Linux 1.0, Red Hat 설립
1996  ─┼─ KDE 프로젝트 시작
1997  ─┼─ GNOME 프로젝트 시작
1998  ─┼─ "Open Source" 용어 탄생
1999  ─┴─ Red Hat IPO
```

### 2000-현재: 주류화와 지배
```
2000  ─┬─ macOS (Darwin 커널) 출시
2004  ─┼─ Ubuntu 출시
2006  ─┼─ Amazon EC2 출시 (클라우드 시대)
2007  ─┼─ Android 발표
2008  ─┼─ Google Chrome (Linux 기반)
2011  ─┼─ Linux 3.0
2013  ─┼─ Docker 출시
2014  ─┼─ Kubernetes 출시
2015  ─┼─ systemd 주류화
2016  ─┼─ Windows Subsystem for Linux (WSL)
2019  ─┼─ Linux 5.0
2024  ─┴─ Linux 6.7, 35M+ 줄의 코드
```

---

## 핵심 교훈

### 1. 단순함의 힘
유닉스는 Multics의 복잡함에 대한 반작용으로 탄생했습니다. "작지만 강력한" 도구들의 조합이 복잡한 단일 시스템보다 우월함을 증명했습니다.

### 2. 오픈소스의 힘
리눅스는 수만 명의 개발자가 협업하여 만든 결과물입니다. 오픈소스 모델이 얼마나 강력한지 보여줍니다.

### 3. 표준과 이식성
C 언어로 작성되어 이식 가능했던 유닉스는 다양한 하드웨어에서 실행될 수 있었고, 이것이 보급의 핵심이었습니다.

### 4. 철학의 중요성
유닉스 철학 (단순성, 모듈화, 재사용성)은 50년 이상 지속되고 있으며, 현대 소프트웨어 개발에도 여전히 유효합니다.

---

## 참고 자료

### 책
- "The UNIX Programming Environment" - Brian Kernighan & Rob Pike
- "The Design and Implementation of the UNIX Operating System" - Maurice Bach
- "A Quarter Century of UNIX" - Peter Salus
- "Just for Fun: The Story of an Accidental Revolutionary" - Linus Torvalds

### 논문
- "The UNIX Time-Sharing System" (1974) - Dennis Ritchie & Ken Thompson
- "The Evolution of the Unix Time-sharing System" (1984) - Dennis Ritchie

### 온라인
- [The Unix Tree](https://www.tuhs.org/) - Unix Heritage Society
- [Linux Kernel Archives](https://www.kernel.org/)
- [Early Linux History](https://www.linuxjournal.com/)

---

[다음: 리눅스 배포판 가이드 →](distributions.md)

[← 목차로 돌아가기](../README.md)
