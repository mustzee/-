/**
 * C++ OpenMP 병렬 처리 데모
 * 컴파일: g++ -fopenmp -O3 -o parallel_demo parallel_demo.cpp -lm
 * 실행: ./parallel_demo
 */

#include <iostream>
#include <vector>
#include <cmath>
#include <chrono>
#include <random>
#include <iomanip>
#include <omp.h>

using namespace std;
using namespace std::chrono;

// 반복 문자열 생성
string repeat(const string& str, int n) {
    string result;
    for (int i = 0; i < n; ++i) result += str;
    return result;
}

// 1. 기본 병렬 루프
void demonstrate_basic_parallel() {
    cout << repeat("=", 60) << endl;
    cout << "1. 기본 병렬 루프 (#pragma omp parallel for)" << endl;
    cout << repeat("=", 60) << endl;

    const int size = 100'000'000;

    // 순차 실행
    auto start = high_resolution_clock::now();
    double sum_seq = 0.0;
    for (int i = 0; i < size; ++i) {
        sum_seq += sin(i) * cos(i);
    }
    auto seq_duration = duration_cast<milliseconds>(high_resolution_clock::now() - start);

    // 병렬 실행
    start = high_resolution_clock::now();
    double sum_par = 0.0;
    #pragma omp parallel for reduction(+:sum_par)
    for (int i = 0; i < size; ++i) {
        sum_par += sin(i) * cos(i);
    }
    auto par_duration = duration_cast<milliseconds>(high_resolution_clock::now() - start);

    cout << "\n크기: " << size << " 원소" << endl;
    cout << "순차 처리: " << seq_duration.count() / 1000.0 << "초" << endl;
    cout << "병렬 처리: " << par_duration.count() / 1000.0 << "초 ("
         << fixed << setprecision(2) << (double)seq_duration.count() / par_duration.count() << "x)" << endl;
    cout << "차이: " << scientific << abs(sum_seq - sum_par) << endl << endl;
}

// 2. 배열 연산
void demonstrate_array_operations() {
    cout << repeat("=", 60) << endl;
    cout << "2. 배열 연산" << endl;
    cout << repeat("=", 60) << endl;

    const int size = 10'000'000;
    vector<double> data(size);
    vector<double> result_seq(size);
    vector<double> result_par(size);

    // 데이터 초기화
    for (int i = 0; i < size; ++i) {
        data[i] = i;
    }

    // 순차 처리
    auto start = high_resolution_clock::now();
    for (int i = 0; i < size; ++i) {
        result_seq[i] = sqrt(abs(sin(data[i]) * cos(data[i])));
    }
    auto seq_duration = duration_cast<milliseconds>(high_resolution_clock::now() - start);

    // 병렬 처리
    start = high_resolution_clock::now();
    #pragma omp parallel for
    for (int i = 0; i < size; ++i) {
        result_par[i] = sqrt(abs(sin(data[i]) * cos(data[i])));
    }
    auto par_duration = duration_cast<milliseconds>(high_resolution_clock::now() - start);

    // 검증
    double diff = 0.0;
    for (int i = 0; i < size; ++i) {
        diff += abs(result_seq[i] - result_par[i]);
    }

    cout << "\n배열 크기: " << size << " 원소" << endl;
    cout << "순차 처리: " << seq_duration.count() / 1000.0 << "초" << endl;
    cout << "병렬 처리: " << par_duration.count() / 1000.0 << "초 ("
         << fixed << setprecision(2) << (double)seq_duration.count() / par_duration.count() << "x)" << endl;
    cout << "결과 차이: " << scientific << diff << endl << endl;
}

