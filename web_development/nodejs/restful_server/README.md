# RESTful 서버 예제

뷰(Vue.js)에서 권장하는 http 통신 라이브러리는 액시오스(Axios)다. 액시오스 사용을 위해 설치하려면, CDN 방식 또는 npm 방식을 통해서 설치할 수 있다. 

```html
<script src="https://unpkg.com/axios/dist/axios.min.js"></script>
```

```sh
npm install axios
```

*window.onload*는 자바스크립트에서 페이지가 로드되면 자동으로 실행되는 전역 콜백함수다. 페이지의 모든 요소들이 로드되어야 호출되며, 한 페이지에서 하나의 window.onload() 함수만 적용될 수 있다.

