#!/bin/bash
# monitor.sh - 시스템 모니터링

# CPU 사용률 확인
check_cpu() {
    cpu=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)
    echo "CPU: $cpu%"

    if (( $(echo "$cpu > 80" | bc -l) )); then
        echo "WARNING: High CPU usage!"
    fi
}

# 메모리 확인
check_memory() {
    mem=$(free | grep Mem | awk '{printf("%.2f", $3/$2 * 100.0)}')
    echo "Memory: $mem%"
}

# 디스크 확인
check_disk() {
    df -h | grep '^/dev/' | while read line; do
        usage=$(echo $line | awk '{print $5}' | sed 's/%//')
        if [ $usage -gt 80 ]; then
            echo "WARNING: Disk usage high on $(echo $line | awk '{print $1}')"
        fi
    done
}

# 실행
check_cpu
check_memory
check_disk
