# 블렌더 맵 → OVERDARE 이식 명세서

JSN_Sangok(산곡, 260×260 m, 인스턴스 2,402 + 충돌 1,669) 작업에서 **실제로 검증된 것만** 담았다.
"아마 그럴 것이다"는 넣지 않았고, **틀린 것으로 판명된 것도 남겼다** — 같은 삽질을 반복하지 않기 위해서다.

작성 2026-08-19. 대상 Studio: `C:\Program Files\Epic Games\OverdareStudioPJVXb\Sandbox\Binaries\Win64\Sandbox-Win64-Shipping.exe`

---

## 0. 도구와 접속

Claude Code 세션에 **overdare MCP 툴은 없다.** 문서에 나오는 `overdare_mesh_bulk_import`,
`overdare_create_instances` 같은 건 OVERDARE Code CLI 쪽(`studiorpc_*`) 이고 여기서는 못 쓴다.

**대신 쓰는 것** — `Desktop\blender\gyeongbokgung\ovdr_*.ps1` 4개. 새로 짜지 말고 dot-source 한다.

| 파일 | 역할 |
|---|---|
| `ovdr_rpc.ps1` | `Invoke-OvdrRpc -Method -Params`. 포트 **13377**, **raw TCP 위 줄바꿈 구분 JSON-RPC**. HTTP 아니다(HTTP로 붙으면 protocol violation). 인증 없음. Studio에 프로젝트가 열려야 포트가 열린다. |
| `ovdr_level.ps1` | `.ovdrjm` 국소 편집. `Get-OvdrLevelPath`, `Read/Write-OvdrText`, `New-OvdrPartJson`, `New-OvdrMeshPartJson`, `Add-OvdrInstances`, `Remove-OvdrInstancesByName`, `Get/Set-OvdrKeyIndex` |
| `ovdr_place.ps1` / `ovdr_readback.ps1` | 에셋 매핑과 검증 |

**RPC 메서드**: `level.browse`, `level.apply`, `level.save.file`, `instance.create`, `instance.delete`,
`game.play`, `game.stop`, `game.screenshot`

**중요한 제약**
- `instance.create` 는 **속성을 안 받는다**(빈 인스턴스만). FBX 임포트 RPC 도 없다.
  → 속성이 있는 건 전부 **레벨 파일 직접 편집 + `level.apply`** 로 넣는다.
- `.ovdrjm` 은 **UTF-16LE + BOM**. 전체를 `ConvertFrom-Json`/`ConvertTo-Json` 왕복시키면
  기존 데이터가 훼손된다. **국소 문자열 치환만** 한다. 검증용으로 `ConvertFrom-Json` 파싱만 해보는 건 괜찮다.
- `.ps1` 은 **UTF-8 BOM 필수**. PS 5.1 은 BOM 없으면 949로 읽어 한글이 깨지고
  `Missing closing '}'` 같은 엉뚱한 파서 에러를 낸다. Write 툴로 만든 직후 붙일 것:
  ```powershell
  $t=[IO.File]::ReadAllText($p,(New-Object System.Text.UTF8Encoding($false)))
  [IO.File]::WriteAllText($p,$t,(New-Object System.Text.UTF8Encoding($true)))
  ```

**카메라 / 스크린샷**
- 에디터 카메라는 **RPC로 못 움직인다.** 레벨의 `Camera` 인스턴스는 인게임 추적 카메라라 무관하다.
- **`game.screenshot` 은 사용자가 지금 보고 있는 뷰포트를 그대로 찍는다.** 사용자가 문제를 보고 있으면
  그 화면을 바로 받을 수 있다. 이걸 늦게 알아서 시야 확보에 많은 시간을 버렸다.
- 플레이 중에는 플레이어 시점. 스폰이 여러 개면 **랜덤**으로 뽑히므로,
  원하는 데서 시작시키려면 다른 `SpawnLocation` 의 `"Enabled"` 를 잠깐 `false` 로 두고 끝나면 되돌린다.

