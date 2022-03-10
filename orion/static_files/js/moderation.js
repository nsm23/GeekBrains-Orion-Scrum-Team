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
                        let innerBtns = a.parentElement.querySelectorAll('a');

                        console.log(innerBtns);
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

                );
        })
})