#!/bin/bash
# backup.sh - 파일 백업 스크립트

set -euo pipefail

# 설정
SOURCE="/home/user"
DEST="/backup"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="backup_$DATE.tar.gz"

# 백업 함수
backup() {
    echo "Starting backup..."
    tar -czf "$DEST/$BACKUP_FILE" "$SOURCE"
    echo "Backup completed: $BACKUP_FILE"
}

# 오래된 백업 삭제
cleanup() {
    echo "Cleaning up old backups..."
    find "$DEST" -name "backup_*.tar.gz" -mtime +30 -delete
}

# 메인
backup
cleanup
