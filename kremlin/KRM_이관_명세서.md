# KRM_Palace — OVERDARE 이관 명세서

**크렘린궁 실내 FPS 맵.** `onlyoneshot` 의 3맵 투표제용 세 번째 맵.
이 폴더만 있으면 OVERDARE Studio 에 넣을 수 있다. 블렌더 파일은 필요 없다.

작성 2026-08-26 · 출처 `Desktop\Kremlin\KRM_Palace_rebuild.blend`
생성 스크립트 `Desktop\Kremlin\overdare_prep.py` (원본 .blend 는 저장하지 않음)

---

## 1. 맵이 뭔가

크렘린궁의 실제 실내 3실을 **허브 앤 스포크**로 이은 근접전 맵이다.
블라디미르 홀이 실제로 파세트궁·테렘궁·게오르기옙스키 홀을 잇는 교차점이라,
이 배치는 역사적으로도 맞고 FPS 3레인 구조도 된다.

```
                   [테렘궁 앙필라드 — 거실]
                    6.5 x 9.0 m 방 3개가 한 줄
                    문이 남쪽으로 치우쳐 뚫려 한 줄 시야
                              |  (세니)
   [파세트궁 대홀] ── 세니 ── ● 블라디미르 홀 ──
    22.25 m 정사각            16 m 팔각 · 창 없음
    엄폐물은 중앙 기둥 1개     빛은 지름 6 m 천창뿐
    볼트 9 m                  16각 텐트볼트 18 m · 회랑 5.6 m
    RED 스폰                  중립 · 점령지            BLUE 스폰
```

여기에 **남북 42 m 직선 회랑 2개**가 측면 루트로 붙고,
블라디미르 홀 회랑은 **NE·SW 계단탑으로만** 올라간다.

**전체 범위 (엔진 좌표)** X −4030..4215 / Y −25..1030 / Z −1910..1910 → **82 × 10 × 38 m**

실측 근거는 `ref/06_파세트궁/0_실측도면/RZ2_tab12.jpg` (1953년 실측 도판).
파세트궁 대홀 22.25 m 정사각 · 볼트 정점 9.0 m · 중앙 기둥 1개는 도면에서 직접 뜬 값이다.

---

## 2. 폴더 내용

```
KRM_Palace_OVERDARE/
  *.fbx                38개   18.5 MB   ← Studio 에 넣는 것
  _tex/                37장             베이크된 컬러맵 (참고용, FBX 에 이미 임베드됨)
  manifest.json                          배치 좌표 · 콜리전 · 소스 추적
  items_col_00.json                      콜리전 파츠 116개 (지금 바로 사용 가능)
  make_items.py                          manifest → overdare_create_instances 페이로드
  IMPORT_ORDER.md                        임포트 절차 (짧은 버전)
  KRM_이관_명세서.md                      이 문서
```

텍스처는 FBX 에 임베드돼 있다. `_tex/` 는 확인용이지 따로 올릴 필요 없다.

---

## 3. 숫자

| | |
|---|---|
| 렌더 오브젝트 105개 → **고유 메시 35개** | 인스턴스 공유가 심해 실제 파일은 38개뿐 |
| FBX | **38개 / 18.5 MB** (최대 1.65 MB) |
| 고유 트라이 | 131,415 |
| 월드 트라이 | 630,481 |
| 메시 배치 | 124 |
| 콜리전 파츠 | 116 |
| **총 파츠** | **240** |

참고: `JSN_Sangok` 이 3,396 파츠다. 이건 그 **7%** 다.
2026-08-25 에 4,666 파츠에서 28 fps 가 나왔던 걸 감안하면 여유가 크다.

---

## 4. OVERDARE 규격 대조

