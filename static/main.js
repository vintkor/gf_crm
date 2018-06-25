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
                console.log();
                self.parents('.list-group').find('.list-group-item').removeClass('list-group-item-info');

                self.addClass('list-group-item-info');
            },
            error: function (error) {
                console.log(error)
            }
        });

    });

});