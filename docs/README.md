# 📚 Documentation

이 폴더에는 프로젝트 관련 문서들이 포함되어 있습니다.

## 파일 목록

### 1. `distributed-systems-concepts.md`
**분산 시스템 개념 체계 정리**

분산 시스템의 핵심 개념을 체계적으로 정리한 한국어 문서입니다.

**주요 내용:**
- 분산 시스템 개요 및 특성
- CAP 정리와 일관성 모델
- 합의 알고리즘 (Paxos, Raft, 2PC/3PC)
- 복제(Replication)와 파티셔닝(Partitioning)
- 분산 트랜잭션과 Saga 패턴
- 시계와 순서 (Lamport/Vector Clock)
- 장애 처리와 내결함성
- 분산 시스템 패턴과 아키텍처
- 실제 사례 (Google, Amazon, Facebook 등)

**대상 독자:** 초급~중급 개발자

### 2. `python-guide.md`
**Python 쌍곡 타일링 구현 가이드**

Python으로 Order-3 heptagonal tiling을 구현하는 방법에 대한 상세 가이드입니다.

**주요 내용:**
- Python 환경 설정
- matplotlib 기반 시각화
- 복소수 연산 활용
- 인터랙티브 컨트롤

**대상 독자:** Python 개발자, 데이터 과학자, 연구자

---

## 문서 작성 가이드

새로운 문서를 추가할 때는 다음 규칙을 따라주세요:

1. **파일명**: `kebab-case.md` 형식 사용
2. **언어**: 한국어 또는 영어 (일관성 유지)
3. **구조**: 목차, 개요, 본문, 참고자료 순서
4. **마크다운**: GitHub Flavored Markdown 사용
5. **README 업데이트**: 새 문서 추가 시 이 README도 업데이트

## 기여

문서 개선 제안이나 오타 수정은 언제든 환영합니다!