// 3. 몬테카를로 π 추정
void demonstrate_monte_carlo() {
    cout << repeat("=", 60) << endl;
    cout << "3. 몬테카를로 π 추정" << endl;
    cout << repeat("=", 60) << endl;

    const long long samples = 100'000'000;

    cout << "\n샘플 수: " << samples << endl;

    auto start = high_resolution_clock::now();
    long long inside = 0;

    #pragma omp parallel
    {
        // 각 스레드마다 독립적인 난수 생성기
        unsigned int seed = omp_get_thread_num();
        long long local_inside = 0;

        #pragma omp for
        for (long long i = 0; i < samples; ++i) {
            double x = (double)rand_r(&seed) / RAND_MAX;
            double y = (double)rand_r(&seed) / RAND_MAX;
            if (x * x + y * y <= 1.0) {
                local_inside++;
            }
        }

        #pragma omp atomic
        inside += local_inside;
    }

    double pi_estimate = 4.0 * inside / samples;
    auto duration = duration_cast<milliseconds>(high_resolution_clock::now() - start);

    cout << "처리 시간: " << duration.count() / 1000.0 << "초" << endl;
    cout << fixed << setprecision(6);
    cout << "π 추정값: " << pi_estimate << endl;
    cout << "실제 π: " << M_PI << endl;
    cout << "오차: " << abs(pi_estimate - M_PI) << endl;
    cout << "처리 속도: " << setprecision(2) << (samples / (duration.count() / 1000.0)) / 1e6 << "M 샘플/초" << endl << endl;
}

// 4. 리덕션 연산
void demonstrate_reduction() {
    cout << repeat("=", 60) << endl;
    cout << "4. 리덕션 연산" << endl;
    cout << repeat("=", 60) << endl;

    const int size = 50'000'000;
    vector<double> data(size);

    // 데이터 초기화
    for (int i = 0; i < size; ++i) {
        data[i] = sin(i);
    }

    cout << "\n배열 크기: " << size << " 원소" << endl;

    // 합계
    auto start = high_resolution_clock::now();
    double sum_seq = 0.0;
    for (int i = 0; i < size; ++i) {
        sum_seq += data[i];
    }
    auto sum_seq_time = duration_cast<milliseconds>(high_resolution_clock::now() - start);

    start = high_resolution_clock::now();
    double sum_par = 0.0;
    #pragma omp parallel for reduction(+:sum_par)
    for (int i = 0; i < size; ++i) {
        sum_par += data[i];
    }
    auto sum_par_time = duration_cast<milliseconds>(high_resolution_clock::now() - start);

    cout << "\n합계:" << endl;
    cout << "  순차: " << sum_seq_time.count() / 1000.0 << "초" << endl;
    cout << "  병렬: " << sum_par_time.count() / 1000.0 << "초 ("
         << fixed << setprecision(2) << (double)sum_seq_time.count() / sum_par_time.count() << "x)" << endl;
    cout << "  차이: " << scientific << abs(sum_seq - sum_par) << endl;

    // 최대값
    start = high_resolution_clock::now();
    double max_seq = data[0];
    for (int i = 1; i < size; ++i) {
        if (data[i] > max_seq) max_seq = data[i];
    }
    auto max_seq_time = duration_cast<milliseconds>(high_resolution_clock::now() - start);

    start = high_resolution_clock::now();
    double max_par = data[0];
    #pragma omp parallel for reduction(max:max_par)
    for (int i = 1; i < size; ++i) {
        if (data[i] > max_par) max_par = data[i];
    }
    auto max_par_time = duration_cast<milliseconds>(high_resolution_clock::now() - start);

    cout << "\n최대값:" << endl;
    cout << "  순차: " << max_seq_time.count() / 1000.0 << "초" << endl;
    cout << "  병렬: " << max_par_time.count() / 1000.0 << "초 ("
         << fixed << setprecision(2) << (double)max_seq_time.count() / max_par_time.count() << "x)" << endl;
    cout << "  차이: " << scientific << abs(max_seq - max_par) << endl << endl;
}

// 5. 중첩 루프
void demonstrate_nested_loops() {
    cout << repeat("=", 60) << endl;
    cout << "5. 중첩 루프" << endl;
    cout << repeat("=", 60) << endl;

    const int rows = 5000;
    const int cols = 5000;

    vector<vector<double>> matrix(rows, vector<double>(cols));
    vector<double> result_seq(rows, 0.0);
    vector<double> result_par(rows, 0.0);

    // 초기화
    for (int i = 0; i < rows; ++i) {
        for (int j = 0; j < cols; ++j) {
            matrix[i][j] = sin(i) * cos(j);
        }
    }

    cout << "\n행렬 크기: " << rows << "x" << cols << endl;

    // 순차 처리
    auto start = high_resolution_clock::now();
    for (int i = 0; i < rows; ++i) {
        for (int j = 0; j < cols; ++j) {
            result_seq[i] += matrix[i][j];
        }
    }
    auto seq_duration = duration_cast<milliseconds>(high_resolution_clock::now() - start);

    // 병렬 처리
    start = high_resolution_clock::now();
    #pragma omp parallel for
    for (int i = 0; i < rows; ++i) {
        for (int j = 0; j < cols; ++j) {
            result_par[i] += matrix[i][j];
        }
    }
    auto par_duration = duration_cast<milliseconds>(high_resolution_clock::now() - start);

    cout << "순차 처리: " << seq_duration.count() / 1000.0 << "초" << endl;
    cout << "병렬 처리: " << par_duration.count() / 1000.0 << "초 ("
         << fixed << setprecision(2) << (double)seq_duration.count() / par_duration.count() << "x)" << endl << endl;
}

