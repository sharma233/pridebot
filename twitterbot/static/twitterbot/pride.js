document.addEventListener('DOMContentLoaded', function() {

    let searchBox = document.querySelector('#searchbox');
    searchBox.addEventListener('keypress', function(event) {
        if (event.key === 'Enter') {
            document.getElementById('searchbutton').click();
        }
    })

    let searchButton = document.querySelector("#searchbutton");
    searchButton.addEventListener('click', searchHandler);

    let prideBoxList = document.querySelectorAll('.pridebox');
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
    let searchBox = document.querySelector('#searchbox');
    let searchBoxValue = (searchBox.value).toLowerCase();
    let regex = `.*${searchBoxValue}.*`;

    let prideBoxList = document.querySelectorAll('.pridebox');
    for ( let i = 0; i < prideBoxList.length; i++) {
        let prideBoxTwitname = prideBoxList[i].querySelector('.twittername');
        let twitName = prideBoxTwitname.innerText.toLowerCase();

        if (twitName.match(regex)) {
            prideBoxList[i].style.display = 'block';
        } else if (searchBox.value === '') {
            prideBoxList[i].style.display = 'block';
        } else {
            console.log('nothing found');
            prideBoxList[i].style.display = 'none';
        }
    }
}