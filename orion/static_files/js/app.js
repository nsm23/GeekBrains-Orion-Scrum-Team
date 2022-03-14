$(document).ready(function () {
    bind_show_reply_form() // показ формы ответа
    bind_hide_reply_form() // скрытие формы ответа при фокусе на поле нового коммента
    bind_save_comment() // сохранение коммента
    bind_comment_validation() // валидцая формы сохранения коммента
});

bind_hide_reply_form = function () {
    if ($('.comments-textarea[hide-reply="true"]').length >= 1) {
        $('.comments-textarea[hide-reply="true"]').on('focus', function () {
            hide_all_reply_forms()
        })
    }
}

bind_show_reply_form = function () {
    $('.reply-link').each(function (_, elem) {
        $(elem).on('click', function () {
            show_reply_form(elem)
        })
    })
}

hide_all_reply_forms = function () {
    $('.reply-form').addClass('d-none')
}

bind_save_comment = function () {
    $('.btn-comment-save').each(function (_, elem) {
        $(elem).on('click', function () {
            save_comment(elem)
        })
    })
}

bind_comment_validation = function () {
    $('.comments-textarea').each(function (_, elem) {
        $(elem).on('input propertychange', function () {
            validate_comment_text(elem)
        })
    })
}

/**
 * Показывает форму ответа при клике на "Ответить"
 */
show_reply_form = function (elem) {
    hide_all_reply_forms()

    var comment_id = $(elem).data('comment_id') ?? 0
    if (comment_id <= 0) return false;

    if ($('#reply-to-' + comment_id + '-form').length > 0) {
        $('#reply-to-' + comment_id + '-form').removeClass('d-none')

        $('#reply-to-' + comment_id + '-form').find('.comments-textarea').focus()
    }
}

save_comment = function (elem) {
    var comment_form = $(elem).closest('.comment-form')
    if (comment_form.length > 0) {
        var comment_textarea = comment_form.find('.comments-textarea') ?? ''
        var post_id = comment_form.data('post_id') ?? 0
        var parent_id = comment_form.data('parent_id') ?? 0
        if (comment_textarea.length > 0 && post_id > 0) {
            var comment_text = comment_textarea.val() ?? ''
            var btn_comment_save = comment_form.find('.btn-comment-save') ?? ''

            if ($.trim(comment_text) !== '') {
                $.ajax({
                    url: '/comments/save/',
                    method: 'post',
                    data: {
                        text: comment_text,
                        post: post_id,
                        parent: parent_id,
                        csrfmiddlewaretoken: Cookies.get('csrftoken'),
                    },
                    error: function (jqXHR, error, errorThrown) {
                        comment_textarea.attr('readonly', false)
                        if (btn_comment_save.length > 0) {
                            btn_comment_save.attr('disabled', false)
                            btn_comment_save.html('Отправить <i class="fas fa-long-arrow-alt-right ms-1"></i>')
                        }

                        if (jqXHR.status && jqXHR.status == 400) {
                            alert(jqXHR.responseText);
                        } else {
                            alert("Something went wrong")
                        }
                    },
                    success: function (json) {
                        comment_textarea.val('')
                        comment_textarea.attr('readonly', false)
                        if (btn_comment_save.length > 0) {
                            btn_comment_save.attr('disabled', false)
                            btn_comment_save.html('Отправить <i class="fas fa-long-arrow-alt-right ms-1"></i>')
                        }

                        if (parent_id > 0) {
                            $('#reply-to-' + parent_id + '-form').addClass('d-none')
                            $('#reply-to-' + parent_id + '-form').parent().append(json.html)
                        } else {
                            var comments_exists = $('#post-comments').find('.comments').length > 0 ? true : false
                            var comment_html = '<div class="comments d-flex flex-start' + (comments_exists ? ' mt-4' : '') + '">' + json.html + '</div>'
                            if (comments_exists) {
                                $('#post-comments').append(comment_html)
                            } else {
                                $('#post-comments').html(comment_html)
                            }

                            $('#comment-' + json.comment_id).find('.reply-link').on('click', function () {
                                show_reply_form($(this))
                            })

                            $('#reply-to-' + json.comment_id + '-form').find('.comments-textarea').on('input propertychange', function () {
                                validate_comment_text($(this))
                            })

                            $('#reply-to-' + json.comment_id + '-form').find('.btn-comment-save').on('click', function () {
                                save_comment($(this))
                            })
                        }
                    },
                    beforeSend: function () {
                        comment_textarea.attr('readonly', true)
                        if (btn_comment_save.length > 0) {
                            btn_comment_save.attr('disabled', true)
                            btn_comment_save.html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Сохранение...')
                        }
                    },
                });
            }
        }
    }
}

validate_comment_text = function (elem) {
    var comment_text = $(elem).val() ?? ''

    var invalid = false
    if ($.trim(comment_text) == '') {
        invalid = true
    }

    $(elem).closest('.comment-form').find('.btn-comment-save').attr('disabled', invalid)
}

tinyMCE.init({
    selector: '.tinymce',
    theme: "silver",
    height: 500,
    menubar: false,
    language: 'ru',
    plugins: [
        'advlist autolink lists link image charmap print preview anchor',
        'searchreplace visualblocks code fullscreen',
        'insertdatetime media table paste code help wordcount'
    ],
    toolbar: 'undo redo | formatselect | bold italic backcolor | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | removeformat | help'
});

function like() {
    const like = $(this);
    const type = like.data('type');
    const pk = like.data('id');
    const action = like.data('action');
    const dislike = like.next();

    $.ajax({
        url: "/" + type + "/" + pk + "/" + action + "/",
        type: 'POST',
        data: {'obj': pk, 'csrfmiddlewaretoken': Cookies.get('csrftoken')},

        success: function (json) {
            $("#likes-total").text(json.sum_rating);

        }

    });
    return false;
}

function dislike() {
    const dislike = $(this);
    const type = dislike.data('type');
    const pk = dislike.data('id');
    const action = dislike.data('action');
    const like = dislike.prev();

    $.ajax({
        url: "/" + type + "/" + pk + "/" + action + "/",
        type: 'POST',
        data: {'obj': pk, 'csrfmiddlewaretoken': Cookies.get('csrftoken')},

        success: function (json) {
            $("#likes-total").text(json.sum_rating);
        }
    });
    return false;
}

function speech() {
  const slug = $(this).data('id');
  const textToSpeech = $('.card-text').text();
  const spinner = $('#spinner')

  spinner.addClass('fa fa-spinner fa-spin')

  $.ajax({
      url: "/posts/speech/" + slug,
      type: 'POST',
      data: {
        'csrfmiddlewaretoken': Cookies.get('csrftoken'),
        'text': textToSpeech,
    },
    success: function (speechFilePath) {
      spinner.removeClass( "fa fa-spinner fa-spin" )
      file = window.location.origin + '/media/' + speechFilePath

      const audio = $(`<audio controls><source id="source" src="${file}" type="audio/mpeg">Your browser does not support the audio element.</audio>`)
      $("#audio-container").append(audio)
    }
  });
}


// Подключение обработчиков
$(function () {
    $('[data-action="like"]').click(like);
    $('[data-action="dislike"]').click(dislike);
    $('[data-action="speech"]').click(speech);
});
