odoo.define('dr_social_website.content_calendar', function (require) {
"use strict";
const publicWidget = require('web.public.widget');
var rpc = require('web.rpc');
console.log('kk',$('.last_post').val(),'ll',$('.last_post'))
if ($('.dashboard-table')[0]) {
   var id =  parseInt($('.dashboard-table')[0].dataset.id);
}
if ($('.last_post')[0]) {
   var id =  parseInt($('.last_post').val());
}

var ajax = require('web.ajax');

$(document).ready(function (ev) {
    $(".revision").hide();
//    $('.o_footer').addClass('header_hide')
//    $('.navbar').addClass('d-none')
    $(".delete_upload").hide();
    $(".search_upload").hide();
    $(".revision_progress").hide();
    $(".show_less").hide();
    $(".green").hide();
    $('.o_footer').addClass('header_hide')
    var posts = $('.dashboard-table')
    var table_1 = $('.db-card')
    var image_upload = $('.add_image')
    var text = $('.text-overflow');
    var feedback = $('.feedback_green');
    var progress_revision = $('.revision_progress');
    console.log('progress_revision',progress_revision.length)
     $('nav a[href^="/' + location.pathname.split("/")[1] + '"]').addClass('active');
    for (let i = 0; i < text.length; i++) {
        rpc.query({
            model: 'social.post',
            method: 'message_content',
            args: [,parseInt(text[i].offsetParent.dataset.id)],

        }).then(function(result){
            var chartdiv = 'chartdiv_' + String(text[i].offsetParent.dataset.id)
            var description = document.getElementById(chartdiv);
            description.innerHTML = result;
            if (!(text[i].scrollHeight > 130)) {
                var more_id = 'more_'+ String(text[i].offsetParent.dataset.id);
                $('#'+more_id).hide()
            }
        });
    }
    for (let i = 0; i < posts.length; i++) {
        if (posts[i].attributes.value.value === 'posted') {
            posts[i].style.pointerEvents = 'none';
//            posts[i].style.color = '#bdbfb7';
//            $('.red')[i].style['background-color']='#bdbfb7';
//            $('.black')[i].style['background-color']='#bdbfb7';
//            $('.value_time')[i].style['color']='#bdbfb7';
//            $('.date_default')[i].style['color']='#bdbfb7';
//            $('.grey')[i].style['background-color']='#bdbfb7';
//            $('.seeMore')[i].style['color']='#bdbfb7';
//            $('.add_image')[i].style['opacity']='0.3';
            $('.db-card')[i].style['opacity']='0.4';
        }
        if (feedback[i].attributes.value){
            var revision = 'revision_' +String(feedback[i].firstElementChild.id)
            var grey = 'grey_' +String(feedback[i].firstElementChild.id)
            var green = 'green_' +String(feedback[i].firstElementChild.id)
            $("#"+green).show();
            $("#"+revision).show();
            $("#"+grey).hide();
        }

    for (let i = 0; i < table_1.length; i++) {
        if (table_1[i].attributes.value.value === 'draft') {
            table_1[i].style.border = '2px solid #ffb914';
        }
        if (table_1[i].attributes.value.value === 'not_approved') {
            table_1[i].style.border = '2px solid red';
            $('.black')[i].style['background-color']='red';
        }
        if (table_1[i].attributes.value.value === 'scheduled') {
            $('.red')[i].style['background-color']='#00F5BE';
        }
    }
    for (let i = 0; i < image_upload.length; i++) {
        if (!('value' in image_upload[i].attributes)) {
            var id = image_upload[i].dataset.id
            var upload_id = 'upload_id_' + String(id)
            var upload = document.getElementById(upload_id);
            upload.classList.remove("d-none");
            var delete_image = 'delete_' + String(id)
            $('#' + delete_image).hide();
            var search_image = 'search_' + String(id)
            $('#' + search_image).hide();

        }
    }
     if (progress_revision.length > 0){
        if (progress_revision[i].attributes.value){
//            var revision = 'revision_' +String(feedback[i].firstElementChild.id)
//            var grey = 'grey_' +String(feedback[i].firstElementChild.id)
            var progress = 'progress_' +String(feedback[i].firstElementChild.id)
            $("#"+progress).show();
//            $("#"+revision).show();
//            $("#"+grey).hide();
        }
        }
    }
//     for (let i = 0; i < more_zoom_id.length; i++) {
//        if (!(more_zoom_id[i].scrollHeight > 130)) {
//        console.log('jfdasfjksdhf')
//                var more_zoom = more_zoom_id[i].id;
//                $('#'+more_zoom).hide()
//            }
//    }
//    var name_def = $('#name_value')[0].innerHTML;
//    console.log(name_def,'name_def')
//    if (name_def !=' '){
//    console.log('hhhhhhhhhhhhhhhhh',$("#default_value"))
//       $("#default_value").show();
//}

})

publicWidget.registry.websiteEventSearchSponsor = publicWidget.Widget.extend({

start: function () {
    var val = $('.dateTimePicker').datetimepicker({
    format: 'h:mm A D MMMM YYYY',
    });
},

 selector:'.content_calendar',
 events: {
        'click .new_post': '_new_post',
        'change .client_selection': '_client_selection',
        'click .client_approval': '_client_approval',
        'click .grey': '_grey',
        'click .grey_button': '_grey_button',
        'click .toggle-view': '_toggle_view',
        'change .post_feedback_textarea': '_load_feedback',
        'change .post_feedback_textarea_button': '_load_feedback_button',
        'change .post_message_textarea': '_load_message',
        'change .post_message_textarea_button': '_load_message_button',
        'change .post_uploded_image': '_load_uploaded_image',
        'change .post_uploded_image_button': '_load_uploaded_image_button',
        'click .approve_button': '_approve_button',
        'keydown .feedback_revision': '_feedback_revision',
        'keydown .feedback_revision_button': '_feedback_revision_button',
        'click .not_approved_button': '_not_approved_button',
        'click .red_button': '_red_button',
        'click .black_button': '_black_button',
        'click .delete_image': '_delete_image',
//        'click .delete_image_button': '_delete_image_button',
        'click .delete_upload': '_delete_upload',
        'click .delete_upload_button': '_delete_upload_button',
        'click .image_zoom': '_image_zoom',
        'click .image_zoom_button': '_image_zoom_button',
        'blur .date_button': '_date_input',
        'blur .value_date_time': '_value_date_time',
        'click .delete_post': '_delete_post',
        'click .delete_post_button': '_delete_post_button',
    },
    _new_post:function(e){
        e.preventDefault();
        console.log('aaaaaaaaaaa',e,id)
//        var last_id = localStorage.setItem("last_id",last);
        id++
        console.log( id,'lllllllllll')
        var upload_id = 'upload_button_' + id
        var chartdiv_id = 'chartdiv_button_' + id
        var green_id = 'green_button_' + id
        var grey_id = 'grey_button_' + id
        var more_id = 'more_id_' + id
        console.log(grey_id)
        var revision_id = 'revision_button_' + id
        var preview_id = 'preview_button_' + id
        var red_id = 'red_button_' + id
        var black_id = 'black_button_' + id
        var delete_upload_id = 'delete_upload_button_' + id
        var delete_image_id = 'delete_image_button_' + id
        var search_upload_id = 'search_upload_button_' + id
        var description_id = 'description_button_' + id
        var image_id = 'image_button_' + id
        var progress_id = 'progress_button_' + id
        var post_button = 'post_button_' + id
        var delete_post_id = 'delete_post_button_' + id
//        var more_zoom = 'more_zoom_'+id

        if ( $('.dashboard-table')[0]){
            $('.dashboard-table')[0].insertAdjacentHTML('beforebegin',
                `<div class="col-sm-12 col md-12 dashboard-table">
                <div class="col-md-12 red-border" id="new_row">
                    <div t-att-id="${post_button}">
                        <div class="db-card new_post_border" id="${id}">
                            <div class="d-flex justify-content-center align-items-center px-4 my-2">
                                <button class="red_button db-button db-button--actions db-button--round mr-2"
                                        id="${red_id}">
                                    <i class="fa fa-check"></i>
                                </button>
                                <button class="black_button db-button db-button--actions db-button--round"
                                        id="${black_id}">
                                    <i class="fa fa-times db-button__icons"></i>
                                </button>

                            </div>
                            <div class="add_image sub-table-2 my-2">
                                <div class="form-input">
                                    <div class="preview">
                                        <a href="#" class="db-card__image-link image_zoom_button"
                                           data-db-user-image="/dr_social_website/static/src/img/user.png"
                                           data-db-description="${description_id}">

                                            <img id="${preview_id}"/>
                                        </a>
                                    </div>
                                    <div class="upload_view"
                                         id="${upload_id}">
                                        <label for="${image_id}">
                                            <i class="fa fa-upload upload_button"></i>
                                        </label>

                                        <input type="file" id="${image_id}" accept="image/*"
                                               class="post_uploded_image_button"/>
                                    </div>
                                </div>
                                <i class="delete_image_button delete_button_post fa fa-trash"
                                                       id="${delete_image_id}"></i>
                                <i class="delete_upload_button delete_button_post fa fa-trash"
                                                       id="${delete_upload_id}"></i>
                                <i class="search_upload_button search_button_post fa fa-search"
                                               id="${search_upload_id}"></i>
                            </div>

                            <div class="ml-4 db-card__textarea-container my-2">
                                <textarea class="db-form-control db-form-control--textarea post_message_textarea_button text-overflow"
                                        id="${chartdiv_id}" placeholder="MESSAGE..."
                                        name="message" style="overflow:hidden"></textarea>
                                <a href="#" class="toggle-view seeMore more-text"
                                   id="${more_id}">
                                    more...
                                </a>
                                <a href="#" class="toggle-view d-none seeLess more-text">
                                    less...
                                </a>
                            </div>
                            <div class="container justify-content-center align-items-center px-4 my-2">
                                <div class="row my-5">
                                    <div class="col-4 mx-auto">
                                        <div class="db-datepicker-group">
                                            <input type="text"
                                                   class="db-datepicker dateTimePicker_button date_button"/>
                                            <i class="fa fa-chevron-down db-datepicker-group__icon"></i>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="ml-3 db-card__textarea-container my-2 feedback_green">
                                <textarea id="${id}"
                                          placeholder="FEEDBACK..."
                                          class="db-form-control db-form-control--textarea post_feedback_textarea_button feedback_revision_button"
                                          name="feedback"></textarea>
                                <div class="db-card__status">
                                    <button class="grey_button db-button db-button--actions db-button--round mr-2"
                                            t-att-data-id="${id}" id="${grey_id}"
                                            groups="social.group_social_manager">
                                        <i class="fa fa-check"></i>
                                    </button>
                                    <button class="green_button db-button db-button--actions db-button--round mr-2"
                                            id="${green_id}">
                                        <i class="fa fa-check"></i>
                                    </button>
                                    <div class="revision_button db-card__status-text mr-2"
                                         id="${revision_id}">
                                        Revision Done
                                    </div>
                                    <div class="revision_progress_button db-card__status mr-2" groups="!social.group_social_manager"
                                         id="${progress_id}">
                                        Revision in progress
                                    </div>
                                </div>
                            </div>
                            <i class="delete_post_button  fa fa-trash" style="margin-top: -208px; color: #AAA7A9;"
                                   t-att-id="${delete_post_id}"></i>
                        </div>
                    </div>
                    </div>
                    </div>


                      `);
                      }
       if ( $('.last_post')[0]){
            $('.last_post')[0].insertAdjacentHTML('beforebegin',
                `<div class="col-sm-12 col md-12 dashboard-table">
                <div class="col-md-12 red-border" id="new_row">
                <div t-att-id="${post_button}">
                        <div class="db-card new_post_border" id="${id}">
                            <div class="d-flex justify-content-center align-items-center px-4 my-2">
                                <button class="red_button db-button db-button--actions db-button--round mr-2"
                                        id="${red_id}">
                                    <i class="fa fa-check"></i>
                                </button>
                                <button class="black_button db-button db-button--actions db-button--round"
                                        id="${black_id}">
                                    <i class="fa fa-times db-button__icons"></i>
                                </button>

                            </div>
                            <div class="add_image sub-table-2 my-2">
                                <div class="form-input">
                                    <div class="preview">
                                        <a href="#" class="db-card__image-link image_zoom_button"
                                           data-db-user-image="/dr_social_website/static/src/img/user.png"
                                           data-db-description="${description_id}">

                                            <img id="${preview_id}"/>
                                        </a>
                                    </div>
                                    <div class="upload_view"
                                         id="${upload_id}">
                                        <label for="${image_id}">
                                            <i class="fa fa-upload upload_button"></i>
                                        </label>

                                        <input type="file" id="${image_id}" accept="image/*"
                                               class="post_uploded_image_button"/>
                                    </div>
                                </div>
                                <i class="delete_image_button delete_button_post fa fa-trash"
                                                       id="${delete_image_id}"></i>
                                <i class="delete_upload_button delete_button_post fa fa-trash"
                                                       id="${delete_upload_id}"></i>
                                <i class="search_upload_button search_button_post fa fa-search"
                                               id="${search_upload_id}"></i>
                            </div>

                            <div class="ml-4 db-card__textarea-container my-2">
                                <textarea class="db-form-control db-form-control--textarea post_message_textarea_button text-overflow"
                                        id="${chartdiv_id}" placeholder="MESSAGE..."
                                        name="message" style="overflow:hidden"></textarea>
                                <a href="#" class="toggle-view seeMore more-text"
                                   id="${more_id}">
                                    more...
                                </a>
                                <a href="#" class="toggle-view d-none seeLess more-text">
                                    less...
                                </a>
                            </div>
                            <div class="container justify-content-center align-items-center px-4 my-2">
                                <div class="row my-5">
                                    <div class="col-4 mx-auto">
                                        <div class="db-datepicker-group">
                                            <input type="text"
                                                   class="db-datepicker dateTimePicker_button date_button"/>
                                            <i class="fa fa-chevron-down db-datepicker-group__icon"></i>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="ml-3 db-card__textarea-container my-2 feedback_green">
                                <textarea id="${id}"
                                          placeholder="FEEDBACK..."
                                          class="db-form-control db-form-control--textarea post_feedback_textarea_button feedback_revision_button"
                                          name="feedback"></textarea>
                                <div class="db-card__status">
                                    <button class="grey_button db-button db-button--actions db-button--round mr-2"
                                            t-att-data-id="${id}" id="${grey_id}"
                                            groups="social.group_social_manager">
                                        <i class="fa fa-check"></i>
                                    </button>
                                    <button class="green_button db-button db-button--actions db-button--round mr-2"
                                            id="${green_id}">
                                        <i class="fa fa-check"></i>
                                    </button>
                                    <div class="revision_button db-card__status-text mr-2"
                                         id="${revision_id}">
                                        Revision Done
                                    </div>
                                    <div class="revision_progress_button db-card__status mr-2" groups="!social.group_social_manager"
                                         id="${progress_id}">
                                        Revision in progress
                                    </div>
                                </div>
                            </div>
                            <i class="delete_post_button  fa fa-trash" style="margin-top: -208px; color: #AAA7A9;"
                                   t-att-id="${delete_post_id}"></i>
                        </div>
                    </div>
                    </div>
                    </div>
                      `);
                      }

                $("#"+revision_id).hide();
                    $(".revision_progress_button").hide();
                    $(".search_upload_button").hide();
                    $(".delete_upload_button").hide();

//                $(".show_less").hide();
                $('#'+green_id).hide();
                $('#'+more_id).hide()
//                $('#'+more_zoom).hide()
                 $('#' + delete_image_id).hide();
                  var table_1 = $('#'+ id)
                 console.log('target',table_1)
                 table_1[0].style.border = '2px solid #ffb914';
                 $('.top-text-org').show()
                 $('.dateTimePicker_button').datetimepicker({
                        format: 'h:mm A D MMMM YYYY',
//<!--                        defaultDate: new Date()-->
                        });

                var client_search = $('.client_selection')[0].attributes.data.value;
                console.log('client_search',client_search,this.res_model,$('.client_selection'),$('.client_selection')[0].attributes.data.value)
            this._rpc({
            model: 'social.post',
            method: 'new_post_create',
            args: [ , client_search],
        }).then(function(result){})

    },
    _client_selection:function(e){
        e.preventDefault();
        console.log('kksdkdskkafuyyrjjey',e,e.target.value)
        var client_name = e.target.value
        $('.client_form').submit()
    },
    _client_approval:function(e){
        e.preventDefault();
        console.log('kkkkkkkkkkkkkkk',e)
        var client_search = $('.client_selection').val();
         ajax.jsonRpc('/client_approval', 'call', {'client_name': client_search
         }).then(function (data) {

               });


//        console.log('kksdkdskkafuyyrjjey',e,e.target.value)
//        var client_name = e.target.value
//        $('.client_form').submit()
    },
    _grey:function(e){
        e.preventDefault();
        console.log('kksdkdskkafuyyrjjey',e)
        var id = e.currentTarget.dataset.id
        var green = 'green_' + String(id);
        var grey = 'grey_' + String(id);
        var progress = 'progress_' + String(id);
        $('#'+ green).show();
        $('#'+grey).hide();
        $('#'+progress).hide();
        var value = 'revision_'+ String(e.currentTarget.dataset.id);
        $('#'+ value).show();
        this._rpc({
            model: 'social.post',
            method: 'write',
            args: [[parseInt(id)], {revision_button: true, revision_progress:false}],
        }).then(function(result){})
    },
    _grey_button:function(e){
        e.preventDefault();
        var id = e.currentTarget.attributes[1].nodeValue
        var green = 'green_button_' + String(id);
        var progress = 'progress_button_' + String(id);
        var grey = 'grey_button_' + String(id);
        $('#'+ green).show();
        $('#'+grey).hide();
        $('#'+progress).hide();
        var revision = 'revision_button_'+ String(id);
        $('#'+ revision).show();
                        console.log('kksdkdskkafuyyrjjey',e.currentTarget.attributes[1].nodeValue,green,grey,revision)

        this._rpc({
            model: 'social.post',
            method: 'write',
            args: [[parseInt(id)], {revision_button: true, revision_progress:false}],
        }).then(function(result){})
    },
    _toggle_view:function(e){
        e.preventDefault();
        let targetTextArea = e.target.parentElement.children[0];
        let seeMore = e.target.parentElement.children[1];
        let seeLess = e.target.parentElement.children[2];
        if (e.target.classList.contains('seeMore')) {
            // Select target textarea
            // Set height according to the content size
            targetTextArea.style.height = targetTextArea.scrollHeight + "px";
            // Hide more label
            e.target.classList.add('d-none');
            // Show less label
            seeLess.classList.remove('d-none');
        } else {
            targetTextArea.style.height = "130px";
            // Hide less label
            e.target.classList.add('d-none');
            // Show more label
            seeMore.classList.remove('d-none');
        }
    },
    _load_feedback:function(ev){
        ev.stopPropagation();
        var id = $(ev.target).data('id');
        var text = $(ev.target).val();
        var session = require('web.session');
        var user = session.user_id
        console.log('rrrrrr',session)
        var progress = 'progress_' + String(id);
//        var revision_button = 'grey_' + String(id);
        console.log('eeeee',document.getElementById(progress))
        setTimeout(function () {
                        $('#'+progress).show();
                    }, 3600000);
//        $('#'+revision_button).hide()
        this._rpc({
                model: 'social.post',
                method: 'load_feedback',
                args: [,parseInt(id), text, user],

            }).then(function(result){
        });
//        this._rpc({
//                model: 'social.post',
//                method: 'write',
//                args: [[parseInt(id)], {feedback:text, client_id:user, revision_progress:true}],
//
//            }).then(function(result){
//        });
    },
    _load_feedback_button:function(ev){
        ev.stopPropagation();
        var id = ev.target.id;
        var text = $(ev.target).val();
        var session = require('web.session');
        var user = session.user_id
        var progress = 'progress_button_' + String(id);
        setTimeout(function () {
                        $('#'+progress).show();
                    }, 3600000);
       this._rpc({
                model: 'social.post',
                method: 'load_feedback',
                args: [,parseInt(id), text, user],

            }).then(function(result){
        });
    },
    _feedback_revision:function(ev){
        ev.stopPropagation();
        var id = $(ev.target).data('id');
        var revision_button = $('.grey')
        var revision_text = $('.revision')
        var value = 'revision_'+ id;
        $('#'+ value).hide();
        var green = 'green_'+ String(id);
        $('#'+ green).hide();
         var grey = 'grey_' + String(id);
        $('#'+grey).show();
//        var progress = 'progress_' + String(id);
//        console.log('hkkk',document.getElementById(progress))
//        setTimeout(function () {
//                        document.getElementById(progress).classList.toggle('d-none');
//                    }, 3600);
         this._rpc({
            model: 'social.post',
            method: 'write',
            args: [[parseInt(id)], {revision_button: false}],

         }).then(function(result){})
    },
    _feedback_revision_button:function(ev){
        ev.stopPropagation();
        var id = ev.target.id;
        var revision_button = $('.grey_button')
        var revision_text = $('.revision_button')
        var value = 'revision_button_'+ id;
        $('#'+ value).hide();
        var green = 'green_button_'+ String(id);
        $('#'+ green).hide();
         var grey = 'grey_button_' + String(id);
        $('#'+grey).show();
         this._rpc({
            model: 'social.post',
            method: 'write',
            args: [[parseInt(id)], {revision_button: false}],

         }).then(function(result){})
    },

    _load_message:function(ev){
        var id = ev.target.offsetParent.dataset.id;
        var message = $(ev.target).val();
        this._rpc({
                model: 'social.post',
                method: 'write',
                args: [[parseInt(id)], {message:message}],

            }).then(function(result){
                console.log("result",result);
                    var more_id = 'more_'+ String(id);
                    if (ev.target.scrollHeight > 130) {
                       $('#'+more_id).show()
                    }
            });
    },

    _load_message_button:function(ev){
        var id = ev.currentTarget.offsetParent.id;
            console.log('jjj',ev,'hh',id)

        var message = $(ev.target).val();
        this._rpc({
                model: 'social.post',
                method: 'write',
                args: [[parseInt(id)], {message:message}],

            }).then(function(result){
                console.log("result",result);
                    var more_id = 'more_id_'+ String(id);
                    if (ev.target.scrollHeight > 130) {
                       $('#'+more_id).show()
                    }
            });
    },
    _load_uploaded_image:function(ev){
        ev.stopPropagation();
        var post_id = 'preview_' + String(ev.target.id);
        var image_id = ev.target.id;
        if(ev.target.files.length > 0){
            var src = URL.createObjectURL(ev.target.files[0]);
            var preview = document.getElementById(post_id);
            preview.src = src;
            preview.style.display = "block";
            var delete_upload = 'delete_upload_' + String(ev.target.id);
             $('#'+delete_upload).show()
             var search_upload = 'search_upload_' + String(image_id);
            $('#'+search_upload).show()
        }

       var self = this
       var id = $(ev.target).data('id');
       var image = ev.target.files;
       for (let i = 0; i < image.length; i++) {
           image = image[i]
           var name = image.name
           var reader = new FileReader();
           reader.readAsDataURL(image);
           reader.onload = function(ev) {
           self._rpc({
                model: 'social.post',
                method: 'image_path',
                args: [ ,parseInt(id),name,ev.target.result],

            }).then(function(result){
            });
            }
       }
    },
    _load_uploaded_image_button:function(ev){
        ev.stopPropagation();
        var id = ev.target.parentNode.offsetParent.id
        var post_id = 'preview_button_' + String(id);
            console.log(ev,'dddddddddddd',post_id,document.getElementById(post_id))

//        var image_id = ev.target.id;
        if(ev.target.files.length > 0){
            var src = URL.createObjectURL(ev.target.files[0]);
            var preview = document.getElementById(post_id);
            preview.src = src;
            preview.style.display = "block";
            var delete_upload = 'delete_upload_button_' + String(id);
            $('#' + delete_upload).show();
//            var upload = document.getElementById(delete_upload);
//            upload.classList.toggle("d-none");
            var search_upload = 'search_upload_button_' + String(id);
            $('#' + search_upload).show();
//            var search_icon = document.getElementById(search_upload);
//            search_icon.classList.toggle("d-none");
        }

       var self = this
//       var id = ev.target.id;
       var image = ev.target.files;
       for (let i = 0; i < image.length; i++) {
           image = image[i]
           var name = image.name
           var reader = new FileReader();
           reader.readAsDataURL(image);
           reader.onload = function(ev) {
           self._rpc({
                model: 'social.post',
                method: 'image_path',
                args: [ ,parseInt(id),name,ev.target.result],

            }).then(function(result){
            });
            }
       }
    },

    _delete_image:function(ev){
        console.log(ev,'delete_image',ev, ev.currentTarget.offsetParent.dataset.id)
        var id = ev.currentTarget.offsetParent.dataset.id;
        var image_id = 'image_id_' + String(id)
        var upload_id = 'upload_id_' + String(id)
        var image = $('#'+ image_id)[0].src
        this._rpc({
            model: 'social.post',
            method: 'delete_image',
            args: [ ,parseInt(id),image],

        }).then(function(result){
              var element = document.getElementById(image_id);
              element.classList.add('d-none');
              var upload = document.getElementById(upload_id);
              upload.classList.toggle("d-none");
              var delete_image = 'delete_' + String(id)
              $('#' + delete_image).hide();
              var search_image = 'search_' + String(id)
              $('#' + search_image).hide();
        });
    },
    _delete_upload:function(ev){
         var image = $('.post_uploded_image')
//         console.log('delete_upl,oad',ev.currentTarget.offsetParent, 'eeee', ev, ev.parentElement.attributes[1].nodeValue)
         var id = ev.currentTarget.offsetParent.dataset.id;
         var post_id = 'preview_' + String(id);
         for (let i = 0; i < image.length; i++) {
            if(image[i].files.length > 0){
                var src = URL.createObjectURL(image[i].files[0]);
                var preview = document.getElementById(post_id);
                preview.src = src;
                preview.style.display = "none"
                var delete_upload = 'delete_upload_' + String(id)
                var search_upload = 'search_upload_' + String(id)
                $('#' + delete_upload).hide();
                $('#' + search_upload).hide();
                this._rpc({
                model: 'social.post',
                method: 'delete_upload',
                args: [ ,parseInt(id)],

                 }).then(function(result){
                 });
            }
         }
    },
    _delete_upload_button:function(ev){
    console.log(ev,'delete')
         var image = $('.post_uploded_image_button')
         var id = ev.currentTarget.offsetParent.attributes[1].nodeValue;
         var post_id = 'preview_button_' + String(id);
         for (let i = 0; i < image.length; i++) {
            if(image[i].files.length > 0){
                var src = URL.createObjectURL(image[i].files[0]);
                var preview = document.getElementById(post_id);
                preview.src = src;
                preview.style.display = "none"
                var delete_upload = 'delete_upload_button_' + String(id)
                var search_upload = 'search_upload_button_' + String(id)
                $('#' + delete_upload).hide();
                $('#' + search_upload).hide();
                this._rpc({
                model: 'social.post',
                method: 'delete_upload',
                args: [ ,parseInt(id)],

                 }).then(function(result){
                 });
            }
         }
    },
//
   _date_input:function(ev){
   console.log('zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz',ev,'lll',ev.target.offsetParent.offsetParent.offsetParent.id)
        var id = ev.target.offsetParent.offsetParent.offsetParent.id;
        var input_date_time = $(ev.target).val()
        console.log(id,'idddddddddddddd')
//        var date = ev.target.date
        this._rpc({
            model: 'social.post',
            method: 'date_time_change',
            args: [,parseInt(id),input_date_time],

        }).then(function(result){
            console.log("result",result);
        });
    },

    _image_zoom:function(e){
    console.log(e,'lllllllllllll')
        var post_id = e.currentTarget.offsetParent.dataset.id;

        var id = 'preview_' + String(post_id);
        e.preventDefault();
        const target_src = e.currentTarget.dataset.dbTarget;
        const message = $('#chartdiv_'+post_id).val();
        const userImage = e.currentTarget.dataset.dbUserImage;
        $('.db-dialog__image').attr('src', target_src);
        $('.db-dialog__user-image').attr('src', userImage);
        $('.db-overlay, .db-dialog').toggleClass('d-none');
        $('body').css('overflow-y', 'hidden');
        var description = document.getElementsByClassName('description_message');
        description[0].innerText = message;
        console.log('$(.db-dialog__description)',description)
//        var more_id = 'more_zoom_'+ String(post_id)

        this._rpc({
                model: 'social.post',
                method: 'zoom_image',
                args: [, parseInt(post_id)],

        }).then(function(result){
            var target_id = '/web/image/ir.attachment/'+String(result[0][0])+'/datas'
            console.log("result",result,target_id);
            $('.db-dialog__image').attr('src', target_id);
//             if(description[0].scrollHeight < 130) {
//        console.log('//////////////////////////////////',more_id,'kkk',description[0].scrollHeight,'ll',$('#'+more_id))
//              $('#'+more_id).hide()
//        }
        });
    },

    _image_zoom_button:function(e){
    console.log(e,'lllllllllllllllllllll',e.currentTarget.offsetParent.attributes[1].nodeValue)
        var post_id = e.currentTarget.offsetParent.attributes[1].nodeValue;
        var id = 'preview_button_' + String(post_id);
        var chartdiv = 'chartdiv_button_' + String(post_id);
        console.log('chartdiv',chartdiv)
        e.preventDefault();
        const target_src = e.currentTarget.dataset.dbTarget;
        const message = $('#'+ chartdiv).val();
         console.log('message',message)
        const userImage = e.currentTarget.dataset.dbUserImage;
        $('.db-dialog__image').attr('src', target_src);
        $('.db-dialog__user-image').attr('src', userImage);
        $('.db-overlay, .db-dialog').toggleClass('d-none');
        $('body').css('overflow-y', 'hidden');
        var description = document.getElementsByClassName('description_message');
        description[0].innerText = message;
//        console.log('$(.db-dialog__description)',description)
        this._rpc({
                model: 'social.post',
                method: 'zoom_image',
                args: [, parseInt(post_id)],

        }).then(function(result){
            var target_id = '/web/image/ir.attachment/'+String(result[0][0])+'/datas'
            console.log("result",result,target_id);
            $('.db-dialog__image').attr('src', target_id);

        });
    },

    _value_date_time:function(ev){
        ev.stopPropagation();
        console.log(ev,'daaaaaaaaaaaaaaa')
        var id = ev.target.id;
        var input_date_time = $(ev.target).val()
        console.log(id,'idddddddddddddd')
//        var date = ev.target.date
        this._rpc({
            model: 'social.post',
            method: 'date_time_change',
            args: [,parseInt(id),input_date_time],

        }).then(function(result){
            console.log("result",result);
        });
    },

    _approve_button: function (ev) {
        ev.stopPropagation();
        var id = ev.currentTarget.offsetParent.dataset.id
        this._rpc({
            model: 'social.post',
            method: 'approve_text',
            args: [ ,parseInt(id)],

        }).then(function(result){
            console.log("result",result);
            if (result == 'Hide text'){
                $(".top-text-org").hide();
            }
        });
    },

     _not_approved_button: function (ev) {
        var posts = $('.dashboard-table')
        var id = ev.currentTarget.offsetParent.dataset.id
        this._rpc({
            model: 'social.post',
            method: 'not_approve_text',
            args: [ ,parseInt(id)],

        }).then(function(result){
            console.log("result",result);
            if (result == 'Hide text'){
                 $(".top-text-org").hide();
            }
        });
    },
    _red_button: function (ev) {
    console.log(ev,'rrrrrrrrrrrrrrrrrrrrrrrr',ev.currentTarget.offsetParent.id)
        var id = ev.currentTarget.offsetParent.id
        ev.currentTarget.nextElementSibling.style['background-color']= '#AAA7A9'
        ev.currentTarget.offsetParent.style.border = 'none';
        ev.currentTarget.style['background-color'] = '#00F5BE';
        this._rpc({
            model: 'social.post',
            method: 'approve_text',
            args: [ ,parseInt(id)],

        }).then(function(result){
            console.log("result",result);
            if (result == 'Hide text'){
                $(".top-text-org").hide();
            }
        });
    },


    _black_button: function (ev) {
        var posts = $('.dashboard-table')
        console.log(ev,'bbbbbbbbbbbbbbbbbbbbb',ev.currentTarget.offsetParent.id)
        var id = ev.currentTarget.offsetParent.id
        ev.currentTarget.offsetParent.style.border = '2px solid red'
        ev.currentTarget.style['background-color']='red';
        ev.currentTarget.previousElementSibling.style['background-color']= '#AAA7A9';
        this._rpc({
            model: 'social.post',
            method: 'not_approve_text',
            args: [ ,parseInt(id)],

        }).then(function(result){
            console.log("result",result);
            if (result == 'Hide text'){
                 $(".top-text-org").hide();
            }
        });
    },
    _delete_post: function (ev) {
        console.log('aaaaaaaaaaaaaaaaa',ev,ev.target.offsetParent.dataset.id)
        var id = ev.target.offsetParent.dataset.id
        var post ='post_id_'+ String(id)
        $('#'+ post).hide()
        this._rpc({
            model: 'social.post',
            method: 'delete_posts',
            args: [ ,parseInt(id)],

        }).then(function(result){

        });
    },
    _delete_post_button: function (ev) {
        var id = ev.target.offsetParent.id
        var post = String(id)
                console.log('aaaaaaaaaaaaaaaaa',ev,post)

        $('#'+ post).hide()
        this._rpc({
            model: 'social.post',
            method: 'delete_posts',
            args: [ ,parseInt(id)],

        }).then(function(result){

        });
    },

})
//publicWidget.registry.websiteImageZoom = publicWidget.Widget.extend({
//    selector:'.image_insta',
////    xmlDependencies: ['/dr_social_website/static/src/xml/search.xml'],
//    events: {
//        'input .search_value': '_onInput',
//        'focusout': '_onFocusOut',
//        'keydown .search-query': '_onKeydown',
//        'search .search-query': '_onSearch',
//    },
//    async _fetch() {
//        const res = await this._rpc({
//            route: '/content_calendar',
//            params: {
////                'search_type': this.searchType,
//                'term': this.$input.val(),
////                'order': this.order,
////                'limit': this.limit,
////                'max_nb_chars': Math.round(Math.max(this.autocompleteMinWidth, parseInt(this.$el.width())) * 0.22),
////                'options': this.options,
//            },
//        });
////        const fieldNames = [
////            'name',
////            'description',
////            'extra_link',
////            'detail',
////            'detail_strike',
////            'detail_extra',
////        ];
////        res.results.forEach(record => {
////            for (const fieldName of fieldNames) {
////                if (record[fieldName]) {
////                    if (typeof record[fieldName] === "object") {
////                        for (const fieldKey of Object.keys(record[fieldName])) {
////                            record[fieldName][fieldKey] = Markup(record[fieldName][fieldKey]);
////                        }
////                    } else {
////                        record[fieldName] = Markup(record[fieldName]);
////                    }
////                }
////            }
////        });
//        return res;
//    },
//
//    _onInput: function () {
//        if (!this.limit) {
//            return;
//        }
//        if (this.searchType === 'all' && !this.$input.val().trim().length) {
//            this._render();
//        } else {
//            this._dp.add(this._fetch()).then(this._render.bind(this));
//        }
//    },
//    /**
//     * @private
//     */
//    _onFocusOut: function () {
//        if (!this.$el.has(document.activeElement).length) {
//            this._render();
//        }
//    },
//    /**
//     * @private
//     */
//    _onKeydown: function (ev) {
//        switch (ev.which) {
//            case $.ui.keyCode.ESCAPE:
//                this._render();
//                break;
//            case $.ui.keyCode.UP:
//            case $.ui.keyCode.DOWN:
//                ev.preventDefault();
//                if (this.$menu) {
//                    let $element = ev.which === $.ui.keyCode.UP ? this.$menu.children().last() : this.$menu.children().first();
//                    $element.focus();
//                }
//                break;
//            case $.ui.keyCode.ENTER:
//                this.limit = 0; // prevent autocomplete
//                break;
//        }
//    },
//    /**
//     * @private
//     */
//    _onSearch: function (ev) {
//        if (this.$input[0].value) { // actual search
//            this.limit = 0; // prevent autocomplete
//        } else { // clear button clicked
//            this._render(); // remove existing suggestions
//            ev.preventDefault();
//            if (!this.wasEmpty) {
//                this.limit = 0; // prevent autocomplete
//                const form = this.$('.o_search_order_by').parents('form');
//                form.submit();
//            }
//        }
//    },
//
//
////         _toggle_view_zoom:function(e){
////        e.preventDefault();
////        console.log('................................................',e)
////        let targetTextArea = e.target.parentElement.children[1];
////        let seeMore = e.target.parentElement.children[2];
////        let seeLess = e.target.parentElement.children[3];
////        if (e.target.classList.contains('seeMore')) {
////            // Select target textarea
////            // Set height according to the content size
////            targetTextArea.style.height = targetTextArea.scrollHeight + "px";
////            // Hide more label
////            e.target.classList.add('d-none');
////            // Show less label
////            seeLess.classList.remove('d-none');
////        } else {
////            targetTextArea.style.height = "100px";
////            // Hide less label
////            e.target.classList.add('d-none');
////            // Show more label
////            seeMore.classList.remove('d-none');
////        }
////    },
//})
publicWidget.registry.websiteEventSearchSponsorss = publicWidget.Widget.extend({

 selector:'.db-revision-lists',
 events: {
//        'click #scheduleListButton': '_load_feedback',
        'click .delete_notification': '_load_client_name',
        'click .db-revision-list__profile-update': '_load_client_names',
    },



    init: function(parent, context) {
        this.action_id = context['id'];
        this._super(parent, context);
    },

    _load_client_names:function(ev){
        $('.db-revision-list__item--active').removeClass("db-revision-list__item--active");
//        var id = $('.db-schedule-input-container__bullet');
//        var day = $('.focused');
//        var month = $('.view-switch');
//
//        self.client_name = []
//        var date_day = day[0].textContent
//        var date_month = month[0].innerHTML
//        var date_object =  date_day + ' ' +date_month
//
//        for (var i = 0 ; i < id.length ; i++) {
//            self.client_name = id[i].parentElement.outerText
//        }
    },

    _load_client_name:function(ev){
        var delete_notification = $('.delete_notification');
        console.log('delete_notification', delete_notification)
        $('.db-revision-list__item--active').hide()
//        var id = $('.db-schedule-input-container__bullet');
//        var day = $('.focused');
//        var month = $('.view-switch');
//
//        self.client_name = []
//        var date_day = day[0].textContent
//        var date_month = month[0].innerHTML
//        var date_object =  date_day + ' ' +date_month
//
//        for (var i = 0 ; i < id.length ; i++) {
//            self.client_name = id[i].parentElement.outerText
//        }
    },

});
});






