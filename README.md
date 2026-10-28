<p>
  <a href="https://mixedcas-lab.github.io/"><img src="assets/mcaslab.png" alt="MCAS Lab" height="34"></a>
  &nbsp;&nbsp;
  <a href="https://english.uos.ac.kr/"><img src="assets/uos.png" alt="University of Seoul" height="20"></a>
</p>

# CTLE Census

ISSCC, VLSI, JSSC, CICC, ESSCIRC/ESSERC, A-SSCC, SSC-L, TCAS-I/II, TVLSI에 실린 **CTLE(continuous-time linear equalizer)와 아날로그 등화기** 논문, 그리고 CTLE를 쓰는 유선 수신기 논문을 모아 보여주는 사이트입니다. MCAS Lab(서울시립대학교)과 김가인 교수님 CASSP Lab(DGIST)의 공동 프로젝트입니다.

- 사이트: https://mixedcas-lab.github.io/ctle-census/
- 데이터 출처: IEEE Xplore API (서지 메타데이터와 링크만 공개, 초록·본문은 올리지 않음)

## 동작 방식

1. **데이터**: adc-census 수집기가 받아 둔 랩 서버 캐시(`~/adc-census/cache/raw`)를 읽기만 합니다. IEEE API를 따로 쓰지 않습니다.
2. **분류** (`collector/classify.py`)
   - **CTLE paper (core)**: 제목에 CTLE, continuous-time/linear/analog/passive equalizer 등이 있는 논문. 제목에 수식어 없는 "equalizer"만 있으면 유선 맥락이 있고 DFE·FFE·FIR·디지털이 아니며, 초록이 아날로그(peaking, zero, boost, continuous-time 등)이거나 디지털 등화 단서가 없을 때만 넣습니다. "CTLE"라는 이름이 생기기 전의 케이블·read channel 등화기도 포함합니다.
   - **Receiver with a CTLE (rx)**: 유선 수신기·송수신기 논문 중 초록에 CTLE를 언급한 것. 이때 전력·면적은 수신기 전체 값이라 표시하지 않습니다.
   - 무선, 송신단 등화(pre-emphasis, 드라이버, 비선형 등화), 보안(AES), SRAM, Ising 머신, 이론·알고리즘(MMSE, blind, neural) 논문은 제외합니다.
3. **태그**: 기법(inductive peaking, passive, RC degeneration, active feedback, multi-path, multi-stage, low/mid-frequency EQ, inverter-based, DFE/FFE 병용, 광 TIA), 변조(NRZ, PAM3/4/6/8, duobinary), 응용(장거리/백플레인, 케이블, 광, die-to-die, 메모리, PCIe/Ethernet/USB, 디스플레이/차량, storage read channel), 적응형 여부.
4. **수치**: 데이터 속도, 보상한 채널 손실(dB), 피킹(boost, dB), 전력, 공정, 면적. 제목 값을 우선하고, 초록 값은 하나뿐일 때만 쓰고, 여럿이면 비워 둡니다.
5. **공개**: cron이 매일 07:02에 재생성하고, 바뀐 것이 있으면 커밋·push합니다.

## 검수 값 넣기

GitHub 웹에서 `data/annotations.csv`를 편집합니다. 열: `id, exclude, level(core/rx), arch, app, mod, rate(b/s), loss(dB), boost(dB), p(W), node(nm), area(mm²), cal, note, by`. `-`는 값 삭제입니다.

## 랩 서버 설정 (1회)

```bash
ssh-keygen -t ed25519 -f ~/.ssh/ctle_census -N "" -C "ctle-census@lab-server"   # 공개키를 Deploy keys에 쓰기 권한으로 등록
git clone github-ctle-census:mixedcas-lab/ctle-census.git ~/ctle-census
( crontab -l; echo "2 7 * * * PYTHON=$HOME/venvs/work/bin/python $HOME/ctle-census/scripts/update.sh >> $HOME/ctle-census/logs/update.log 2>&1" ) | crontab -
```

GitHub Pages: Settings → Pages에서 Branch를 **main / (root)**로 지정합니다.
