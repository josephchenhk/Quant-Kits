var Student = {
    name: 'Robot',
    height: 1.2,
    run: function () {
        console.log(this.name + ' is running...');
    }
};

var xiaoming = {
    name: '小明'
};

xiaoming.__proto__ = Student;

xiaoming.name; // '小明'
alert(xiaoming.run()); // 小明 is running...

//alert('Hello, world');
