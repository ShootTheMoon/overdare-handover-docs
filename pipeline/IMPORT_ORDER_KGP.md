# 크렘린 대궁전 → OVERDARE 임포트 절차

출처: `Desktop\Большой Кремлёвский дворец\Kremlin_Grand_Palace_COMPLETE.blend`
익스포터: `Desktop\blender\kgp_export.py` (헤드리스, 원본 .blend 는 읽기만 한다)
프로젝트: `Desktop\onlyonetap\onlyoneshot.ovdrjm`

## 이 폴더

```
kremlin_grand_palace_v1/
  01_SHELL/*.fbx      건축·장식 (월드 좌표를 정점에 구움)
  10_MASTERS/*.fbx    여러 번 쓰는 메시 1개씩 (의자·기사상·기둥 부재 등)
  _tex/*.png          재질별 단색 8×8 (FBX 에 임베드됨, 참고용)
  scene_dump.json     배치 좌표·크기·색·콜리전
  kgp_place.py        scene_dump → items_*.json
  IMPORT_ORDER.md     이 문서
```

## 좌표 규약

```
engine X = blender x * 100 + 146000
engine Y = blender z * 100
engine Z = -blender y * 100 - 1400
size     = bbox cm, Y/Z 교환
```

기존 맵과 겹치지 않는 구역을 골랐다: 산곡 X −38000…−22000 · 화성 −67000…−49000 ·
창덕궁 22800…37200 · 크렘린 실내 95800…105500 → **대궁전 X 142900…149100, Z −2900…2900**.

## 순서

1. **플레이 정지.** 재생 중에 쓰면 `level.apply` 가 타임아웃되고 Studio 메인 스레드가 잠긴다.
2. 백업: `onlyoneshot.ovdrjm` → `onlyoneshot_BEFORE_KGP_<날짜>.ovdrjm`
3. 콜리전부터 넣어 좌표를 눈으로 검증한다 (임포트 없이 바로 된다):
   ```
   python kgp_place.py            # items_col_00.json 생성
   ```
   `ServerStorage` 밑에 `KGP_GrandPalace` Model 을 만들고 그 안에 `items_col_*` 를 붓는다.
   `KGP_COL_FLOOR_hall_000` 이 X 146000 · Y −25 · Z −1400 근처, 크기 3200 × 50 × 5600 이면 맞다.
   투명도 1 이라 안 보이므로 처음에는 `transparency` 를 0 으로 바꿔 한 장 찍어 보는 편이 빠르다.
4. **벌크 임포트.** `01_SHELL` + `10_MASTERS` 의 `*.fbx` 를 한 번에 넘긴다(200개 한도).
   결과 `[{asset, meshId, textureId}]` 를 `meshids.json` 으로 저장한다.
   - 재임포트는 교체가 아니라 중복 발행이다. 한 번 올린 파일은 다시 올리지 않는다.
   - 30,000 삼각형은 파일 단위 한도다. 익스포터가 25,000 이하로 맞춰 두었다.
5. 배치 JSON 생성:
   ```
   python kgp_place.py meshids.json      # items_static_*, items_master_* 생성
   ```
6. `overdare_create_instances` 로 `items_static_*` → `items_master_*` 순서로 붓는다.
   부모는 3번에서 만든 `KGP_GrandPalace`.
7. 스폰과 경계: `KGP_Spawn_Red` / `KGP_Spawn_Blue`, `KGP_Bound_North/South/East/West` 를 같은 Model 안에 둔다.
   산곡·화성 것을 복제해 이름만 바꾸는 편이 빠르다.
8. `overdare_save`.
9. MapService 에 `kgp` 항목 추가:
   `containers = { "KGP_GrandPalace" }`, `rect = { minX = 142900, maxX = 149100, minZ = -2900, maxZ = 2900 }`,
   `center = { x = 146000, z = 0 }`, `groundY = 0`, `label = "KREMLIN GRAND"`.
   `M.ORDER` 에 `"kgp"` 를 넣으면 투표에 나온다.