---

## 1. 좌표 규약 — 세 가지를 전부 틀리기 쉽다

정본은 `Desktop\blender\gyeongbokgung\export_overdare.py`. 경복궁을 실제로 배치해 검증된 파이프라인이다.

### 1-1. 축

```
X = bx * 100
Y = bz * 100
Z = -by * 100          ← 부호를 빼면 행렬식 −1 인 거울이 되어 남북이 뒤집힌다
```

행렬 `M = [[1,0,0],[0,0,1],[0,-1,0]]`, det = +1.
근거: FBX Model 노드의 `Lcl Rotation = (−90,0,0)` → `Rx(−90)` = `(x,y,z)→(x,z,−y)`.

### 1-2. 회전 — **ZXY 로 분해**

```python
R_e = M @ R_b @ M.transposed()
eu  = R_e.to_euler('ZXY')          # ← 이것만 맞다
```

- 축별 부호반전 근사: pitch/roll 이 0이 아니면 최대 **46°** 틀린다
- `YXZ` 로 분해: 최대 **160°**, 전체의 **24%가 10° 초과**로 틀어진다

**판정법 (가장 빠르다)**: `Orientation(90,90,0)` 을 써 넣고 저장한 뒤 Studio 가 어떻게 되쓰는지 읽는다.
`(90,0,−90)` 으로 되쓰면 짐벌락 정규화이고, 이 등가가 성립하는 순서는 6개 중 **ZXY 하나뿐**이다.

### 1-3. 피벗 — 임포터가 bbox 중심으로 재중심화한다

`CFrame.Position` 은 메시의 로컬 원점이 아니라 **bbox 중심**이다.
- 마스터 피벗이 바닥 중앙이면(FBX 실측: bbox min z = 0) **로컬 up 으로 h/2 올려야** 한다.
  안 올리면 큰 나무가 자기 높이의 절반만큼 파묻힌다.
- 월드 좌표가 이미 구워진 메시도 `(0,0,0)` 이 아니라 **각자의 bbox 중심**에 놓는다.

**판정법**: 여러 메시를 전부 원점에 놓아본다. 한 자리에 겹쳐 쌓이면 bbox 중심 규약이 맞다.

### 1-4. Size 는 cm 실치수다 (백분율 아님)

- `UnitExtent` 는 **절반값**. `Size = 2 × UnitExtent` 이면 배율 1.
- 구버전 `overdare_create_instances` API 문서는 `size` 가 백분율이라 섞여 있는데 **이 Studio 는 cm 다.**

**판정법**: 엔진 `Part`(프리미티브라 cm 라는 데 이견이 없다)를 문제의 MeshPart 와
같은 자리·같은 의도 크기로 놓고 `game.screenshot` 으로 비교한다.
실측 예 — `Size=100` 을 넣은 지형 타일(UnitExtent 3250)이 1 m 큐브로 렌더돼 화면에서 사라졌고,
같은 자리에 `Size 6500` 인 Part 를 놓자 65 m 슬래브로 나왔다.

---

## 2. 에셋 발행

- **자동화 경로가 없다.** RPC/MCP 에 메시 임포트가 없어서 Studio GUI 의 Bulk Import 를 사람이 클릭해야 한다.
- 폴리곤 **30,000 한계는 메시가 아니라 파일 단위**다. 두 개를 같이 넘기면 실패하거나 Studio 가 크래시한다.
- **재임포트는 교체가 아니라 중복 발행이고 되돌릴 수 없다.** 한 번 올린 에셋은 어떤 경우에도 다시 올리지 않는다.
- ID 매핑은 **이름이 아니라 contentId 집합 차이**로 잡는다.
  JSN 에서는 두 방법으로 교차검증했다 — (a) createdTime 순서 짝짓기, (b) FBX 에 박힌 텍스처 파일명.
  30/30 일치를 확인하고 나서야 배치에 들어갔다. **이 교차검증은 생략하지 마라.**

---

