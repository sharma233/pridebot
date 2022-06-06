document.addEventListener('DOMContentLoaded', function() {

    //let searchBox = document.querySelector('#searchbox');
    let searchButton = document.querySelector("#searchbutton");
    //console.log(searchBox);
    //console.log(searchButton);
    let prideBoxList = document.querySelectorAll('.pridebox');

    searchButton.addEventListener('click', searchHandler);

    for (let i = 0; i < prideBoxList.length; i++) {
        prideBoxList[i].style.border = 'thin solid black';
        prideBoxList[i].style.padding = '5px';
        prideBoxList[i].style.margin = '10px';

        let profileButton = prideBoxList[i].querySelector('.profilebutton');
        profileButton.addEventListener('click', linkHandler.bind(this));
    }
});

function linkHandler(element) {
    console.log('div was clicked!');
    let twitname = element.target.parentElement.querySelector('.twittername');
    console.log(twitname.innerText);
    let myWindow = window.open(`http://twitter.com/${twitname.innerText}`);
}

function searchHandler(element) {
    let searchBox = document.querySelector('#searchbox')
    console.log(element.target);
    console.log(searchBox.value);

    let prideBoxList = document.querySelectorAll('.pridebox');
    for ( let i = 0; i < prideBoxList.length; i++) {
        let prideBoxTwitname = prideBoxList[i].querySelector('.twittername');
        let parent = prideBoxList[i];
        console.log(prideBoxTwitname.parentElement);

        if ((searchBox.value).toLowerCase() === (prideBoxTwitname.innerText).toLowerCase()) {
            parent.style.display = 'block';
        } else if (searchBox.value === '') {
            parent.style.display = 'block';
        } else {
            parent.style.display = 'none';
        }
    }
}