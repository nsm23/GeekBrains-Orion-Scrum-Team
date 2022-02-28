const NOTIFICATIONS_HEADER_URL = "/notifications/header/";
const NOTIFICATION_SET_READ_URL = "/notifications/mark-as-read/";
const NOTIFICATION_SET_READ_AND_REDIRECT_URL = "/notifications/mark-as-read/{{id}}/";
const POST_URL = "/posts/{{slug}}/"
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
        return markNotificationReadFetch([a.dataset.commentId])
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

`
<li class="row mb-2">
    <div class="col-2 text-center py-2">
        <img class="w-75 rounded-circle"
             src="/media/avatars/1_knXJc0PyM5n7OaGnJi79EQ.png">
    </div>
    <div class="col-8">
        <div>Пользователю <a href="/cabinet/3/user_detail/" class="text-dark">@marya</a>
            понравилась ваша публикация.</div>
    </div>
    <div class="col-2">
        <a title="Прочитано" data-is-read="false" data-comment-id="29" class="text-secondary">
            <i class="bi bi-check-circle-fill"></i>
        </a>
        <a href="/notifications/mark-as-read/29/" title="Перейти к комментарию"
            class="text-secondary">
            <i class="bi bi-box-arrow-up-right"></i>
        </a>
    </div>
</li>
`

const generateAvatarDiv = (user_img_url) => {
    let div = document.createElement("div");
    div.classList.add("col-2", "text-center", "py-2");

    let img = document.createElement('img');
    img.classList.add("w-75", "rounded-circle");
    img.setAttribute("src", user_img_url);
    div.appendChild(img);

    return div;
}

const generateCommentDiv = (username, user_id, user_img_url, text, dateTime) => {
    let div = document.createElement("div");
    div.classList.add("col-8");

    let aUser = document.createElement("a");
    let user_url = USER_PROFILE_URL.replace("{{id}}", user_id)
    aUser.setAttribute("href", user_url);
    aUser.classList.add("text-dark");
    aUser.textContent = "@" + username;
    div.appendChild(aUser);

    let divDate = document.createElement("div");
    divDate.classList.add("mt-2");
    let dateSmall = document.createElement("small");
    dateSmall.textContent = dateTime;
    divDate.appendChild(dateSmall);
    div.appendChild(divDate);

    let divText = document.createElement("div");
    divText.textContent = text;
    div.appendChild(divText);

    return div;
}

const generateLinksDiv = (username, user_id, user_img_url, text, dateTime, comment_id) => {
    let div = document.createElement("div");
    div.classList.add("col-2");

    let aCommentRead = document.createElement("a");
    aCommentRead.setAttribute("title", "Прочитано");
    aCommentRead.setAttribute("data-is-read", "false");
    aCommentRead.setAttribute("data-comment-id", comment_id);
    aCommentRead.classList.add("text-secondary");
    aCommentRead.innerHTML = '<i class="bi bi-check-circle-fill"></i>';
    aCommentRead.addEventListener("click", event => {
        event.preventDefault();
        markNotificationRead(event);
    });
    div.appendChild(aCommentRead);

    let aCommentLink = document.createElement("a");
    aCommentLink.href = NOTIFICATION_SET_READ_AND_REDIRECT_URL.replace("{{id}}", comment_id);
    aCommentLink.setAttribute("title", "Перейти к комментарию");
    aCommentLink.classList.add("text-secondary");
    aCommentLink.innerHTML = ' <i class="bi bi-box-arrow-up-right"></i>';
    div.appendChild(aCommentLink);

    return div;
}


const generateNotification = (username, user_id, user_img_url, text, dateTime, comment_id) => {
    let li = document.createElement("li");
    li.classList.add("row", "mb-2");

    let avatarDiv = generateAvatarDiv(user_img_url);
    li.appendChild(avatarDiv);

    let commentDiv = generateCommentDiv(username, user_id, user_img_url, text, dateTime);
    li.appendChild(commentDiv);

    let linksDiv = generateLinksDiv(username, user_id, user_img_url, text, dateTime, comment_id);
    li.appendChild(linksDiv);

    return li;
}

