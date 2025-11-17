#!/usr/bin/env python3
"""
첫 번째 프로그램: 환영 메시지와 시스템 정보
"""

import os
import platform
import psutil


def get_system_info():
    """시스템 정보를 수집합니다"""
    cpu_count = os.cpu_count()
    memory_gb = psutil.virtual_memory().total / (1024**3)
    os_name = platform.system()

    return {
        'cpu_count': cpu_count,
        'memory_gb': memory_gb,
        'os_name': os_name
    }


def main():
    print("🎉 환영합니다! 병렬처리의 세계로!")
    print()

    # 시스템 정보 수집
    info = get_system_info()

    print("💻 당신의 컴퓨터 정보:")
    print(f"   - CPU 코어 수: {info['cpu_count']}")
    print(f"   - 사용 가능한 메모리: {info['memory_gb']:.1f} GB")
    print(f"   - 운영체제: {info['os_name']}")
    print()

    # 병렬처리 가능성 평가
    if info['cpu_count'] >= 4:
        print("✅ 병렬처리에 적합한 CPU입니다!")
    else:
        print("⚠️  CPU 코어가 적지만 괜찮습니다. 학습은 가능합니다!")

    if info['memory_gb'] >= 8:
        print("✅ 충분한 메모리가 있습니다!")
    else:
        print("⚠️  메모리가 적지만 작은 데이터셋으로 학습 가능합니다!")

    print()
    print("="*60)
    print("✅ 모든 라이브러리가 정상적으로 설치되었습니다!")
    print("👉 이제 Step 1로 넘어갈 준비가 되었습니다!")
    print("="*60)


if __name__ == "__main__":
    main()
