"use strict";


const NOTIFICATIONS_HEADER_URL = "/notifications/header/";
const NOTIFICATION_SET_READ_URL = "/notifications/mark-as-read/";
const NOTIFICATION_SET_READ_AND_REDIRECT_URL = "/notifications/mark-as-read/{{id}}/";
const USER_PROFILE_URL = "/cabinet/{{id}}/user_detail/"
const USER_PROFILE_NOTIFICATIONS_URL = "/cabinet/{{id}}/user_notifications/"


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


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


const markNotificationReadFetch = ids => {
    const csrftoken = getCookie('csrftoken');
    const request = new Request(NOTIFICATION_SET_READ_URL);
    const options = {
        method: "POST",
        mode: "same-origin",
        body: JSON.stringify({"ids": ids}),
        headers: {"X-CSRFToken": csrftoken, 'Content-Type': 'application/json'}
    };
    return makeFetch(request, options)
}


const markNotificationRead = event => {
    let a = event.target.closest("a");
    if (a.dataset.isRead === "false") {
        return markNotificationReadFetch([a.dataset.objectId])
            .then(response => {
                if (response["ids"]){
                    const notificationsCounterSpan = document.querySelector('#notifications-counter');
                    let count = +notificationsCounterSpan.textContent - 1;
                    notificationsCounterSpan.textContent = count > 0 ? count : "";
                    a.classList.remove("text-dark");
                    a.classList.add("text-success");
                    a.setAttribute("title", "Не прочитано");
                    a.setAttribute("data-is-read", "true");
                }
            })
    }
}


const commentNotificationTemplate = (comment) => {
    return `
        <li class="row mb-2">
            <div class="col-2 text-center py-2">
                <img class="w-75 rounded-circle" src="${ comment.user_avatar_url }">
            </div>
            <div class="col-8">
                <a href="${ USER_PROFILE_URL.replace('{{id}}', comment.user_id) }" class="text-dark">
                    @${ comment.username }</a>
                <div class="mt-2"><small>${ comment.created_at }</small></div>
                <div>${ comment.text }</div>
            </div>
            <div class="col-2">
                <a title="Прочитано" data-is-read="false" data-object-id="${ comment.comment_id }"
                        class="text-secondary">
                    <i class="bi bi-check-circle-fill mark-as-read"></i>
                </a>
                <a href="${ NOTIFICATION_SET_READ_AND_REDIRECT_URL.replace('{{id}}',comment.comment_id) }"
                    title="Перейти к комментарию" class="text-secondary">
                        <i class="bi bi-box-arrow-up-right"></i>
                </a>
            </div>
        </li>
    `
}


const likeNotificationTemplate = (like) => {
    let text = '';
    let className = '';
    if (like.vote === 1) {
        text = `<small><i class="bi bi-hand-thumbs-up-fill"></i></small> Понравилась ваша публикация`;
        className = 'text-success';
    }
    else if (like.vote === -1) {
        text = `<small><i class="bi bi-hand-thumbs-down-fill"></i></small> Не понравилась ваша публикация`;
        className = 'text-danger';
    }

    return `
        <li class="row mb-2">
            <div class="col-2 text-center py-2">
                <img class="w-75 rounded-circle" src="${ like.user_avatar_url }">
            </div>
            <div class="col-8">
                <a href="${ USER_PROFILE_URL.replace('{{id}}', like.user_id) }" class="text-dark">
                    @${ like.username }</a>
                <div class="${ className }">${ text }</div>
            </div>
            <div class="col-2">
                <a title="Прочитано" data-is-read="false" data-object-id="${ like.like_id }" class="text-secondary">
                    <i class="bi bi-check-circle-fill mark-as-read"></i>
                </a>
                <a href="${ NOTIFICATION_SET_READ_AND_REDIRECT_URL.replace('{{id}}',like.like_id) }"
                    title="Перейти к публикации" class="text-secondary" href="">
                    <i class="bi bi-box-arrow-up-right"></i>
                </a>
            </div>
        </li>
    `
}


const AllNotificationsLinkTemplate = user_id => {
    return `
        <li class="row mt-4 mb-2">
            <div class="col text-center">
                <a href="${ USER_PROFILE_NOTIFICATIONS_URL.replace("{{id}}", user_id) }" class="text-dark">
                    Просмотреть все уведомления
                </a>
            </div>
        </li>
    `
}


const generateNoificationsBar = (notifications_count, comments, likes, current_user_id) => {
    const notificationsCounterSpan = document.querySelector('#notifications-counter');
    const notificationsUl = document.querySelector('#notifications-ul');


    if (notifications_count > 0)
        notificationsCounterSpan.textContent = notifications_count;

    notificationsUl.innerHTML = '';
    if (comments.length > 0) {
        notificationsUl.innerHTML += "<h5 class='mt-3'>Новые комментарии</h5>";

        for (let comment of comments) {
            let commentLi = commentNotificationTemplate(comment);
            notificationsUl.innerHTML += commentLi;
        }
    }
    if (likes.length > 0) {
        notificationsUl.innerHTML += "<h5 class='mt-3'>Новые отклики</h5>";
        for (let like of likes)
            notificationsUl.innerHTML += likeNotificationTemplate(like);
    }
    notificationsUl.innerHTML += AllNotificationsLinkTemplate(current_user_id);
}

document.addEventListener("DOMContentLoaded", event => {
    const request = new Request(NOTIFICATIONS_HEADER_URL);
    const options = {method: "GET", mode: "same-origin"};

    makeFetch(request, options)
        .then(response => {
            if (response["error"])
                console.log(response["error"])
            else {
                generateNoificationsBar(
                    response["notifications_count"],
                    response["comments"],
                    response["likes"],
                    response["current_user_id"],
                    );
            }
        })
        .then(() => {
                let markAsReadBtns = document.querySelectorAll('.mark-as-read');

                for (let btn of markAsReadBtns) {
                    btn.addEventListener("click", event => {
                        event.preventDefault();

                        markNotificationRead(event);
                    })
                }
            }
        )
        .catch()
});
