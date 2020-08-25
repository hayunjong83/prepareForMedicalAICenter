# docker 환경에서 PyTorch 개발하기

## docker 설치

**Ubuntu** 환경

구버전의 도커가 설치되어 있으면(*docker, docker.io 또는 docker-engine*), 우선 제거해준다.

```bash
$ sudo apt-get remove docker docker-engine docker.io containerd runc
```



새로운 버전의 도커(*docker-ce*)를 설치를 위해, 필요한 패키지를 설치해준다.

```bash
$ sudo apt-get update

$ sudo apt-get install apt-transport-https ca-certificates curl \
						gnupg-agent software-properties-common
```

도커의 공식 GPG 키를 추가한다. [설치 페이지](https://docs.docker.com/engine/install/ubuntu/) 를 참고하여 키의 fingerprint를 통한 유효성 검사를 할 수 있다.

```bash
$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
```

*stable repository*를 설정한다.

```bash
$ sudo add-apt-repository \
	"deb [arch=amd64] https://download.docker.com/linux/ubuntu \
	$(lsb_release -cs) \
	stable"
```

도커를 설치한다. (단, 이 경우 최신버전을 설치한다.)

```bash
$ sudo apt-get update
$ sudo apt-get install docker-ce docker-ce-cli containerd.io
```



도커는 커맨드 실행 시 관리자 권한이 필요하다. 따라서 현재 사용자에게 root 권한을 부여해서, 사용의 편의성을 도모한다.

```bash
# Create the docker group
$ sudo groupadd docker

# Add user to the docker gropu
$ sudo usermod -aG docker $USER
```



## nvidia-docker 설치

[nvidia-docker](https://github.com/NVIDIA/nvidia-docker) 를 참고한다.

```bash
# Add the package repositories
$ distribution=$(./etc/os-release;echo $ID$VERSION_ID)
$ curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
$ curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list

$ sudo apt-get update && sudo apt-get install -y nvidia-container-toolkit
$ sudo systemctl restart docker
```

*nvidia-docker*의 정상 설치 여부를 확인해 볼 수 있다.

```bash
$ docker run --gpus all nvidia/cuda:10.0-base nvidia-smi
```



## docker에서 pytorch 설치 및 사용

최신 이미지가 아닌 특정 버전을 사용하려면, 도커 허브의 [PyTorch 저장소](https://hub.docker.com/r/pytorch/pytorch/) 를 참고하여  태그를 지정한다. 최신 이미지를 내려받는다.

```bash
$ docker pull pytorch/pytorch
```



컨테이너를 생성한다.

```bash
$ docker run -itd --name pytorch -v /home/$USER/share:/root/share -p 8888:8888 --gpus all --restart=always pytorch/pytorch
```

사용자 home 디렉토리에 share 디렉토리를 생성한 후, 컨테이너와 공유하는 볼륨으로 설정한다. gpu를 사용할 수 있도록 지정한다. *restart* 옵션을 주면, 도커가 재실행될 때 컨테이너도 자동으로 실행된다. 

컨테이너를 실행한다.

```bash
$ docker exec -it pytorch bash
```

exit 명령어로 컨테이너에서 빠져 나올 수 있고, *docker attach* 명령어로 다시 접속할 수 있다.



## 배포하기

배포할 컨테이너는 중지 되어야 한다.

```bash
$ docker stop pytorch
```

[도커 허브](https://hub.docker.com/) 에 로그인한다.

```bash
$ docker login
# After login, set $DOCKER_ID as your docker id
```



배포할 컨테이너를 이미지 파일로 만든다. *commit* 명령어 다음에는 차례로 **컨테이너 이름**, **배포할 이미지 이름: 버전** 을 지정해준다.

```bash
$ docker commit pytorch $DOCKER_ID/pytorch_test:1
```

 *push* 명령어를 이용하여 배포한다. 

```bash
$ docker push $DOCKER_ID/pytorch_test:1
```

