"use strict";


const POST_APPROVE_URL = "/moderation/posts/approve/{{post_id}}/";


const postApproveFetch = post_id => {
    const csrftoken = getCookie('csrftoken');
    const request = new Request(POST_APPROVE_URL.replace('{{post_id}}', post_id));
    const options = {
        method: "POST",
        mode: "same-origin",
        headers: {"X-CSRFToken": csrftoken, 'Content-Type': 'application/json'}
    };
    return makeFetch(request, options);
}


document.addEventListener('DOMContentLoaded', event => {
    let postApproveBtns = document.querySelectorAll('.post-approve');

    for (let btn of postApproveBtns)
        btn.addEventListener("click", event => {
            event.preventDefault();

            let a = event.target.closest("a");
            postApproveFetch(a.dataset.postId)
                .then(response => {
                    if ("error" in response)
                        console.log("Post approving error: " + response["error"])
                    else {
                        a.classList.add('disabled');
                        a.classList.remove('btn-outline-success');
                        a.classList.add('btn-outline-secondary');
                    }
                })
                .catch(

                );
        })
})