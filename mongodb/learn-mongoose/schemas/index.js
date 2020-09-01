const mongoose = require('mongoose')

const connect = () => {
    // 개발 환경이 아닐 때, 몽구스가 생성하는 쿼리 내용을 콘솔로 출력
    if (process.env.NODE_ENV != 'production'){
        mongoose.set('debug', true);
    }
    // 테스트용 아이디와 비밀번호를 설정하였다
    mongoose.connect('mongodb://hayunjong83:mongodb1234@localhost:27017/admin', {
        dbName: 'nodejs',
        userNewUrlParser: true,
        useCreateIndex: true,
    }, (error) =>{
        if (error){
            console.log('몽고디비 연결 에러', error);
        }else{
            console.log('몽고디비 연결 성공');
        }
    });
};

mongoose.connection.on('error', (error) => {
    console.log('몽고디비 연결 에러', error);
});
mongoose.connection.on('disconnected', () =>{
    console.log('몽고디비 연결이 끊겼습니다. 연결을 재시도합니다.');
    connect();
})

module.exports = connect;