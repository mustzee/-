# 분산 시스템 개념 정리

## 목차
1. [분산 시스템 개요](#1-분산-시스템-개요)
2. [분산 시스템의 주요 특성](#2-분산-시스템의-주요-특성)
3. [CAP 정리](#3-cap-정리)
4. [일관성 모델](#4-일관성-모델)
5. [합의 알고리즘](#5-합의-알고리즘)
6. [복제 (Replication)](#6-복제-replication)
7. [파티셔닝 (Partitioning)](#7-파티셔닝-partitioning)
8. [분산 트랜잭션](#8-분산-트랜잭션)
9. [시계와 순서](#9-시계와-순서)
10. [장애 처리와 내결함성](#10-장애-처리와-내결함성)
11. [분산 시스템 패턴과 아키텍처](#11-분산-시스템-패턴과-아키텍처)
12. [실제 사례](#12-실제-사례)

---

## 1. 분산 시스템 개요

### 1.1 정의
분산 시스템은 네트워크로 연결된 여러 독립적인 컴퓨터(노드)들이 협력하여 사용자에게는 하나의 통합된 시스템처럼 보이도록 작동하는 시스템입니다.

### 1.2 분산 시스템이 필요한 이유
- **확장성 (Scalability)**: 단일 시스템의 한계를 넘어서는 처리 능력 필요
- **가용성 (Availability)**: 일부 노드 장애 시에도 서비스 지속
- **성능 (Performance)**: 지리적으로 분산된 사용자에게 낮은 지연시간 제공
- **내결함성 (Fault Tolerance)**: 하드웨어/소프트웨어 장애에 대한 복원력
- **비용 효율성**: 고가의 단일 서버 대신 상대적으로 저렴한 서버 여러 대 사용

### 1.3 분산 시스템의 도전 과제
- **네트워크 지연과 실패**: 네트워크는 신뢰할 수 없고 지연이 발생
- **부분 장애**: 시스템의 일부만 장애가 발생하는 상황 처리
- **동시성 제어**: 여러 노드에서 동시에 데이터 접근 시 일관성 유지
- **합의 문제**: 분산된 노드들 간의 의사결정
- **시계 동기화**: 분산 환경에서 시간 순서 결정의 어려움

---

## 2. 분산 시스템의 주요 특성

### 2.1 투명성 (Transparency)
사용자가 시스템이 분산되어 있다는 사실을 인식하지 못하도록 하는 특성

- **접근 투명성**: 로컬/원격 자원 접근 방법이 동일
- **위치 투명성**: 자원의 물리적 위치를 알 필요 없음
- **이주 투명성**: 자원이 이동해도 사용자가 알 수 없음
- **복제 투명성**: 복제본이 여러 개 있어도 하나처럼 보임
- **장애 투명성**: 장애가 발생해도 사용자가 인식하지 못함
- **동시성 투명성**: 여러 사용자가 동시에 접근해도 충돌 없음

### 2.2 확장성 (Scalability)

#### 수평 확장 (Horizontal Scaling)
- 더 많은 노드를 추가하여 확장
- 선형적 확장이 이상적이지만 실제로는 어려움
- 샤딩, 파티셔닝을 통해 구현

#### 수직 확장 (Vertical Scaling)
- 개별 노드의 성능 향상 (CPU, RAM 증가)
- 물리적 한계 존재
- 단일 장애점(SPOF) 위험

#### 확장성의 차원
- **크기 확장성**: 더 많은 사용자/자원 처리
- **지리적 확장성**: 물리적으로 분산된 환경에서 작동
- **관리적 확장성**: 여러 조직이 관리하는 환경에서 작동

### 2.3 신뢰성과 가용성

#### 가용성 (Availability)
```
가용성 = (전체 시간 - 다운타임) / 전체 시간 × 100%
```

| 가용성 레벨 | 연간 다운타임 | 일반적 명칭 |
|------------|-------------|----------|
| 99% | 3.65일 | Two 9s |
| 99.9% | 8.76시간 | Three 9s |
| 99.99% | 52.56분 | Four 9s |
| 99.999% | 5.26분 | Five 9s |

#### 신뢰성 (Reliability)
- MTBF (Mean Time Between Failures): 평균 고장 간격
- MTTR (Mean Time To Repair): 평균 수리 시간
- 신뢰성 = MTBF / (MTBF + MTTR)

### 2.4 성능 메트릭
- **처리량 (Throughput)**: 단위 시간당 처리되는 요청 수
- **지연시간 (Latency)**: 요청부터 응답까지 걸리는 시간
- **응답시간 (Response Time)**: 사용자 관점에서의 대기 시간

---

## 3. CAP 정리

### 3.1 CAP 정리란?
Eric Brewer가 제안한 이론으로, 분산 시스템에서 다음 세 가지 특성 중 최대 두 가지만 동시에 만족할 수 있다는 정리

### 3.2 세 가지 특성

#### C - Consistency (일관성)
- 모든 노드가 같은 시간에 같은 데이터를 보는 것
- 모든 읽기 작업은 가장 최근의 쓰기 결과를 반환

#### A - Availability (가용성)
- 모든 요청이 (성공 또는 실패) 응답을 받는 것
- 시스템의 일부 노드가 다운되어도 서비스 가능

#### P - Partition Tolerance (파티션 내성)
- 네트워크 파티션(분할) 발생 시에도 시스템이 계속 동작
- 노드 간 통신 장애가 발생해도 시스템 운영 가능

### 3.3 CAP 조합

#### CP 시스템 (일관성 + 파티션 내성)
- 네트워크 파티션 발생 시 일관성을 유지하기 위해 가용성 희생
- 예: HBase, MongoDB (기본 설정), Redis (특정 설정)
- 사용 사례: 금융 거래, 재고 관리

#### AP 시스템 (가용성 + 파티션 내성)
- 네트워크 파티션 발생 시 가용성을 유지하지만 일관성 희생
- 최종 일관성(Eventual Consistency) 모델 사용
- 예: Cassandra, DynamoDB, CouchDB
- 사용 사례: 소셜 미디어, 추천 시스템

#### CA 시스템 (일관성 + 가용성)
- 실제 분산 시스템에서는 불가능 (네트워크 파티션은 항상 발생 가능)
- 단일 노드 또는 클러스터 내부에서만 가능
- 예: 전통적인 RDBMS (단일 서버)

### 3.4 CAP 정리의 한계와 확장
- **PACELC 정리**: CAP의 확장
  - **P**artition이 발생하면: **A**vailability와 **C**onsistency 중 선택
  - **E**lse (정상 상태): **L**atency와 **C**onsistency 중 선택

---

## 4. 일관성 모델

### 4.1 강한 일관성 (Strong Consistency)
- 쓰기 작업 후 모든 읽기가 최신 값을 반환
- 구현: 동기 복제, 합의 알고리즘
- 장점: 프로그래밍 모델이 간단
- 단점: 성능과 가용성 저하

#### 선형화 가능성 (Linearizability)
- 가장 강한 일관성 모델
- 모든 작업이 즉시 원자적으로 실행되는 것처럼 보임
- 전역 순서가 실시간 순서와 일치

#### 순차 일관성 (Sequential Consistency)
- 모든 프로세스가 같은 순서로 작업을 관찰
- 실시간 순서는 보장하지 않음

### 4.2 약한 일관성 (Weak Consistency)
- 쓰기 후 읽기가 최신 값을 반환하지 않을 수 있음
- 성능과 가용성 향상

#### 최종 일관성 (Eventual Consistency)
- 쓰기 작업 중단 후 충분한 시간이 지나면 모든 읽기가 최신 값 반환
- DNS, Amazon DynamoDB가 사용
- 변형:
  - **Causal Consistency**: 인과 관계가 있는 작업은 순서 보장
  - **Read-your-writes**: 자신이 쓴 값은 항상 읽을 수 있음
  - **Monotonic Reads**: 읽기 값이 시간상 과거로 돌아가지 않음
  - **Monotonic Writes**: 쓰기 순서가 보존됨

### 4.3 일관성 수준 선택
```
일관성 수준 설정 예 (Cassandra):
- ONE: 1개 노드만 응답하면 성공
- QUORUM: 과반수 노드 응답 필요
- ALL: 모든 노드 응답 필요
```

### 4.4 Quorum 읽기/쓰기
```
N = 복제본 수
W = 쓰기 Quorum (쓰기 성공에 필요한 노드 수)
R = 읽기 Quorum (읽기 성공에 필요한 노드 수)

W + R > N 이면 강한 일관성 보장
W + R ≤ N 이면 최종 일관성
```

**예시:**
- N=3, W=2, R=2: 강한 일관성 (2+2 > 3)
- N=3, W=1, R=1: 최종 일관성 (1+1 ≤ 3)

---

## 5. 합의 알고리즘

### 5.1 합의 문제란?
분산 시스템에서 여러 노드가 하나의 값에 동의하는 문제

### 5.2 Two-Phase Commit (2PC)

#### 동작 과정
1. **Phase 1 - Prepare**
   - 코디네이터가 모든 참여자에게 준비 요청
   - 각 참여자는 커밋 가능 여부 응답

2. **Phase 2 - Commit/Abort**
   - 모든 참여자가 Yes → 커밋 명령
   - 하나라도 No → 중단 명령

#### 문제점
- **블로킹 프로토콜**: 코디네이터 장애 시 참여자들이 대기
- **단일 장애점**: 코디네이터가 SPOF
- **성능**: 2번의 네트워크 라운드트립

### 5.3 Three-Phase Commit (3PC)
- 2PC의 블로킹 문제 해결
- PreCommit 단계 추가
- 타임아웃으로 진행 가능
- 여전히 네트워크 파티션에 취약

### 5.4 Paxos

#### 특징
- 비동기 환경에서 안전한 합의 보장
- 노드의 과반수만 있으면 진행 가능
- 이론적으로 정확하지만 구현이 복잡

#### 역할
- **Proposer**: 값을 제안
- **Acceptor**: 제안을 수락
- **Learner**: 합의된 값을 학습

#### 동작 (간략)
1. **Phase 1a (Prepare)**: Proposer가 제안 번호로 prepare 요청
2. **Phase 1b (Promise)**: Acceptor가 이전 제안보다 큰 번호면 promise
3. **Phase 2a (Accept)**: Proposer가 값과 함께 accept 요청
4. **Phase 2b (Accepted)**: Acceptor가 수락

#### 변형
- **Multi-Paxos**: 연속된 값들에 대한 합의
- **Fast Paxos**: 2 라운드로 단축 (특정 조건)

### 5.5 Raft

#### 특징
- Paxos보다 이해하기 쉬운 대안
- 명확한 리더 선출
- etcd, Consul에서 사용

#### 주요 개념
- **Leader**: 클라이언트 요청 처리, 로그 복제
- **Follower**: 수동적, 리더 요청에 응답
- **Candidate**: 리더 선출 중인 상태

#### 리더 선출
1. Follower가 타임아웃되면 Candidate로 전환
2. Term 증가 후 투표 요청
3. 과반수 투표 받으면 Leader
4. 각 Term마다 최대 1명의 Leader

#### 로그 복제
1. Leader가 클라이언트 요청을 로그에 추가
2. 과반수 Follower에게 복제
3. 과반수 확인 후 커밋
4. 상태 머신에 적용

#### 안전성 보장
- **Election Safety**: Term마다 최대 1개 Leader
- **Leader Append-Only**: Leader는 로그 수정/삭제 불가
- **Log Matching**: 같은 인덱스/Term이면 같은 명령
- **Leader Completeness**: 커밋된 엔트리는 미래 Leader에 존재
- **State Machine Safety**: 같은 인덱스에는 같은 명령 적용

### 5.6 Byzantine Fault Tolerance (BFT)

#### 비잔틴 장애
- 노드가 악의적으로 행동 (거짓 정보, 다른 노드에 다른 메시지)
- 일반 장애보다 처리 어려움

#### PBFT (Practical Byzantine Fault Tolerance)
- 3f+1개 노드로 f개의 비잔틴 장애 허용
- 블록체인에서 사용 (예: Hyperledger Fabric)
- 성능: O(n²) 메시지 복잡도

---

## 6. 복제 (Replication)

### 6.1 복제의 목적
- **고가용성**: 노드 장애 시에도 서비스 가능
- **성능 향상**: 읽기 요청 분산
- **지리적 분산**: 사용자와 가까운 위치에서 서비스
- **내결함성**: 데이터 손실 방지

### 6.2 복제 방식

#### 6.2.1 단일 리더 복제 (Single-Leader Replication)

**동작:**
- 1개의 Leader(Primary), 여러 Follower(Secondary)
- 모든 쓰기는 Leader로
- Follower는 Leader의 변경사항 복제

**장점:**
- 구현이 간단
- 쓰기 충돌 없음

**단점:**
- Leader가 SPOF
- 쓰기 확장성 제한

**사용 예:** MySQL, PostgreSQL (streaming replication), MongoDB

#### 복제 방법

**동기 복제 (Synchronous Replication)**
```
Client → Leader → Follower1 (대기) → Follower2 (대기) → Client 응답
```
- 장점: 강한 일관성, 데이터 손실 없음
- 단점: 느림, 가용성 낮음

**비동기 복제 (Asynchronous Replication)**
```
Client → Leader → Client 응답 (즉시)
Leader → Follower1, Follower2 (백그라운드)
```
- 장점: 빠름, 가용성 높음
- 단점: 복제 지연, 데이터 손실 가능

**반동기 복제 (Semi-Synchronous)**
- 최소 1개 Follower는 동기, 나머지는 비동기
- 절충안

#### 6.2.2 다중 리더 복제 (Multi-Leader Replication)

**동작:**
- 여러 개의 Leader
- 각 Leader가 쓰기 수락
- Leader 간 변경사항 동기화

**장점:**
- 쓰기 성능 향상
- 데이터센터 간 지연시간 감소
- 네트워크 장애 내성

**단점:**
- 쓰기 충돌 처리 필요
- 복잡한 구현

**사용 사례:**
- 다중 데이터센터 운영
- 오프라인 작업 지원 (모바일 앱)
- 협업 편집 (Google Docs)

**충돌 해결 전략:**
1. **최종 쓰기 우선 (Last Write Wins, LWW)**
   - 타임스탬프가 늦은 것 선택
   - 데이터 손실 가능

2. **사용자 개입**
   - 충돌을 사용자에게 보여주고 선택하게 함

3. **커스텀 로직**
   - 애플리케이션 레벨에서 병합

4. **CRDT (Conflict-free Replicated Data Types)**
   - 수학적으로 충돌 해결 보장
   - 예: 카운터, 셋, 맵

#### 6.2.3 리더 없는 복제 (Leaderless Replication)

**동작:**
- 모든 노드가 동등
- 클라이언트가 여러 노드에 직접 쓰기
- Quorum 기반

**장점:**
- 높은 가용성
- 단일 장애점 없음

**단점:**
- 일관성 관리 복잡
- 충돌 해결 필요

**사용 예:** Cassandra, DynamoDB, Riak

**Quorum 읽기/쓰기:**
```
N = 3 (복제본 수)
W = 2 (쓰기 quorum)
R = 2 (읽기 quorum)

쓰기: 2개 노드에 성공하면 OK
읽기: 2개 노드에서 읽어서 최신값 선택
```

**Sloppy Quorum와 Hinted Handoff:**
- 정상 노드가 부족할 때 임시 노드 사용
- 나중에 원래 노드로 전송

### 6.3 복제 지연 문제

#### Read-after-Write 일관성
- 사용자가 쓴 데이터를 바로 읽을 때 최신 값 보장
- 해결: 자신이 수정한 데이터는 Leader에서 읽기

#### Monotonic Reads
- 시간이 되돌아가지 않음 (읽은 값이 이전보다 오래되지 않음)
- 해결: 사용자를 같은 Replica에 라우팅

#### Consistent Prefix Reads
- 인과관계가 있는 쓰기는 순서대로 읽힘
- 해결: 관련 쓰기를 같은 파티션에 배치

---

## 7. 파티셔닝 (Partitioning)

### 7.1 파티셔닝의 목적
- 데이터가 단일 노드에 저장하기에 너무 큼
- 쿼리 처리량이 단일 노드 능력을 초과
- 수평 확장 (Scale-out)

### 7.2 파티셔닝 방식

#### 7.2.1 범위 기반 파티셔닝 (Range Partitioning)
```
파티션 1: A-F
파티션 2: G-M
파티션 3: N-Z
```

**장점:**
- 범위 쿼리 효율적
- 순서 유지

**단점:**
- 핫스팟 발생 가능 (특정 범위 집중 접근)
- 불균등 분산

**사용 예:** HBase, Bigtable

#### 7.2.2 해시 기반 파티셔닝 (Hash Partitioning)
```
partition = hash(key) % num_partitions
```

**장점:**
- 균등 분산
- 핫스팟 완화

**단점:**
- 범위 쿼리 비효율
- 순서 손실

**일관성 해싱 (Consistent Hashing)**
- 노드 추가/삭제 시 최소한의 키만 재배치
- 해시 링 구조
- 가상 노드로 균등 분산 개선

```
전통적 해싱: 노드 변경 시 대부분 키 재배치
일관성 해싱: 노드 변경 시 평균 K/N 개 키만 재배치 (K=총 키, N=노드 수)
```

#### 7.2.3 복합 파티셔닝
- **파티션 키 + 정렬 키**: Cassandra
  - 같은 파티션 내에서 정렬 키로 정렬
  - 예: `(user_id, timestamp)`

### 7.3 보조 인덱스 파티셔닝

#### 문서 기반 파티셔닝 (Local Index)
- 각 파티션이 자신의 문서에 대한 인덱스 유지
- 쓰기는 빠름
- 읽기는 모든 파티션 스캔 필요 (Scatter/Gather)

#### 용어 기반 파티셔닝 (Global Index)
- 인덱스 자체를 파티셔닝
- 읽기는 빠름
- 쓰기는 여러 파티션 업데이트 필요

### 7.4 리밸런싱 (Rebalancing)

#### 리밸런싱이 필요한 경우
- 노드 추가/제거
- 하드웨어 업그레이드
- 부하 불균형 해소

#### 전략

**1. 고정 파티션 수**
- 처음부터 많은 파티션 생성
- 노드 변경 시 파티션 이동
- 예: Riak, Elasticsearch

**2. 동적 파티셔닝**
- 파티션 크기에 따라 자동 분할/병합
- 예: HBase, MongoDB

**3. 노드 비례 파티셔닝**
- 노드 수에 비례하여 파티션 수 결정
- 예: Cassandra (256 가상 노드/물리 노드)

#### 리밸런싱 주의사항
- 자동 vs 수동
- 점진적 이동
- 성능 영향 최소화

### 7.5 요청 라우팅

클라이언트가 어느 파티션에 접근해야 하는지 결정

#### 방법 1: 클라이언트가 임의 노드 접근
- 노드가 올바른 노드로 포워딩
- Cassandra, Riak

#### 방법 2: 라우팅 계층
- 모든 요청이 라우팅 계층 경유
- 라우팅 계층이 올바른 노드로 전달

#### 방법 3: 클라이언트가 직접 판단
- 클라이언트가 파티셔닝 정보 보유
- 직접 올바른 노드 접근

#### 파티션 메타데이터 관리
- **ZooKeeper**: 중앙 집중식 메타데이터 관리
  - HBase, Kafka에서 사용
- **Gossip 프로토콜**: 탈중앙화
  - Cassandra, Riak에서 사용

---

## 8. 분산 트랜잭션

### 8.1 ACID 속성

#### Atomicity (원자성)
- 트랜잭션의 모든 작업이 전부 성공하거나 전부 실패
- All-or-nothing

#### Consistency (일관성)
- 트랜잭션 전후 데이터 무결성 규칙 유지
- 애플리케이션 레벨 속성

#### Isolation (격리성)
- 동시 실행 트랜잭션이 서로 영향을 주지 않음

#### Durability (지속성)
- 커밋된 트랜잭션은 영구적 저장

### 8.2 분산 환경에서의 도전

#### 분산 원자성
- 여러 노드에 걸친 작업의 원자성 보장
- 2PC, 3PC, Saga 패턴

#### 분산 격리성
- 격리 수준:
  1. **Read Uncommitted**: 더티 읽기 가능
  2. **Read Committed**: 커밋된 데이터만 읽기
  3. **Repeatable Read**: 같은 쿼리 반복 시 같은 결과
  4. **Serializable**: 완전 격리 (직렬 실행과 동일)

### 8.3 분산 트랜잭션 프로토콜

#### Two-Phase Commit (2PC)
- 앞서 [5.2 Two-Phase Commit](#52-two-phase-commit-2pc) 참조
- 단점: 블로킹, 성능 저하

#### Saga 패턴

**개념:**
- 여러 로컬 트랜잭션의 시퀀스
- 각 로컬 트랜잭션은 커밋 후 메시지/이벤트 발행
- 실패 시 보상 트랜잭션(Compensating Transaction) 실행

**장점:**
- 비블로킹
- 높은 가용성
- 장기 실행 트랜잭션 지원

**단점:**
- 격리성 보장 어려움
- 복잡한 보상 로직

**구현 방식:**

1. **Choreography (안무)**
   - 각 서비스가 이벤트 리슨하고 반응
   - 탈중앙화
   - 복잡도 증가 가능

2. **Orchestration (오케스트레이션)**
   - 중앙 코디네이터가 순서 제어
   - 명확한 흐름
   - 중앙 장애점

**예시:**
```
주문 생성 Saga:
1. 주문 생성 (Order Service)
2. 결제 처리 (Payment Service)
3. 재고 감소 (Inventory Service)
4. 배송 시작 (Shipping Service)

실패 시 보상:
- 배송 취소 → 재고 복구 → 결제 환불 → 주문 취소
```

### 8.4 분산 락

#### 목적
- 여러 노드에서 동시에 같은 자원 수정 방지

#### 구현

**Redlock (Redis)**
- 여러 Redis 인스턴스에 락 획득
- 과반수에서 성공하면 락 획득
- 논쟁: 안전성에 대한 의문 제기됨 (Martin Kleppmann)

**ZooKeeper 기반**
- Ephemeral Sequential Node 사용
- 가장 작은 번호 노드가 락 보유
- Watch로 락 해제 감지

**Fencing Token**
- 락 획득 시 단조 증가하는 토큰 발급
- 요청에 토큰 포함
- 서버가 오래된 토큰 거부

```
Client A: 락 획득 (토큰 33) → 네트워크 지연 → 요청 (토큰 33)
Client B: 락 획득 (토큰 34) → 요청 (토큰 34) ✓
Server: 토큰 34 이후 토큰 33 거부
```

---

## 9. 시계와 순서

### 9.1 분산 시스템에서 시간의 중요성
- 이벤트 순서 결정
- 타임아웃 판단
- 성능 측정
- 로그 정렬

### 9.2 물리적 시계

#### Time-of-Day 시계
- 벽시계 시간 (Wall-clock time)
- Unix timestamp (1970년 1월 1일부터 초)
- NTP(Network Time Protocol)로 동기화

**문제점:**
- 시간이 뒤로 갈 수 있음 (NTP 조정)
- 노드 간 시계 차이 (Clock skew)
- 지속적인 시간 흐름 (Time drift)

#### Monotonic 시계
- 항상 증가만 하는 시계
- 절대 시간이 아닌 경과 시간 측정
- 타임아웃, 성능 측정에 사용

### 9.3 논리적 시계

#### Lamport Timestamp
Leslie Lamport가 제안한 논리적 시계

**규칙:**
1. 각 프로세스는 카운터 유지
2. 이벤트 발생 시 카운터 증가
3. 메시지 전송 시 현재 카운터 포함
4. 메시지 수신 시: `counter = max(local_counter, received_counter) + 1`

**특성:**
- a → b 이면 L(a) < L(b)
- 하지만 L(a) < L(b)라고 a → b는 아님 (인과관계 보장 안됨)

**사용:**
- 전역 순서 부여
- 분산 뮤텍스

#### Vector Clock
인과관계를 추적할 수 있는 논리적 시계

**구조:**
- 각 프로세스가 모든 프로세스의 카운터 벡터 유지
- 프로세스 Pi의 벡터: VC[i] = [c1, c2, ..., cn]

**규칙:**
1. 로컬 이벤트 시: VC[i][i]++
2. 메시지 전송 시: 현재 VC 포함
3. 메시지 수신 시:
   ```
   VC[i][j] = max(VC[i][j], received_VC[j]) for all j
   VC[i][i]++
   ```

**비교:**
```
VC1 ≤ VC2 iff VC1[i] ≤ VC2[i] for all i
VC1 < VC2 iff VC1 ≤ VC2 and VC1 ≠ VC2

VC1 < VC2: VC1의 이벤트가 VC2 이전 (인과관계)
VC1 || VC2: 동시 이벤트 (concurrent)
```

**사용:**
- 인과관계 추적
- 충돌 감지 (Dynamo, Riak)
- 버전 관리

**단점:**
- 벡터 크기 = 노드 수 (확장성 문제)

#### Hybrid Logical Clock (HLC)
- 물리적 시계와 논리적 시계 결합
- 물리적 시간과 유사하면서 인과관계 보장
- CockroachDB에서 사용

### 9.4 전역 순서

#### Total Order Broadcast
- 모든 노드가 같은 순서로 메시지 수신
- 합의 알고리즘으로 구현
- 사용: 상태 머신 복제, 직렬화 가능 트랜잭션

#### Causal Order
- 인과관계가 있는 메시지만 순서 보장
- Total Order보다 약하지만 구현 효율적

---

## 10. 장애 처리와 내결함성

### 10.1 장애 유형

#### 노드 장애
- **Crash-Stop**: 노드가 멈추고 재시작 안됨
- **Crash-Recovery**: 노드가 멈췄다가 재시작
- **Byzantine**: 악의적/임의적 행동

#### 네트워크 장애
- **패킷 손실**: 메시지가 도착하지 않음
- **네트워크 파티션**: 노드 그룹 간 통신 단절
- **지연**: 메시지가 늦게 도착

### 10.2 장애 감지

#### Timeout 기반
- 일정 시간 응답 없으면 장애로 간주
- 문제: 느린 것과 죽은 것 구분 어려움

#### Heartbeat
- 주기적으로 생존 신호 전송
- 신호 없으면 장애로 간주

#### Phi Accrual Failure Detector
- Cassandra에서 사용
- 확률적 장애 감지
- 네트워크 상태에 따라 임계값 조정

```
Φ(t) = -log10(P(t))
Φ > threshold → 장애로 간주
```

### 10.3 복구 전략

#### 체크포인팅 (Checkpointing)
- 주기적으로 상태 저장
- 장애 시 마지막 체크포인트부터 재실행

#### 로그 기반 복구
- 모든 작업을 로그에 기록
- 장애 시 로그 재생 (Replay)
- WAL (Write-Ahead Log)

#### 이벤트 소싱
- 상태 변경을 이벤트로 저장
- 현재 상태 = 이벤트들의 집합 적용
- 감사 로그, 디버깅에 유용

### 10.4 Chaos Engineering

#### 개념
- 프로덕션에서 의도적으로 장애 주입
- 시스템 복원력 검증
- Netflix의 Chaos Monkey

#### 실험 예시
- 임의 서버 종료
- 네트워크 지연 주입
- 디스크 Full 시뮬레이션
- 의존성 서비스 장애

---

## 11. 분산 시스템 패턴과 아키텍처

### 11.1 마이크로서비스 아키텍처

#### 특징
- 작고 독립적인 서비스들
- 서비스별 독립 배포
- 기술 스택 자유도
- 팀 자율성

#### 장점
- 확장성
- 유연성
- 장애 격리
- 빠른 배포

#### 단점
- 분산 시스템 복잡성
- 네트워크 지연
- 데이터 일관성
- 테스트 어려움

### 11.2 이벤트 주도 아키텍처

#### 이벤트 스트리밍
- **Apache Kafka**: 분산 로그
- **RabbitMQ**: 메시지 브로커
- **Amazon Kinesis**: 실시간 스트리밍

#### 패턴

**Publish-Subscribe**
- 발행자와 구독자 분리
- 1:N 통신

**Event Sourcing**
- 상태 변경을 이벤트로 저장
- 이벤트 재생으로 상태 복원

**CQRS (Command Query Responsibility Segregation)**
- 읽기와 쓰기 모델 분리
- 각각 최적화 가능

### 11.3 서비스 메시 (Service Mesh)

#### 개념
- 서비스 간 통신 인프라 계층
- 사이드카 프록시 패턴

#### 기능
- 로드 밸런싱
- 서비스 디스커버리
- 암호화
- 인증/인가
- 관찰성 (Observability)
- 회로 차단기 (Circuit Breaker)
- 재시도 정책

#### 구현
- **Istio**: Kubernetes 기반
- **Linkerd**: 경량
- **Consul Connect**: HashiCorp

### 11.4 API Gateway

#### 역할
- 단일 진입점
- 라우팅
- 인증/인가
- Rate Limiting
- 프로토콜 변환
- 응답 집계

#### 구현
- **Kong**: Nginx 기반
- **AWS API Gateway**
- **Apigee**

### 11.5 분산 캐싱

#### 전략

**Cache-Aside (Lazy Loading)**
```
1. 캐시 확인
2. 캐시 미스 → DB 조회
3. 캐시에 저장
```

**Write-Through**
```
1. 캐시 + DB 동시 쓰기
2. 항상 일관성 유지
```

**Write-Behind (Write-Back)**
```
1. 캐시에만 쓰기
2. 비동기로 DB 업데이트
```

**Read-Through**
```
1. 캐시가 자동으로 DB 조회
2. 애플리케이션은 캐시만 접근
```

#### 캐시 무효화
- **TTL (Time-To-Live)**: 시간 기반
- **이벤트 기반**: 데이터 변경 시 무효화
- **LRU (Least Recently Used)**: 공간 부족 시 제거

#### 분산 캐시 구현
- **Redis Cluster**: 샤딩, 복제
- **Memcached**: 단순, 빠름
- **Hazelcast**: In-memory 데이터 그리드

### 11.6 회로 차단기 (Circuit Breaker)

#### 상태
1. **Closed**: 정상 작동, 요청 통과
2. **Open**: 장애 감지, 요청 즉시 실패
3. **Half-Open**: 시험 요청, 복구 확인

```
Closed --[실패율 초과]--> Open
Open --[타임아웃]--> Half-Open
Half-Open --[성공]--> Closed
Half-Open --[실패]--> Open
```

#### 구현
- **Hystrix** (Netflix, deprecated)
- **Resilience4j** (권장)
- **Polly** (.NET)

### 11.7 벌크헤드 패턴 (Bulkhead)

#### 개념
- 자원 격리
- 한 서비스 장애가 전체에 영향 방지
- 선박의 격벽에서 유래

#### 구현
- 스레드 풀 분리
- 연결 풀 분리
- 세마포어 사용

### 11.8 재시도와 백오프

#### 재시도 전략
- **고정 재시도**: 일정 간격
- **지수 백오프**: 점차 간격 증가
- **Jitter**: 랜덤성 추가 (동시 재시도 방지)

```python
# 지수 백오프 with Jitter
delay = min(max_delay, base_delay * 2^attempt + random(0, jitter))
```

---

## 12. 실제 사례

### 12.1 Google

#### BigTable
- 분산 컬럼 패밀리 데이터베이스
- GFS (Google File System) 위에 구축
- Tablet 기반 파티셔닝
- Chubby (락 서비스)

#### Spanner
- 전역 분산 데이터베이스
- 강한 일관성 + 높은 가용성
- TrueTime API (원자 시계, GPS)
- 외부 일관성 보장

#### MapReduce
- 대규모 데이터 처리 프레임워크
- Map + Reduce 단계
- 장애 내성
- Hadoop의 영감

### 12.2 Amazon

#### DynamoDB
- NoSQL 키-값 데이터베이스
- 최종 일관성
- 일관성 해싱
- Quorum 기반 복제
- 벡터 클락 (버전 관리)

#### S3 (Simple Storage Service)
- 객체 스토리지
- 최종 일관성 (이제는 강한 일관성 지원)
- 99.999999999% (11 9s) 내구성

### 12.3 Facebook

#### Cassandra
- 분산 NoSQL 데이터베이스
- 리더 없는 복제
- 일관성 해싱
- Gossip 프로토콜
- Tunable 일관성

#### TAO (The Associations and Objects)
- 소셜 그래프 캐시
- MySQL 위 분산 캐시
- 읽기 최적화

### 12.4 Netflix

#### Microservices
- 수백 개의 마이크로서비스
- 클라우드 네이티브 (AWS)
- Chaos Engineering

#### Hystrix
- 회로 차단기 라이브러리
- 장애 격리
- 현재는 유지보수 모드

### 12.5 LinkedIn

#### Kafka
- 분산 이벤트 스트리밍 플랫폼
- 고처리량, 낮은 지연
- 파티셔닝
- 복제
- ZooKeeper 의존 (KRaft로 전환 중)

#### Voldemort
- 분산 키-값 저장소
- DynamoDB 영감
- 리더 없는 복제

### 12.6 Uber

#### Ringpop
- 애플리케이션 레벨 샤딩
- 일관성 해싱
- Gossip 프로토콜

#### Schemaless
- MySQL 기반 NoSQL
- 샤딩
- 버퍼링 쓰기

### 12.7 Airbnb

#### SmartStack
- 자동 서비스 디스커버리
- 로드 밸런싱
- 헬스 체크

### 12.8 Twitter

#### Manhattan
- 분산 키-값 저장소
- 강한 일관성 옵션
- 다중 데이터센터

#### Finagle
- RPC 프레임워크
- 회로 차단기
- 로드 밸런싱

---

## 참고 자료

### 필독 논문
1. **"Time, Clocks, and the Ordering of Events in a Distributed System"** - Leslie Lamport (1978)
2. **"The Byzantine Generals Problem"** - Lamport, Shostak, Pease (1982)
3. **"Impossibility of Distributed Consensus with One Faulty Process"** - Fischer, Lynch, Paterson (1985)
4. **"Paxos Made Simple"** - Leslie Lamport (2001)
5. **"The Chubby Lock Service"** - Google (2006)
6. **"Dynamo: Amazon's Highly Available Key-value Store"** - Amazon (2007)
7. **"Bigtable: A Distributed Storage System"** - Google (2006)
8. **"MapReduce: Simplified Data Processing"** - Google (2004)
9. **"Spanner: Google's Globally-Distributed Database"** - Google (2012)
10. **"In Search of an Understandable Consensus Algorithm (Raft)"** - Ongaro, Ousterhout (2014)

### 추천 도서
1. **"Designing Data-Intensive Applications"** - Martin Kleppmann
   - 분산 시스템의 바이블
2. **"Distributed Systems: Principles and Paradigms"** - Tanenbaum, Van Steen
3. **"Database Internals"** - Alex Petrov
4. **"Building Microservices"** - Sam Newman
5. **"Site Reliability Engineering"** - Google

### 온라인 자료
- **Jepsen**: 분산 시스템 테스트 (https://jepsen.io)
- **The Morning Paper**: 논문 리뷰 블로그
- **AWS Architecture Blog**
- **Martin Kleppmann's Blog**
- **Aphyr's Blog** (Kyle Kingsbury - Jepsen 저자)

---

## 요약

분산 시스템은 현대 소프트웨어 아키텍처의 핵심입니다. 주요 개념을 정리하면:

### 핵심 원칙
1. **트레이드오프**: CAP 정리처럼 모든 것을 동시에 가질 수 없음
2. **장애는 정상**: 네트워크, 노드 장애를 예상하고 설계
3. **비동기성**: 동기 호출은 확장성과 가용성 저해
4. **멱등성**: 같은 작업 반복 시 같은 결과
5. **관찰성**: 로그, 메트릭, 트레이싱으로 시스템 이해

### 설계 시 고려사항
- **일관성 vs 가용성**: 비즈니스 요구사항에 맞게 선택
- **복제 전략**: 데이터 중요도와 접근 패턴에 따라
- **파티셔닝**: 핫스팟 방지, 균등 분산
- **합의 알고리즘**: 강한 일관성 필요 시
- **이벤트 주도**: 느슨한 결합, 확장성

### 실무 팁
1. **단순하게 시작**: 필요할 때 복잡도 추가
2. **측정**: 추측하지 말고 측정
3. **테스트**: Chaos Engineering으로 복원력 검증
4. **모니터링**: 관찰 가능한 시스템 구축
5. **문서화**: 아키텍처 결정 이유 기록

분산 시스템은 어렵지만, 올바른 이해와 도구로 확장 가능하고 신뢰할 수 있는 시스템을 구축할 수 있습니다.
