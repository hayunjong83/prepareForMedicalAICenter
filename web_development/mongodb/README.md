# 몽고디비

## 설치

### Windows10 환경

[MongoDB Community Server 다운로드 페이지](https://www.mongodb.com/try/download/community)에서 설치용 .msi 파일을 받는다. 함께 설치할 수 있는 MongoDB Compass는 GUI를 갖춘 몽고디비 관리도구다.



## 실행

### 몽고디비 실행 (mongod 명령어)

<mark>**mongod**</mark>를 입력하여 몽고디비를 실행한다. 간편한 사용을 위해서 path를 지정해준다. 직접 *데이터 디렉토리*를 지정해주려면 *--dbpath* 옵션을 사용한다. 기본적으로 지정된 포트는 27017이므로, 웹 브라우저에서 localhost:27017에 접속하면 실행 여부를 확인할 수 있다. 항상 이렇게 mongod 명령어로 먼저 서버를 실행한 후에, 몽고디비를 사용함을 기억한다.

### 관리자 계정 추가

몽고디비가 실행된 후, <mark>**mongo**</mark> 명령어로 몽고디비 프롬프트에 접속한다. mongod 실행 시 *--auth*이 없었기 때문에, 비밀번호를 요구하지 않는다. 관리자 계정과 비밀번호를 추가한 후에는 몽고디비를 재 실행하고, 관리자 계정과 비밀번호를 이용해 로그인한다.

```bash
> use admin
switched to db admin
> db.createUser({ user: '이름', pwd: 'password', roles:['root']})
```

실행됐던 몽고디비를 중지시킨 후 --auth 옵션을 줘서 다시 실행시킨다.

mongo 명령어로 접속한 후 db.auth 명령어로 인증을 하거나, 생성한 유저명, 비밀번호를 이용해 접속한다.

```bash
>use.admin
>db.auth("이름", "password")
```

이 경우 1이 출력되면 인증이 성공된 것이다.

```bash
mongo -u "이름" -p "password"
```



## 데이터베이스 생성

데이터베이스를 만드는 명령어는 <mark>*use [데이터베이스명]*</mark>이다.

```bash
> show test_db
switched to db test_db
```

데이터베이스 목록을 확인하는 명령어는 <mark>*show dbs*</mark>이다. 그런데 데이터베이스를 생성한 직후에는 목록에서 표시되지 않는다. 최소한 하나의 데이터라도 포함되어야 이 목록에 표시된다. 단, 현재 사용중인 데이터베이스 명은 <mark>*db*</mark> 명령어로 알 수 있다.



## 컬렉션 생성

다큐먼트(document)를 넣는 순간 컬렉션도 자동 생성되지만, 직접 생성하는 명령어는 <mark>*db.createCollections*</mark>이다.

```bash
>db.createCollections('users')
{"ok" : 1}
```

컬레션은 <mark>*show collections*</mark>로 확인할 수 있다.



## 컬렉션 제거

우선, 현재 db에 있는 컬렉션은 *db.getCollectionNames()* 메소드로 확인할 수 있다. 그 후 <mark>*drop*</mark> 메소드를 이용해서 컬레션을 제거할 수 있다.

```bash
> db.getCollectionNames()
["users"]
> db.users.drop()
true
> db.getCollectionNames()
[ ]
```



## 데이터베이스 제거

<mark>*dropDatabase*</mark> 명령어로 데이터베이스를 제거할 수 있다.

```bash
> use test_db
switched to db test_db
> db.dropDatabase()
{"dropped" : "test_db", "ok" : 1}
```





## CRUD 작업

### Create

```bash
$ mongo
> use test_db
switched to db test_db
> db.users.save({name: 'kim', age: 35, married: false, comment:'첫번째 사람', createdAt: new Date()});
WriteResult({"nInserted" : 1})
> db.users.save({name: 'ha', age: 24, married: true, comment:'두번째 사람', createdAt: new Date()});
WriteResult({"nInserted" : 1})
```

<mark>*db.컬렉션명.save(다큐먼트)*</mark>로 다큐먼트를 생성한다. <mark>*db.컬렉션명.insert(다큐먼트)*</mark>도 사용할 수 있다.

### Read

```bash
> db.users.find({});
```

*find({})*는 컬렉션 내의 모든 다큐먼트를 조회한다. 특정 필드를 조회할 때, 조회할 필드의 인자를 1 또는 true로 표시하여 넣는다. 기본적으로 가져오는 _id 필드에 0 또는 false를 입력하면 표시되지 않는다.

```bash
> db.users.find({}, {_id: 0, name: 1, married: 1});
{"name": "kim", "married": false}
```

조회 시 조건을 사용하려면, 첫 번째 인자 객체에 기입한다. 

```bash
> db.users.find({age: {$gt : 30}, married: false}, {_id: 0, name: 1, age: 1});
{"name": "kim", "age": 35}
```

이와 같은 연산자는 $gt(초과), $gte(이상), $lt(미만), $lte(이하), $ne(같지 않음), $or(또는), $in(배열 요소 중 하나) 등이 있다.

조회된 결과에 대해 <mark>*sort*</mark>  메소드를 사용하면 정렬할 수 있다. -1은 내림차순, 1은 오름차순 정렬이다.

```bash
> db.user.find({}, {_id:0, name:1, age:1 }).sort({age: -1})
{ "name": "kim", "age": 35}
{ "name": "ha", "age": 24}
```

<mark>*limit*</mark> 메소드를 사용하면 조회할 다큐먼트 개수를 설정할 수 있다.

<mark>*skip*</mark> 메소드를 사용하면 조회 시 건너뛸 도큐먼트 개수를 설정할 수 있다.



### Update

**$set 연산자를 사용하면 지정된 필드만 바꿀 수 있지만**, $set 연산자 없이 수정하면 다큐먼트가 통째로 두 번째 객체내용으로 바껴버린다. 

```bash
> db.users.update({name: 'kim'}, {$set: {age : 38}});
WriteResult({"nMatched" : 1, "nUpserted" : 0, "nModified" : 1})
```

수정에 성공하면, 첫번째 객체에 해당하는 다큐먼트 수(nMatched)와 수정된 다큐먼트 수(nModified)를 확인할 수 있다.



### Delete

```bash
> db.users.remove({ name: 'kim'})
WriteResult({ 'nRemoved': 1})
```

삭제할 다큐먼트 정보를 객체로 넘겨주면, 삭제 성공 후 삭제된 개수가 반환된다.



## 몽구스(mongoose)

[Node.js 교과서](http://www.kyobobook.co.kr/product/detailViewKor.laf?mallGb=KOR&barcode=9791160505221#)의 내용을 참고한다. 몽구스는 ODM(Object Document Mapping)으로서 문서를 DB에서 조회할 때 자바스크립트 객체로 바꿔준다.

### 설치

몽구스를 사용하면 스키마(schema)를 생성할 수 있어서, 몽고디비에 데이터를 저장하기 전에 자료형과 필수 내용 포함여부를 사전에 필터링할 수 있다.

우선, Express-generator로 프로젝트를 생성한다.

```bash
$ express learn-mongoose --view=pug
```

npm 패키지 설치한 후, 몽구스를 설치한다.

```bash
$ cd mongoose && npm i
$ npm i mongoose
```



### 몽고디비 연결하기

몽고디비와 연결하는 주소 형식은 mongodb://[username:password@]host[:port] [/[database]] [?options]]와 같다. schemas 디렉토리를 만든 후, index.js 파일을 생성하여 관련내용을 작성한다.

계정이 있는 데이터베이스가 admin이므로 접속을 시도하는 주소의 데이터베이스는 admin이지만, 실제로 사용하려는 데이터베이스를 *dbName* 옵션으로 줘야한다. *nodejs*라는 데이터베이스를 몽고디비에서 생성하였고, 이를 사용한다. 

- mongoose.set('useNewUrlParser': true) : 몽고디비가 새로 만든 MongoDB connection string parser 도구를 사용하도록 한다.
- mongoose.set('useCreateIndex': true):  createIndex() 메소드를 사용하게 한다.

사실 위 두가지 설정 모두 최신 몽고디비 사용할 때, deprecatedError 메시지를 없애기 위해서 쓴다.



### 스키마 정의

schema 디렉토리에 user.js와 comment.js를 만들어 스키마를 각각 정의한다. 보통 한 파일에 하나의 스키마를 작성한다. 나중에 스키마가 수정되어도 미리 저장되었던 데이터들은 바뀌지 않는다. 정의된 스키마는 서버 실행되는 부분에서 require 되어야 한다.

mongoose 모듈의 Schema 생성자를 사용해 스키마를 만든다.(*new mongoose.Schema()*)

스키마 정의가 끝난 후에 몽구스의 <mark>*model 메소드*</mark>로 스키마와 몽고디비의 컬렉션을 연결하는 모델을 만든다. 첫 번째 인자로 입력한 컬렉션 이름은 **소문자 + 복수형** 이름으로 바뀐다. 강제로 컬렉션이름을 지정하려면 세 번째 인자로 컬렉션 이름을 지정한다.

comments.js에서 ref 속성으로 User가 주어졌으므로, commenter 필드에 User 스키마의 사용장 ObjectId가 들어간다. 



### mongoose.js 참고사항

*document.querySelectorAll()*는 특정 CSS 선택자를 가진 모든 요소를 배열로 가져오는 메소드다. 이 때 생성되는 것은 엄밀하게 유사배열이므로, 배열의 메소드인 forEach를 사용하기 위해 *[].forEach.call( els, function(el){});* 과 같은 방식을 사용한다.

*addEventListener*는 이벤트를 등록하는 가장 권장되는 방식이다. *click* 이벤트 발생시 *textContent* 프로퍼티를 사용한다. 불필요한 공백을 제거하는 *innerText*에 비해 *textContent*는 텍스트를 그대로 가져온다.

*XMLHttpRequest(XHR)* 객체는 서버와 상호작용하기 위해 사용되는데, 전체 페이지를 새로고침하지 않아도 url로부터 데이터를 받아올 수 있다. *responseText*는 요청에 대한 응답을 텍스트로 갖는 DOMString을 반환하는 메소드다. 반환된 문자열을 분석하여 객체로 반환하는 *JSON.parse*를 사용한다.

*map* 메소드는 반복문을 수행하면서 배열 안의 요소들 각각에 변환을 수행하게 해준다. *document.createElement*를 이용하면 문자열에 해당하는 요소를 생성해준다.  생성된 요소는 *.appendChild()*를 통해 선택한 요소의 자식요소로서 추가될 수 있다.

*XMLHttpRequest.open(method, url[, async])*는 서버로의 요청을 준비하고, *XMLHttpRequest.send*는 준비된 요청을 서버에 전달한다. *open*에서 HTTP 메소드로 *'GET'*메소드를 사용한 경우, url의 일부인 *query_string*으로 데이터를 서버로 전송하고, *'POST'*를 사용하면 *Reqeust Body*에 담아 데이터를 전송한다.  요청을 처리할 페이지 url 다음에, 이 요청을 비동기로 처리할 지 여부를 bool 값으로 정의할 수도 있다. *XMLHttpRequest.onload* 메소드는 브라우저가 서버로부터 응답을 받을 때, 발생하는 이벤트를 다룬다.

*prompt()*함수는 문자열을 입력할 때 사용한다. 첫 번째 매개변수는 입력 창에 띄워줄 메시지를 의미하고, 두 번째 매개변수를 지정하면 입력부분의 기본 문자열을 지정할 수 있다.

*PATCH*는 자원 일부만 수정하는 http 메소드 중 하나다. JSON 타입의 데이터를 보내기 위해서 HTTP요청 헤더의 값을 설정하는 *XMLHttpRequest.setRequestHeader()*메소드는 반드시 open() 뒤에, 또 send()가 호출되기 전에 호출해야한다. *application/json* 또는 *application/x-json*으로 Content-Type을 설정하면 json 데이터를 보낼 수 있다. 이 때 보내는 json 데이터를 만들기 위해 *JSON.stringify()*를 사용한다. *JSON.stringify()*메소드는 자바스크립트 값이나 객체를 JSON 문자열로 변환한다.

사용자 등록을 위해 id속성이 user-form인 요소를 *.getElementById()*로 찾아낸다. 반환된 Element 객체에 submit 이벤트가 발생했을 때, 처리할 함수를 이벤트리스너로 등록한다. *event.preventDefault()*를 써서 현재 이벤트의 기본 동작을 중단한 뒤에 필수 값의 존재 여부를 확인하고 그 값을 저장한다. *event.target*속성은 이벤트가 시작한 DOM요소를 가리킨다.



### index.js 참고사항

User.find({})로 찾은 모든 사용자를 mongoose.pug를 렌더링할 때 users 변수로 넣어준다. 몽구스도 기본적으로 프로미스를 지원한다. 따라서 then과 catch를 사용해서 조회 성공과 실패 시의 정보를 얻을 수 있다. *aysnc / await*을 활용한 표현은 아래와 같다.  

```javascript
router.get('/', async(req, res, next) => {
    try{
        const user = await User.find();
        res.render('mongoose', {users});
    }catch (error){
        console.log(error);
        next(error);
    }
})
```



### users.js 참고사항

GET /users와 POST /users 주소로 요청이 들어올 때의 라우터다. GET은 사용자를 조회하는 요청이고, POST는 사용자를 등록하는 요청을 처리한다. 정의된 스키마에 부합되지 않는 데이터를 등록하려고 하면 몽구스가 에러를 발생시킨다.



### comments.js 참고사항

