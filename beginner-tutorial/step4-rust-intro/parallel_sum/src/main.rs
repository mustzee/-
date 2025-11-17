use rayon::prelude::*;
use std::time::Instant;

fn main() {
    println!("{}", "=".repeat(60));
    println!("Rust 병렬 처리 with Rayon");
    println!("{}", "=".repeat(60));

    let data: Vec<i32> = (0..10_000_000).collect();

    println!("\n데이터 크기: {} 원소\n", data.len());

    // 순차 처리
    println!("1️⃣ 순차 처리");
    let start = Instant::now();
    let sum_seq: i32 = data.iter().sum();
    let seq_time = start.elapsed();
    println!("   합계: {}", sum_seq);
    println!("   시간: {:.3}초\n", seq_time.as_secs_f64());

    // 병렬 처리
    println!("2️⃣ 병렬 처리 (Rayon)");
    let start = Instant::now();
    let sum_par: i32 = data.par_iter().sum();  // par_iter()만 추가!
    let par_time = start.elapsed();
    println!("   합계: {}", sum_par);
    println!("   시간: {:.3}초\n", par_time.as_secs_f64());

    // 결과
    let speedup = seq_time.as_secs_f64() / par_time.as_secs_f64();
    println!("{}", "=".repeat(60));
    println!("📊 결과");
    println!("{}", "=".repeat(60));
    println!("속도 향상: {:.1}배! 🚀", speedup);
    println!("\n💡 .iter()를 .par_iter()로 바꾸기만 하면 됩니다!");
}
