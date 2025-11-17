# 고급 셸 스크립팅

## 목차
- [배열](#배열)
- [정규표현식](#정규표현식)
- [에러 처리](#에러-처리)
- [디버깅](#디버깅)

---

## 배열

```bash
#!/bin/bash

# 배열 선언
FRUITS=("apple" "banana" "cherry")

# 접근
echo "${FRUITS[0]}"  # apple
echo "${FRUITS[@]}"  # 모든 요소
echo "${#FRUITS[@]}" # 길이

# 추가
FRUITS+=("date")

# 반복
for fruit in "${FRUITS[@]}"; do
    echo "$fruit"
done

# 연관 배열
declare -A CONFIG
CONFIG[host]="localhost"
CONFIG[port]=8080

echo "${CONFIG[host]}"
```

---

## 정규표현식

```bash
#!/bin/bash

# 패턴 매칭
if [[ "$email" =~ ^[a-zA-Z0-9]+@[a-zA-Z0-9]+\.[a-zA-Z]+$ ]]; then
    echo "Valid email"
fi

# grep 활용
if echo "$text" | grep -q "pattern"; then
    echo "Pattern found"
fi

# sed 활용
result=$(echo "$text" | sed 's/old/new/g')
```

---

## 에러 처리

```bash
#!/bin/bash

# set 옵션
set -e  # 에러 시 중단
set -u  # 미정의 변수 사용 시 에러
set -o pipefail  # 파이프 에러 감지

# trap으로 정리 작업
cleanup() {
    echo "Cleaning up..."
    rm -f /tmp/tempfile
}

trap cleanup EXIT
trap cleanup ERR INT TERM

# 에러 확인
if ! command_that_might_fail; then
    echo "Command failed"
    exit 1
fi

# 명령 성공 확인
command || {
    echo "Command failed"
    exit 1
}
```

---

## 디버깅

```bash
# bash -x로 디버그
$ bash -x script.sh

# 스크립트 내에서
#!/bin/bash
set -x  # 디버그 활성화
# ... 코드 ...
set +x  # 디버그 비활성화

# 부분 디버깅
debug_section() {
    set -x
    echo "Debug this"
    ls -l
    set +x
}

# 로그 레벨
LOG_LEVEL=DEBUG

log_debug() {
    [ "$LOG_LEVEL" = "DEBUG" ] && echo "[DEBUG] $1"
}

log_info() {
    echo "[INFO] $1"
}

log_error() {
    echo "[ERROR] $1" >&2
}
```

---

[다음: 예제 스크립트 →](examples/)

[← 함수로 돌아가기](functions.md)

[← 목차로 돌아가기](../README.md)
