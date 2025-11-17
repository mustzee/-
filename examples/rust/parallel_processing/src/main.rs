use rayon::prelude::*;
use std::time::Instant;
use std::sync::atomic::{AtomicUsize, Ordering};

/// 1. 기본 병렬 이터레이터
fn demonstrate_basic_parallelism() {
    println!("{}", "=".repeat(60));
    println!("1. 기본 병렬 이터레이터");
    println!("{}", "=".repeat(60));

    let data: Vec<i32> = (0..10_000_000).collect();

    // 순차 처리
    let start = Instant::now();
    let sum_seq: i32 = data.iter().map(|&x| x * 2).sum();
    let seq_duration = start.elapsed();

    // 병렬 처리
    let start = Instant::now();
    let sum_par: i32 = data.par_iter().map(|&x| x * 2).sum();
    let par_duration = start.elapsed();

    println!("\n크기: {} 원소", data.len());
    println!("순차 처리: {:.3}초", seq_duration.as_secs_f64());
    println!("병렬 처리: {:.3}초 ({:.2}x)",
             par_duration.as_secs_f64(),
             seq_duration.as_secs_f64() / par_duration.as_secs_f64());
    println!("결과 검증: {}", sum_seq == sum_par);
    println!();
}

/// 2. 복잡한 연산
fn demonstrate_complex_operations() {
    println!("{}", "=".repeat(60));
    println!("2. 복잡한 연산");
    println!("{}", "=".repeat(60));

    let size = 5_000_000;
    let data: Vec<f64> = (0..size).map(|i| i as f64).collect();

    // 순차 처리
    let start = Instant::now();
    let result_seq: Vec<f64> = data
        .iter()
        .map(|&x| (x.sin() * x.cos()).abs().sqrt())
        .collect();
    let seq_duration = start.elapsed();

    // 병렬 처리
    let start = Instant::now();
    let result_par: Vec<f64> = data
        .par_iter()
        .map(|&x| (x.sin() * x.cos()).abs().sqrt())
        .collect();
    let par_duration = start.elapsed();

    println!("\n배열 크기: {} 원소", size);
    println!("순차 처리: {:.3}초", seq_duration.as_secs_f64());
    println!("병렬 처리: {:.3}초 ({:.2}x)",
             par_duration.as_secs_f64(),
             seq_duration.as_secs_f64() / par_duration.as_secs_f64());

    // 결과 검증
    let diff: f64 = result_seq
        .iter()
        .zip(result_par.iter())
        .map(|(a, b)| (a - b).abs())
        .sum();
    println!("결과 차이: {:.2e}", diff);
    println!();
}

/// 3. 몬테카를로 π 추정
fn monte_carlo_pi(samples: usize) -> f64 {
    use rand::Rng;

    let inside = (0..samples)
        .into_par_iter()
        .map(|_| {
            let mut rng = rand::thread_rng();
            let x: f64 = rng.gen();
            let y: f64 = rng.gen();
            if x * x + y * y <= 1.0 { 1 } else { 0 }
        })
        .sum::<usize>();

    4.0 * inside as f64 / samples as f64
}

fn demonstrate_monte_carlo() {
    println!("{}", "=".repeat(60));
    println!("3. 몬테카를로 π 추정");
    println!("{}", "=".repeat(60));

    let samples = 100_000_000;

    println!("\n샘플 수: {}", samples);

    let start = Instant::now();
    let pi_estimate = monte_carlo_pi(samples);
    let duration = start.elapsed();

    println!("처리 시간: {:.3}초", duration.as_secs_f64());
    println!("π 추정값: {:.6}", pi_estimate);
    println!("실제 π: {:.6}", std::f64::consts::PI);
    println!("오차: {:.6}", (pi_estimate - std::f64::consts::PI).abs());
    println!("처리 속도: {:.2}M 샘플/초",
             samples as f64 / duration.as_secs_f64() / 1_000_000.0);
    println!();
}

/// 4. 필터와 맵 체인
fn demonstrate_filter_map() {
    println!("{}", "=".repeat(60));
    println!("4. 필터와 맵 체인");
    println!("{}", "=".repeat(60));

    let data: Vec<i32> = (0..10_000_000).collect();

    // 순차 처리
    let start = Instant::now();
    let result_seq: Vec<i32> = data
        .iter()
        .filter(|&&x| x % 2 == 0)
        .map(|&x| x * x)
        .filter(|&x| x % 3 == 0)
        .collect();
    let seq_duration = start.elapsed();

    // 병렬 처리
    let start = Instant::now();
    let result_par: Vec<i32> = data
        .par_iter()
        .filter(|&&x| x % 2 == 0)
        .map(|&x| x * x)
        .filter(|&x| x % 3 == 0)
        .collect();
    let par_duration = start.elapsed();

    println!("\n원본 크기: {} 원소", data.len());
    println!("결과 크기: {} 원소", result_seq.len());
    println!("순차 처리: {:.3}초", seq_duration.as_secs_f64());
    println!("병렬 처리: {:.3}초 ({:.2}x)",
             par_duration.as_secs_f64(),
             seq_duration.as_secs_f64() / par_duration.as_secs_f64());
    println!();
}