## 3. 지형 충돌 — 메시로는 못 걷는다

### 3-1. 확인된 사실

- MeshPart 에 **`CollisionFidelity` 같은 속성이 없다.** 엔진이 알아서 convex 분해를 한다.
- 높이맵 한 장을 볼록 덩어리 ~30개로 쪼개는 거라 **골짜기는 메워지고 능선은 뭉개진다.**
- `CanCollide=true` 를 켜면 로그상 `[UpdateCollisionEnabled] ... QueryAndPhysics` 로 잡히지만
  **플레이어는 그냥 뚫고 떨어진다.**
- 예전에 본 `Convex hull generation produced zero convex particles` 는 **별개 원인**이었다 —
  그때는 지형 `Size=100` 이라 1 m 큐브로 찌그러져 있었다. 크기를 고치면 이 에러는 안 난다.

### 3-2. 해법 — 쿼드트리 기울어진 Part 슬래브

1. **높이맵 뜨기** — 블렌더에서 지형 오브젝트에 `obj.ray_cast` 로 257×257 격자(0.2초).
   `scene.ray_cast` 는 나무·바위에 맞으니 **반드시 오브젝트 단위 ray_cast** 를 쓴다.
   257 = 2⁸+1 이라 쿼드트리 반분이 정확히 떨어진다.
2. **적응 분할** — 셀마다 최소자승 평면을 맞추고 최대잔차 > 0.5 m 면 4분할, 최소 4 m 까지.
   260×260 m 기준 **1,669개**. 균일 4 m 격자면 4,225개인데 품질은 같다.
3. **리프마다 Block Part**
   - 법선: 블렌더 `(-a,-b,1)` → 엔진 `(-a, 1, b)` (정규화)
   - 회전: `Vector((0,1,0)).rotation_difference(N).to_matrix().to_euler('ZXY')`
     — **Part 는 임포트 에셋이 아니므로 1-2의 180도류 보정을 넣지 않는다**
   - 한 변 = `셀크기 / cosθ + 60 cm` (경사면 투영 보정 + 이웃과 겹침)
   - 두께 = `clamp(2×잔차×100 + 200, 300, 3000)` cm — 절벽 셀은 두껍게 해 속을 채운다
   - 중심 = `평면 위 점 − N × (두께/2)` → **윗면이 지면에 정확히 온다**
4. **넣는 순서** — 처음엔 `Transparency 0` + 눈에 띄는 색으로 넣고 한 장 찍어 지형에 붙었는지 본다.
   확인되면 `Transparency 1` 로 돌린다. 처음부터 투명하게 넣으면 틀려도 안 보인다.
5. **지형 MeshPart 의 `CanCollide` 는 `false` 로 되돌린다.** 엉성한 hull 이 정확한 Part 층과 싸운다.
   바위(볼록에 가깝다)는 켜도 된다. 나무·풀은 끈 채로 둔다.

측정 참고 (JSN, 표고 −1.3 ~ 78.4 m, 최대경사 65°):

| 셀크기 | 파트수 | 잔차 max | 잔차 RMS |
|---|---|---|---|
| 4 m | 4,225 | 2.33 m | 0.05 m |
| 8 m | 1,024 | 5.01 m | 0.16 m |
| 적응(0.5 m/최소 4 m) | **1,669** | — | 평균 0.49 m |

### 3-3. 로그 읽기

`%LOCALAPPDATA%\Sandbox\Saved\Logs\Sandbox.log` (수십 MB). **타임스탬프는 UTC** 다 — 로컬시각과 9시간 차.
`LogLuaBasePart: [UpdateCollisionEnabled]`, `LogPhysics: Warning: TConvex ... BodySetup` 을 본다.

---

## 4. 타일 이음매 선 — **미해결. 여기까지는 아니라고 확인됨**

지형을 4×4 타일로 쪼개 넣으면 타일 경계에 선이 보인다. **이 항목은 해결하지 못했다.**
다음 맵에서 다시 붙기 전에 아래를 먼저 읽어라.

