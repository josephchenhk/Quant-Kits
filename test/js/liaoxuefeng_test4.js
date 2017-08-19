'use strict';

var obj = {
    birth: 1990,
    getAge: function (year) {
        var b = this.birth; // 1990
        //var fn = (y) => y - this.birth; // this.birth仍是1990
		var fn;
		fn = function(y){
			return y - this.birth;
		}
        return fn.call({birth:2000}, year);
    }
};
console.log(obj.getAge(2015)); // 25
