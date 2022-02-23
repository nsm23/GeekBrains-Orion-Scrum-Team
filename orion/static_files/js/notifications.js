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

const generateCommentNotification = (username, user_img_url, text, dateTime) => {
    return `
        <li class="row mb-2">
            <div class="col-2 text-center py-2">
                <img src="${ user_img_url }" class="w-75 rounded-circle">
            </div>
            <div class="col-9">
                <div><a href="" class="text-dark"><strong>@${ username }</strong></a></div>
                <div class="mt-2"><small>${ dateTime }</small></div>
                <div>
                    ${text}
                </div>
            </div>
        </li>
    `
}


document.addEventListener("DOMContentLoaded", event => {
    const notificationsCounterSpan = document.querySelector('#notifications-counter');
    const notificationsUl = document.querySelector('#notifications-ul');

    const request = new Request('/notifications/header/');
    const options = {method: "GET", mode: "same-origin"};

    makeFetch(request, options)
        .then(response => {
            if (response["error"])
                console.log(response["error"])
            else {
                notificationsCounterSpan.textContent = response["notifications_count"];

                notificationsUl.innerHTML = '';
                for (let notification of response["comments"]) {
                    let template = generateCommentNotification(notification.username, notification.avatar,
                        notification.text, notification.created_at);
                    notificationsUl.innerHTML += template;
                }
                if (response["comments"].length < response["notifications_count"])
                    notificationsUl.innerHTML += `<li class="row mt-4 mb-2">
                        <div class="col text-center"><a href="" class="text-dark">Просмотреть все уведомления</a></div></li>`
            }
        })
        .catch()



});