/// 5. 리덕션 연산
fn demonstrate_reduction() {
    println!("{}", "=".repeat(60));
    println!("5. 리덕션 연산");
    println!("{}", "=".repeat(60));

    let size = 50_000_000;
    let data: Vec<f64> = (0..size).map(|i| (i as f64).sin()).collect();

    println!("\n배열 크기: {} 원소", size);

    // 합계
    let start = Instant::now();
    let sum_seq: f64 = data.iter().sum();
    let sum_seq_time = start.elapsed();

    let start = Instant::now();
    let sum_par: f64 = data.par_iter().sum();
    let sum_par_time = start.elapsed();

    println!("\n합계:");
    println!("  순차: {:.3}초", sum_seq_time.as_secs_f64());
    println!("  병렬: {:.3}초 ({:.2}x)",
             sum_par_time.as_secs_f64(),
             sum_seq_time.as_secs_f64() / sum_par_time.as_secs_f64());
    println!("  차이: {:.2e}", (sum_seq - sum_par).abs());

    // 최대값
    let start = Instant::now();
    let max_seq = data.iter().cloned().fold(f64::NEG_INFINITY, f64::max);
    let max_seq_time = start.elapsed();

    let start = Instant::now();
    let max_par = data.par_iter().cloned().reduce(|| f64::NEG_INFINITY, f64::max);
    let max_par_time = start.elapsed();

    println!("\n최대값:");
    println!("  순차: {:.3}초", max_seq_time.as_secs_f64());
    println!("  병렬: {:.3}초 ({:.2}x)",
             max_par_time.as_secs_f64(),
             max_seq_time.as_secs_f64() / max_par_time.as_secs_f64());
    println!("  차이: {:.2e}", (max_seq - max_par).abs());
    println!();
}

/// 6. 청크 처리
fn demonstrate_chunks() {
    println!("{}", "=".repeat(60));
    println!("6. 청크 처리");
    println!("{}", "=".repeat(60));

    let size = 10_000_000;
    let data: Vec<f64> = (0..size).map(|i| i as f64).collect();
    let chunk_size = 10_000;

    println!("\n배열 크기: {} 원소", size);
    println!("청크 크기: {} 원소", chunk_size);

    // 청크별 처리
    let start = Instant::now();
    let chunk_sums: Vec<f64> = data
        .par_chunks(chunk_size)
        .map(|chunk| chunk.iter().map(|&x| x.sin()).sum())
        .collect();
    let total: f64 = chunk_sums.iter().sum();
    let duration = start.elapsed();

    println!("\n청크 수: {}", chunk_sums.len());
    println!("처리 시간: {:.3}초", duration.as_secs_f64());
    println!("총합: {:.2e}", total);
    println!();
}

/// 7. 행렬 곱셈 (간단한 버전)
fn demonstrate_matrix_multiplication() {
    println!("{}", "=".repeat(60));
    println!("7. 행렬 곱셈");
    println!("{}", "=".repeat(60));

    let size = 500;
    let a: Vec<Vec<f64>> = (0..size)
        .map(|_| (0..size).map(|_| rand::random::<f64>()).collect())
        .collect();
    let b: Vec<Vec<f64>> = (0..size)
        .map(|_| (0..size).map(|_| rand::random::<f64>()).collect())
        .collect();

    println!("\n행렬 크기: {}x{}", size, size);

    // 병렬 행렬 곱셈
    let start = Instant::now();
    let c: Vec<Vec<f64>> = (0..size)
        .into_par_iter()
        .map(|i| {
            (0..size)
                .map(|j| {
                    (0..size).map(|k| a[i][k] * b[k][j]).sum()
                })
                .collect()
        })
        .collect();
    let duration = start.elapsed();

    println!("처리 시간: {:.3}초", duration.as_secs_f64());
    println!("결과 행렬 크기: {}x{}", c.len(), c[0].len());
    println!();
}

/// 8. 커스텀 스레드 풀
fn demonstrate_custom_threadpool() {
    println!("{}", "=".repeat(60));
    println!("8. 커스텀 스레드 풀");
    println!("{}", "=".repeat(60));

    let data: Vec<i32> = (0..10_000_000).collect();

    println!("\nCPU 코어 수: {}", num_cpus::get());
    println!("\n스레드 수별 성능:");

    for num_threads in [1, 2, 4, 8] {
        if num_threads > num_cpus::get() {
            break;
        }

        let pool = rayon::ThreadPoolBuilder::new()
            .num_threads(num_threads)
            .build()
            .unwrap();

        let start = Instant::now();
        let sum: i32 = pool.install(|| {
            data.par_iter().map(|&x| x * 2).sum()
        });
        let duration = start.elapsed();

        println!("  {} 스레드: {:.3}초", num_threads, duration.as_secs_f64());
    }
    println!();
}

