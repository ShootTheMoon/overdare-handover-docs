# OVERDARE 이관 명세서 · 작업 기록 보관소

`ShootTheMoon` 의 OVERDARE 맵 작업에서 나온 **이관 명세서와 작업 기록**을 모아 둔 곳이다.
실행 코드도 에셋도 없다 — 전부 문서다.

작업은 **PC 두 대를 왕복**하면서 진행됐다. 한쪽에서 Blender 로 만들고, 다른 쪽에서
OVERDARE Studio 로 임포트한다. 그래서 "다음 사람(또는 다음 세션)이 이것만 읽고
이어받을 수 있게" 쓴 명세서가 계속 나왔고, 그게 이 저장소의 내용이다.

실제 스크립트·에셋·게임 코드는 아래 저장소에 있다. 이 저장소는 그 **짝이 되는 문서**다.

| 저장소 | 무엇 |
|---|---|
| [onlyoneshot](https://github.com/ShootTheMoon/onlyoneshot) | 게임 본체 (Luau), 마일스톤·인계 문서 |
| [overdare-map-pipeline](https://github.com/ShootTheMoon/overdare-map-pipeline) | Blender → Studio 변환·배치 파이프라인 |
| [heritage-maps](https://github.com/ShootTheMoon/heritage-maps) | 국가유산 3D 기반 한국 배경 맵 (산곡·경복궁·창덕궁·소쇄원) |
| [kremlin-palace](https://github.com/ShootTheMoon/kremlin-palace) | 크렘린 대궁전 생성 스크립트·이관 세트 |
| [overdare-mcp](https://github.com/ShootTheMoon/overdare-mcp) | Studio RPC(13377) + UE Remote Control(30010) MCP 서버 |

---

## kremlin/ — 크렘린 파세트궁 (17건)

모스크바 크렘린 중 **파세트궁(Грановитая палата) 실내 한 방**으로 범위를 좁힌 뒤의 기록이다.
외피는 버렸다.

| 파일 | 무엇 |
|---|---|
| `KRM_내부MCP_명세서.md` | Studio **내부** 에이전트에게 넘긴 명세서. 방 방향(yaw) 교정 작업 |
| `KRM_이관_명세서.md` | FBX·배치표·콜리전 이관 규약 |
| `크렘린_이관_명세서.md` | 프로젝트 전체 이관 명세 (PC 간 인계) |
| `IMPORT_ORDER.md` · `IMPORT_export_v1.md` | Studio 임포트 순서, 발행 패키지 v1 |
| `probe_results.md` | P0 프로브 실측 결과 |
| `작업로그.md` | 가장 긴 문서(45 KB). 시도와 실패가 날짜순으로 |
| `남은작업.md` · `실내소품_생성지시.md` | 미완 목록, Hunyuan3D 소품 생성 지시서 |
| `이_PC_진행.md` | 이 PC 쪽에서 어디까지 했는지 |
| `ref/` | 레퍼런스 7건 — 실측 도면 색인 2종(바르테네프 / 소련 1953), 사진·치수 레퍼런스, Hunyuan3D 프롬프트와 그 소스 분석, 8뷰 분류, AI 입력에서 제외한 컷 |

## sangok2/ — SGK (산옥 II) (12건)

산곡을 **5v5 대칭 3레인**으로 다시 만든 리메이크. 게임 안 표기는 `SANGOK`,
내부 id 는 `sgk` 다. 구버전 `JSN_Sangok` 은 로테이션에서 빠졌다.

| 파일 | 무엇 |
|---|---|
| `plan.md` | 설계 전체(22 KB). 레인 구조·시야선·전투 거리 |
| `SGK_이관_명세서.md` | 이관 규약 |
| `asset_survey.md` · `gate1_blockout.md` · `gate2_dressing.md` · `sightlines.md` | 단계별 게이트 기록 |
| `IMPORT_GUIDE.md` · `IMPORT_BATCHES*.md` | Studio 벌크 임포트 (1·2·3차). 2·3차는 잎 알파 아틀라스 재작업 |
| `_이PC_동기화_메모.md` | **잎이 검은 판으로 보인 진짜 원인**과 3차 판 |
| `CREDITS.md` | 외부 에셋 크레딧 |

## hwaseong/ — 수원 화성 v25 (4건)

장안문 아레나. **1차는 위치만, 감축·베이크는 2·3차**로 나눈 단계별 리메이크다.

| 파일 | 무엇 |
|---|---|
| `README_v25_export.md` | 인계 본문(33 KB). 이관 세트 쪽 최신판 |
| `README_v25_rebuild.md` | 같은 문서의 리빌드 작업 쪽 판본 |
| `OVERDARE_화성v25_이관_명세서.md` | 산곡 리버전 규약을 따른 이관 명세 |
| `IMPORT_BATCHES_hws.md` | 벌크 임포트 순서 (세션당 12파일 이하) |

## pipeline/ — 파이프라인·좌표 규약 (9건)

맵 하나에 묶이지 않는 문서들. 좌표 규약, 에이전트에게 던진 질문, 폐기 에셋 목록.

| 파일 | 무엇 |
|---|---|
| `OVERDARE_맵이식_명세서.md` | 블렌더 맵 → OVERDARE 이식 일반 절차 |
| `OVERDARE_화성_이식_명세서.md` | 화성 이식 명세 (v25 이전 세대, 27 KB) |
| `화성_인계프롬프트_v2.md` · `화성_폐가문제_인계프롬프트.md` | 세션 인계용 프롬프트. 뒤쪽은 **"이미 검증한 것 — 다시 재지 마라"** 로 시작한다 |
| `SPEC_FOR_OVERDARE_MCP.md` | Studio MCP 담당자에게 넘긴 산곡 배치 명세 |
| `OVERDARE_AGENT_QUESTIONS.md` | Studio 에이전트에게 보낸 좌표 규약 확인 요청 |
| `KGP_이관_명세서.md` · `IMPORT_ORDER_KGP.md` | 크렘린 **대**궁전(KGP) — 파세트궁으로 좁히기 전 세대 |
| `kgp_unused_assets.md` | 안 쓰는 에셋 목록 (114 KB) |

---

## 읽는 순서

처음 보는 사람이라면 이 순서가 빠르다.

1. `pipeline/OVERDARE_맵이식_명세서.md` — 블렌더에서 OVERDARE 로 뭘 어떻게 옮기는지
2. 맡은 맵의 `*_이관_명세서.md`
3. 그 맵의 `IMPORT_*.md` — 실제 임포트 절차
4. 막히면 `kremlin/작업로그.md` 나 화성 인계프롬프트 — **같은 함정을 이미 밟은 기록**이 있다

## 이 문서들을 읽을 때

- 좌표·치수는 **적힌 시점의 실측값**이다. 그 뒤로 맵이 바뀐 것도 있다 (화성은 크기를
  두 번 되돌렸고, 산곡은 통째로 리메이크됐다). 값을 그대로 믿지 말고 레벨에서 다시 재라.
- 날짜가 적혀 있으면 그게 기준이다. 날짜가 없는 문서는 같은 폴더의 다른 문서로 시점을 잡아라.
- 로컬 경로(`C:\Users\...`)가 그대로 남아 있다. 작업 PC 두 대 사이의 기록이라 그렇다.

## 라이선스

문서는 작업 기록이다. 레퍼런스 도판·사진의 출처와 라이선스는 `kremlin/ref/` 안의
해당 색인에 적혀 있고, 외부 에셋 크레딧은 `sangok2/CREDITS.md` 에 있다.
