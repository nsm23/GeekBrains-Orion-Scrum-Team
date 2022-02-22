const makeFetch = async (request, options)  => {
    return fetch(request, options)
        .then(async response => {
            if (response.ok)
                return response.json()
            else {
                response = `${response.status} ${response.statusText}`
                return {"error": response}
            }
        })
        .catch(error => console.log("Error: " + error))
}


document.addEventListener("DOMContentLoaded", event => {
    const notificationsCounterSpan = document.querySelector('#notifications-counter');
    const notificationsUl = document.querySelector('#notifications-ul');

    const request = new Request('/notifications/comment/');
    const options = {method: "GET", mode: "same-origin"};

    makeFetch(request, options)
        .then(response => {
            if (response["error"])
                console.log(response["error"])
            else {
                notificationsCounterSpan.textContent = response["notifications"].length;

                for (let notification of response["notifications"]) {
                    let li = document.createElement('li');
                    let a = document.createElement('a');

                    a.href = `/posts/${ notification.post_id }/`;
                    a.textContent = `Новый комментарий от @${ notification.username } на ваш пост`;
                    a.classList.add('dropdown-item');


                    li.appendChild(a);
                    notificationsUl.appendChild(li);
                }

            }
        })
        .catch()



});