### 4-1. 아니라고 확인된 것 (다시 시도하지 말 것)

| 가설 | 검증 방법 | 결과 |
|---|---|---|
| 타일 위치·크기가 어긋났다 | 블렌더 원본 메시에서 타일 16장의 bbox 중심·크기를 다시 계산해 레벨값과 대조 | **최대 오차 0.006 cm (0.06 mm).** 어긋난 게 아니다 |
| 구운 텍스처에 베이크 마진이 없어 가장자리가 배경색이다 | 타일 PNG 의 맨 바깥 행/열 픽셀을 안쪽과 직접 비교 | 동일 (예: `81,78,48` vs `84,80,51`). 텍스처 가장자리는 멀쩡 |
| `Size.Y` 와 `2×UnitExtent.Y` 불일치로 미세 단차 | 정확히 맞춤 | 선 안 없어짐 |
| 겹치게 만들면 덮인다 | `Size.X/Z ×1.0005` → `×1.001` → `×1.002` | 선 안 없어짐 |
| 높이를 체스판으로 ±1.5 cm 벌리면 Z-파이팅이 사라진다 | 적용 | **더 나빠졌다.** 단차가 곧 처마 끝이라 그 선이 또렷해진다 |
| 한 면 껍질이라 처마 뒷면이 컬링돼 하늘이 샌다 | `DoubleSided: true` | 확대해선 깨끗했지만 **실사용 시야에서는 선이 더 잘 보였다** |

**겹침 + 단차 조합은 특히 나쁘다.** 겹치면 처마가 생기고, 단차가 있으면 그 처마 끝이 선이 된다.
둘 중 하나만 쓰거나 둘 다 안 쓰는 게 낫다.

### 4-2. 마지막에 확인한 선의 실제 모습

사용자 뷰포트를 그대로 받아 확대해 보니 — **밝은 균열이 아니라 지면 색조가 직선으로 딱 끊기는 경계**였다.
한쪽은 밝은 올리브, 다른 쪽은 어두운 녹색. 그래서 기하 쪽을 아무리 만져도 안 없어진 것이다.

**남은 후보 두 개**
1. **타일마다 구운 텍스처의 색조가 다르다** → 레벨에서 타일별 `Color` 배율로 보정 가능. **재발행 불필요.**
   인접 타일의 맞닿는 가장자리 띠 평균색을 비교해 게인을 최소자승으로 풀면 된다(모자이크 색보정).
2. **밉맵 전환 띠** → 카메라에서 일정 거리에 생긴다. 타일과 무관.

**1초에 가르는 법**: 카메라를 앞뒤로 움직인다.
선이 **지면에 붙어 같이 움직이면 텍스처 색조**, **카메라를 따라와 항상 같은 거리에 머물면 밉맵**이다.

### 4-3. 다음 맵에 대한 권고

- **가능하면 지형을 쪼개지 마라.** 폴리곤 한계 때문에 쪼갤 수밖에 없다면 **타일 수를 최소로** 한다.
- 쪼갠다면 **베이크 단계에서 타일 간 색조를 맞춰서 구워라.** 사후 보정보다 훨씬 싸다.
- 배치가 끝나면 **다른 것 하기 전에 이음매부터 확인**해라. 나는 충돌까지 다 만든 뒤에 붙었다.

---

## 5. 진단 기법 — 재사용 가치가 높은 순서

1. **짐벌락 탐침** — 애매한 값을 써 넣고 Studio 가 어떻게 되쓰는지 읽는다. Euler 순서를 한 방에 판정.
2. **기준자 Part** — 엔진 프리미티브를 옆에 놓고 비교. 단위·배율 규약 판정.
3. **전부 원점에 놓기** — 피벗 규약 판정. 한 자리에 쌓이면 bbox 중심.
4. **타일별 색칠** — `Color` 를 빨강/파랑 체스판으로 넣으면 경계가 눈에 보인다.
   선이 그 경계와 겹치는지 한눈에 판정된다. **사람이 화면을 보고 있으면 이걸 띄워 두고 물어보는 게 제일 빠르다.**
