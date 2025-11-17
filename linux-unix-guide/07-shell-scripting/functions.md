# 함수

## 목차
- [함수 정의](#함수-정의)
- [함수 인자](#함수-인자)
- [반환 값](#반환-값)
- [실전 함수 예제](#실전-함수-예제)

---

## 함수 정의

```bash
#!/bin/bash

# 방법 1
function greet {
    echo "Hello, World!"
}

# 방법 2 (권장)
greet() {
    echo "Hello, World!"
}

# 함수 호출
greet
```

---

## 함수 인자

```bash
#!/bin/bash

greet() {
    echo "Hello, $1!"
}

greet "Alice"  # Hello, Alice!

# 여러 인자
add() {
    local sum=$(($1 + $2))
    echo "$sum"
}

result=$(add 5 3)
echo "Result: $result"
```

---

## 반환 값

```bash
#!/bin/bash

# return (종료 상태 0-255)
is_root() {
    if [ "$EUID" -eq 0 ]; then
        return 0  # 성공
    else
        return 1  # 실패
    fi
}

if is_root; then
    echo "Running as root"
else
    echo "Not root"
fi

# echo로 값 반환
get_date() {
    echo $(date +%Y%m%d)
}

today=$(get_date)
echo "Today: $today"
```

---

## 실전 함수 예제

```bash
#!/bin/bash

# 로그 함수
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a script.log
}

# 에러 처리
error_exit() {
    log "ERROR: $1"
    exit 1
}

# 백업 함수
backup_file() {
    local file=$1
    local backup="${file}.backup_$(date +%Y%m%d)"

    if [ -f "$file" ]; then
        cp "$file" "$backup"
        log "Backed up: $file -> $backup"
    else
        error_exit "File not found: $file"
    fi
}

# 메인 스크립트
log "Script started"
backup_file "important.txt"
log "Script completed"
```

---

[다음: 고급 기법 →](advanced.md)

[← 제어 구조로 돌아가기](control-flow.md)

[← 목차로 돌아가기](../README.md)
