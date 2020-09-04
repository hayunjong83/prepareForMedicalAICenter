# Faster R-CNN 구현

참고) [Object Detection and Classification using R-CNN](https://www.telesens.co/2018/03/11/object-detection-and-classification-using-r-cnns/)

구현 참조) [jwyang/faster-rcnn.pytorch](https://github.com/jwyang/faster-rcnn.pytorch)

## 참고 블로그 요약

### 1단계) 이미지 전처리(Image Pre-Processing)

> 이미지 크기를 조정(scaling)하고, 평균 픽셀값을 삐준다(subtract). 훈련과 추론과정에 동일하게 적용된다.

평균 벡터(mean vector)는 모든 훈련/테스트 이미지에 동일하게 적용되는 설정 값으로서 하나의 입력 이미지에서 추출한 평균 픽셀 값이 아니다. 채널 수를 고려한 3 X 1 벡터다.

*targetSize*는 600, *maxSize*는 1,000이다. *minDim, maxDim*은 너비와 너비 중 최소값과 최대값이다. *scale*은 *(targetSize / minDim)*이지만, *scale*과 *maxDim*의 곱이 *maxSize*보다 클 때의 *scale* 값은 *(maxSize / maxDim)*으로 결정된다.

### 2단계) 네트워크 구성(Network Organization)

> 네트워크의 주요한 구성요소 3가지는 "head" 네트워크, 지역제안 네트워크 (RPN, Region Proposal Network), 분류 네트워크다.

*R-CNN*에서 신경망의 크게 두 가지 기능을 수행한다. 객체가 있을 가능성이 큰 ROI(Region of Interest)를 파악하고, 각 ROI의 클래스 확률분포를 계산한다. 이를 위해 3가지 주요 구성요소가 있어야 한다.

1. Head
2. Region Proposal Network(RPN)
3. Classification Network

