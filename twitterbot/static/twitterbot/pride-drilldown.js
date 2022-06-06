document.addEventListener('DOMContentLoaded', function() {

    let profileButton = document.querySelector('.profilebutton');
    profileButton.addEventListener('click', linkHandler.bind(this));

    let indexButton = document.querySelector('.indexbutton');
    indexButton.addEventListener('click', linkHandler.bind(this));

    let prideBoxList = document.querySelectorAll('.pridebox');
    for (let i = 0; i < prideBoxList.length; i++) {
        prideBoxList[i].style.border = 'thin solid black';
        prideBoxList[i].style.padding = '5px';
        prideBoxList[i].style.margin = '10px';

        prideBoxList[i].addEventListener('click', function(element) {
            let prideBoxUser = element.target.querySelector('.twittername').innerText;
            let newWindow = window.open(`/profile/${prideBoxUser}`, '_self');
        });

        prideBoxList[i].addEventListener('mouseover', function() {
            prideBoxList[i].style.backgroundColor = 'lightgrey';
        })

        prideBoxList[i].addEventListener('mouseout', function() {
            prideBoxList[i].style.backgroundColor = 'white';
        })

    }
});

function linkHandler(element) {
    //console.log('div was clicked!');
    //let twitname = document.querySelector('.twittername');
    //console.log(twitname.innerText);
    //console.log(element.target.className);
    //let myWindow = window.open(`http://twitter.com/${twitname.innerText}`);

    let buttonClass = element.target.className;
    if (buttonClass === "profilebutton") {
        let twitname = document.querySelector('.twittername');
        let myWindow = window.open(`http://twitter.com/${twitname.innerText}`);
    } else if (buttonClass === 'indexbutton') {
        let myWindow = window.open('/', '_self');
    }
}