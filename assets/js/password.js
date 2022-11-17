let string = '';
var myarray = [''];
var index = ''
let buttons = document.querySelectorAll('.img-op2');
Array.from(buttons).forEach((button) => {
    button.addEventListener('click', (e) => {
        console.log(myarray, 'array h');
        data = document.getElementById('unique').value;
        if (data) {
            console.log('data h');
        } else {
            myarray = [];
            document.getElementById('unique').value = '';
            console.log('karke rahegye');
            string = '';
        };
        console.log(typeof(e.target.value));
        console.log(myarray.includes(e.target.value));
        if (myarray.includes(e.target.value) == false) {
            console.log('ok');
            if (myarray == []) {
                console.log('working');
                myarray = [];
            };
            if (string == '') {
                string = e.target.value;
                console.log(string);
                myarray = string.split('+');
                console.log(myarray);
            } else {
                string = string + '+' + e.target.value;
                console.log(string, 'else');
                myarray = string.split('+');
                console.log(myarray);
            };
            console.log(myarray);
            document.getElementById('unique').value = myarray;
        } else {
            console.log('hatana h finally !');
            var index = myarray.indexOf(e.target.value);
            var sindex = '+' + e.target.value;
            console.log(index);
            console.log(sindex);
            if (index > -1) {
                myarray.splice(index, 1);
                //  string.replace(sindex, '');
                string = string.slice(0, string.length - 5);
            };
            console.log(myarray);
            document.getElementById('unique').value = myarray;
        };
        console.log('final array' + myarray);
    });
});

function submit() {
    document.getElementById('formid2').submit();
}