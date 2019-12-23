var parent = document.querySelector('.pagination-list');
var pages = parent.getElementsByClassName('row');
console.log(pages);
for(var i=1;i<pages.length;i++){
    pages[i].style.display = 'none';
}

var Anchors = parent.getElementsByTagName('a');
for (var i = 1; i < Anchors.length-1; i++) {
    Anchors[i].addEventListener("click", 
        function (event) {
            event.preventDefault();
            console.log(pages);
            console.log(event.target.innerHTML);
            pages[event.target.innerHTML-1].style.display = 'block';
            var divs  = document.querySelectorAll("body > div > div:not(#p"+event.target.innerHTML+")");
            for(var i=0;i<divs.length;i++){
                divs[i].style.display = 'none';
            }
        }, 
        false);
}