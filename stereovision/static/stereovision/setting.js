var left = document.querySelector('#left_camera');
var right = document.querySelector('#right_camera');

left.addEventListener("change", re);
right.addEventListener("change", re);

function re() {
    document.getElementsByName('preview')[0].click();
};
