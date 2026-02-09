1. 시스템 아키텍처 (Architecture)
우리 시스템은 지휘, 지능, 실행 레이어가 분리된 하이브리드 멀티 에이전트 구조입니다. 

Goose Manager (The Captain): 워크플로우 전체를 지휘하며 실질적인 파일 수정, 터미널 명령 실행, pytest 기반의 셀프 힐링을 수행합니다.

Gemini CLI (The Architect): .gemini/commands/에 정의된 TOML 레시피를 주입받아 정액제 비용 내에서 고수준의 기획과 설계를 제공합니다.

Spec-kit (The Blueprint): specs/ 디렉토리에 명세서(spec.md)와 구현 계획(plan.md)을 관리하며 모든 개발의 근거를 기록합니다.

1. 핵심 워크플로우 및 마일스톤 (Workflow)
Antigravity 비행은 다음 3대 마일스톤을 반드시 통과해야 합니다.

M1. Spec-Lock (기획 및 명세 확정)
Requirement Agent: .gemini/commands/speckit.specify.toml 레시피를 활용해 요구사항을 분석하고 spec.md 초안을 작성합니다.

Internal Review: speckit.analyze.toml 기반의 Review Agent가 비판적 검토를 수행하여 결함을 수정합니다.

Human Approval: 사용자가 명세 내용을 검토하고 APPROVED 사인을 남깁니다.

M2. Code-Complete (구현 및 테스트)
Planning: speckit.plan.toml을 통해 상세 구현 시나리오를 수립합니다.

Implementation: **Code Agent(Goose)**가 실제 로직을 작성합니다.

Self-Healing: pytest 실행 결과 에러 발생 시 Goose가 스스로 코드를 수정하는 Ralph Loop를 수행합니다.

M3. Final Verification (검증 및 완료)
Code Review: speckit.checklist.toml을 활용해 최종 코드의 무결성을 검사합니다.

Merge: 사용자의 최종 승인 후 결과물을 병합합니다.

3. 에이전트용 레시피 (TOML Recipes)
Goose Manager는 다음 레시피들을 상황에 맞게 서브 에이전트에게 할당합니다.

speckit.specify.toml: 고품질 SDD 명세서 작성 가이드.

speckit.analyze.toml: 기획의 모순과 예외 상황을 찾아내는 비판적 검토용 프롬프트.

speckit.plan.toml: 단계별 구현 및 테스트 시나리오 설계서.

speckit.implement.toml: 코드 컨벤션 및 품질 가이드라인 준수 구현 지침.

4. 프로젝트 헌법 v1.1.0 주요 원칙 (Core Rules)
SDD First: 승인된 spec.md 없이는 소스코드 파일을 생성하거나 수정할 수 없습니다.

Adversarial Review: 모든 기획과 코드는 반드시 다른 페르소나의 비판적 검토를 거쳐야 합니다.

Cost Optimization: 지능 공급은 정액제 Gemini CLI를 최우선으로 하며, API는 보조적으로 사용합니다.

Test-First: 구현 시 테스트 코드를 먼저 혹은 동시에 작성하며 pytest 100% 통과를 지향합니다.