5. **구운 텍스처 가장자리 픽셀 읽기** — 텍스처 문제인지 기하 문제인지 오프라인으로 가른다(재발행 판단).
6. **블렌더 원본에서 bbox 재계산 후 레벨값 대조** — 정렬 오차를 mm 단위로 정량화.
7. **격리 테스트** — 나머지를 `CFrame.Position.Y -= 200000` 으로 치우고 둘만 남겨 본다.
8. **`game.screenshot` 은 사용자 뷰포트다** — 사용자가 보고 있는 걸 그대로 받는다. 이걸 먼저 써라.

**교훈**: 값을 다시 읽어 대조하는 건 검증이 아니다. 내가 쓴 값을 내가 읽는 것일 뿐이다.
**그림으로 확인**하거나 **독립적인 경로로 측정**해야 검증이다.

---

## 6. PowerShell 5.1 함정

| 증상 | 원인 | 처방 |
|---|---|---|
| `Missing closing '}'`, 한글 깨짐 | BOM 없는 UTF-8 을 949로 읽음 | `.ps1` 에 UTF-8 **BOM** 붙이기 |
| JSON 이 `True` 로 깨짐 | `$ds` / `$DS` 는 **같은 변수**(대소문자 무시). `'true'` 문자열이 bool 로 강제됨 | 변수명을 겹치지 않게 (`$dsText`) |
| 빈 컨테이너에 자식 1개로 보임 | `@($null).Count == 1` | null 필터링 |
| 압축 해제가 조용히 실패 | `ZipFile.ExtractToDirectory(src,dst,overwrite)` 오버로드가 .NET Framework 4.x 에 없음 | 엔트리별 `ZipFileExtensions::ExtractToFile` |
| 엉뚱한 키에 값이 써짐 | MeshPart JSON 에서 `PivotOffsetCFrame` 이 `CFrame` **보다 먼저** 나온다 | `'"CFrame":'` **리터럴로 앵커**(앞의 따옴표 때문에 `PivotOffsetCFrame` 에는 안 걸린다) |
| Bash 툴이 2분에 끊김 | `game.play` + `level.apply` 여러 번이면 넘는다 | `timeout` 을 300000 등으로 올린다 |

---

## 7. 권장 작업 순서

1. 블렌더에서 좌표·치수 측정 → `master_dims.json`, `static_dims.json`
2. FBX 발행 (사람이 GUI, 파일당 30k 폴리곤 이하, 한 번에 하나씩)
3. 에셋 ID 매핑 **두 방법으로 교차검증**
4. **캘리브레이션 먼저** — 기준자 Part / 짐벌락 값 / 원점 배치 3종으로 규약 확정
5. 배치 (레벨 파일 편집 + `level.apply`)
6. **육안 검증** — 색칠 진단 포함. **여기서 이음매까지 확인하고 넘어간다**
7. 충돌 Part
8. `level.save.file` + 단계별 백업

---

## 8. 안전 규칙

- **발행된 에셋은 어떤 경우에도 다시 올리지 않는다** (중복 발행, 되돌릴 수 없음)
- **`level.publish` 를 부르지 않는다**
- **플레이 중에 편집하지 않는다** — 항상 `game.stop` 먼저
- **매 단계 전에 백업** — `Desktop\ovdr_backup\<단계이름>.ovdrjm`. 되돌리기는 파일 복사 → `level.apply` → `level.save.file`
- **작업 대상 밖의 인스턴스를 건드리지 않는다.** 확인은 백업과의 blockwise diff 로:
  인스턴스별로 이름 → 블록 해시를 만들어 대조한다. `ObjectKey` 는 저장 때마다 재부여되므로 그것만 다른 건 정상이다.
- 백업은 **신선한지 확인**하고 쓴다. 오래된 스냅샷을 믿고 되돌리면 그사이 작업이 날아간다.
