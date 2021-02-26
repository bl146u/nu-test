"use strict";


(($) => {


    const SERVER_ERROR = "Во время загрузки изображения произошла ошибка!<br />Попробуйте загрузить позднее...";


    let reset_form = (form) => {
        form.find(".error").remove();
    }


    let form_error = (form, message) => {
        reset_form(form);
        form.append($(`<div class="error">${message}</div>`));
    }


    let read_file = (file, callback) => {
        if (window.FileReader){
            let reader = new FileReader();
            reader.onloadend = (event) => {
                callback({
                    data:event.target.result,
                });
            };
            reader.readAsDataURL(file);
        }
    }


    let prepend_image = (data) => {
        let block = $(".list-images > tbody"),
            tr = $(`
                <tr class="id-${ data.id }">
                    <td class="image"><img src="${ data.image }" alt="" /></td>
                    <td class="history"></td>
                    <td class="update"><span data-id="${ data.id }">Обновить</span></td>
                </tr>
            `);
        for (let i=0; i<data.history.length; i++){
            tr.find(".history").append(`
                <div><code>${ data.history[i].created }</code> ${ data.history[i].image }</div>
            `);
        }
        tr.find("td.update > span").bind("click", update_image);
        block.prepend(tr);
        block.children(".empty").remove();
    }


    let update_view_image = (data) => {
        let tr = $(`.list-images > tbody > tr.id-${data.id}`);
        tr.find(".image > img").attr("src", data.image);
        tr.find(".history").html("");
        for (let i=0; i<data.history.length; i++){
            tr.find(".history").append(`
                <div><code>${ data.history[i].created }</code> ${ data.history[i].image }</div>
            `);
        }
    }


    let update_image = (event) => {
        let field = $('<input accept="image/png, image/jpeg, image/jpg" class="file-upload-field" name="image" type="file" />'),
            id = event.currentTarget.dataset.id;
        event.preventDefault();
        field.bind("input", (event) => {
            read_file(event.currentTarget.files[0], (image) => {
                image.id = id;
                $.ajax({
                    url:"/api/v1/update-image/",
                    data:JSON.stringify(image),
                    type:"POST",
                    dataType:"json",
                    contentType:"application/json; charset=utf-8",
                    headers:{"X-CSRFToken":$.cookie("csrftoken")},
                    success:(data, status) => {
                        if (status === "success"){
                            update_view_image(data);
                        } else {
                            form_error(SERVER_ERROR);
                        }
                    },
                    error:(xhr) => {
                        form_error($(".file-upload"), xhr.responseJSON ? xhr.responseJSON.error : SERVER_ERROR);
                    },
                    complete:() => {
                        event.currentTarget.SendImage = undefined;
                    }
                })
            });
        }).trigger("click");
    }


    $(() => {

        $(".file-upload").bind("submit", (event) => {
            event.preventDefault();
            let form = $(event.currentTarget);
            reset_form(form);
            $.ajax({
                url:"/api/v1/upload-image/",
                data:JSON.stringify(event.currentTarget.SendImage),
                type:"POST",
                dataType:"json",
                contentType:"application/json; charset=utf-8",
                headers:{"X-CSRFToken":$.cookie("csrftoken")},
                success:(data, status) => {
                    if (status === "success"){
                        prepend_image(data);
                    } else {
                        form_error(SERVER_ERROR);
                    }
                },
                error:(xhr) => {
                    form_error(form, xhr.responseJSON ? xhr.responseJSON : SERVER_ERROR);
                },
                complete:() => {
                    event.currentTarget.SendImage = undefined;
                }
            })
        })

        $(".file-upload-field").bind("input", (event) => {
            read_file(event.currentTarget.files[0], (image) => {
                event.currentTarget.form.SendImage = image;
                $(event.currentTarget.form).submit();
                event.currentTarget.value = "";
            });
        })

        $(".list-images td.update > span").bind("click", update_image)

    })


})(jQuery);
