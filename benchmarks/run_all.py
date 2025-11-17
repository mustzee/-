#!/usr/bin/env python3
"""
모든 언어의 병렬 처리 벤치마크 실행
결과를 비교하고 시각화
"""

import subprocess
import time
import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Tuple
import platform


class BenchmarkRunner:
    def __init__(self):
        self.results = {}
        self.project_root = Path(__file__).parent.parent
        self.results_dir = Path(__file__).parent / "results"
        self.results_dir.mkdir(exist_ok=True)

    def run_command(self, cmd: List[str], cwd: Path = None) -> Tuple[float, str]:
        """명령 실행 및 시간 측정"""
        print(f"  실행 중: {' '.join(cmd)}")
        start = time.time()
        try:
            result = subprocess.run(
                cmd,
                cwd=cwd or self.project_root,
                capture_output=True,
                text=True,
                timeout=300
            )
            duration = time.time() - start
            return duration, result.stdout + result.stderr
        except subprocess.TimeoutExpired:
            return -1, "Timeout"
        except Exception as e:
            return -1, str(e)

    def benchmark_python(self):
        """Python 벤치마크"""
        print("\n" + "="*60)
        print("Python 벤치마크")
        print("="*60)

        examples_dir = self.project_root / "examples" / "python"
        scripts = ["01_numpy_basics.py", "02_parallel_concepts.py", "03_multiprocessing_advanced.py"]

        results = []
        for script in scripts:
            script_path = examples_dir / script
            if script_path.exists():
                duration, output = self.run_command(
                    ["python3", str(script_path)],
                    cwd=examples_dir
                )
                results.append({
                    "script": script,
                    "duration": duration,
                    "status": "success" if duration > 0 else "failed"
                })
                print(f"  {script}: {duration:.2f}초")
            else:
                print(f"  {script}: 파일 없음")

        self.results["python"] = {
            "language": "Python",
            "version": self._get_python_version(),
            "results": results
        }

    def benchmark_julia(self):
        """Julia 벤치마크"""
        print("\n" + "="*60)
        print("Julia 벤치마크")
        print("="*60)

        if not self._check_command("julia"):
            print("  Julia가 설치되지 않음")
            self.results["julia"] = {"status": "not_installed"}
            return

        examples_dir = self.project_root / "examples" / "julia"
        script = "01_parallel_julia.jl"

        duration, output = self.run_command(
            ["julia", f"--threads={os.cpu_count()}", str(script)],
            cwd=examples_dir
        )

        self.results["julia"] = {
            "language": "Julia",
            "version": self._get_julia_version(),
            "duration": duration,
            "status": "success" if duration > 0 else "failed"
        }
        print(f"  실행 시간: {duration:.2f}초")

    def benchmark_rust(self):
        """Rust 벤치마크"""
        print("\n" + "="*60)
        print("Rust 벤치마크")
        print("="*60)

        if not self._check_command("cargo"):
            print("  Rust가 설치되지 않음")
            self.results["rust"] = {"status": "not_installed"}
            return

        project_dir = self.project_root / "examples" / "rust" / "parallel_processing"

        # 빌드
        print("  빌드 중...")
        build_duration, _ = self.run_command(
            ["cargo", "build", "--release"],
            cwd=project_dir
        )

        # 실행
        duration, output = self.run_command(
            ["cargo", "run", "--release"],
            cwd=project_dir
        )

        self.results["rust"] = {
            "language": "Rust",
            "version": self._get_rust_version(),
            "build_duration": build_duration,
            "run_duration": duration,
            "status": "success" if duration > 0 else "failed"
        }
        print(f"  빌드: {build_duration:.2f}초, 실행: {duration:.2f}초")

    def benchmark_go(self):
        """Go 벤치마크"""
        print("\n" + "="*60)
        print("Go 벤치마크")
        print("="*60)

        if not self._check_command("go"):
            print("  Go가 설치되지 않음")
            self.results["go"] = {"status": "not_installed"}
            return

        project_dir = self.project_root / "examples" / "go"

        duration, output = self.run_command(
            ["go", "run", "main.go"],
            cwd=project_dir
        )

        self.results["go"] = {
            "language": "Go",
            "version": self._get_go_version(),
            "duration": duration,
            "status": "success" if duration > 0 else "failed"
        }
        print(f"  실행 시간: {duration:.2f}초")

    def benchmark_cpp(self):
        """C++ 벤치마크"""
        print("\n" + "="*60)
        print("C++ 벤치마크")
        print("="*60)

        if not self._check_command("g++"):
            print("  g++이 설치되지 않음")
            self.results["cpp"] = {"status": "not_installed"}
            return

        project_dir = self.project_root / "examples" / "cpp"

        # 빌드
        print("  빌드 중...")
        build_duration, _ = self.run_command(
            ["make", "clean"],
            cwd=project_dir
        )
        build_duration, _ = self.run_command(
            ["make"],
            cwd=project_dir
        )

        # 실행
        duration, output = self.run_command(
            ["./parallel_demo"],
            cwd=project_dir
        )

        self.results["cpp"] = {
            "language": "C++",
            "version": self._get_cpp_version(),
            "build_duration": build_duration,
            "run_duration": duration,
            "status": "success" if duration > 0 else "failed"
        }
        print(f"  빌드: {build_duration:.2f}초, 실행: {duration:.2f}초")

    def _check_command(self, cmd: str) -> bool:
        """명령어 사용 가능 여부 확인"""
        try:
            subprocess.run([cmd, "--version"], capture_output=True, timeout=5)
            return True
        except:
            return False

    def _get_python_version(self) -> str:
        try:
            result = subprocess.run(
                ["python3", "--version"],
                capture_output=True,
                text=True
            )
            return result.stdout.strip()
        except:
            return "unknown"

    def _get_julia_version(self) -> str:
        try:
            result = subprocess.run(
                ["julia", "--version"],
                capture_output=True,
                text=True
            )
            return result.stdout.strip()
        except:
            return "unknown"

    def _get_rust_version(self) -> str:
        try:
            result = subprocess.run(
                ["rustc", "--version"],
                capture_output=True,
                text=True
            )
            return result.stdout.strip()
        except:
            return "unknown"

    def _get_go_version(self) -> str:
        try:
            result = subprocess.run(
                ["go", "version"],
                capture_output=True,
                text=True
            )
            return result.stdout.strip()
        except:
            return "unknown"

    def _get_cpp_version(self) -> str:
        try:
            result = subprocess.run(
                ["g++", "--version"],
                capture_output=True,
                text=True
            )
            return result.stdout.split('\n')[0]
        except:
            return "unknown"

    def save_results(self):
        """결과 저장"""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        output_file = self.results_dir / f"benchmark_{timestamp}.json"

        # 시스템 정보 추가
        self.results["system"] = {
            "platform": platform.platform(),
            "processor": platform.processor(),
            "cpu_count": os.cpu_count(),
            "timestamp": timestamp
        }

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)

        print(f"\n결과 저장됨: {output_file}")
        return output_file

    def print_summary(self):
        """결과 요약 출력"""
        print("\n" + "="*60)
        print("벤치마크 요약")
        print("="*60)

        print(f"\n시스템: {self.results['system']['platform']}")
        print(f"CPU 코어: {self.results['system']['cpu_count']}")
        print("\n언어별 결과:")
        print("-" * 60)

        for lang in ["python", "julia", "rust", "go", "cpp"]:
            if lang in self.results:
                result = self.results[lang]
                if result.get("status") == "not_installed":
                    print(f"{lang.upper():<10} - 설치되지 않음")
                elif "run_duration" in result:
                    print(f"{lang.upper():<10} - 실행: {result['run_duration']:.2f}초")
                elif "duration" in result:
                    print(f"{lang.upper():<10} - 실행: {result['duration']:.2f}초")

        print("\n" + "="*60)

    def run_all(self):
        """모든 벤치마크 실행"""
        print("="*60)
        print("병렬 처리 벤치마크 스위트")
        print("="*60)
        print(f"CPU 코어: {os.cpu_count()}")
        print(f"플랫폼: {platform.platform()}")

        self.benchmark_python()
        self.benchmark_julia()
        self.benchmark_rust()
        self.benchmark_go()
        self.benchmark_cpp()

        output_file = self.save_results()
        self.print_summary()

        print(f"\n상세 결과: {output_file}")


def main():
    runner = BenchmarkRunner()
    runner.run_all()


if __name__ == "__main__":
    main()
