async  function makeRequest(url, method='GET') {
    let response = await fetch(url, {method});
    if (response.ok) {
        return  await response.text();
    }
    else {
        let error = new Error(response.statusText);
        error.response = response;
        throw  error;
    }
}


async function onLike(event) {
    event.preventDefault();
    let likeButton = event.target;
    try {
        let response = await makeRequest(event.target.href);
        const counter = event.target.parentElement.getElementsByClassName('counter')[0];
        counter.innerText = response;
    }
    catch (error) {
        console.log(error);
    }

    likeButton.classList.toggle('hidden');
    let unlikeButton = likeButton.parentElement.getElementsByClassName('unlike')[0];
    unlikeButton.classList.toggle('hidden');
}

async function onUnLike(event) {
    event.preventDefault();
    let UnlikeButton = event.target;
    try {
        let response = await makeRequest(event.target.href);
        const counter = event.target.parentElement.getElementsByClassName('counter')[0];
        counter.innerText = response;
    }
    catch (error) {
        console.log(error);
    }

    UnlikeButton.classList.toggle('hidden');
    let likeButton = UnlikeButton.parentElement.getElementsByClassName('like')[0];
    likeButton.classList.toggle('hidden');
}

window.addEventListener('load', function () {
    const  likeButton = document.getElementsByClassName('like');
    const  unlikeButton = document.getElementsByClassName('unlike');

    for (let btn of likeButton) {btn.onclick = onLike}
    for (let btn of unlikeButton) {btn.onclick = onUnLike}

});