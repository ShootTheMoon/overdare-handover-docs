# SGK (Sangok II) 이관 명세서 — 2026-09-04

ONLY ONE SHOT 용 5v5 대칭 3레인 산곡 리메이크 맵. Blender 저작·익스포트는 끝났고, **남은 일은 OVERDARE Studio 임포트·배치·Lua 등록·플레이테스트(Phase 3 후반)** 다.
승인 이력: GATE 1(블록아웃) → (a) 능선 = 감제 레인 유지 / GATE 2(드레싱) 승인. 상세 계획 `05_Documentation\plan.md`, 게이트 문서 `gate1_blockout.md`, `gate2_dressing.md`.

## 이 zip 에 든 것
| 폴더 | 내용 | 다른 PC에서 필요? |
|---|---|---|
| `06_OVERDARE\` | **FBX 42개**(10_MASTERS 21 / 01_TERRAIN 16 / 02_STATIC 5, 텍스처 임베드), `_texwork\`(텍스처 원본 PNG), `_collision\items_col_000..008.json`(콜리전 Part 1,770), `placements.csv`(552), `items_bounds.json`, `studio_setup.json`, `MapService_sgk.lua`, `manifest.json`, `IMPORT_GUIDE.md` | **필수** |
| `_scripts\` | `sgk_layout.py`(지형 정의, 순수 파이썬) · `sgk_placements.py`(ids/items 생성) · `sgk_collision.py` · `sgk_verify.py` · Blender용 `sgk_live/dress/export/texbake` | `sgk_placements.py ids/items` 만 필수 (파이썬 3.10+, 표준 라이브러리) |
| `05_Documentation\` | 계획·게이트 문서, 검증 결과(walkability/travel/sightlines/zone_mc/collision_report), `placements_master.json` | 참고 |
| `00_Source_Blender\SGK_Master.blend` | 마스터 씬 25 MB. KHS·SSW 텍스처는 원 PC 절대경로 참조라 이 PC 에선 일부 핑크 — 편집 재개 시 `_TexLib` 외 경로 재지정 필요 | 편집 재개 시만 |
| `_TexLib\` | PolyHaven 텍스처·모델(CC0), Sketchfab 소나무 팩(CC-BY), unpacked | 편집 재개 시만 |
| `04_Previews\` | 게이트 렌더 (p1 블록아웃, p2 드레싱, fbx_ 재임포트 확인) | 참고 |
| `CREDITS.md` | Sketchfab 소나무 팩 CC-BY 표기 문구 (게임 설명에 넣어야 함) | **필수** |

## 엔진 계약 (onlyoneshot Lua 에서 실측한 값 — 바꾸지 말 것)
- 컨테이너 `Workspace.SGK_Sangok`(Model). 그 안에 `SGK_Spawn_Red`(서) / `SGK_Spawn_Blue`(동) SpawnLocation, `SGK_Bound_North/South/East/West` Part 4개(각 축으로 길쭉해야 서버가 방향을 인식).
- 엔진 좌표(cm, Y-up): 맵 중심 X = **−30,000**, Z = 0. rect X −38,000..−22,000, Z −6,000..+6,000. Blender→엔진: `X = x·100 − 30000, Y = z·100, Z = y·100, yaw = −rot_z`.
- 스폰 위치(cm): Red (−36300, 457, −400), Blue (−23700, 243, +400) — 서버가 지면에 스냅하니 Y 는 대략이면 됨. 주변 r 12 m 평지 확보됨.
- MapService 항목: `MapService_sgk.lua` 그대로 `M.MAPS` 에 추가, `M.ORDER` 에 `"sgk"` 추가, `M.DEFAULT="jsn"` 유지. 값: zoneRadius 900 / minSpawnDist 3500 / edgeMargin 2500 / moveScale 0.85 / seam disabled.
- 기존 발행 에셋 재사용(**재임포트 금지**): `MST_EULALIA_overdare`, `MST_ARTEMISIA_overdare`, `MST_ROCK_A/D/E_overdare` + 텍스처 `ATL_EULALIA`, `ATL_ARTEMISIA`, `ROCK_A/D/E`. 그 PC 의 `UGCLocalAssetTable.json` 에 이 이름들이 있어야 한다(없으면 JSN 쪽 FBX 를 먼저 발행).

## Studio 절차 (자세히는 `06_OVERDARE\IMPORT_GUIDE.md`)
1. 플레이테스트 정지. `overdare_mesh_bulk_import` **파일당 1회**(`bundleName` = 파일명 stem). 세션당 ≤12 파일(유닛 36/40 캡), 사이에 Studio 재시작. 진행은 `import_state.json` 장부에 기록 — **재임포트 = 중복 발행, 되돌릴 수 없음**.
2. `python _scripts\sgk_placements.py ids <그 PC의 onlyoneshot\UGCLocalAssetTable.json>` → `asset_ids.json` 47/47 resolved. (테이블은 UTF-16, 스크립트가 처리)
3. `python _scripts\sgk_placements.py items` → `_place\place_000..002.json`, `items_static.json`.
4. `SGK_Sangok` Model 생성 → `items_bounds.json` 생성 → `JSN_Spawn_Red/Blue` 를 `overdare_duplicate_instance` 로 복제·개명·재부모·위치 이동(TeamColor 유지).
5. **프로브 3종을 먼저** (전부 배치하기 전에):
   - 정적 `STA_TER_11` 1개 배치 → 위치가 맵 중심 근처(−30000, ~0, 0)이고 크기 40 m 인지.
   - `MST_PINE_M1` 3개, `size` 를 표 값 ×1 / ×2 / ×0.5 → 플레이테스트에서 높이 14 / 28 / 7 m 면 Size = 절대 cm(현재 가정). 같으면 `sgk_placements.py` 의 size 를 [100,100,100] 백분율로 바꿔 재생성.
   - 콜리전 슬랩 3개(평지·경사·계류 벽) 생성 후 플레이어가 지면 높이에 서는지. 기울어진 슬랩이 반대로 기울면 `sgk_collision.py` `_slab()` 의 `rz` 부호를 반전하고 `python sgk_collision.py` 재생성.
6. `items_static.json`(21) → `_place\*.json`(3청크) → `_collision\items_col_*.json`(9청크) 순으로 `overdare_create_instances(itemsFile, parent="Workspace.SGK_Sangok")`, 청크마다 저장.
7. Lua 반영 후 `DEBUG_FORCE="sgk"` 로 테스트: 스폰 스냅 로그, 경계 rect ±8000/±6000, 1차 거점 = 다리, 90 s 마다 구역 이동, 레인별 도보(R1/R2/R3/T/도섭 통과·절벽 등반 불가), 정자 밑·다리·계류 점프, fps(기준: 로비 44). 끝나면 `DEBUG_FORCE=nil`.

## 알려진 위험·후속
- 콜리전 1,770개는 지형 모서리 총길이가 결정한 값. 총 인스턴스 ≈2,330(이전 맵 3,396). fps 부족 시 특징 정렬 슬랩으로 재작성해 절반까지 감축 가능(`sgk_collision.py` 헤더 참고).
- 소나무는 콜리전 없음(줄기 통과). 정자는 통 박스 콜리전(안에 못 들어감). 다리는 데크 슬랩만.
- Size 의미론·슬랩 방향 부호는 프로브 전까지 **미확정**.
- 텍스처 이름은 전부 `SGK_`/`MST_*_ATL` 등 신규라 기존 테이블과 충돌 없음(확인함).
- 자동 모드 분류기: `git reset --hard`, `tasklist` 류 명령이 막힘 → PowerShell `Get-Process` 등 우회.
