# 크렘린 파세트궁(KRM_Palace) 인계 명세서 — Studio 내부 에이전트용

작성 2026-08-27. 대상 레벨 `C:\Users\HSP\Desktop\onlyoneshot\onlyoneshot.ovdrjm`.

이 문서 하나만 읽고 일할 수 있게 썼다. **먼저 「지금 상태」와 「이미 배제한 것」을 읽어라.**
바깥에서 이미 이틀치 조사를 했고, 같은 걸 다시 파면 시간만 버린다.

---

## 1. 해야 할 일

**방들의 방향(yaw)을 눈으로 보고 맞추는 것.** 이것 하나다.

사용자가 반복해서 지적한 증상 :

> "모든 방들이 죄다 중앙이랑 정반대로 180도 돌아져 있다"
> "현재 막혀 있는 부분 정반대에 문이 있다"
> "방마다 다 돌려야 한다"

즉 **방(GRA / TER / 회랑 / 스텁 / 터렛)의 출입구가 중앙 홀을 등지고 있다.**
중앙 팔각홀(VLA)은 대칭이라 문제가 안 보인다.

지금은 `yaw = 원본 + 180` 으로 지어져 있다. 이게 맞는지 틀리는지 **아직 아무도 눈으로 확인 못 했다** —
그동안 궁전 자체가 화면에 안 보였기 때문이다(원인은 아래 4절에서 해결됨).

### 판정 기준

중앙 팔각홀(VLA, 중심 `X 100000, Z 0`)에서 밖으로 나가는 통로가 각 방의 **문**과 이어져야 한다.
방의 막힌 벽이 중앙을 향하고 있으면 틀린 것이다.

### 부차 과제 (여유 있으면)

- **회랑 `cor_n` / `cor_s` 에 문 구멍이 없다.** 메시 자체가 막힌 관이다.
  이건 회전으로 안 고쳐지고 블렌더에서 메시를 뚫어 재발행해야 한다. **손대지 말고 보고만 해라.**
- 소품(의자·책상·촛대)에 콜라이더가 하나도 없다. 전부 통과된다.

---

## 2. 지금 상태 (2026-08-27 실측)

`Workspace / KRM_Palace` (Model), 자식 **293**개.

| 종류 | 개수 | 이름 규칙 | 비고 |
|---|---:|---|---|
| MeshPart | **123** | `KRMM_*` | 셸 25 + 소품 98 |
| Part (콜리전) | **164** | `KRM_COL_*` | `Transparency = 1`, `CanCollide = true`. 눈에 안 보인다 |
| SpawnLocation | **2** | `KRM_Spawn_Red` / `KRM_Spawn_Blue` | 팀색 21 / 23 |
| Part (경기구역 표시) | **4** | `KRM_Bound_North/South/East/West` | 빨간 Neon, 바닥에 낮게 깔린 테두리 |

**공간 범위** : X 96000 ~ 105300 · Y −25 ~ 1815 · Z −1910 ~ 1910 (cm). 1 unit = 1 cm.
궁전 바닥은 **Y 0**, 지붕 최고점 **Y 1815**.

**셸 25개** (문제의 대상) :

```
KRMM_KRM_SHELL_VLA_FloorPlate / VLA_Room / VLA_Gallery / VLA_Oculus / VLA_Tent.017   <- 중앙 팔각홀
KRMM_KRM_SHELL_GRA_FloorPlate / GRA_Room / GRA_Pier / GRA_Vault                       <- 동쪽 큰 방
KRMM_KRM_SHELL_TER_FloorPlate / TER_Rooms / TER_Vaults                                <- 서쪽 방
KRMM_KRM_SHELL_Windows
KRMM_cor_n / cor_s                    <- 남북 회랑
KRMM_seni_e / seni_w                  <- 전실
KRMM_stub_gn / gs / tn / ts / vn / vs <- 연결 토막
KRMM_turret_ne / turret_sw            <- 팔각탑
```

현재 회전 : 중앙 VLA 5개와 소품 98개는 `yaw 0`, **나머지 셸 20개가 `yaw −180`**.

---

## 3. 절대 하면 안 되는 것

1. **FBX 재임포트 금지.** 이 프로젝트에서 메시 발행은 **되돌릴 수 없다.**
   다시 임포트하면 교체가 아니라 **에셋이 중복 발행**되고 자산표가 지저분해진다.
   지금 올라간 에셋 25종은 **정상이다**(서버 썸네일로 확인함). 다시 올릴 이유가 없다.
2. **`Lighting` / `Atmosphere` 를 맵 사정으로 고치지 마라.** 전역 서비스 하나뿐이라
   산곡·화성과 로비가 같이 바뀐다. 맵별 조명은 `ReplicatedStorage/MapService` 의 프리셋이 담당한다.
