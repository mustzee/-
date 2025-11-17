#!/usr/bin/env python3
"""
설치 확인 스크립트
필요한 모든 라이브러리가 제대로 설치되었는지 확인합니다.
"""

def check_library(name, import_name=None):
    """라이브러리 설치 여부 확인"""
    if import_name is None:
        import_name = name

    try:
        __import__(import_name)
        print(f"✅ {name} - 설치됨")
        return True
    except ImportError:
        print(f"❌ {name} - 설치 안됨")
        print(f"   설치: pip install {name}")
        return False


def main():
    print("="*60)
    print("🔍 라이브러리 설치 확인")
    print("="*60)

    libraries = [
        ("numpy", "numpy"),
        ("pandas", "pandas"),
        ("dask", "dask"),
        ("matplotlib", "matplotlib"),
        ("psutil", "psutil"),
    ]

    results = []
    for name, import_name in libraries:
        results.append(check_library(name, import_name))

    print("\n" + "="*60)
    if all(results):
        print("✅ 모든 라이브러리가 설치되었습니다!")
        print("👉 다음 단계로 진행할 수 있습니다.")
    else:
        print("❌ 일부 라이브러리가 설치되지 않았습니다.")
        print("👉 위의 설치 명령을 실행하세요.")
    print("="*60)


if __name__ == "__main__":
    main()
