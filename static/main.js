$(document).ready(function(){

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function csrfSafeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    function sameOrigin(url) {
        var host = document.location.host;
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            !(/^(\/\/|http:|https:).*/.test(url));
    }

    var csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    // -------------------------- Загрузка майлстоунов --------------------------

    $('body').on('click', '.project-loader', function (e) {
        e.preventDefault();

        var action = $(this).data('action'),
            link = $(this).attr('href'),
            self = $(this),
            forHide = $(this).data('hide');

        if(action == 'description') {
            var taskId = $(this).data('task');
            Cookies.set('last_visited_task', taskId);
        }

        if (action == 'tasks') {
            var module_id = $(this).data('module');
            var addTaskLink = $('#addTask');
            var link_parts = addTaskLink.attr('href').split('?module_id=');
            // console.log(link_parts);
            var new_link = link_parts[0] + '?module_id=' + module_id;

            addTaskLink.attr('href', new_link);
        }

        forHide.forEach(function (el) {
            var body = $('body');
            body.find('#'+el).html('');
            body.find('.'+el+'-container').hide();
        });

        $.ajax({
            url: link,
            method: 'get',
            success: function (response) {
                $('#' + action).html(response);
                $('.' + action +'-container').show();
                self.parents('.list-group').find('.list-group-item').removeClass('list-group-item-info');

                self.addClass('list-group-item-info');
            },
            error: function (error) {
                console.log(error)
            }
        });

    });

    // -------------------------- Добавления коммантария к задаче --------------------------

    $('body').on('click', '#addCommentToTask', function (e) {
       e.preventDefault();

       var form = $(this).parent('form');

       $.ajax({
           url: form.attr('action'),
           data: form.serialize(),
           method: 'post',
           success: function (response) {
               if (response.status == 0) {
                   toastr.warning(response.message);
               } else {
                   $('#addCommentContainer').html(response);
                   toastr.success('Комментарий успешно добавлен');
               }

           },
           error: function (e) {
               console.log('error')
           }
       });

    });

    // -------------------------- Добавление задачи - отображение модалки с формой --------------------------

    $('body').on('click', '#addTask', function (e) {
        e.preventDefault();

        $.ajax({
            url: $(this).attr('href'),
            success: function (response) {
                $('#modalContent').html(response);
                $('.select2').select2({
                    width: '100%'
                });
                $('#myModal').modal('show');
            },
            error: function (e) {
                console.log('error')
            }
        });

    });

    // -------------------------- Добавление задачи - обработка формы --------------------------

    $('body').on('click', '#addTaskBtn', function (e) {
        e.preventDefault();

        var form = $(this).parents('form');

        $.ajax({
            url: form.attr('action'),
            method: 'post',
            data: form.serialize(),
            success: function (response) {
                $('#tasks').append(response);
                $('#myModal').modal('hide');
                toastr.success('Задача успешно добавлена');
            },
            error: function (e) {
                console.log('error')
            }
        });

    });

});
