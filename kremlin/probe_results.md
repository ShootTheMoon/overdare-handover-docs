# P0 프로브 결과 — 2026-08-27

계획서: `C:\Users\HSP\.claude\plans\linear-drifting-breeze.md`
레벨 백업: `Desktop\ovdr_backup\20260827_000716_BEFORE_KRM_PROBE`
스크립트: `gyeongbokgung\krm_probe_parts.ps1` / `krm_probe_meshes.ps1` / `krm_probe2.ps1` / `krm_probe3.ps1`

---

## 결과 표

| # | 항목 | 결과 | 근거 |
|---|---|---|---|
| **P0-1** | **UV wrap (UV > 1)** | **통과** | 4색 띠 텍스처가 `UV 0..4` 판에서 **정확히 4주기(16띠)** 반복 |
| **P0-2** | 음수·비정수 UV | **통과** | `UV −1..3.5` 판이 **4.5주기**로 반복하고 끝에서 반쪽으로 잘림 |
| **P0-3** | 2048 텍스처 | **통과** | 임포트 성공, 4 px 체커·동심원이 선명 |
| **P0-4** | 2 m/타일 밀도 체감 | **통과** | 27×6 m 판에 실제 테렘궁 사진 타일 13.5×3 반복 — 또렷하게 읽힘 |
| **P0-5** | **정점색(버텍스컬러)** | **실패** | 흰→검 그라디언트를 구운 판의 좌→우 밝기 **0.262 / 0.268 / 0.248 / 0.249** (비 1.05). 정점색 없는 판과 구별 불가 |
| **P0-6** | 파츠 `Color` 틴트 | **통과** | 같은 메시·같은 2048 텍스처가 `Color` 255,255,255 / 255,150,60 에서 뚜렷이 갈림 |
| **P0-7** | **텍스처 알파** | **실패** | RGBA 유리 텍스처(구멍 + 반투명 링)를 흰 배경판 앞에 놓아도 `Basic`·`Glass` 둘 다 **완전 불투명** |
| **P0-8** | MaterialVariant | **보류** | 레벨에는 정확히 저장되나 **화면에 반영 안 됨**. 전역 슬롯(`MaterialService.Marble`) 등록해도 동일 |
| **P0-9** | PointLight | **통과** | 지정 색(255,190,120)의 빛 웅덩이가 벽·바닥에 뚜렷. 이 프로젝트 최초 광원 |
| **P0-10** | 스케일·단차 | **자료로 해결** | 아래 참조 — 걷기 시험 불필요 |
| **덤** | **내장 Material 93종** | **발견** | `Marble`·`HouseBricks` 를 Part 와 MeshPart 양쪽에 적용 → **실제 PBR 표면이 나온다.** 임포트·텍셀 예산 0 |
| G3 | 치수 왕복 | **통과** | 되읽은 `UnitExtent` 가 실치수의 정확히 절반 (400→200, 2700×600→1350×300), `Size` 100 |
| G4 | UV 파일 생존 | **통과** | 익스포트→되임포트 UV 범위 `0..4` / `−1..3.5` / `0..13.5` 그대로 |
| R5 | 미러 접기 | **통과** | 5쌍은 회전 없는 동일 메시(오차 0.0000 cm), turret 만 yaw 180°(0.0002). 거울 0건 |

---

## P0-10 — 걷지 않고 결정된 것

`MovementSpeedServer_6.lua` 를 읽어서 끝났다.

- `:186` `humanoid.CapsuleHeight = 164 * CHARACTER_SCALE`, `:33` `CHARACTER_SCALE = 1.25`
  → **캐릭터 캡슐 205 cm, 반지름 30 cm.** 1 unit = 1 cm 에 사람 크기다.
  → **맵은 실척(22.25 m 대홀 = 실제 22.25 m)이 맞다. 스케일 조정 없음.** UV 타일 2 m 확정.
- `:16` `BASE_WALK_SPEED = 700` (7 m/s), 달리기 ×1.7 = 11.9 m/s. 「이동속도 0.72」는 **기하 문제가 아니라
  속도 튜닝**이고, WalkSpeed 는 JSN 과 공유하는 전역이라 맵 스왑에서 다룰 일이다.
