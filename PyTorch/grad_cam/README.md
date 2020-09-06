# Grad-CAM

## 논문 요약

[Grad-CAM: Visual Explanations from Deep Networks via Gradient-based Localization](https://arxiv.org/pdf/1610.02391v1.pdf)

**그래디언트 기반 위치파악(gradient-based localization)을 통한 심층 신경망의 시각적 설명**

컨볼루션 신경망 모델을 예측할 때, 중요하게 고려되는 입력 이미지의 영역을 시각화함으로써 좀 더 투명하게 CNN에 대해 시각적 설명을 한다.  <mark>Grad-CAM</mark>(Gradient-weighted Class Activation Mapping)방식은 CNN의 가장 마지막 컨볼루션 층으로 들어오는 클래스별 그래디언트 정보(class-specific gradient information)를 사용하여, 입력 이미지에서 대략적인 위치지정 맵(coarse localization map)을 만든다. 

기존의 CAM이 몇몇 CNN 모델에서만 사용할 수 있는 반면, Grad-CAM은 어떠한 CNN 기반 아키텍쳐에 폭넓게 적용할 수 있다. 또한 기존의 픽셀공간 시각화 방식과 Grad-CAM을 결합하여 고해상도 클래스 판별 시각화방식(high-resolution class discriminative visualization)인 Guided Grad-CAM을 소개한다.

Grad-CAM이나 Guided Grad-CAM을 사용하면, 이미지 분류 모델의 실패한 예측에 대한 설명 등도 할 수 있다. 컨볼루션 신경망은 컴퓨터 비전 작업에서 전례없는 성과를 거두고 있지만, 이해할 수 있는 직관적 요소로 분해하기 어려운 점은 CNN을 해석하기 어렵게 만든다. 따라서 실패한 예측이 생기면 설명하기 어렵다. 해석가능성(interpretability)은 중요하다. 정확도(accuracy)와 단순함/해석가능성 간에는 트레이드 오프가 존재한다. 심층 모델을 사용하면 많은 수의 레이어를 통한 높은 추상화(greater abstraction), 엔드-투-엔드 학습으로 탄탄한 통합(tight integration)으로부터 뛰어난 성능을 달성할 수 있지만 해석불가능한 면도 가지게 된다. 따라서 심층망들은 해석가능성과 정확도 사이에서 탐색을 시작하고 있다.

클래스 활성맵(CAM, Class Activation Mapping)은 이미지 내의 판별 영역(discriminative region)을 찾아내는 기술이다. CAM은 완전연결층을 포함하지 않는 특정 이미지 분류 모델에서만 사용된다. 이 경우 모델 투명성을 위하여 모델 복잡도를 희생하는 것이다. 하지만 최신 심층망을 아키텍쳐 변경없이 해석할 수 있게 만든다면,  해석가능성과 정확도 사이의 트레이드 오프 간 선택을 피할 수 있다. 이 논문의 목표는 어떠한 CNN 기반 아키텍쳐에도 CAM을 적용하는 일반화 과정에 있다. 즉, 완전 연결층이나 RNN이 적용된 CNN에도 CAM을 사용할 수 있다.

좋은 시각적 설명이란 예를 들어 이미지 분류 모델에서 이미지 안의 객체의 파악된 카테고리와 위치파악을 위해 클래스 판별성(class discrimination)와 세부사항을 잘 파악하는 고해상도(high resolution)을 갖춰야 한다.

Grad-CAM은 클래스 판별성이 높다(highly class-discriminative). 그러나 대부분의 Grad-CAM의 클래스 판별맵의 크기는 CNN의 최종 컨볼루션 층 크기로서 낮은 공간 해상도 때문에 세부사항 파악이 쉽지 않다. 이를 해결하기 위해 기존의 픽셀공간 그래디언트 시각화(pixel-space gradient visualization)를 Grad-CAM과 결합하여 Guided Grad-CAM을 만든다. 그 결과 이미지 안에 여러 클래스 객체가 있더라도, 찾으려는 클래스 파악에 중요한 영역이 고해상도 세부사항으로 시각화될 수 있다.

CAM(Class Activation Mapping)은 컨볼루션 특성맵을 전역평균풀링(globl average pooling)하여 소프트맥스 층으로 직접 연결하는 특별한 종류의 아키텍쳐를 가진 CNN에서 위치파악 맵(localization map)을 만들어낸다. 끝에서 두 번째 특성맵 k개에 대하여 전역평균풀링(GAP)을 수행하고, 선형변환하여 각 클래스에 대한 점수를 만든다. 
$$
y^c = \sum_{k} w_{k}^{c}~ {{1}\over{Z}} \sum_{i} \sum_{j} A_{ij}^{k}
$$
위치파악 맵(localization map)을 만들기 위해, CAM에서는 마지막 층의 학습된 가중치를 이용해, 최종 특성맵과의 선형변환을 계산한다.
$$
L_{CAM}^{c} = \sum_{k} w_{k}^c A^{k}
$$
CAM을 여러 층의 완전연결층을 마지막 층 앞에 갖는 신경망에 적용하기 위해서는, 완전연결층을 컨볼루션 층으로 대신하고 신경망은 재훈련되어야 한다.

### Gradiend-weighted Class Activation Mapping

일반적인 아키텍쳐에서 클래스-판별 위치맵(class-discriminative localization map)을 얻기 위해서는, 우선 컨볼루션 레이어의 특성맵 A에 대한 클래스 스코어의 그래디언트를 계산한다. 이런 그래디언트를 전역평균풀링하여서 가중치를 구한다.
$$
\alpha_{k}^{c} = {{1}\over{Z}} \sum_{i} \sum_{j} {{\partial y^{c}} \over {\partial A_{ij}^{k}}}
$$
가중치는 특성맵으로부터 신경망으로의 다운스트림의 부분선형화(partial linearization)를 나타내고, 대상클래스에 대한 특성맵 k의 중요도를 파악한다. 경험적으로 GAP를 통한 평균 그래디언트를 사용하는 것은 다른 선택보다 그래디언트에 있는 노이즈에 강인한 특성을 보였고, 더 나은 위치 파악 결과로 이어졌다.  CAM처럼 Grad-CAM 히트맵은 특성맵과 가중치의 결합이지만 추가로 ReLU를 거친다.
$$
L_{Grad-CAM}^{c} = ReLU(\sum_k \alpha_{k}^{c} A^{k})
$$
이 결과는 마지막 컨볼루션 특성맵의 크기와 같은 대략적인 히트맵이다. VGG나 AlexNet 에서는 마지막 컨볼루션 층의 크기인 14 x 14이 된다. CAM이 적용가능한 아키텍쳐에서는 w가 정확히 $\alpha$다 ReLU를 적용하는 점을 제외하면 이점이 Grad-CAM을 CAM의 일반화로 만든다. ReLU를 쓰는 이유는 관심있는 클래스에 양성(positive) 영향을 끼치는 특성에만 신경쓰고 싶기 때문이다. 즉 y^c를 높이기 위해 강도(intensity)가 커져야만 하는 픽셀 등에 주목하기 위해서이다.



## 구현참고

[pytorch-grad-cam](https://github.com/jacobgil/pytorch-grad-cam)

### 사용법

```sh
$ python grad_cam.py <이미지 경로>
```



### 구현 코드에서 사용된 메소드 참조

*register_hook* 은 *backward hook*으로 사용할 함수를 등록할 수 있게 해준다. 즉, 그래디언트가 계산될 때마다 실행될 함수를 지정하는 것이다. 여기서는 *save_gradient* 함수가 실행되도록 하여, gradients 리스트에 저장한다.