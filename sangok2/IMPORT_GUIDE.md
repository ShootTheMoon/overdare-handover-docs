# SGK (Sangok II) — Studio 임포트 절차 (Phase 3)

전제: OVERDARE Studio 에 `C:\Users\29\Desktop\onlyoneshot` 프로젝트가 열려 있고 플레이테스트 정지 상태. 임포트는 **되돌릴 수 없다** (재임포트 = 중복 발행). 장부 = `import_state.json`.

## 파일
- `10_MASTERS\*.fbx` 21 (소나무 12, 바위 2, 고사리, 그루터기, 고사목, 정자, 다리, 담장 2) — 각 1메시·1텍스처(밴드 아틀라스 `_texwork\MST_*_ATL.png`)
- `01_TERRAIN\STA_TER_xy.fbx` 12 (40 m 타일, 월드좌표) + `STA_WALL_N/S/E/W.fbx` 4
- `02_STATIC\` 석축 2, 돌탑, 계단, 물 5
- 재사용(재임포트 금지): `MST_EULALIA_overdare`, `MST_ARTEMISIA_overdare`, `MST_ROCK_A/D/E_overdare` (asset_alias)
- 합계 42 파일 ≈ 126 유닛 → 세션당 ≤12 파일(36 유닛), 세션 사이 Studio 재시작

## 순서
1. `overdare_mesh_bulk_import(files=[1개], bundleName=<stem>)` 파일당 1회. 순서: 01_TERRAIN 16 → 02_STATIC 5 → 10_MASTERS (정자·다리·담장 → 바위·고사리·그루터기·고사목 → 소나무 12). 파일마다 `import_state.json` 갱신.
2. `python _scripts\sgk_placements.py ids C:\Users\29\Desktop\onlyoneshot\UGCLocalAssetTable.json` → `asset_ids.json` 47개 전부 resolved 확인.
3. `python _scripts\sgk_placements.py items` → `_place\place_000..002.json` (552) + `items_static.json` (21).
4. Studio: `SGK_Sangok` Model 생성 → `items_bounds.json` 4개 생성(부모 SGK_Sangok) → `JSN_Spawn_Red/Blue` 복제 → `SGK_Spawn_Red/Blue` 개명·재부모·위치(`studio_setup.json`).
5. **프로브**: (a) 정적 1개 `STA_TER_11` 배치 → 위치·크기 확인 (b) `MST_PINE_M1` 3개 size ×1 / ×2 / ×0.5 → 실제 높이로 Size 의미 확정 (c) 콜리전 슬랩 3개(평지·경사·계류벽) → 플레이테스트에서 서보기 → 방향 부호 확인. 틀리면 `sgk_collision._slab` rz 부호 반전 후 재생성.
6. `items_static.json` → `overdare_create_instances(itemsFile, parent=SGK_Sangok)` → 저장. `_place\*.json` 3청크 → 저장. `_collision\items_col_*.json` 9청크(1,770) → 저장.
7. Lua: `MapService_1.lua` `M.MAPS` 에 `MapService_sgk.lua` 항목 추가 + `M.ORDER` 에 "sgk" + 테스트 세션 `DEBUG_FORCE = "sgk"`.
8. 플레이테스트 체크리스트: `gate3` 문서.