// 6. 행렬 곱셈
void demonstrate_matrix_multiplication() {
    cout << repeat("=", 60) << endl;
    cout << "6. 행렬 곱셈" << endl;
    cout << repeat("=", 60) << endl;

    const int size = 500;

    vector<vector<double>> A(size, vector<double>(size));
    vector<vector<double>> B(size, vector<double>(size));
    vector<vector<double>> C(size, vector<double>(size, 0.0));

    // 초기화
    random_device rd;
    mt19937 gen(rd());
    uniform_real_distribution<> dis(0.0, 1.0);

    for (int i = 0; i < size; ++i) {
        for (int j = 0; j < size; ++j) {
            A[i][j] = dis(gen);
            B[i][j] = dis(gen);
        }
    }

    cout << "\n행렬 크기: " << size << "x" << size << endl;

    auto start = high_resolution_clock::now();

    #pragma omp parallel for collapse(2)
    for (int i = 0; i < size; ++i) {
        for (int j = 0; j < size; ++j) {
            double sum = 0.0;
            for (int k = 0; k < size; ++k) {
                sum += A[i][k] * B[k][j];
            }
            C[i][j] = sum;
        }
    }

    auto duration = duration_cast<milliseconds>(high_resolution_clock::now() - start);

    cout << "처리 시간: " << duration.count() / 1000.0 << "초" << endl;
    cout << "결과 행렬 크기: " << C.size() << "x" << C[0].size() << endl << endl;
}

// 7. 동적 스케줄링
void demonstrate_dynamic_scheduling() {
    cout << repeat("=", 60) << endl;
    cout << "7. 동적 스케줄링" << endl;
    cout << repeat("=", 60) << endl;

    const int size = 100;
    vector<double> work_times(size);

    // 불균형한 작업 부하 (i가 클수록 작업 시간 증가)
    for (int i = 0; i < size; ++i) {
        work_times[i] = 0.0;
    }

    cout << "\n작업 수: " << size << " (불균형한 부하)" << endl;

    // Static 스케줄링
    auto start = high_resolution_clock::now();
    #pragma omp parallel for schedule(static)
    for (int i = 0; i < size; ++i) {
        double sum = 0.0;
        // i가 클수록 더 많은 작업
        for (int j = 0; j < i * 100'000; ++j) {
            sum += sin(j) * cos(j);
        }
        work_times[i] = sum;
    }
    auto static_duration = duration_cast<milliseconds>(high_resolution_clock::now() - start);

    // Dynamic 스케줄링
    start = high_resolution_clock::now();
    #pragma omp parallel for schedule(dynamic)
    for (int i = 0; i < size; ++i) {
        double sum = 0.0;
        for (int j = 0; j < i * 100'000; ++j) {
            sum += sin(j) * cos(j);
        }
        work_times[i] = sum;
    }
    auto dynamic_duration = duration_cast<milliseconds>(high_resolution_clock::now() - start);

    // Guided 스케줄링
    start = high_resolution_clock::now();
    #pragma omp parallel for schedule(guided)
    for (int i = 0; i < size; ++i) {
        double sum = 0.0;
        for (int j = 0; j < i * 100'000; ++j) {
            sum += sin(j) * cos(j);
        }
        work_times[i] = sum;
    }
    auto guided_duration = duration_cast<milliseconds>(high_resolution_clock::now() - start);

    cout << "Static 스케줄링: " << static_duration.count() / 1000.0 << "초" << endl;
    cout << "Dynamic 스케줄링: " << dynamic_duration.count() / 1000.0 << "초" << endl;
    cout << "Guided 스케줄링: " << guided_duration.count() / 1000.0 << "초" << endl;
    cout << "\n💡 불균형한 작업에는 dynamic/guided가 효과적" << endl << endl;
}

