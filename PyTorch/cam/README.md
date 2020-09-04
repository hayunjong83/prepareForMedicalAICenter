# CAM(Class Activation Mapping)

논문: [Learning Deep Features for Discriminative Localization](https://arxiv.org/pdf/1512.04150.pdf)

# 개요

합성곱 신경망(CNN)의 *컨볼루션 레이어들*은 물체의 위치에 대한 답(supervision)이 없어도 객체 탐색기(object detector)로서 동작할 수 있다. 그러나 이런 능력은 분류를 위한 완전 연결층(fully-connected layer)를 거치면서 사라진다. 하지만 <mark>**전역 평균 풀링(global average pooling)**</mark> 층을 사용하면, 원래의 구조적 규제부여(structural regularize) 목적 뿐만 아니라 위치 파악(localization) 능력을 최종 레이어까지 보유하게 할 수 있다. 즉 판별에 핵심적인 이미지 내의 영역(*discriminative image regions*)을 쉽게 파악할 수 있다.

전역평균풀링(GAP, Global Average Pooling)을 사용한 클래스 활성맵(CAM, Class Activation Map)을 쓰면 CNN이 분류를 위해 주목한 이미지 영역을 볼 수 있다. GooLeNet 처럼 많은 컨볼루션 레이어로 구성된 신경망의 최종 레이어(예 - 분류를 위해 쓰는 softmax 층) 바로 앞에서 컨볼루션 특성맵 위에 GAP를 수행한다. 출력층으로의 가중치를 다시 컨볼루션 특성맵으로 투영함으로써 이미지 영역마다의 중요도를 파악하는 방식이 CAM이다.

## 구현 세부사항

참고: [pytorch_CAM](https://github.com/zhoubolei/CAM/blob/master/pytorch_CAM.py)

