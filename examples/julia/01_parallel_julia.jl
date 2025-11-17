#!/usr/bin/env julia
"""
Julia 병렬 처리 기초
네이티브 멀티스레딩과 분산 컴퓨팅
"""

using Base.Threads
using Distributed
using BenchmarkTools
using Statistics
using SharedArrays
using Printf

println("="^60)
println("Julia 병렬 처리 데모")
println("="^60)
println("Julia 스레드 수: ", nthreads())
println("워커 프로세스 수: ", nworkers())
println()

# 1. 기본 멀티스레딩
function demonstrate_threading()
    println("="^60)
    println("1. 멀티스레딩 기초 (@threads)")
    println("="^60)

    n = 100_000_000

    # 순차 실행
    function sequential_sum(n)
        total = 0.0
        for i in 1:n
            total += sin(i) * cos(i)
        end
        return total
    end

    # 병렬 실행
    function parallel_sum(n)
        total = Atomic{Float64}(0.0)
        @threads for i in 1:n
            atomic_add!(total, sin(i) * cos(i))
        end
        return total[]
    end

    # 더 효율적인 병렬 실행 (리덕션)
    function parallel_sum_reduction(n)
        partial_sums = zeros(nthreads())
        @threads for i in 1:n
            tid = threadid()
            partial_sums[tid] += sin(i) * cos(i)
        end
        return sum(partial_sums)
    end

    println("\n크기: ", n)

    # 순차 실행 벤치마크
    print("순차 실행: ")
    seq_time = @elapsed result_seq = sequential_sum(n)
    @printf("%.3f초\n", seq_time)

    # 병렬 실행 (Atomic)
    print("병렬 (Atomic): ")
    par_time_atomic = @elapsed result_par = parallel_sum(n)
    @printf("%.3f초 (%.2fx)\n", par_time_atomic, seq_time/par_time_atomic)

    # 병렬 실행 (Reduction)
    print("병렬 (Reduction): ")
    par_time = @elapsed result_par_red = parallel_sum_reduction(n)
    @printf("%.3f초 (%.2fx)\n", par_time, seq_time/par_time)

    println("\n결과 검증:")
    println("  순차: ", result_seq)
    println("  병렬 (Atomic): ", result_par)
    println("  병렬 (Reduction): ", result_par_red)
    println("  차이: ", abs(result_seq - result_par_red))
    println()
end

# 2. 배열 연산 병렬화
function demonstrate_array_operations()
    println("="^60)
    println("2. 배열 연산 병렬화")
    println("="^60)

    n = 10_000_000
    x = rand(n)
    y = zeros(n)

    # 순차 실행
    function process_sequential!(y, x)
        for i in eachindex(x)
            y[i] = sqrt(abs(sin(x[i]) * cos(x[i])))
        end
    end

    # 병렬 실행
    function process_parallel!(y, x)
        @threads for i in eachindex(x)
            y[i] = sqrt(abs(sin(x[i]) * cos(x[i])))
        end
    end

    # 벡터화 (Julia의 broadcast)
    function process_vectorized!(y, x)
        y .= sqrt.(abs.(sin.(x) .* cos.(x)))
    end

    println("\n배열 크기: ", n)

    # 벤치마크
    print("순차 실행: ")
    seq_time = @elapsed process_sequential!(y, x)
    @printf("%.3f초\n", seq_time)

    print("병렬 실행: ")
    par_time = @elapsed process_parallel!(y, x)
    @printf("%.3f초 (%.2fx)\n", par_time, seq_time/par_time)

    print("벡터화: ")
    vec_time = @elapsed process_vectorized!(y, x)
    @printf("%.3f초 (%.2fx)\n", vec_time, seq_time/vec_time)
    println()
end

