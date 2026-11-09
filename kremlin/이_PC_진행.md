# 이 PC(HSP)에서의 KRM_Palace 진행 — 2026-08-26

인계 문서는 `KRM_이관_명세서.md`. 그 문서는 **다른 PC 기준**이라 이 PC 와 다른 점이 셋 있다.

## 1. 명세서의 도구가 이 PC 엔 없다

`overdare_mesh_bulk_import` / `overdare_create_instances` / `overdare_stop` 은 이 PC 의
Claude Code 에 붙어 있지 않다. 여기서 쓰는 것은:

- `gyeongbokgung\ovdr_*.ps1` — 포트 13377 raw JSON-RPC + `.ovdrjm`(UTF-16LE) 국소 삽입
- 사이드카 카탈로그(`~\.overdare\mcp\studios\*.json`) 40개 툴에도 **메시 임포트는 없다.**
  FBX 38개 벌크 임포트는 **Studio GUI 에서 사람이** 해야 한다.

그래서 명세서 6절을 이 PC 용으로 옮긴 스크립트 두 개를 만들었다:

| 스크립트 | 하는 일 |
|---|---|
| `gyeongbokgung\krm_place.ps1` | `KRM_Palace` Model + 콜리전 Part 116 + 스폰 2 삽입 |
| `gyeongbokgung\krm_place_meshes.ps1` | 임포트 후 MeshPart 124 삽입 (`-Snapshot` → 임포트 → `-Resolve` → `-Apply`) |

## 2. 원점 보정 ΔX +100000

KRM 원좌표(X −4090..4345, Z ±1970)를 그대로 넣으면 원점의 `GND_Base`(X −2734..2266,
Y −40..0)와 **바닥이 겹친다.** 레벨 점유 현황을 실제로 읽어 대조한 결과:

| 컨테이너 | X 범위 |
|---|---|
| JSN_Sangok (Workspace) | −73649 .. −46546 |
| 경복궁 (ServerStorage) | −4115 .. 4115 |
| 로비 · GND_Base · WarCitySpawn | 원점 부근 |
| 창덕궁 (Workspace) | 27000 .. 33000 |
| 화성 (ServerStorage) | 42800 .. 80000 |
| **KRM_Palace (신규)** | **95910 .. 104345** |

가장 가까운 화성과 15.9 km 떨어진다. Y·Z 보정은 0.

## 3. `Arena_Bound_*` 는 아직 넣지 않았다

명세서 7절은 `Arena_Bound_North/South/East/West` 를 KRM 안에 넣으라고 하지만,
`CaptureServer.useArenaBounds()` 는 `Workspace:FindFirstChild(name, **true**)` 로
**재귀 검색**한다. 지금 Workspace 최상위에 JSN 용 같은 이름 벽 4개가 이미 있어서,
KRM 안에 같은 이름을 하나 더 만들면 **어느 쪽이 잡힐지 모른다** — 살아 있는 JSN 경기가
망가질 수 있다. 이건 맵 스왑(`MapService`) 작업에서 이름 규칙과 함께 처리한다.

스폰은 `KRM_Spawn_Red/Blue` 라 충돌하지 않는다(TeamServer 는 `JSN_Spawn_*` 만 찾는다).
즉 지금 넣은 스폰은 **아직 게임에 붙지 않은 예비 지점**이다.

## 4. 남은 순서

1. Studio 에서 `onlyoneshot` 열기 (포트 13377 은 프로젝트가 열려야 열린다)
2. `.\krm_place_meshes.ps1 -Snapshot`
3. Studio GUI 에서 `KRM_Palace_OVERDARE\*.fbx` 38개 벌크 임포트
4. `.\krm_place.ps1 -Apply` → 콜리전 + 스폰
5. `.\krm_place_meshes.ps1 -Resolve` → 이름 대조 → `-Apply`
6. 스크린샷으로 눈 확인 (값 대조는 검증이 아니다)
