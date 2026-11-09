# KRM_Palace → OVERDARE 이식 준비 완료

출처: `KRM_Palace_rebuild.blend` (Codex 재작업본, **저장하지 않고 읽기만 함**)
생성: `overdare_prep.py` — 원본 씬을 사본으로만 건드리고 `.blend` 는 손대지 않았다.

## 지금 폴더에 있는 것

```
_overdare/
  *.fbx              38개  (18.5 MB, 최대 1.65 MB)   ← 이걸 Studio 에 넣는다
  _tex/              38장  베이크된 컬러맵 (512 / 히어로 소품 1024)
  manifest.json      배치 좌표 · 콜리전 · 소스 추적
  items_col_00.json  콜리전 파츠 116개  (지금 바로 쓸 수 있다)
  make_items.py      manifest → overdare_create_instances 페이로드 생성기
```

## OVERDARE 규칙 대조

| 규칙 | 상태 |
|---|---|
| 메시당 ≤ 30,000 tris | ✅ 최대 27,999 (Pechka). 35,599짜리 옥좌는 **2조각으로 분할**했다 |
| 머티리얼 하나 = 임포트 단위 하나 | ✅ 다중 머티리얼 메시를 분리 (Icon → m0/m1/m2) |
| MeshPart 텍스처 1장 | ✅ 전부 단일 컬러맵으로 베이크. 재임포트 검증에서 **오브젝트 1 / 머티리얼 1 / 텍스처 1** 확인 |
| 텍스처 ≤ 1024 (512 권장) | ✅ 512 기본. 원본은 **4096 짜리가 22장**이었다 — 그대로 넣으면 임포터가 OOM 난다 |
| FBX당 ≤ 200 메시 | ✅ 파일당 1개 |
| 파일 ≤ 250 MB | ✅ 최대 1.65 MB |
| Y-up, cm | ✅ `axis_forward='-Z', axis_up='Y'` |
| 콜라이더는 FBX 에 못 넣음 | ✅ 엔진 Part 116개로 `items_col_00.json` 에 분리 |
| 벌크 임포트 ≤ 200 파일 | ✅ 38개 → **한 번에 끝난다** |

## 숫자

| | |
|---|---|
| 렌더 오브젝트 105개 → **고유 메시 35개** | 인스턴스 공유가 심해서 실제로 올릴 건 38 파일뿐 |
| 고유 트라이 | 131,415 |
| 월드 트라이 | 630,481 |
| 배치 | 124 |
| 콜리전 | 116 |
| **총 파츠** | **240** |

참고로 `JSN_Sangok` 이 3,396 파츠다. 이건 그 **7%** 다.

## 좌표 규약 — ★ 한 개로 먼저 검증하고 나머지를 깔아라

```
blender (bx,by,bz)      →  engine (bx, bz, -by)        FBX 가 Y-up 으로 쓰였다
blender size (sx,sy,sz) →  engine size (sx, sz, sy)    Y 가 높이다
blender yaw(+Z)         →  engine orientation [0, yaw, 0]
```

manifest 는 이 변환을 이미 적용한 값을 담고 있다. 그래도 **`KRM_COL_gra_floor`
하나를 먼저 만들어 보고** 파세트궁 바닥 자리에 맞는지 눈으로 확인한 뒤 나머지를 넣어라.
기대 위치는 `[2972.5, -25, 0]`, 크기 `[2745, 50, 2745]`.

전체 범위 (엔진 좌표): X −4030..4215 / Y −25..1030 / Z −1910..1910 → **82 × 10 × 38 m**

## 순서

1. **`overdare_stop` 먼저.** 플레이 중에 쓰면 `level.apply` 가 타임아웃되고 Studio 메인
   스레드가 잠긴다. 사용자가 Stop 을 눌러야만 풀린다 (2026-08-25 에 실제로 겪음).
2. 백업: `onlyoneshot_BEFORE_KRM_<날짜>.ovdrjm`
3. `overdare_mesh_bulk_import` 에 `_overdare/*.fbx` **38개를 한 번에** 넘긴다.
   → `[{asset, meshId, textureIds[]}]` 가 돌아온다.
4. 그 결과를 `meshids.json` 으로 저장한다:
   ```json
   { "mesh": {"KRM_SHELL_GRA_Vault": "ovdrassetid://...", ...},
     "tex":  {"KRM_SHELL_GRA_Vault": "ovdrassetid://...", ...} }
   ```
   키는 manifest 의 `mesh` 값과 같아야 한다.
5. `python make_items.py meshes` → `items_mesh_*.json`
6. 부모 `Workspace` 밑에 `KRM_Palace` Model 을 만들고 그 안에
   `overdare_create_instances` 로 `items_mesh_*` → `items_col_00` 순으로 붓는다.
7. 스폰 2개(`KRM_Spawn_Red` / `KRM_Spawn_Blue`)와 `Arena_Bound_*` 4개를 같은 Model 안에
   넣는다. `CaptureServer.useArenaBounds()` 가 벽 4개를 찾으면 하드코딩 좌표를 무시하므로
   **점령지가 맵을 따라온다.**
8. `overdare_save`

## 알아둘 것

- **MeshPart 는 전부 `canCollide=false`** 다. 물리와 레이캐스트는 투명 박스 116개가 전담한다.
  OVERDARE MeshPart 에는 `CollisionFidelity` 속성이 아예 없다(타입 파일에서 확인).
  `canQuery` 는 **true** 로 둬야 한다 — `TeamServer.snapToGround()` 가 스폰을 바닥에
  앉히려고 아래로 레이캐스트한다.
- 콜리전 116개 중 **48개는 회전이 메시에 구워져 있었다.** 그대로 `dimensions` 를 쓰면
  45° 벽이 911×200 슬래브가 아니라 **786×786 정육면체**로 들어가 팔각형 모서리를 막고
  문까지 막는다. `oriented_box()` 가 지오메트리에서 실제 축을 복원한다.
  같은 이유로 위치도 오브젝트 원점이 아니라 **지오메트리 중심**에서 뽑았다.
- 옥좌는 `KRM_PROP_Throne_p00` / `p01` 두 파일이지만 **텍스처는 한 장을 공유**한다
  (분할 전에 구웠다). 임포트하면 각각 MeshPart 가 되고 같은 자리에 겹쳐 놓으면 된다.
- `KRM_SHELL_Windows` 는 창유리 24장이 **메시 하나**다 (8020 × 2515 × 380). 파츠 1개로
  전체 창을 덮는다.