# 3. 몬테카를로 시뮬레이션
function demonstrate_monte_carlo()
    println("="^60)
    println("3. 몬테카를로 π 추정")
    println("="^60)

    function estimate_pi_sequential(n)
        count = 0
        for i in 1:n
            x, y = rand(), rand()
            if x^2 + y^2 <= 1.0
                count += 1
            end
        end
        return 4.0 * count / n
    end

    function estimate_pi_parallel(n)
        counts = zeros(Int, nthreads())
        @threads for i in 1:n
            x, y = rand(), rand()
            if x^2 + y^2 <= 1.0
                counts[threadid()] += 1
            end
        end
        return 4.0 * sum(counts) / n
    end

    n = 100_000_000
    println("\n샘플 수: ", n)

    print("순차 실행: ")
    seq_time = @elapsed pi_seq = estimate_pi_sequential(n)
    @printf("%.3f초, π ≈ %.6f\n", seq_time, pi_seq)

    print("병렬 실행: ")
    par_time = @elapsed pi_par = estimate_pi_parallel(n)
    @printf("%.3f초, π ≈ %.6f (%.2fx)\n", par_time, pi_par, seq_time/par_time)

    println("실제 π: ", π)
    @printf("오차 (순차): %.6f\n", abs(pi_seq - π))
    @printf("오차 (병렬): %.6f\n", abs(pi_par - π))
    println()
end

# 4. 행렬 곱셈
function demonstrate_matrix_operations()
    println("="^60)
    println("4. 행렬 연산")
    println("="^60)

    n = 2000
    A = randn(n, n)
    B = randn(n, n)

    println("\n행렬 크기: ", n, "x", n)

    # Julia의 행렬 곱셈은 기본적으로 최적화된 BLAS 사용
    print("행렬 곱셈 (BLAS): ")
    blas_time = @elapsed C = A * B
    @printf("%.3f초\n", blas_time)

    # 요소별 연산 병렬화
    D = similar(A)
    print("요소별 연산 (병렬): ")
    elem_time = @elapsed begin
        @threads for i in 1:n
            for j in 1:n
                D[i,j] = sin(A[i,j]) + cos(B[i,j])
            end
        end
    end
    @printf("%.3f초\n", elem_time)
    println()
end

# 5. 공유 배열
function demonstrate_shared_arrays()
    println("="^60)
    println("5. 공유 배열 (SharedArrays)")
    println("="^60)

    n = 10_000_000

    # 일반 배열
    function process_regular(n)
        arr = zeros(n)
        @threads for i in 1:n
            arr[i] = sin(i) * cos(i)
        end
        return arr
    end

    # 공유 배열
    function process_shared(n)
        arr = SharedArray{Float64}(n)
        @threads for i in 1:n
            arr[i] = sin(i) * cos(i)
        end
        return arr
    end

    println("\n배열 크기: ", n)

    print("일반 배열: ")
    reg_time = @elapsed arr_reg = process_regular(n)
    @printf("%.3f초\n", reg_time)

    print("공유 배열: ")
    sha_time = @elapsed arr_sha = process_shared(n)
    @printf("%.3f초\n", sha_time)

    println("\n💡 공유 배열은 프로세스 간 공유 가능")
    println()
end

# 6. 리덕션 패턴
function demonstrate_reduction()
    println("="^60)
    println("6. 리덕션 패턴")
    println("="^60)

    n = 50_000_000
    data = randn(n)

    println("\n배열 크기: ", n)

    # 합계
    print("합계 (순차): ")
    seq_time = @elapsed sum_seq = sum(data)
    @printf("%.3f초\n", seq_time)

    print("합계 (병렬): ")
    par_time = @elapsed begin
        partial_sums = zeros(nthreads())
        @threads for i in eachindex(data)
            partial_sums[threadid()] += data[i]
        end
        sum_par = sum(partial_sums)
    end
    @printf("%.3f초 (%.2fx)\n", par_time, seq_time/par_time)

    # 최대값
    print("최대값 (순차): ")
    max_time = @elapsed max_seq = maximum(data)
    @printf("%.3f초\n", max_time)

    print("최대값 (병렬): ")
    max_par_time = @elapsed begin
        partial_max = fill(-Inf, nthreads())
        @threads for i in eachindex(data)
            tid = threadid()
            if data[i] > partial_max[tid]
                partial_max[tid] = data[i]
            end
        end
        max_par = maximum(partial_max)
    end
    @printf("%.3f초 (%.2fx)\n", max_par_time, max_time/max_par_time)

    println("\n결과 검증:")
    @printf("  합계 차이: %.2e\n", abs(sum_seq - sum_par))
    @printf("  최대값 차이: %.2e\n", abs(max_seq - max_par))
    println()
