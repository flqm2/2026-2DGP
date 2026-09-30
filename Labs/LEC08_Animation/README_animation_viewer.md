# Drill #8 애니메이션 뷰어

## 실행
저장소 루트에서 다음을 실행합니다. Python 3.10 이상과 pico2d가 필요합니다.

```powershell
python Labs/LEC08_Animation/animation_viewer.py
```

다른 작업 디렉터리에서도 파일의 절대 경로로 실행할 수 있습니다.
ESC 또는 창 닫기로 종료합니다. 정지 중에도 종료 이벤트를 처리합니다.

## 구현 내용 및 제출 시 가산점 설명
- 제공된 `Pixel-Sprite-Sheet2.png`의 모든 행을 위에서 아래 순서로 재생합니다.
- IDLE 6개, WALK 8개, RUN 8개, FIGHTING STANCE 6개, ATTACK 1 5개: 총 33개.
- 모든 프레임을 800×600 화면의 중앙 (400, 300)에 표시합니다.
- 각 프레임 0.1초, 각 동작 5회 완주 후 마지막 프레임을 1초 유지합니다.
- 마지막 동작 이후 첫 동작으로 돌아가 종료할 때까지 무한 반복합니다.
- 동작별 일정 배율로 비율을 보존하고, 가장 작은 프레임도 높이 300픽셀 이상으로 표시합니다.
- **불규칙 프레임 크기 지원 (+2점 관련):** 프레임별 left/bottom/width/height를
  `animation_frames.json`에 저장합니다. 공격 시 위로 뻗는 칼까지 포함하여
  각기 다른 사각형을 자르며, 고정 칸 크기 계산을 사용하지 않습니다.
- **동작별 서로 다른 프레임 수 지원 (+2점 관련):** 각 동작의 `len(frames)`를
  사용합니다. 6/8/8/6/5개의 프레임을 빈 프레임 없이 각각 5회 순환합니다.

위 두 항목을 과제 제출 설명에 명시하세요. 최종 점수는 채점자가 결정합니다.

## 원본과 좌표
원본은 회색 배경과 글자를 포함하고, ATTACK 1의 칼끝이 윗행 가까이 뻗습니다.
`build_animation_atlas.py`는 원본의 연결된 픽셀 영역 전체가 지정 사각형 안에
들어오는 경우에만 추출하여 인접 행의 캐릭터가 섞이지 않도록 합니다.
배경과 각 채널 차이가 30 이하인 픽셀은 제거하므로 가장자리 색이 일부 단순화됩니다.
원본은 보존하고 추출한 투명 `animation_atlas.png`를 pico2d로 로드합니다.
PNG의 위쪽 기준 좌표는 `bottom = atlas_height - top - frame_height`로 변환합니다.

일반 실행에는 Pillow가 필요하지 않습니다. 원본에서 시트를 다시 만들 때만 필요합니다.

```powershell
python -m pip install Pillow
python Labs/LEC08_Animation/build_animation_atlas.py
```

## 검증
```powershell
python Labs/LEC08_Animation/animation_viewer.py --check
python -m unittest discover -s Labs/LEC08_Animation -p test_animation_viewer.py -v
python Labs/LEC08_Animation/animation_viewer.py --smoke-test
```

테스트는 5회 완주, 정확히 1초 정지, 행별 프레임 순서, 전체 순환,
큰 시간 간격에서의 전환, 확대 및 이미지 영역 경계를 검증합니다.
`--smoke-test`는 실제 pico2d로 모든 프레임을 그린 후 자동 종료합니다.

참고: `character_runs.py`, `../../Slides/LEC 08 애니메이션.html`.
단계별 작업은 `WORK_LOG.md`와 01~21 커밋 메시지에서 확인할 수 있습니다.
