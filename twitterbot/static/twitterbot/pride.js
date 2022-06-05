document.addEventListener('DOMContentLoaded', function() {

    let prideBoxList = document.querySelectorAll('.pridebox');

    for (let i = 0; i < prideBoxList.length; i++) {
        prideBoxList[i].style.border = 'thin solid black';
        prideBoxList[i].style.padding = '5px';
        prideBoxList[i].style.margin = '10px';
    }
})