| 규칙 | 상태 |
|---|---|
| 메시당 ≤ 30,000 tris | ✅ 최대 27,999 (Pechka). 35,599짜리 옥좌는 **2조각 분할** |
| 머티리얼 1개 = 임포트 단위 1개 | ✅ 다중 머티리얼 메시 분리 (Icon → m0/m1/m2) |
| MeshPart 텍스처 1장 | ✅ 전부 단일 컬러맵으로 베이크 |
| 텍스처 ≤ 1024 (512 권장) | ✅ 512 기본 / 히어로 소품 1024 |
| FBX당 ≤ 200 메시 | ✅ 파일당 1개 |
| 파일 ≤ 250 MB | ✅ 최대 1.65 MB |
| Y-up, cm | ✅ `axis_forward='-Z', axis_up='Y'` |
| 콜라이더는 FBX 에 못 넣음 | ✅ 엔진 Part 116개로 분리 |
| 벌크 임포트 ≤ 200 파일 | ✅ 38개 → 한 번에 |

**검증 완료** — 5개 파일을 다시 임포트해 대조했다.
트라이 수 일치, 전부 **오브젝트 1 / 머티리얼 1 / 텍스처 1**, 치수 보존.

> ⚠ 원본에는 **4096 텍스처가 22장** 있었다. 그대로 넣으면 임포터가 OOM 난다.
> 전부 512/1024 로 베이크했고, AO·Rough·Displacement·Normal 은 버렸다
> (MeshPart 는 컬러맵 1장만 받는다).

---

## 5. 좌표 규약 — ★ 하나로 먼저 검증하고 나머지를 깔아라

```
blender (bx,by,bz)      →  engine (bx, bz, -by)          FBX 가 Y-up 으로 쓰였다
blender size (sx,sy,sz) →  engine size (sx, sz, sy)      Y 가 높이다
blender yaw(+Z)         →  engine orientation [0, yaw, 0]
```

`manifest.json` 은 **이미 변환된 값**을 담고 있다. 그래도 처음 한 개는 확인해라.

**검증용 파츠**: `KRM_COL_gra_floor` → 기대 위치 `[2972.5, -25, 0]`, 크기 `[2745, 50, 2745]`.
파세트궁 바닥 자리에 정확히 깔리면 나머지를 그대로 부으면 된다.

---

## 6. 임포트 순서

1. **`overdare_stop` 먼저.** 플레이 중에 쓰면 `level.apply` 가 타임아웃되고 Studio
   메인 스레드가 잠긴다. 사용자가 Stop 을 눌러야만 풀린다 (2026-08-25 실제로 겪음).
2. 백업: `onlyoneshot_BEFORE_KRM_<날짜>.ovdrjm`
3. `overdare_mesh_bulk_import` 에 `*.fbx` **38개를 한 번에** 넘긴다.
   → `[{asset, meshId, textureIds[]}]` 가 돌아온다.
4. 결과를 `meshids.json` 으로 저장. 키는 manifest 의 `mesh` 값과 같아야 한다:
   ```json
   { "mesh": {"KRM_SHELL_GRA_Vault": "ovdrassetid://...", ...},
     "tex":  {"KRM_SHELL_GRA_Vault": "ovdrassetid://...", ...} }
   ```
5. `python make_items.py meshes` → `items_mesh_*.json`
6. `Workspace` 밑에 **`KRM_Palace` Model** 을 만들고 그 안에
   `overdare_create_instances` 로 `items_mesh_*` → `items_col_00` 순으로 붓는다.
7. 스폰 2개와 경계벽 4개를 **같은 Model 안에** 넣는다 (아래 7절).
8. `overdare_save`

---

## 7. 맵을 게임에 붙이려면 (아직 안 한 것)

**`KRM_Palace` Model 안에 직접 넣어야 하는 것 — 이걸 해야 기존 서버 스크립트가 붙는다.**

| 넣을 것 | 이유 |
|---|---|
| `KRM_Spawn_Red` (SpawnLocation) | 파세트궁 쪽. `TeamServer.findSpawn()` 이 맵 안에서 못 찾으면 Workspace 전체를 뒤지는 폴백이 있다 |
| `KRM_Spawn_Blue` (SpawnLocation) | 테렘궁 앙필라드 끝 |
| `Arena_Bound_North/South/East/West` | **`CaptureServer.useArenaBounds()` 가 이 벽 4개를 찾으면 하드코딩 좌표를 무시한다.** 즉 점령지가 맵을 따라온다. 이게 맵 스왑의 후크다 |

