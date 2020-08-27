# MNIST 예제 코드 참고사항



## 사용된 함수

```python
torch.nn.Module
```

모든 신경망 모듈의 베이스 클래스로서, 작성하려는 모델은 nn.Module의 하위클래스다.

```python
torch.nn.Conv2d(in_channels: int, out_channels:int, 
				kernel_size: Union[T, Tuple[T, T]],
				stride: Union[T, Tuple[T, T]] =1,
				padding: Union[T, Tuple[T, T]] = 0,
                bias: bool = True,
				padding_mode: str = 'zeros')
```

생략되지 않은 [Conv2d 레이어의 명세](https://pytorch.org/docs/stable/generated/torch.nn.Conv2d.html#torch.nn.Conv2d)를 참고한다. *kernel_size, stride, padding*은 단일 정수 값도 가능하다. 따라서 **nn.Con2d(1, 32, 3, 1)**은 단일 입력 채널의 입력을 32개의 출력으로 바꾸는 컨볼루션 레이어다. 이 때 커널은 (3, 3) 크기의 정사각 필터이고, 스트라이드는 1 이다.

```python
torch.nn.Dropout2d(p: float = 0.5, inplace: bool = False)
```

[Dropout2d 레이어](https://pytorch.org/docs/stable/generated/torch.nn.Dropout2d.html#torch.nn.Dropout2d) 참고. *p*는 확률이고, *inplace*가 True면 in-place연산으로 이뤄진다.

```python
torch.nn.Linear(in_features: int, out_features: int, bool = True)
```

[Linear 레이어](https://pytorch.org/docs/stable/generated/torch.nn.Linear.html#torch.nn.Linear) 참고. *bias*가 False로 설정되면, 편향 값을 포함시키지 않을 수 있다.



```python
torch.nn.functional.relu(input, inplace=False) → Tensor
```

*torch.nn.functional.relu_(input)*은 relu의 in-place 버전이다. 

```
torch.nn.functional.max_pool2d(**args, **kwargs)
```

[*torch.nn.MaxPool2d*](https://pytorch.org/docs/stable/generated/torch.nn.MaxPool2d.html#torch.nn.MaxPool2d) 참고. 단일 정수로로 표현될 수 있는 kernel_size와 stride, padding 표현을 갖는다. 따라서 예제 코드에서는 (2,2) 커널을 이용해 MaxPooling의 수행을 뜻한다.

```python
torch.flatten(input, start_dim=0, end_dim= -1) → Tensor
```

예제에서는 첫번째 차원을 따라 flatten했으므로, 배치 내의 각 데이터별로 2차원 데이터가 1차원 데이터로 펼쳐진다.

```python
torch.nn.functional.log_softmax(input, dim=None, _stacklevel=3, dtype=None)
```

동일한 결과를 나타내는 log(softmax(x)) 연산보다 빠르고, 안정적인 연산을 수행한다. 



## argparse 사용법

다양한 실행 옵션을 부여하기 위해서, 파이썬 내장 패키지인 **argparse**를 사용한다.

1. <mark>argsparse.ArgumentParser()</mark> 에 description을 사용해서, 파서 객체를 생성한다.
2. <mark>add_argument()</mark> 메소드를 사용해서, 원하는 인자 종류를 추가한다.
3. <mark>parse_args()</mark> 메소드로 입력된 인자를 파싱한다.



인자 이름을 지정할 때 두 개를 연속해서 나열해서, 그 인자명에 대한 약자도 지정할 수 있다. *type* 지정이 되지 않으면, 입력된 값을 문자열로 취급한다. add_argument()에서 **type**을 사용해서 데이터 타입을 지정할 수 있다. 같은 방식으로 **default** 옵션을 통해 기본값을 설정할 수 있다. 

기억할만한 **action**의 종류로 *store*, *append*, *store_true*, 등이다. 

- *store* : action이 지정되지 않으면 store다. 인자 바로 뒤의 값이 저장된다.
- *append* : 하나가 아닌 여러 개의 값을 저장하고 싶을 때 사용한다.
- *store_true* : 인자를 적으면, 값을 주지 않고 True를 저장한다. (↔ *store_false*)

*metavar*는 help 메시지에서 표시되는 인자의 이름을 지정한다.