// 8. 스케일링 테스트
void demonstrate_scaling() {
    cout << repeat("=", 60) << endl;
    cout << "8. 스케일링 테스트" << endl;
    cout << repeat("=", 60) << endl;

    const int size = 100'000'000;
    double base_time = 0.0;

    int max_threads = omp_get_max_threads();
    cout << "\n작업 크기: " << size << " 원소" << endl;
    cout << "사용 가능 스레드: " << max_threads << endl;
    cout << "\n스레드 수별 성능:" << endl;
    cout << repeat("-", 60) << endl;

    vector<int> thread_counts = {1, 2, 4, 8};

    for (int num_threads : thread_counts) {
        if (num_threads > max_threads) break;

        omp_set_num_threads(num_threads);

        auto start = high_resolution_clock::now();
        double sum = 0.0;

        #pragma omp parallel for reduction(+:sum)
        for (int i = 0; i < size; ++i) {
            sum += sqrt(abs(sin(i) * cos(i)));
        }

        auto duration = duration_cast<milliseconds>(high_resolution_clock::now() - start);
        double time_sec = duration.count() / 1000.0;

        if (num_threads == 1) {
            base_time = time_sec;
        }

        double speedup = base_time / time_sec;
        double efficiency = speedup / num_threads * 100.0;

        cout << "  " << setw(2) << num_threads << " 스레드: "
             << fixed << setprecision(3) << time_sec << "초 | "
             << "속도향상: " << setprecision(2) << speedup << "x | "
             << "효율: " << setprecision(1) << efficiency << "%" << endl;
    }

    // 스레드 수 복원
    omp_set_num_threads(max_threads);
    cout << endl;
}

int main() {
    cout << repeat("=", 60) << endl;
    cout << "C++ OpenMP 병렬 처리 데모" << endl;
    cout << repeat("=", 60) << endl;
    cout << "최대 스레드 수: " << omp_get_max_threads() << endl << endl;

    demonstrate_basic_parallel();
    demonstrate_array_operations();
    demonstrate_monte_carlo();
    demonstrate_reduction();
    demonstrate_nested_loops();
    demonstrate_matrix_multiplication();
    demonstrate_dynamic_scheduling();
    demonstrate_scaling();

    cout << repeat("=", 60) << endl;
    cout << "C++ OpenMP 핵심 정리" << endl;
    cout << repeat("=", 60) << endl;
    cout << R"(
1. 기본 지시문
   #pragma omp parallel for   - 병렬 루프
   #pragma omp parallel        - 병렬 영역
   #pragma omp sections        - 섹션 분할

2. 리덕션
   reduction(+:sum)   - 합계
   reduction(*:prod)  - 곱셈
   reduction(max:val) - 최대값
   reduction(min:val) - 최소값

3. 스케줄링
   schedule(static)   - 정적 (균등 분배)
   schedule(dynamic)  - 동적 (작업 큐)
   schedule(guided)   - 가이드 (적응적)

4. 절
   private(var)       - 스레드별 복사
   shared(var)        - 공유 변수
   firstprivate(var)  - 초기값 복사
   lastprivate(var)   - 마지막 값 저장

5. 동기화
   #pragma omp barrier   - 동기화 지점
   #pragma omp critical  - 임계 영역
   #pragma omp atomic    - 원자적 연산

6. 컴파일 및 실행
   g++ -fopenmp -O3 -o parallel_demo parallel_demo.cpp -lm
   ./parallel_demo

   스레드 수 설정:
   export OMP_NUM_THREADS=8
   ./parallel_demo

7. 최적화 팁
   - 외부 루프를 병렬화
   - collapse로 중첩 루프 병렬화
   - 적절한 스케줄링 선택
   - false sharing 주의

8. 다음 단계
   - SIMD 벡터화 (#pragma omp simd)
   - 태스크 병렬성 (#pragma omp task)
   - GPU 오프로딩 (OpenMP 4.5+)
)" << endl;

    return 0;
}