3. **`KRM_Spawn_Red` / `KRM_Spawn_Blue` 와 `KRM_Bound_*` 4장의 이름을 바꾸거나 지우지 마라.**
   맵 투표 시스템이 이 이름으로 찾는다 (7절 참조).
4. **`KRM_COL_*` 164장을 지우지 마라.** 이게 유일한 충돌면이다. 셸 메시로는 못 걷는다.
5. 소품(`KRMM_KRM_PROP_*` 98개)은 자리가 맞다. 건드릴 이유가 없다.

---

## 4. ★ 궁전이 안 보였던 이유 (해결됨 — 다시 만들지 마라)

**경기구역 벽 `KRM_Bound_*` 4장이 범인이었다.**

반투명 Neon 판을 **높이 3000 cm 로 궁전 전체를 감싸게** 세워 놨더니, 편집기에서 밖에서 볼 때
궁전을 통째로 덮어버렸다. 소품은 작고 어두워서 보였고 흰 셸은 파묻혔다.

증명 : 벽 없이 재건축 → 궁전 보임 → 벽 4장 추가 → 즉시 사라짐.

**해결** : 벽 높이를 **120 cm 로 눕혔다.** 판정은 한 치도 안 변한다 —

```lua
-- BoundaryServer.readRect()
if size.X < size.Z then          -- 두께로 동/서를 가른다
    minX / maxX <- pos.X          -- 위치만 쓴다
else
    minZ / maxZ <- pos.Z
end
```

`size.Y` 는 어디서도 안 읽는다. `CaptureServer` 도 사각형만 받고,
인게임 빨간 울타리는 `BoundaryFX` 가 사각형에서 따로 그린다.

⚠ **벽을 다시 높이 세우지 마라.** 세우면 궁전이 또 사라진다.

---

## 5. 이미 배제한 것 (조사 재탕 금지)

「셸이 안 보인다」를 파면서 전부 확인했다. 아래는 **원인이 아니다.**

| 확인한 것 | 결과 |
|---|---|
| 레벨 데이터가 손상됐나 | 아니오. 작업 전 백업과 289개 노드가 **바이트 단위로 동일** |
| 에셋이 비활성인가 | 아니오. 셸 25개 전부 `bIsActive: true` |
| 발행된 메시가 비었나 | 아니오. **서버 썸네일에 아치 문 달린 방이 제대로 나온다** |
| 법선이 뒤집혔나 | 아니오. 블렌더 원본의 부호 부피가 전부 양수(바깥 방향) |
| `MeshId` 가 엉뚱한 걸 가리키나 | 아니오. 25개 전부 이름이 맞는 `STATIC_MESH` |
| `Size` / `Transparency` | 전부 `Size 100` / `Transparency 0`. 소품과 완전히 동일 |
| `DoubleSided` | 켜도 변화 없었다 (지금은 `false` 로 돌아가 있다) |
| 콜리전이 가리나 | 아니오. 164장 전부 `Transparency = 1` |
| 완전 삭제 후 재건축 | 그 자체로는 변화 없었다 (벽을 다시 넣으면 또 사라졌다) |

---

## 6. 함정 목록 (실측으로 데인 것들)

- **`MeshPart.Size` 는 배율이다. `100` 이 원본 크기다.** 실치수(cm)를 넣으면 수십 배로 커진다.
  `UnitExtent` 가 실제 절반치수이고 Studio 가 되써 준다.
- **실내에서는 「위에서 아래로」 레이캐스트가 항상 지붕을 먼저 맞는다.**
  스폰을 30 m 위에서 쏘게 뒀더니 `Y 10 → 1065`(지붕)에 붙어서 플레이어가 궁전 위에 섰다.
  지금은 맵별로 낮춰 뒀다(`MapService.krm.snapRise = 300`, `rayTop = 400`).
- **텍스처 알파가 안 먹는다. 정점색도 안 먹는다.** (P0 프로브 실측)
- **셸 텍스처가 거의 순백/단색이다.** 텍셀 밀도가 5~10 px/m 라 벽이 흐릿하다.
  UV 타일링은 되는 것으로 확인됐지만 UV 는 메시에 구워지므로 재발행이 필요하다 — 지금은 손대지 마라.
- 임포터가 에셋 이름의 **점을 밑줄로 바꾼다** (`Bench_i.014` → `Bench_i_014`).

---

## 7. 게임 연결부 — 이 이름들이 깨지면 경기가 안 돈다

크렘린은 **3맵 투표제**(산곡·화성·크렘린)의 한 맵이다. 정의는 `ReplicatedStorage/MapService`.