- `Humanoid` 에 **스텝업 속성이 없다**(`CapsuleHeight`/`CapsuleRadius`/`MaxSlopeAngle`/`JumpHeight` 뿐).
  `:22` `JUMP_HEIGHT = 190` 이라 46.68 cm 턱은 점프로는 넘는다. 그래도 **22.9° 램프**면
  `MaxSlopeAngle` 45° 아래라 확실히 걸어 오른다 → **계단은 램프로 확정.**
- **개구부 최소 규격이 생겼다: 높이 ≥ 220 cm, 폭 ≥ 70 cm.** P2 에서 전 개구부를 검사할 것.

---

## 계획에 미치는 영향

1. **타일링이 열렸다 → 텍셀 밀도 문제 해결.** 5.2 px/m → 2 m/타일 @1024 = **512 px/m**.
   파츠·트라이 증가 없음. 「베이 모듈 폴백」은 보험으로만 남긴다.
2. **조명 층 1(정점색에 조명 굽기)은 폐기.** 대체:
   - **층 A** 파츠 `Color` 구역 틴트 (확인됨) — 셸을 방·높이별 몇 구역으로 나눠 색조를 준다
   - **층 B** PointLight (확인됨) — 전 맵 8~12개
   - **층 C** 히어로 유니크 텍스처에 명암을 굽는다 (타일 표면은 De-lighting 유지)
   부수 효과: **50 cm 정점 격자가 필요 없어졌다.** 그 트라이 예산을 실제 장식으로 돌린다.
3. **알파가 없다 → 스테인드글라스의 납선·창살은 전부 실제 지오메트리로 만든다.**
   유리는 판별 `Transparency`(파츠 단위)로 처리한다. 계획의 「창틀 + 창살 + 유리 3층」이 필수가 됐다.
4. **내장 머티리얼 93종을 쓴다.** 바닥·소클·석재 벽·회랑 같은 큰 면은 `Marble`/`StoneFloor`/
   `PavingStones`/`HouseBricks` 등으로 덮으면 **텍스처 자산 0장에 무한 해상도**다.
   임포트 텍스처는 **내장으로 흉내 낼 수 없는 것**(프레스코 인물화, 꽃문양, 이콘, 융단)에만 쓴다.
5. **MaterialVariant 는 당장 쓰지 않는다.** 스키마는 확보했으니(아래) 나중에 play 모드에서 재시험.

### MaterialVariant 확정 스키마 (Studio 가 되쓴 값)

```json
{ "InstanceType": "MaterialVariant",
  "BaseMaterial": "Basic", "UseCustomPhysicsProperties": false,
  "MetersPerTile": 2, "Metalness": 0, "Roughness": 0.6,
  "ColorMap":     { "ObjectType": "Content", "Content": "ovdrassetid://NNNN" },
  "MetalnessMap": { "ObjectType": "Content", "Content": "" },
  "NormalMap":    { "ObjectType": "Content", "Content": "" },
  "RoughnessMap": { "ObjectType": "Content", "Content": "" },
  "CustomPhysicalProperties": { "ObjectType": "PhysicalProperties", "Density": 1, "Friction": 1, "Elasticity": 1 },
  "Color": { "ObjectType": "Color3", "R": 255, "G": 255, "B": 255 } }
```
부모는 `MaterialService`. `Emissive`/`EmissiveIntensity` 는 **유효 속성이 아니다**(타입 파일에는 있으나 직렬화가 거부).

---

## 절차상 주의 (겪은 것)

- **`Test-OvdrMethod` 는 메서드를 실제로 호출한다.** `game.play` 를 확인하려다 플레이가 켜졌다.
  즉시 `game.stop` 으로 껐고 손상은 없었다. **부작용 있는 메서드에 쓰지 마라.**
- **이미지 임포트는 이 세션에서 스크립트로 안 된다.** 포트 13377 에 `asset.*` 메서드가 없고
  사이드카(11000)도 응답하지 않는다. → 텍스처 교체는 GUI 수작업이므로
  **텍스처를 발행 전에 완성해 FBX 에 임베드하는 쪽**으로 무게를 옮긴다.
- **에디터 카메라를 RPC 로 옮길 수 없다.** 판정 대상을 카메라 쪽으로 옮기는 편이 빠르다.
- `$(++$k)` 는 PowerShell 문자열 보간에서 **빈 값**이 된다. 미리 증가시켜 변수로 넣어라.
- 파라미터 `$Lights` 와 지역변수 `$lights` 는 대소문자 무시로 충돌한다.