`TeamServer.snapToGround()` 는 레이캐스트 기반이라 **이미 맵 무관**이다 —
스폰 높이를 손으로 맞출 필요 없다. 대신 콜리전 파츠의 `canQuery` 가 **true** 여야 한다.

**맵 이름이 하드코딩된 곳** (스왑 구조를 넣을 때 여기만 고치면 된다):

| 파일 | 줄 | 내용 |
|---|---|---|
| `TeamServer.lua` | 89 | `Workspace:FindFirstChild("JSN_Sangok")` |
| `CaptureServer.lua` | 56–59 | `MAP_NAME` + 하드코딩 X/Z 범위 |
| `SeamFiller.lua` | 24 | `MAP_NAME` — 산곡 지형 전용, 다른 맵이면 즉시 return 시켜야 한다 |
| `MovementSpeedServer_6.lua` | — | 259×271 m 기준 이동속도(700). **82 m 실내에선 너무 빠르다.** 배수 0.72 권장 |

`MapService` ModuleScript 초안이 `Desktop\Kremlin\engine\MapService.lua` 에 있다.

---

## 8. 알아둘 함정

- **MeshPart 는 전부 `canCollide=false`** 다. 물리와 레이캐스트는 투명 박스 116개가 전담한다.
  OVERDARE MeshPart 에는 `CollisionFidelity` 속성이 **아예 없다** (타입 파일에서 확인).
  `canQuery` 는 **true** 로 둬야 한다 — 스폰 접지 레이캐스트가 이걸 쓴다.
- **콜리전 116개 중 48개는 회전이 메시에 구워져 있었다.** 그래서 `dimensions` 를 그대로 쓰면
  45° 팔각 벽이 911×200 슬래브가 아니라 **786×786 정육면체**로 들어가 모서리를 막고 문까지
  막는다. 지오메트리에서 실제 축을 복원해 넣었다. 위치도 오브젝트 원점이 (0,0,0) 이라
  **지오메트리 중심**에서 뽑았다. 둘 다 에러가 안 나므로 임포트 후에야 "왜 못 지나가지"로
  나타난다.
- 옥좌는 `KRM_PROP_Throne_p00` / `p01` 두 파일이지만 **텍스처는 한 장을 공유**한다
  (분할 전에 구웠다). 같은 자리에 겹쳐 놓으면 된다.
- `KRM_SHELL_Windows` 는 창유리 24장이 **메시 하나**다 (8020 × 2515 × 380).
  파츠 1개로 맵 전체 창을 덮는다.
- 재임포트했을 때 `UnitExtent` 는 **half-extent** 다. 2배 해야 원본과 맞는다.
  안 그러면 완벽한 임포트가 50% 축소된 것처럼 보인다.

---

## 9. 에셋 출처

구조 셸(벽·볼트·바닥·계단)과 벽 텍스처 7종은 **자체 제작**이다.
스케치팹에 크렘린 실내에 쓸 수 있는 구조 셸은 없다.

소품은 스케치팹에서 가져왔고 **전부 CC0 또는 CC Attribution, ShareAlike 0건**이다.
저작자 표시 의무가 있으므로 목록은 `Desktop\Kremlin\ATTRIBUTION.md` 를 그대로 유지할 것.
받았다가 버린 것들(뭉개진 타일 스토브 3종 등)도 이유와 함께 거기 적혀 있다.

색유리 창 텍스처는 `ref/07_테렘궁/_indoor/12.jpg` 의 실제 테렘궁 창을 잘라 만들었다.

---

## 10. 이 폴더에 없는 것

- `.blend` 원본 (`Desktop\Kremlin\` 에 4개 있다)
- 스폰·경계벽 (7절 참조 — 엔진에서 만들어야 한다)
- 맵 스왑 구조 (`MapService.lua` 초안만 있음)
- 3맵 투표 UI
