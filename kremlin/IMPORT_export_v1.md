# KRM_Palace 발행 패키지 v1 — 2026-08-27

**받은 패키지를 그대로 쓰되 미러 6쌍만 접은 판.** 지오메트리·텍스처는 원본과 동일하다.

| | 원본 패키지 | 이 패키지 |
|---|---:|---:|
| 발행 FBX | 38 | **32** |
| 텍스처(임베드) | 37 | **31** |
| 용량 | 18.5 MB | **17.5 MB** |
| 고유 tris | 131,415 | 131,079 |
| 월드 tris | 630,481 | **630,481** (동일) |
| 메시 인스턴스 | 124 | **124** (동일) |
| 콜리전 파츠 | 116 | 116 (변경 없음) |

## 통과한 게이트

되임포트해서 원본과 대조: **32/32 통과.**

| 게이트 | 결과 |
|---|---|
| 파일당 tris ≤ 28,800 | ✅ 최대 **27,999** (Pechka) |
| 오브젝트 1 / 머티리얼 1 / 텍스처 1 | ✅ 32/32 |
| 텍스처 ≤ 2048 | ✅ 512 / 1024 뿐 |
| 치수 왕복 | ✅ 32/32 원본과 동일 |
| UV 범위 왕복 | ✅ 32/32 동일 |
| 배치 다중집합 대조 | ✅ 124 = 124, **유일한 차이가 의도한 `turret_sw` yaw 180°** |
| 미러(음수 determinant) | ✅ 0건 — 접은 6쌍 전부 순수 평행이동/yaw |

익스포트 설정(왕복 검증 완료): 씬 **1 unit = 1 cm**,
`global_scale=1.0, apply_unit_scale=True, apply_scale_options=FBX_SCALE_NONE,
bake_space_transform=False, axis_forward=-Z, axis_up=Y, use_triangles=True,
path_mode=COPY, embed_textures=True`

## 접은 6쌍

| 남긴 메시 | 없앤 파일 | 방법 |
|---|---|---|
| `cor_n` | cor_s | 정점 완전 동일 → 위치만 다르게 |
| `seni_e` | seni_w | 〃 |
| `stub_gn` | stub_gs | 〃 |
| `stub_tn` | stub_ts | 〃 |
| `stub_vn` | stub_vs | 〃 |
| `turret_ne` | turret_sw | **yaw 180°** (접은 뒤 최대 오차 0.0002 cm) |

## 발행 절차

**메시 발행은 되돌릴 수 없다. 재임포트는 교체가 아니라 중복 발행이다.**

1. **Studio 에서 플레이를 멈춘다.** (`game.stop`. 플레이 중 `level.apply` 는 메인스레드를 잠근다)
2. 레벨 백업 — `Backup-OvdrLevel -Tag BEFORE_KRM`
3. 프로브 정리(선택) — `.\krm_probe_parts.ps1 -Remove -Apply`, `.\krm_probe_meshes.ps1 -Remove -Apply`,
   `.\krm_probe2.ps1 -Remove -Apply`
4. **임포트 직전 스냅샷** — `.\krm_place_meshes.ps1 -Snapshot`
   (에셋 매핑은 이름이 아니라 **contentId 집합 차이**로 한다)
5. **Studio GUI 에서 이 폴더의 `*.fbx` 32개를 벌크 임포트한다.** 이 PC 엔 메시 임포트 RPC 가 없다.
6. `.\krm_place.ps1 -Apply` — `KRM_Palace` Model + 콜리전 116 + 스폰 2 (ΔX +100000)
7. `.\krm_place_meshes.ps1 -Resolve` 로 이름 대조 → 이상 없으면 `-Apply`
8. `game.screenshot` 으로 눈 확인. **값 대조는 검증이 아니다.**

## 이 패키지가 고치지 않은 것 (알고 넘어가는 것)

전부 **발행과 무관하고 나중에 되돌릴 수 있게 고칠 수 있다.**

**표면** — 셸 텍셀 밀도가 GRA 5.2 / VLA 8.7 / TER 9.5 / 회랑 10.6 px/m 다. 벽이 흐릿하게 나온다.
텍스처 내용도 32단계 양자화 고유색이 25~86 수준(사실상 단색 노이즈판)이고,
**샹들리에 텍스처는 1024 전면 순수 검정**, 옥좌는 최대휘도 0.31 이다.
→ UV wrap 이 통과했으므로(P0-1) **타일링으로 512 px/m 까지 올릴 수 있다.** 다만 UV 는
메시에 구워지므로 **재발행이 필요하다.**

**콜리전** — 재발행 없이 `items_col_00.json` 수정만으로 끝난다.
- 계단탑 라이저 **46.68 cm × 12칸** → 22.9° 램프 2장으로 교체 (콜리전 24 → 2)
- VLA(점령지) **천장 콜라이더 없음** (콜리전 Y 최대 900 vs 텐트볼트 921)
- `vla_wall_104`/`110` 만 윗면 560, 나머지 10장은 900 → 회랑 높이에 **3.4 m 틈**
- `turret_side` 가 팔각탑당 2면뿐
- **소품 콜라이더 0개** — 인스턴스 98개가 전부 통과 가능(FPS 엄폐물이 중앙 기둥 1개뿐)

**게임 연결** — `TeamServer` 는 `JSN_Spawn_*` 만 찾으므로 `KRM_Spawn_Red/Blue` 는 아직 예비 지점이다.
`Arena_Bound_*` 는 **일부러 안 넣었다** (`CaptureServer.useArenaBounds()` 가 재귀 검색이라
JSN 용 동명 벽과 충돌해 살아 있는 경기를 망칠 수 있다). 맵 스왑 작업에서 함께 처리한다.
`MovementSpeedServer_6.lua` 의 `BASE_WALK_SPEED = 700` 은 259 m 야외 기준이라 82 m 실내엔 빠르다.

**저작권** — 소품은 스케치팹 CC0/CC-BY 인데 **`ATTRIBUTION.md` 가 이 PC 에 없다.**
공개 발행 전에 다른 PC 에서 받아 와야 한다.