end

# 7. 실전 예제: 이미지 블러
function demonstrate_image_blur()
    println("="^60)
    println("7. 실전 예제: 이미지 블러")
    println("="^60)

    height, width = 1000, 1000
    image = rand(height, width)
    blur_size = 5

    function box_blur_sequential(img, size)
        h, w = size(img)
        result = similar(img)
        half = size ÷ 2

        for i in 1:h
            for j in 1:w
                i_min = max(1, i - half)
                i_max = min(h, i + half)
                j_min = max(1, j - half)
                j_max = min(w, j + half)

                result[i, j] = mean(img[i_min:i_max, j_min:j_max])
            end
        end
        return result
    end

    function box_blur_parallel(img, blur_size)
        h, w = size(img)
        result = similar(img)
        half = blur_size ÷ 2

        @threads for i in 1:h
            for j in 1:w
                i_min = max(1, i - half)
                i_max = min(h, i + half)
                j_min = max(1, j - half)
                j_max = min(w, j + half)

                result[i, j] = mean(img[i_min:i_max, j_min:j_max])
            end
        end
        return result
    end

    println("\n이미지 크기: ", height, "x", width)
    println("블러 크기: ", blur_size, "x", blur_size)

    print("순차 실행: ")
    seq_time = @elapsed result_seq = box_blur_sequential(image, blur_size)
    @printf("%.3f초\n", seq_time)

    print("병렬 실행: ")
    par_time = @elapsed result_par = box_blur_parallel(image, blur_size)
    @printf("%.3f초 (%.2fx)\n", par_time, seq_time/par_time)

    println("\n결과 차이: ", maximum(abs.(result_seq .- result_par)))
    println()
end

# 8. 스케일링 테스트
function demonstrate_scaling()
    println("="^60)
    println("8. 스케일링 테스트")
    println("="^60)

    n = 100_000_000

    function work(n, num_threads)
        result = zeros(num_threads)
        @threads for i in 1:n
            result[threadid()] += sin(i) * cos(i)
        end
        return sum(result)
    end

    # 순차 실행 시간 측정
    seq_time = @elapsed work(n ÷ nthreads(), 1)
    theoretical_par_time = seq_time

    println("\n작업 크기: ", n)
    println("사용 가능 스레드: ", nthreads())
    println("\n스레드 수별 성능:")
    println("-" ^ 60)

    actual_time = @elapsed work(n, nthreads())
    speedup = theoretical_par_time * nthreads() / actual_time
    efficiency = speedup / nthreads() * 100

    @printf("  %2d 스레드: %.3f초 | 속도향상: %.2fx | 효율: %.1f%%\n",
            nthreads(), actual_time, speedup, efficiency)
    println()
end

# 메인 실행
function main()
    demonstrate_threading()
    demonstrate_array_operations()
    demonstrate_monte_carlo()
    demonstrate_matrix_operations()
    demonstrate_shared_arrays()
    demonstrate_reduction()
    demonstrate_image_blur()
    demonstrate_scaling()

    println("="^60)
    println("Julia 병렬 처리 핵심 정리")
    println("="^60)
    println("""
1. @threads 매크로
   - 간단하고 효과적인 병렬화
   - 스레드 안전성 주의 (Atomic, 스레드별 버퍼)

2. 성능 특성
   - C/Fortran 수준의 성능
   - 거의 선형적인 확장성
   - 낮은 오버헤드

3. 리덕션 패턴
   - 스레드별 부분 결과 계산
   - 최종 결과 병합
   - 경쟁 조건 방지

4. 최적화 팁
   - @threads는 외부 루프에만
   - 벡터화와 병렬화 조합
   - BLAS 루틴 활용 (행렬 연산)

5. 다음 단계
   - Distributed 모듈 (분산 컴퓨팅)
   - GPU 가속 (CUDA.jl, AMDGPU.jl)
   - @spawn, @async (태스크 기반 병렬성)

Julia 스레드 시작:
  julia --threads=auto script.jl
  julia --threads=8 script.jl

환경변수:
  export JULIA_NUM_THREADS=8
""")
end

main()