/// 9. 실전 예제: 이미지 블러
fn box_blur_parallel(image: &[Vec<u8>], blur_size: usize) -> Vec<Vec<u8>> {
    let height = image.len();
    let width = image[0].len();
    let half = blur_size / 2;

    (0..height)
        .into_par_iter()
        .map(|i| {
            (0..width)
                .map(|j| {
                    let i_min = i.saturating_sub(half);
                    let i_max = (i + half + 1).min(height);
                    let j_min = j.saturating_sub(half);
                    let j_max = (j + half + 1).min(width);

                    let sum: u32 = (i_min..i_max)
                        .flat_map(|ii| (j_min..j_max).map(move |jj| image[ii][jj] as u32))
                        .sum();

                    let count = (i_max - i_min) * (j_max - j_min);
                    (sum / count as u32) as u8
                })
                .collect()
        })
        .collect()
}

fn demonstrate_image_blur() {
    println!("{}", "=".repeat(60));
    println!("9. 실전 예제: 이미지 블러");
    println!("{}", "=".repeat(60));

    let height = 1000;
    let width = 1000;
    let blur_size = 5;

    let image: Vec<Vec<u8>> = (0..height)
        .map(|_| (0..width).map(|_| rand::random::<u8>()).collect())
        .collect();

    println!("\n이미지 크기: {}x{}", height, width);
    println!("블러 크기: {}x{}", blur_size, blur_size);

    let start = Instant::now();
    let blurred = box_blur_parallel(&image, blur_size);
    let duration = start.elapsed();

    println!("처리 시간: {:.3}초", duration.as_secs_f64());
    println!("결과 크기: {}x{}", blurred.len(), blurred[0].len());
    println!();
}

/// 10. 스케일링 테스트
fn demonstrate_scaling() {
    println!("{}", "=".repeat(60));
    println!("10. 스케일링 테스트");
    println!("{}", "=".repeat(60));

    let size = 50_000_000;
    let data: Vec<f64> = (0..size).map(|i| i as f64).collect();

    println!("\n작업 크기: {} 원소", size);
    println!("사용 가능 코어: {}", num_cpus::get());
    println!("\n스레드 수별 성능:");
    println!("{}", "-".repeat(60));

    let base_time = {
        let pool = rayon::ThreadPoolBuilder::new()
            .num_threads(1)
            .build()
            .unwrap();

        let start = Instant::now();
        pool.install(|| {
            data.par_iter().map(|&x| (x.sin() * x.cos()).abs().sqrt()).sum::<f64>()
        });
        start.elapsed().as_secs_f64()
    };

    for num_threads in [1, 2, 4, 8] {
        if num_threads > num_cpus::get() {
            break;
        }

        let pool = rayon::ThreadPoolBuilder::new()
            .num_threads(num_threads)
            .build()
            .unwrap();

        let start = Instant::now();
        pool.install(|| {
            data.par_iter().map(|&x| (x.sin() * x.cos()).abs().sqrt()).sum::<f64>()
        });
        let duration = start.elapsed().as_secs_f64();

        let speedup = base_time / duration;
        let efficiency = speedup / num_threads as f64 * 100.0;

        println!("  {:2} 스레드: {:.3}초 | 속도향상: {:.2}x | 효율: {:.1}%",
                 num_threads, duration, speedup, efficiency);
    }
    println!();
}

fn main() {
    println!("{}", "=".repeat(60));
    println!("Rust Rayon 병렬 처리 데모");
    println!("{}", "=".repeat(60));
    println!("CPU 코어: {}", num_cpus::get());
    println!();

    demonstrate_basic_parallelism();
    demonstrate_complex_operations();
    demonstrate_monte_carlo();
    demonstrate_filter_map();
    demonstrate_reduction();
    demonstrate_chunks();
    demonstrate_matrix_multiplication();
    demonstrate_custom_threadpool();
    demonstrate_image_blur();
    demonstrate_scaling();

    println!("{}", "=".repeat(60));
    println!("Rust Rayon 핵심 정리");
    println!("{}", "=".repeat(60));
    println!(r#"
1. Rayon의 장점
   - 거의 완벽한 병렬화 효율
   - 데이터 레이스 방지 (컴파일 타임)
   - 간단한 API (par_iter)
   - Zero-cost abstraction

2. 주요 메서드
   - par_iter(): 병렬 이터레이터
   - map(): 변환
   - filter(): 필터링
   - reduce(): 리덕션
   - sum(), max(), min(): 집계

3. 성능 특성
   - C++ 수준의 성능
   - 낮은 오버헤드
   - 우수한 확장성
   - 메모리 안전성

4. 사용 팁
   - 작은 작업은 순차 처리
   - 적절한 청크 크기 선택
   - 커스텀 스레드 풀로 제어
   - 중첩 병렬화 가능

5. 컴파일 및 실행
   cargo build --release
   cargo run --release

   ⚠️  --release 플래그 필수 (최적화)

6. 다음 단계
   - 비동기 병렬성 (async/await)
   - crossbeam 채널
   - 분산 처리 (MPI, etc.)
"#);
}