## 알아둘 것

- 메시는 전부 `CanCollide=false` 다. 걷는 면과 레이캐스트는 `KGP_COL_*` Part 가 맡는다.
- 계단은 발판마다 슬랩 1개(좌우 30개씩)라 실제로 걸어 올라갈 수 있다.
- 문짝은 열린 각도 그대로 구워져 있다. 여닫이가 필요하면 문짝만 마스터로 다시 뽑아
  `Mobility=Movable` 로 넣고 Lua 로 돌린다(화성 `HwsDoorServer` 방식).
- 블렌더의 절차적 재질(대리석 결·물 굴절·발광)은 FBX 로 넘어가지 않는다.
  색은 재질별 단색 텍스처 + MeshPart `Color` 로 간다. 분수 물과 유리는 불투명하게 보인다.
- 임포트한 에셋 이름에 한글이 있으면 테이블에 한글로 남는다. 익스포터는 전부 ASCII 로 쓴다.


---

## 2026-09-17 실장 기록 — 끝났다

180개 FBX 를 45개씩 4묶음(`_batch_01`~`_batch_04`)으로 나눠 벌크 임포트했다.
한 번에 180개를 넘기면 Studio 가 D3D12 OutOfMemory 로 죽는다. 4묶음은 무사했다.

에셋 테이블에 STATIC_MESH 180 + MODEL 180 이 등록됐고 중복 발행은 없었다.
메시/텍스처 id 는 `UGCLocalAssetTable.json` 에서 이름으로 해석해 `meshids.json` 으로 저장했다
(이름 뒤에 `_YYYYMMDDHHMMSS` 가 붙으므로 그 접미를 떼고 맞춘다).

```
KGP_X0=100650 python kgp_place.py meshids.json
```

**옛 크렘린 파세트궁 자리(X 100650)에 앉혔다.** 결과 `Workspace.KGP_GrandPalace` 443개:
콜리전 Part 93 · 밀폐 6 · 경계 4 · 정적 메시 176 · 마스터 인스턴스 162 · 스폰 2.

### 걸린 것들

- **`overdare_create_instances` 는 Part 의 Shape 를 기본 Cylinder 로 만든다.**
  콜리전 바닥이 원통이 되면 모서리로 떨어진다. `shape: "Block"` 을 반드시 넣는다.
- **`level.apply` 가 10초 제한을 넘겨 타임아웃해도 작업은 끝나 있을 때가 있다.**
  타임아웃이 뜨면 재시도하기 전에 마지막 항목이 들어갔는지 먼저 확인한다. 안 그러면 중복된다.
- **한 번에 176개를 부으면 좌표가 통째로 날아간다.** 20개씩 끊어 넣었고,
  그래도 마지막 묶음 16개 + 프레임 12개가 원점에 박혀서 `overdare_instance_update` 로
  CFrame 을 다시 넣었다. **부은 뒤에는 반드시 전수 대조한다**(`_fixpos.json` 참고).
- **`overdare_save` 는 Studio 메모리를 `Lua\*.lua` 로 덮어쓴다.** 스크립트를 파일에서 고치면
  저장 한 번에 날아간다. `.ovdrjm` 안의 `Source` 를 국소 치환하고 `level.apply` 해야 한다.
  UTF-16LE 이고 JSON 문자열 안이라 `"` 는 `\"` 로 이스케이프해야 한다(안 하면 파일이 깨진다).
- **메시는 전부 180도 돌아서 들어온다.** 명세서 3-2 참조. `kgp_place.py` 가 이제 자동으로 넣는다.
- 편집기 뷰포트에서 맵이 까맣게/안 보이는 건 정상이다. 실내라 광원이 없고,
  X 100650 은 하늘 구체 바깥이라 뷰포트가 가려진다. **플레이로 확인한다.**