| 이름 | 쓰는 곳 | 깨지면 |
|---|---|---|
| `KRM_Palace` (Model, Workspace 직속) | `MapService.krm.containers[1]` | 맵 스왑이 이 이름으로 컨테이너를 옮긴다. 이름이 바뀌면 스왑 실패 |
| `KRM_Spawn_Red` / `KRM_Spawn_Blue` | `TeamServer` | 팀 배정·부활 위치. 없으면 배치가 통째로 안 된다 |
| `KRM_Bound_North/South/East/West` | `BoundaryServer` | **4장이 다 있어야 한다.** 하나만 없어도 경기구역 판정이 조용히 쉰다 |
| `KRM_COL_*` | 충돌 | 셸 메시에는 콜리전이 없다. 이게 유일한 발판 |

경기구역 사각형 : **X 96000 ~ 105300 · Z −1900 ~ 1900**.
`MapService.krm.rect` 에 같은 값이 폴백으로 적혀 있으니 벽을 옮기면 그쪽도 같이 고쳐야 한다.

⚠ **벽의 「얇은 축」 규칙** : `size.X < size.Z` 면 동/서 벽으로 친다.
남/북 벽은 X 가 길어야 하고 동/서 벽은 Z 가 길어야 한다. 어기면 사각형이 안 나온다.

---

## 8. 바깥에서 쓰던 도구 (참고용, 안 써도 된다)

`C:\Users\HSP\Desktop\blender\gyeongbokgung\` 의 PowerShell 스크립트들.
포트 13377 의 JSON-RPC(`level.apply` / `level.save.file`)로 레벨을 밀어 넣는 방식이다.

| 스크립트 | 하는 일 |
|---|---|
| `krm_build.ps1` | **KRM_Palace 를 통째로 다시 짓는다.** 이게 정본 배치 도구 |
| `vote_bounds.ps1 -Map krm` | 경기구역 벽 4장 재생성 |
| `vote_krm3.ps1` | 자식들의 위치·회전을 종류별로 덤프 |
| `vote_krm6.ps1` | `DoubleSided` / `Material` 덤프 |
| `vote_count.ps1` | Workspace / ServerStorage 인스턴스 수 |

### `krm_build.ps1` 회전 스위치

배치 원본은 `kremlin\KRM_work\export_v1\placement.json` (전부 블렌더 cm).
메시 124 + 콜리전 164 + 스폰 2. `KRM_SHELL_GRA_Responds` 는 문을 막아서 기본으로 제외된다(→ 123).

```
기본 규약 : engine = (bx, bz, -by),  engine yaw = byaw

-YawOfs <각도>   yaw 에 상수를 더한다
-KeepCenter      중앙 팔각홀(KRM_SHELL_VLA*) 은 YawOfs 에서 제외
-RoomsOnly       소품(KRM_PROP*) 은 YawOfs 에서 제외
-FlipZ           engine z 부호 반전 (남북 거울)
-FlipYaw         yaw 부호 반전
```

**지금 쓰인 명령** :

```powershell
.\krm_build.ps1 -YawOfs 180 -KeepCenter -RoomsOnly -Apply
.\vote_bounds.ps1 -Map krm -Apply          # 위 명령이 벽을 지우므로 반드시 뒤이어 실행
```

방향이 틀리면 `-YawOfs` 만 90 / 270 으로 바꿔 다시 지으면 된다. 몇 초짜리다.
`-YawOfs 0` 이 원본 그대로다.

⚠ **`krm_build.ps1` 은 `KRM_Bound_*` 를 모른다.** 재건축하면 벽이 사라지므로
반드시 `vote_bounds.ps1 -Map krm -Apply` 를 뒤이어 실행해라.

---

## 9. 되돌리기

- **백업** : `C:\Users\HSP\Desktop\ovdr_backup\` 에 단계별로 전부 있다.
  이번 작업 시작 직전은 `20260827_065850_before_mapvote`.
- **크렘린만 되돌리기** : `krm_build.ps1 -YawOfs 180 -KeepCenter -RoomsOnly -Apply` + `vote_bounds.ps1 -Map krm -Apply`
- **통째로 지우기** : `krm_build.ps1 -Remove -Apply`
- 이번 작업에는 **메시·텍스처 발행이 하나도 없었다.** 되돌릴 수 없는 것은 없다.

---

## 10. 확인 방법

**값 대조는 검증이 아니다. 반드시 눈으로 봐라.**

- 편집기 뷰포트로 `X 96000~105300, Z ±1900` 를 본다.
- 플레이로 확인하려면 `MapService.DEBUG_FORCE = "krm"` 를 켜면 부팅 후 크렘린으로 강제 스왑하고
  플레이어를 전장에 세운다. **확인이 끝나면 반드시 `nil` 로 되돌려라.**
- Lua `print` 출력은 `C:\Users\HSP\AppData\Local\Sandbox\Saved\Logs\Sandbox.log` 의
  **`LogLuaMachine`** 채널에 남는다. (`LogLuaBasePart` / `LogLuaMeshPart` 는 엔진 경고라 걸러라)
