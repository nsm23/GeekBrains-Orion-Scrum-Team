"use strict";


const POST_APPROVE_URL = "/moderation/posts/approve/{{post_id}}/";
const POST_DECLINE_URL = "/moderation/posts/decline/{{post_id}}/";


const postModerationFetch = (post_id, action) => {
    let url;
    if (action === 'approve') {
        url = POST_APPROVE_URL.replace('{{post_id}}', post_id);
    } else if (action === 'decline')
        url = POST_DECLINE_URL.replace('{{post_id}}', post_id);
    else
        return ;

    const csrftoken = getCookie('csrftoken');
    const request = new Request(url);
    const options = {
        method: "POST",
        mode: "same-origin",
        headers: {"X-CSRFToken": csrftoken, 'Content-Type': 'application/json'}
    };
    return makeFetch(request, options);
}


const moderationBtnClick = (event, action) => {
    event.preventDefault();

    let a = event.target.closest("a");
    postModerationFetch(a.dataset.postId, action)
        .then(response => {
            if ("error" in response)
                console.log(`Post ${action} error: ${response["error"]}`)
            else {
                let innerBtns = a.parentElement.querySelectorAll('a');
                for (let inner_btn of innerBtns) {
                    inner_btn.classList.remove('btn-outline-success');
                    inner_btn.classList.remove('btn-outline-danger');
                    inner_btn.classList.add('disabled');
                    inner_btn.classList.add('btn-outline-secondary');
                    inner_btn.blur();
                }
            }
        })
        .catch(
            // ToDo: catch errors!
        );
}


document.addEventListener('DOMContentLoaded', event => {
    let postApproveBtns = document.querySelectorAll('.post-approve');
    let postDeclineBtns = document.querySelectorAll('.post-decline');

    for (let btn of postApproveBtns)
        btn.addEventListener("click", event => {
            moderationBtnClick(event, "approve");
        });
    for (let btn of postDeclineBtns)
        btn.addEventListener("click", event => {
            moderationBtnClick(event, "decline");
        });
})
