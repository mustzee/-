# 리눅스/유닉스 완벽 가이드 📚

> 초보자부터 전문가까지, 리눅스/유닉스 시스템을 체계적으로 학습할 수 있는 종합 가이드입니다.

## 🎯 이 가이드의 목표

- **체계적 학습**: 기초부터 고급까지 단계별로 구성
- **실용적 예제**: 실무에서 바로 활용할 수 있는 다양한 예제 제공
- **깊이 있는 설명**: 단순 명령어 나열이 아닌 원리와 동작 방식 이해
- **문제 해결**: 실제 현장에서 마주치는 문제들의 해결 방법 제시

## 📖 목차

### [1. 소개 및 역사](01-introduction/)
- [유닉스의 역사와 철학](01-introduction/history.md)
- [리눅스 배포판 가이드](01-introduction/distributions.md)
- [유닉스/리눅스 철학과 설계 원칙](01-introduction/philosophy.md)

### [2. 시스템 아키텍처](02-system-architecture/)
- [커널의 이해](02-system-architecture/kernel.md)
- [부팅 프로세스 상세 분석](02-system-architecture/boot-process.md)
- [시스템 계층 구조](02-system-architecture/system-layers.md)

### [3. 파일 시스템](03-filesystem/)
- [FHS (Filesystem Hierarchy Standard)](03-filesystem/fhs-standard.md)
- [파일시스템 타입과 특징](03-filesystem/filesystem-types.md)
- [inode와 링크 구조](03-filesystem/inode-links.md)
- [마운트와 fstab](03-filesystem/mounting.md)

### [4. 필수 명령어](04-commands/)
- [파일 탐색과 네비게이션](04-commands/navigation.md)
- [파일 작업 명령어](04-commands/file-operations.md)
- [텍스트 처리 도구](04-commands/text-processing.md)
- [파일 검색과 필터링](04-commands/searching.md)
- [압축과 아카이브](04-commands/compression.md)

### [5. 파일 권한과 소유권](05-permissions/)
- [기본 권한 체계](05-permissions/basic-permissions.md)
- [특수 권한 (SUID, SGID, Sticky Bit)](05-permissions/special-permissions.md)
- [ACL (Access Control Lists)](05-permissions/acl.md)
- [실전 예제 모음](05-permissions/examples.md)

### [6. 프로세스 관리](06-processes/)
- [프로세스 확인과 모니터링](06-processes/viewing-processes.md)
- [프로세스 제어와 작업 관리](06-processes/process-control.md)
- [시그널의 이해와 활용](06-processes/signals.md)
- [시스템 리소스 모니터링](06-processes/monitoring.md)

### [7. 셸 스크립팅](07-shell-scripting/)
- [Bash 기초](07-shell-scripting/bash-basics.md)
- [변수와 환경 설정](07-shell-scripting/variables.md)
- [제어 구조 (조건문, 반복문)](07-shell-scripting/control-flow.md)
- [함수와 모듈화](07-shell-scripting/functions.md)
- [고급 스크립팅 기법](07-shell-scripting/advanced.md)
- [실전 스크립트 예제](07-shell-scripting/examples/)

### [8. 네트워킹](08-networking/)
- [네트워크 설정과 관리](08-networking/configuration.md)
- [네트워크 진단 도구](08-networking/diagnostics.md)
- [SSH 완벽 가이드](08-networking/ssh.md)
- [파일 전송 방법들](08-networking/file-transfer.md)
- [방화벽 설정](08-networking/firewall.md)

### [9. 패키지 관리](09-package-management/)
- [APT (Debian/Ubuntu)](09-package-management/apt-debian.md)
- [DNF/YUM (Red Hat/CentOS)](09-package-management/dnf-redhat.md)
- [Pacman (Arch Linux)](09-package-management/pacman-arch.md)
- [소스 컴파일과 설치](09-package-management/building-from-source.md)

### [10. 시스템 관리](10-system-admin/)
- [사용자와 그룹 관리](10-system-admin/user-management.md)
- [systemd 서비스 관리](10-system-admin/systemd.md)
- [작업 스케줄링 (cron, systemd timers)](10-system-admin/cron.md)
- [로그 관리와 분석](10-system-admin/logging.md)

### [11. 보안](11-security/)
- [보안 기본 원칙과 Best Practices](11-security/best-practices.md)
- [SSH 보안 강화](11-security/ssh-hardening.md)
- [방화벽과 네트워크 보안](11-security/firewall.md)
- [보안 도구와 감사](11-security/security-tools.md)

