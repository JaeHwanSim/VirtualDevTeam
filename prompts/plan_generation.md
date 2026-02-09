당신은 소프트웨어 아키텍트입니다.
다음 Feature Specification을 기반으로 Implementation Plan을 작성하세요.

---

**Feature**: {issue_title}

**Spec 문서**:
```markdown
{spec_content}
```

---

## 출력 요구사항

다음 형식의 Markdown 문서를 작성하세요:

```markdown
# Implementation Plan: {issue_title}

**Date**: (오늘 날짜)

## Summary

(Spec에서 추출한 핵심 요약 - 2-3문장)

## Technical Context

**Language/Version**: (적절한 프로그래밍 언어 및 버전)
**Framework**: (사용할 프레임워크)
**Primary Dependencies**: (필요한 라이브러리 목록)
**Testing**: (테스트 프레임워크)

## Project Structure

```
project/
├── src/
│   ├── (모듈 구조)
├── tests/
└── README.md
```

## Implementation Phases

### Phase 1: Setup

- [ ] 프로젝트 초기화
- [ ] 의존성 설치
- [ ] 기본 구조 생성

### Phase 2: Core Implementation

- [ ] (핵심 기능 1 구현)
- [ ] (핵심 기능 2 구현)
- [ ] 단위 테스트 작성

### Phase 3: Integration

- [ ] (통합 작업)
- [ ] Error handling
- [ ] 로깅 추가

### Phase 4: Verification

- [ ] 통합 테스트
- [ ] 성능 테스트
- [ ] 문서 작성

---

## API Endpoints (해당되는 경우)

### POST /resource
- 설명
- Request/Response 형식

---

## Verification Plan

### Automated Tests

```bash
(테스트 실행 명령어)
```

### Manual Testing

1. (수동 테스트 단계 1)
2. (수동 테스트 단계 2)
```

## 주의사항

- Spec의 모든 요구사항을 반영하세요
- 각 Phase는 **독립적으로 완료 가능**해야 합니다
- 구체적인 파일명과 경로를 포함하세요
- 실제 구현 가능한 계획을 작성하세요