const generateLikeNotification = (username, user_id, user_img_url) => {
    let li = document.createElement("li");
    li.classList.add("row", "mb-2");

    // div block: user avatar
    let div1 = document.createElement("div");
    div1.classList.add("col-2", "text-center", "py-2");

    let img = document.createElement('img');
    img.classList.add("w-75", "rounded-circle");
    img.setAttribute("src", user_img_url);

    div1.appendChild(img);
    li.appendChild(div1);
}

const generateCommentNotification = (username, user_id, user_img_url, text, dateTime, comment_id) => {
    let li = document.createElement("li");
    li.classList.add("row", "mb-2");

    // div block: user avatar
    let div1 = document.createElement("div");
    div1.classList.add("col-2", "text-center", "py-2");

    let img = document.createElement('img');
    img.classList.add("w-75", "rounded-circle");
    img.setAttribute("src", user_img_url);

    div1.appendChild(img);
    li.appendChild(div1);


    // div block: comment
    let div2 = document.createElement("div");
    div2.classList.add("col-8");
    li.appendChild(div2);

    let aUser = document.createElement("a");
    let user_url = USER_PROFILE_URL.replace("{{id}}", user_id)
    aUser.setAttribute("href", user_url);
    aUser.classList.add("text-dark");
    aUser.textContent = "@" + username;
    div2.appendChild(aUser);

    let div2Date = document.createElement("div");
    div2Date.classList.add("mt-2");
    let dateSmall = document.createElement("small");
    dateSmall.textContent = dateTime;
    div2Date.appendChild(dateSmall);
    div2.appendChild(div2Date);

    let div2Text = document.createElement("div");
    div2Text.textContent = text;
    div2.appendChild(div2Text);


    // div block: links
    let div3 = document.createElement("div");
    div3.classList.add("col-2");
    li.appendChild(div3);

    let aCommentRead = document.createElement("a");
    aCommentRead.setAttribute("title", "Прочитано");
    aCommentRead.setAttribute("data-is-read", "false");
    aCommentRead.setAttribute("data-comment-id", comment_id);
    aCommentRead.classList.add("text-secondary");
    aCommentRead.innerHTML = '<i class="bi bi-check-circle-fill"></i>';
    aCommentRead.addEventListener("click", event => {
        event.preventDefault();
        markNotificationRead(event);
    });
    div3.appendChild(aCommentRead);

    let aCommentLink = document.createElement("a");
    aCommentLink.href = NOTIFICATION_SET_READ_AND_REDIRECT_URL.replace("{{id}}", comment_id);
    aCommentLink.setAttribute("title", "Перейти к комментарию");
    aCommentLink.classList.add("text-secondary");
    aCommentLink.innerHTML = ' <i class="bi bi-box-arrow-up-right"></i>';
    div3.appendChild(aCommentLink);

    return li;
}


const generateAllNotificationsLink = (user_id) => {
    let li = document.createElement('li');
    li.classList.add("row", "mt-4", "mb-2");

    let div = document.createElement("div");
    div.classList.add("col", "text-center");
    li.appendChild(div);

    let a = document.createElement("a");
    a.classList.add("text-dark");
    a.href = USER_PROFILE_NOTIFICATIONS_URL.replace("{{id}}", user_id);
    a.textContent = "Просмотреть все уведомления";
    div.appendChild(a);

    return li;
}


const generateNoificationsBar = (notifications_count, comments, current_user_id) => {
    const notificationsCounterSpan = document.querySelector('#notifications-counter');
    const notificationsUl = document.querySelector('#notifications-ul');


    if (notifications_count > 0)
        notificationsCounterSpan.textContent = notifications_count;

    notificationsUl.innerHTML = '';
    if (comments) {
        for (let comment of comments) {
            let commentLi = generateCommentNotification(
                comment.username,
                comment.user_id,
                comment.avatar,
                comment.text,
                comment.created_at,
                comment.comment_id,
                comment.post_slug,
            );
            notificationsUl.appendChild(commentLi);
        }
    }
    let allNotificationsLink = generateAllNotificationsLink(current_user_id);
    notificationsUl.appendChild(allNotificationsLink);
}

document.addEventListener("DOMContentLoaded", event => {
    const request = new Request(NOTIFICATIONS_HEADER_URL);
    const options = {method: "GET", mode: "same-origin"};

    makeFetch(request, options)
        .then(response => {
            if (response["error"])
                console.log(response["error"])
            else {
                generateNoificationsBar(response["notifications_count"], response["comments"], response["current_user_id"]);
            }
        })
        .catch()
});