### [12. 고급 주제](12-advanced/)
- [LVM (Logical Volume Management)](12-advanced/lvm.md)
- [RAID 구성과 관리](12-advanced/raid.md)
- [컨테이너 기술 (Docker)](12-advanced/containers.md)
- [커널 파라미터 튜닝](12-advanced/kernel-tuning.md)
- [자동화와 Ansible](12-advanced/automation.md)

### [13. 문제 해결](13-troubleshooting/)
- [부팅 문제 해결](13-troubleshooting/boot-issues.md)
- [디스크 공간 관리](13-troubleshooting/disk-space.md)
- [성능 최적화](13-troubleshooting/performance.md)
- [네트워크 문제 진단](13-troubleshooting/network-issues.md)

### [부록](appendix/)
- [키보드 단축키 모음](appendix/shortcuts.md)
- [정규 표현식 가이드](appendix/regex.md)
- [유용한 원라이너 모음](appendix/one-liners.md)
- [추천 도서 및 자료](appendix/resources.md)

## 🚀 학습 방법

### 초보자를 위한 학습 경로
1. [소개 및 역사](01-introduction/) - 리눅스/유닉스의 배경 이해
2. [파일 시스템](03-filesystem/) - 디렉토리 구조 파악
3. [필수 명령어](04-commands/) - 기본 명령어 실습
4. [파일 권한](05-permissions/) - 권한 개념 학습
5. [셸 스크립팅 기초](07-shell-scripting/bash-basics.md) - 자동화 시작

### 중급자를 위한 학습 경로
1. [프로세스 관리](06-processes/) - 시스템 모니터링
2. [네트워킹](08-networking/) - 네트워크 설정과 관리
3. [시스템 관리](10-system-admin/) - systemd, 사용자 관리
4. [보안](11-security/) - 시스템 보안 강화
5. [셸 스크립팅 고급](07-shell-scripting/advanced.md) - 복잡한 스크립트 작성

### 고급 사용자를 위한 학습 경로
1. [시스템 아키텍처](02-system-architecture/) - 깊이 있는 시스템 이해
2. [고급 주제](12-advanced/) - LVM, RAID, 커널 튜닝
3. [성능 최적화](13-troubleshooting/performance.md) - 시스템 최적화
4. [자동화](12-advanced/automation.md) - 인프라 자동화

## 💡 실습 환경 구축

### 가상 머신 사용 (추천)
```bash
# VirtualBox 또는 VMware 사용
# - Ubuntu 22.04 LTS (초보자 추천)
# - CentOS Stream 9 (엔터프라이즈 환경 학습)
# - Arch Linux (고급 사용자)
```

### Docker 컨테이너 사용
```bash
# 빠른 실습을 위한 컨테이너
docker run -it ubuntu:22.04 /bin/bash
docker run -it rockylinux:9 /bin/bash
docker run -it archlinux:latest /bin/bash
```

### 클라우드 환경
- AWS EC2 Free Tier
- Google Cloud Platform Free Tier
- Azure Free Account
- Oracle Cloud Free Tier

## 📝 문서 규칙

### 명령어 표기
```bash
# 일반 사용자 명령어
$ command

# root 권한 필요
# sudo command

# 실제 실행 예제
$ ls -la
total 48
drwxr-xr-x  6 user user 4096 Jan 17 10:00 .
drwxr-xr-x 24 user user 4096 Jan 17 09:55 ..
```

### 주석 아이콘
- 💡 **팁**: 유용한 정보나 꿀팁
- ⚠️ **주의**: 주의해야 할 사항
- 🔥 **중요**: 반드시 알아야 할 내용
- 🎯 **실습**: 직접 해볼 수 있는 실습 예제
- 🐛 **버그**: 알려진 문제나 버그
- 📌 **참고**: 추가 참고 자료

## 🤝 기여 방법

이 가이드는 지속적으로 업데이트됩니다. 오류 발견, 개선 제안, 예제 추가 등 모든 기여를 환영합니다!

## 📜 라이선스

이 문서는 학습과 교육 목적으로 자유롭게 사용할 수 있습니다.

## 🙏 감사의 말

이 가이드는 수많은 오픈소스 커뮤니티, 리눅스 개발자들, 그리고 문서 기여자들의 노력 덕분에 만들어졌습니다.

---

**마지막 업데이트**: 2025-01-17
**버전**: 2.0
**언어**: 한국어 🇰🇷
