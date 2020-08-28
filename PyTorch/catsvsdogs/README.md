# 사전훈련된 resnet 모델을 통한 고양이vs개 분류

[PyTorch HUB](https://pytorch.org/hub/) 에서 사전훈련된 모델을 내려받는다. 이 때 <mark>*torch.hub.load()*</mark> 함수를 사용할 수 있다.

```python
torch.hub.load(github, model, *args, **kwargs)
```

resnet18, resnet34 모델은 /home/$USER/.cache/torch/checkpoints/ 안에 받아진다. 사전훈련 모델로 **전이 학습(transfer learning)**을 수행할 때, ImageNet의 평균과 표준편차로 훈련되었을 <mark>*배치 정규화(BatchNorm) 층*</mark>을 제외한 다른 층들의 매개변수는 동결(freeze)시킨다. *backward()함수*는 *.requires_grad* 속성이 True로 설정된 변수의 grad 값을 갱신한다. 

고양이vs개는 2개의 클래스만 분류하면 되므로 분류층(classifier)를 바꿔준다.

학습을 할 때는 <mark>*model.train()*</mark>를 호출하여 **학습모드**로 전환하였다면, 추론 과정에서는 <mark>*model.eval()*</mark>를 호출하여 드롭아웃이나 배치 정규화 등을 **평가모드**로 설정한다.

데이터 집합을 원하는 크기(batch_size)의 미니 배치로 나눠 읽어 주는 *데이터 로더(DataLoader)*를 사용한다.

```python
torch.utils.data.DataLoader(dataset, batch_size=1, shuffle=False)
```

- dataset(Dataset) : 읽어 들일 데이터 집합
- batch_size(int, optional) : 배치 크기, 기본값은 1
- shuffle(bool, optional): 각 에포크마다 데이터를 셔플링할지 여부, 기본값을 False

*optimizer.zero_grad()*를 호출하여 역전파 단계를 실행하기 전에 그래드언트를 0으로 설정한다. GPU가 사용가능할 경우 *to(torch.device("cuda"))*로 GPU에서 실행 가능한 텐서로 변환해준다. *loss.backward()*를 호출하여 각 변수마다의 loss에 대한 그래디언트를 구한다. 마지막으로, *optimizer.step()*를 실행하면 모델의 파라미터들이 업데이트된다. *.item()*함수는 1개의 원소를 가진 텐서를 스칼라로 바꿔준다.

*torch.max()* 함수는 주어진 텐서 배열의 최댓값이 있는 인덱스를 반환해준다. *torch.eq()*는 원소별로 동일값 여부를 확인하여 torch.BoolTensor로 반환한다. *view()*함수는 텐서의 형상을 reshape해준다.

Transform은 일반적인 이미지 변형(image transformation)이다.(참고: [torch.transforms](https://pytorch.org/docs/stable/torchvision/transforms.html#torchvision-transforms)) <mark>Compose</mark> 메소드를 통해 여러 transform이 연결될 수 있다. *torchvision.transforms.ToTensor()*는 PIL 이미지를 NumPy 배열(ndarray)이나 텐서로 바꿔준다. *torchvision.transforms.Normalize()*는 텐서 이미지를 평균과 표준편차로 정규화한다. 3개의 채널 각각에 대한 평균과 표준편차를 입력한 것이다.

케글의 dogs-vs-cats의 train 디렉토리에는 개와 고양이 사진이 각각 12,500 장씩 25,000 장이 있는 데이터셋이다. 각 파일명에 있는 인덱스를 이용하여서 16,000장은 train디렉토리에 남겨두고, 4,500장씩 validation디렉토리와 test디렉토리로 옮긴다. <mark>*torchvision.datasets.ImageFolder*</mark>를 이용해서 데이터셋을 만들 때, 데이터는 각 분류별 디렉토리로 나눠져 있어야 한다. 

PyTorch 모델을 저장하고 불러올 때, 핵심 함수는 3가지다.[참고](https://tutorials.pytorch.kr/beginner/saving_loading_models.html)

1. *torch.save* : 파이썬의 pickle 모듈을 사용해 직렬화된 객체를 디스크에 저장한다.
2. *torch.load* : 저장된 객체 파일을 역직렬화하여 메모리에 올린다.
3. *torch.nn.Module.load_state_dict* : 역직렬화된 *state_dict*를 사용해 모델의 매개변수를 불러온다.

이후 추론(inference) 과정을 위해 모델(예 - class MyModel(torch.nn.Module)의 객체 model)을 저장하려면, 

```python
torch.save(model.state_dict(), PATH)
```

모델을 불러오려면, 아래처럼 한다.

```python
model = MyModel(*args, **kwargs)
model.load_state_dict(torch.load(PATH))
model.eval()
```

모델 저장시 가장 권장되는 방법은 위의 내용처럼, 학습된 모델의 학습된 매개변수만 저장하는 것이다. 따라서 model의 state_dict를 저장하였다. PyTorch에서 모델이 저장되면 *.pt*, 또는 *.pth* 확장자를 사용한다. 마지막으로 추론을 실행하기 전에 반드시 <mark>*model.eval()*</mark>을 호출하여 Dropout 및 BatchNormalization을 평가 모드로 설정하여야 한다. 추가적으로 전체 모델을 저장하고 불러올 때는 다음처럼 하여도 가능하다.

```python
# Save the whole model
torch.save(model, PATH)

# Load the whole model
model = torch.load(PATH)
model.eval()
```

