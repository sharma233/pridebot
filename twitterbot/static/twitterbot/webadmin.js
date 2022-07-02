document.addEventListener('DOMContentLoaded', function() {

    let addButton = document.querySelector('.addbutton');
    addButton.addEventListener('click', addHandler.bind(this));

});

function addHandler(element) {
    enteredValue = document.querySelector('#id_username');
    console.log(enteredValue.value);

    fetch('/add/', {
        method: 'POST',
        body: JSON.stringify({
            userToAdd: enteredValue.value
        })
    })

}