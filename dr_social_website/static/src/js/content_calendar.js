odoo.define('dr_social_website.content_calendar', function (require) {
"use strict";
//console.log('lllllllllllllll')
const publicWidget = require('web.public.widget');
var rpc = require('web.rpc');



 $(document).ready(function (ev) {
// console.log('lllllllllllllllllllllllllllllllllllllllllllllllllll', ev)
    $(".revision").hide();
    $(".show_less").hide();
    $(".green").hide();
//    $(".grey").hide();
//    $(".seeMore").hide();
    $('.o_footer').addClass('header_hide')
//    $('.o_header_standard').addClass('header_hide')

    var posts = $('.dashboard-table')
    var table_1 = $('.db-card')
    var image_upload = $('.add_image')
    var text = $('.text-overflow');
    var feedback = $('.feedback_green');
 for (let i = 0; i < text.length; i++) {
//    var id = text[i].offsetParent.dataset.id
//       console.log(id,'kssssssssssssssssssssssssssss')
//       var chartdiv = 'chartdiv_' + String(post_id)

            rpc.query({
                model: 'social.post',
                method: 'message_content',
                args: [,parseInt(text[i].offsetParent.dataset.id)],

            }).then(function(result){
//            text.innerHtml = result
        var chartdiv = 'chartdiv_' + String(text[i].offsetParent.dataset.id)
        var description = document.getElementById(chartdiv);

        description.innerHTML = result;
//         console.log('rrrrrrrrrr',description,chartdiv)
          if (!(text[i].scrollHeight > 130)) {
          var more_id = 'more_'+ String(text[i].offsetParent.dataset.id);
//        console.log(more_id,text[i].scrollHeight)
           $('#'+more_id).hide()
        }

            });

}

//    console.log(posts,'lllllllllllll',$('.red'))
//    console.log(posts.value,'hhhhhhhhhhh')
    for (let i = 0; i < posts.length; i++) {
//    console.log($('.red')[i].style.background-color,'ooooooooo')
        if (posts[i].attributes.value.value === 'posted') {
//        console.log(posts[i].style.border = 'red','posts[i].style')
            posts[i].style.pointerEvents = 'none';
            posts[i].style.color = '#bdbfb7';
//           console.log($('.red'),red)
//            posts[i].style.border = '2px solid red';#bdbfb7;
            $('.red')[i].style['background-color']='#bdbfb7';
            $('.black')[i].style['background-color']='#bdbfb7';
            $('.value_time')[i].style['color']='#bdbfb7';
            $('.date_default')[i].style['color']='#bdbfb7';
            $('.grey')[i].style['background-color']='#bdbfb7';
            $('.seeMore')[i].style['color']='#bdbfb7';
//            console.log(i,'lllllllllllllllllllllllllllllllll')
            $('.add_image')[i].style['opacity']='0.3';
//            $('.form-input').style['background-color']='#bdbfb7';
//            $('.form-input').css('background-color', '#bdbfb7');
//            $('.value_time').css('color', '#bdbfb7');

        }
            console.log(feedback,'feeeeeeed',feedback[i].attributes.value)

        if (feedback[i].attributes.value){
            var revision = 'revision_' +String(feedback[i].firstElementChild.id)
            var grey = 'grey_' +String(feedback[i].firstElementChild.id)
            var green = 'green_' +String(feedback[i].firstElementChild.id)
            $("#"+green).show();
            $("#"+revision).show();
            $("#"+grey).hide();
            console.log('hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh',feedback[i].firstElementChild.id)
        }
        }
        for (let i = 0; i < table_1.length; i++) {
//    console.log(table_1[i].attributes.value.value,'ppppppppppppppp')
        if (table_1[i].attributes.value.value === 'draft') {
            table_1[i].style.border = '2px solid #ffb914';

        }
        if (table_1[i].attributes.value.value === 'not_approved') {
            table_1[i].style.border = '2px solid red';
            $('.black')[i].style['background-color']='red';

        }
        if (table_1[i].attributes.value.value === 'scheduled') {
            $('.red')[i].style['background-color']='rgb(33, 210, 151)';

        }
//         if (posts[i].attributes.value.value === 'draft') {
////        console.log(posts[i].style.border = 'red','posts[i].style')
//            posts[i].style.border = '2px solid red';
////            posts[i].style.border = '2px solid red';
//
//        }
    }
    for (let i = 0; i < image_upload.length; i++) {
//        console.log('ppppppppppppppp',image_upload[i],image_upload[i].attributes)
        if (!('value' in image_upload[i].attributes)) {
         var id = image_upload[i].dataset.id
         var upload_id = 'upload_id_' + String(id)
//            table_1[i].style.border = '2px solid #ffb914';
//              console.log('kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk')
              var upload = document.getElementById(upload_id);
//              console.log(upload_id,upload,'iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii')

                upload.classList.toggle("d-none");
                var delete_image = 'delete_' + String(id)
                $('#' + delete_image).hide();

        }
}
 })



//    console.log(document.getElementsByClassName("def_date").value,'lllllllllllllll')
//    document.getE("date_input1").value = "2022-06-15";




//$(document).on("focusout", ".value_time", function(event){
//        console.log('ooooooooooooooooooooooooooooooooooooooooo',event.target.value)
//        var id = $(event.target).data('id');
//        var time = $(event.target).val()
////        console.log(date);
//        this._rpc({
//                model: 'social.post',
//                method: 'write',
//                args: [[parseInt(id)], {post_method:'scheduled', scheduled_date:time}],
//
//            }).then(function(result){
//                console.log("result",result);
//            });
//})
//$(document).on("focusout", ".date_input", function(event){
//        console.log('ooooooooooooooooooooooooooooooooooooooooo',event.target.value)
//        var id = $(event.target).data('id');
//        var date = $(event.target).val()
////        console.log(date);
//        this._rpc({
//                model: 'social.post',
//                method: 'write',
//                args: [[parseInt(id)], {post_method:'scheduled', scheduled_date:date}],
//
//            }).then(function(result){
//                console.log("result",result);
//            });
//})
//$(document).ready(function() {
//console.log("Date fields: ", document.getElementsByClassName("date"));
//console.log("Date fields: ", $(".date"));
//        $('.date').on('click', function() {
//            console.log("Date field clicked....");
//            $('.date').calendar({
//            type: 'date'
//            });
////            $('#time').calendar({
////            type: 'time'
////            });
//        });
//
//        $('#test').on('click', function() {
//            console.log("Date field clicked....");
//            $('#test').calendar({
//            type: 'date'
//            });
////            $('#time').calendar({
////            type: 'time'
////            });
//        });
//
//         });

publicWidget.registry.websiteEventSearchSponsor = publicWidget.Widget.extend({

 selector:'.dashboard-table',
 events: {
        'click .grey': '_grey',
        'change .post_feedback_textarea': '_load_feedback',
        'change .post_message_textarea': '_load_message',
        'change .post_uploded_image': '_load_uploaded_image',
//        'change .approve_text': '_approve_text',
        'click .approve_button': '_approve_button',

        'click .feedback_revision': '_feedback_revision',
        'click .not_approved_button': '_not_approved_button',
        'click .delete_image': '_delete_image',
        'click .delete_upload': '_delete_upload',
//        'click .show_less': '_show_less',
        'click .image_zoom': '_image_zoom',
//        'click #dialogClose': '_dialogClose',
        'blur .date_input1': '_date_input',
        'blur .value_time': '_value_time',
    },
    _grey:function(e){
        e.preventDefault();
        var id = e.currentTarget.dataset.id
        var green = 'green_' + String(id);
        var grey = 'grey_' + String(id);
        $('#'+ green).show();
        $('#'+grey).hide();
//<!--                                            $(this).css('background-color', '#21d297');-->
        var value = 'revision_'+ String(e.currentTarget.dataset.id);
        $('#'+ value).show();
                console.log(e,'dddddddddddddddddddddddddd',id)

        this._rpc({
            model: 'social.post',
            method: 'write',
            args: [[parseInt(id)], {revision_button: true}],

                }).then(function(result){})
    },
        _load_feedback:function(ev){
        ev.stopPropagation();
        var id = $(ev.target).data('id');
        var text = $(ev.target).val();
        console.log(id,'oooooooooooooooo')
//        var revision_button = $('.grey')
//        var revision_text = $('.revision')
//        var value = 'revision_'+ id;
//        $('#'+ value).hide();
//        revision_button.css('background-color', '#625454');
////        console.log(text,this,revision_text);
        this._rpc({
                model: 'social.post',
                method: 'write',
                args: [[parseInt(id)], {feedback:text}],

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
         this._rpc({
            model: 'social.post',
            method: 'write',
            args: [[parseInt(id)], {revision_button: false}],

                }).then(function(result){})
    },
//        revision_button.css('background-color', '#625454');
//        console.log(text,this,revision_text);


    _load_message:function(ev){
        console.log(ev,'messsssssssss')
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
//                    console.log(post_id,more_id,text[i].scrollHeight)
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
         var upload = document.getElementById(delete_upload);
//         console.log(upload,delete_upload,'iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii')

         upload.classList.toggle("d-none");
//        $('#' + delete_upload).toggle('d-none');
        }

       var self = this
       var id = $(ev.target).data('id');
       var image = ev.target.files;
       for (let i = 0; i < image.length; i++) {
          image = image[i]
          var name = image.name
          var reader = new FileReader();
//           console.log(image,name,ev.target.result)
           reader.readAsDataURL(image);
           reader.onload = function(ev) {
           self._rpc({
                model: 'social.post',
                method: 'image_path',
                args: [ ,parseInt(id),name,ev.target.result],

            }).then(function(result){
//                var post_id = '.test_preview_' + String(image_id);
//                console.log("add_image",post_id);
//                $(post_id).load(window.location.href + " "+post_id);

            });
        }
//        $(".db-card").load(window.location.href + " .db-card");
        }
//                $('#'+ post_id).load(window.location.href + ' #'+ post_id);

//        $("#image_reload").load(location.href + " #image_reload");
//        location.reload()

//        $('.preview').load(window.location.href + ".preview" );
//        this.reload();
//        const img_val= (image) =>
//    image.replace('data:', '').replace(/^.+,/, '');
//        console.log(typeof image,'image')

//        console.log('kkkkkkkkkkk',document.getElementById('attachments'))
//        var attachment1 = document.getElementById('attachments').files[0];
//        if (attachment1){
//        console.log('iiiiiiiiiiiii')
//            var reader = new FileReader();
//            reader.readAsDataURL(attachment1);
//            reader.onload = function(ev)
//    {
//        this._rpc({
////            'w_submission': w_submission,
////            'project_summary_three_phase': project_summary_validation.project_summary_2,
////            'project_summary_single_phase': project_summary_validation.project_summary_1,
//            'attachment': ev.target.result,
////            'attachment_name': attachment1.name,
////            'user_id': session.user_id
//        }).then(function(data){
//            window.location.href = data;
//        });
//    }
//}


    },
//      _show_more:function(ev){
//          var text = $('.text-overflow');
//           console.log('h',ev.delegateTarget.dataset.id)
//          var post_id = ev.delegateTarget.dataset.id
//          var id = 'chartdiv_'+ String(post_id);
//          for (let i = 0; i < text.length; i++) {
//               if (ev.delegateTarget.dataset.id == post_id) {
//                   var h = text[i].scrollHeight;
//
//                   var value = String(h) + 'px'
//                   document.getElementById(id).style.height = value;
//                   $("#less_"+post_id).show();
//                   $("#more_"+post_id).hide();
//}
//}
//    },
     _delete_image:function(ev){
     console.log('lllllllllllllllllllllllllllllllllllllllllllllllllll',ev,ev.target.parentElement.children[1].firstElementChild.dataset.dbTarget,ev.currentTarget.nextElementSibling.dataset.dbTarget)
     var id = ev.delegateTarget.dataset.id
      var image_id = 'image_id_' + String(id)
      var upload_id = 'upload_id_' + String(id)
     var image = $('#'+ image_id)[0].src
//     var image = ev.currentTarget.nextElementSibling.dataset.dbTarget
     this._rpc({
                model: 'social.post',
                method: 'delete_image',
                args: [ ,parseInt(id),image],

            }).then(function(result){
//            var image_class = $('.image_view')
//              if (result == '') {
              var element = document.getElementById(image_id);

              element.classList.add('d-none');
              console.log(upload_id,'llllllllllllllllllllllllllllllllllllllljjjjjjjjjj',document)
              var upload = document.getElementById(upload_id);
              console.log(upload_id,upload,'iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii')

              upload.classList.toggle("d-none");
              var delete_image = 'delete_' + String(id)
              $('#' + delete_image).hide();
//             }
//              else{
//                   var element = document.getElementById(image_id);
//                   element.classList.add('d-none');
//                   var target_id = '/web/image/ir.attachment/'+String(result[0])+'/datas'
//                   console.log("resultttttttttttttttttttt",result,target_id);
//                   $('#'+image_id).attr('src', target_id);
//              }
            });
    },
     _delete_upload:function(ev){
     var image = $('.post_uploded_image')
     console.log('gggggggggggggggggggggggggggg',ev,'pp',image)

     var id = ev.delegateTarget.dataset.id
     var post_id = 'preview_' + String(id);
     for (let i = 0; i < image.length; i++) {
        if(image[i].files.length > 0){
        var src = URL.createObjectURL(image[i].files[0]);
        var preview = document.getElementById(post_id);
        preview.src = src;
        preview.style.display = "none"
        var delete_upload = 'delete_upload_' + String(id)
        $('#' + delete_upload).hide();
        this._rpc({
        model: 'social.post',
        method: 'delete_upload',
        args: [ ,parseInt(id)],

         }).then(function(result){
         });
         }
        }
        },
//     var post_id = 'preview_' + String(id);
////      var image_id = 'image_id_' + String(id)
//      var upload_id = 'upload_id_' + String(id)
//      console.log('post_id',$('#'+post_id),'upload_id',$('#'+upload_id))
//     var image = $('#'+ image_id)[0].src
//     console.log(image[0].src,'pppppppppppppppppppppp')
////     var image = ev.currentTarget.nextElementSibling.dataset.dbTarget
//     this._rpc({
//                model: 'social.post',
//                method: 'delete_upload',
//                args: [ ,parseInt(id),image],
//
//            }).then(function(result){
////            var image_class = $('.image_view')
//              if (result == '') {
//              var element = document.getElementById(image_id);
//
//              element.classList.add('d-none');
//              console.log(upload_id,'llllllllllllllllllllllllllllllllllllllljjjjjjjjjj',document)
//              var upload = document.getElementById(upload_id);
//              console.log(upload_id,upload,'iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii')
//
//              upload.classList.toggle("d-none");
//              var delete_image = 'delete_' + String(id)
//              $('#' + delete_image).hide();
//             }
//              else{
//                   var element = document.getElementById(image_id);
//                   element.classList.add('d-none');
//                   var target_id = '/web/image/ir.attachment/'+String(result[0])+'/datas'
//                   console.log("resultttttttttttttttttttt",result,target_id);
//                   $('#'+image_id).attr('src', target_id);
//              }
//            });

   _date_input:function(ev){
    var id = $(ev.target).data('id');
    var date = $(ev.target).val()
    console.log(date,'ddddddddddddddddddddddddddddd',id);
    this._rpc({
            model: 'social.post',
            method: 'input_date',
//                 method: 'search_read',
            args: [ ,parseInt(id), date],

        }).then(function(result){
            console.log("result",result);
        });
    },

    _image_zoom:function(e){
        var post_id = e.delegateTarget.dataset.id;
        var id = 'preview_' + String(e.target.id);
//        console.log('eeeeeeeeeeeeeeeeeee',e,e.delegateTarget.dataset.id,e.currentTarget.dataset.dbDescription,e.currentTarget.dataset.dbUserImage,e.currentTarget.dataset.dbTarget)
        e.preventDefault();
        console.log('ooooooooooooo',e)
        const target_src = e.currentTarget.dataset.dbTarget;
        const message = $('#chartdiv_'+post_id).val();
        const userImage = e.currentTarget.dataset.dbUserImage;
        console.log("Target src: ", message);

//        $('.db-dialog__description').html(description);

        $('.db-dialog__image').attr('src', target_src);
        $('.db-dialog__user-image').attr('src', userImage);
        $('.db-overlay, .db-dialog').toggleClass('d-none');
        $('body').css('overflow-y', 'hidden');
        var description = document.getElementsByClassName('description_message');
        description[0].innerText = message;
        console.log('$(.db-dialog__description)',description)
        this._rpc({
                model: 'social.post',
                method: 'zoom_image',
//                 method: 'search_read',
                args: [, parseInt(post_id)],

            }).then(function(result){
//                console.log(result,'image',result[0].id)
                var target_id = '/web/image/ir.attachment/'+String(result[0][0])+'/datas'
                console.log("result",result,target_id);
                $('.db-dialog__image').attr('src', target_id);

            });
//            const target_id = $(this).data('db-id');

        },

//    _dialogClose:function(e){
//      console.log('kkkkaaaaa',e)
//        e.preventDefault();
//            $('.db-overlay, .db-dialog').addClass('d-none');
//            $('body').css('overflow-y', 'auto');
//    },
    _value_time:function(ev){
    ev.stopPropagation();
//      console.log('jjjjjjjj',ev)
        var id = $(ev.target).data('id');
        var input_time = $(ev.target).val()
        var date = ev.target.date
//        if (input_time = ' '){
//            console.log('ddddddddddddd')
//            }else {
                this._rpc({
                    model: 'social.post',
                    method: 'time_change',
                    args: [,parseInt(id),input_time],

                }).then(function(result){
                    console.log("result",result);
                });
//            }
    },

    _approve_button: function (ev) {
    ev.stopPropagation();
//    var posts = $('.dashboard-table')
    var id = ev.currentTarget.offsetParent.dataset.id
//    console.log('approveeeeeeeeeee',posts)
//     this._rpc({
//        model: 'social.post',
//        method: 'write',
//        args: [[parseInt(id)], {state:'scheduled'}],
//
//    }).then(function(result){
//        console.log("result",result);
//    });
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
//
//     _approve_text:function(ev){
//     console.log('fffffffffffffffffffffffffffffffffffffffffffffffffff')
//        ev.stopPropagation();
////      console.log('jjjjjjjj',ev)
//        var id = ev.currentTarget.offsetParent.dataset.id;
////        if (input_time = ' '){
////            console.log('ddddddddddddd')
////            }else {
//                this._rpc({
//                    model: 'social.post',
//                    method: 'approve_text',
//                    args: [,parseInt(id)],
//
//                }).then(function(result){
//                    console.log("result",result);
//                });
////            }
//    },

     _not_approved_button: function (ev) {
     var posts = $('.dashboard-table')
     var id = ev.currentTarget.offsetParent.dataset.id
          console.log('not approveeeeeeee',id)

//     this._rpc({
//                model: 'social.post',
//                method: 'write',
//                args: [[parseInt(id)], {state:'not_approved'}],
//
//            }).then(function(result){
//                console.log("result",result);
//            });
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


//    _image_preview: function (ev) {
//         var id = $(ev.target).data('id')
////         this._rpc({
////                    model: 'social.post',
////                    method: 'write',
////                    args: [[parseInt(id)], {image_ids:'not_approved'}],
////
////                }).then(function(result){
////                    console.log("result",result);
////                });
//        },
//        _add_image: function (ev) {
//        console.log('image',$(ev.target).data())
//        }


})
publicWidget.registry.websiteEventSearchSponsorss = publicWidget.Widget.extend({

 selector:'.db-wrapper',
 events: {
//        'click #scheduleListButton': '_load_feedback',
        'click .selected': '_load_client_name',
    },


    willStart: function () {
//        $('.o_header_standard').addClass('header_hide')
//        $('.o_footer').addClass('header_hide')
    let locals_datas = []
    console.log('locals_datas', locals_datas)

    },

    init: function(parent, context) {
        this.action_id = context['id'];
        this._super(parent, context);
            let locals_datas = []

        let inputEl = $('#scheduleListInput');
    let scheduleBtn = $('#scheduleListButton');
    let scheduleListEl = $('.db-schedule-input-container__list');
    let errorEl = $('.db-error');

    /**
     * Change Day of Week name to two letters
     */

    // Update selected DOW
    function selectDOW(i, currISO, dow) {
      let selectedDow = new Date(currISO).getDay();

      // If dow is selected dow
      if (i === selectedDow) {
        dow.classList.add('selected');
      }
    }
    // List of new days of week names
    const DOW_NAMES = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
    // Get day of the week ISO String from selected date
    let currISO = $('.db-schedule-container .day.selected').data('date');
    // Get all the days of the week from the calendar widget
    var dowOld = $('.db-schedule-container .dow');
    // Loop through each existing day of week
    dowOld.each(function (i, dow) {
      // If dow is selected dow
      selectDOW(i, currISO, dow);
      // Replace the text of each day of the week with the new ones
      dow.innerText = DOW_NAMES[i];
    });

    /**
     * Chage DOW Highligh on Date click
     */
    // Listen for clicks in the date field
    $('.db-schedule-container .day').on('click', function (e) {
      // Clear all selected class from DOW
      $('.db-schedule-container .dow').each(function (i, dow) {
        dow.classList.remove('selected');
      })
      // Get day of the week ISO String from selected date
      let currISO = $(this).data('date');

      // Loop through each existing day of week
      dowOld.each(function (i, dow) {
        // If dow is selected dow
        selectDOW(i, currISO, dow);
      });
    });

    /**
    * LOAD VALUES TO SHCEDULE LIST
    * mode = 1: Execute on load only
    */
    function loadLocalData(selectedDate, mode) {
      let localData = JSON.parse(localStorage.getItem(`cal_${selectedDate}`));
      let selectedEl = $('.datepicker-cell.selected');


      // Reset Schedule List
      $(scheduleListEl).html(`
            <li class="db-schedule-input-container__item">
                <div class="db-schedule-input-container__bullet mr-3"></div>
                <input class="db-schedule-input-container__input" id="scheduleListInput">
              </li>
        `);

      if (localData) {
        localData.items.forEach(function (item, i) {
          $(scheduleListEl).append(`
              <li class="db-schedule-input-container__item">
                <div class="db-schedule-input-container__bullet mr-3"></div>
                ${item}
              </li>
      `);

        })
      }
    }
    // Load Dots fore Dates
    $('.db-schedule-container .day').each(function (i, elem) {
      let currentItemDate = elem.dataset.date;
      let currentLocalData = JSON.parse(localStorage.getItem(`cal_${currentItemDate}`));

      // Check if local storage has an item for current date
      if (currentLocalData) {
        currentLocalData.items.forEach(function (item, i) {
          if (i == 0) {
            $(elem).append("<div class='db-schedule-dot-container'><span class='db-schedule-dot'></span></div>");
          } else {
            $('.datepicker-cell.selected .db-schedule-dot-container').append("<span class='db-schedule-dot'></span>");
          }
        })
      };
    })
    // On selecting another date.
    $('.db-schedule-container .day').on('click', function (e) {
      let selectedDate = e.target.dataset.date;
      loadLocalData(selectedDate, 0);
    });
    // On loading for the first time
    $(window).on('load', function (e) {
      let selectedDate = $('.datepicker-cell.selected').data('date');
      loadLocalData(selectedDate, 1);
    });

    /**
     * Schedule List
     */

    /// Add New Items

    // Listen for submit button click.
    scheduleBtn.on('click', function (e) {
      // Clear Errors.
      errorEl.html('');
      // Get Selected Date.
      let selectedDate = $('.datepicker-cell.selected');
      let selectedDateDotContainer = $('.datepicker-cell.selected .db-schedule-dot-container');
      //  Get Input Value.
      let enteredValue = $('#scheduleListInput').val();
      // Check if the entered value is empty.
      if ($.trim(enteredValue).length == 0) {
        errorEl.html('Please enter a value.')
      } else {

        /**
         * SAVE DATA TO LOCAL STORAGE
        */

        // Read for local data
        let localData = JSON.parse(localStorage.getItem(`cal_${selectedDate.data('date')}`));

        // Check if data already exists for the selected date
        if (localData) {
          localData.items.push(enteredValue);
        } else {
          // Consturct a new object to be stored on the local storage
          localData = {
            'date': selectedDate.data('date'),
            'items': new Array(enteredValue)
          }
        }


            rpc.query({
             model: 'revision.request.client',
                    method: 'client_name',
                    args: [localData,1,1],
        }).then(function(result){
            console.log("result!!!!!!!!!11",result);
            console.log("result!!!!!!!!!11",result[0]);


        });
        locals_datas.push(localData)
        // Save data to local storage
        localStorage.setItem(`cal_${selectedDate.data('date')}`, JSON.stringify(localData));


        // Clear input element.
        inputEl.val('');
        // Create a new schedule list element if entered value is not empty.
        $(scheduleListEl).append(`
              <li class="db-schedule-input-container__item">
                <div class="db-schedule-input-container__bullet mr-3"></div>
                ${enteredValue}
              </li>
      `);
        // Check if the selected date already has events scheduled.
        if (!$(selectedDate).find('.db-schedule-dot-container').length == 1) {
          // If not add a new dot for the first time.
          $(selectedDate).append("<div class='db-schedule-dot-container'><span class='db-schedule-dot'></span></div>");
        } else {
          // Else add dot along with existing ones.
          $(selectedDateDotContainer).append("<span class='db-schedule-dot'></span>");
        }
      }
    });
    },

    _load_client_name:function(ev){
        console.log('ooooooooooooooooooooooooooooooooooooooo', $('.o_header_standard'))
//                console.log('pppppppppppppppppooooooooooooopppppppppppppppp', locals_datas)

        var id = $('.db-schedule-input-container__bullet');
        var day = $('.focused');
        var month = $('.view-switch');

        self.client_name = []
        var date_day = day[0].textContent
        var date_month = month[0].innerHTML
        var date_object =  date_day + ' ' +date_month

        for (var i = 0 ; i < id.length ; i++) {
            self.client_name = id[i].parentElement.outerText
        }

//         this._rpc({
//             model: 'revision.request.client',
//                    method: 'client_name',
//                    args: [self.client_name,date_day,date_month],
//        }).then(function(result){
//            console.log("result!!!!!!!!!11",result);
//            console.log("result!!!!!!!!!11",result[0]);
//            console.log("***************",$('.db-schedule-input-container__bullet'));
//
//        });

    },
//        _load_client_name:function(ev){
//            this._rpc({
//             model: 'revision.request.client',
//                    method: 'client_name',
//                    args: [self.client_name,date_day,date_month],
//        }).then(function(result){
//            console.log("result!!!!!!!!!11",result);
//            console.log("result!!!!!!!!!11",result[0]);
//            $('.db-schedule-input-container__bullet mr-3').empty()
//            $('.db-schedule-input-container__item').append('<div class="db-schedule-input-container__bullet mr-3">'+ result[0] +'</div>')
//
//
//
//        });
//    },
});


});







//var AbstractAction = require('web.AbstractAction');
//var ajax = require('web.ajax');
//var core = require('web.core');
//var rpc = require('web.rpc');
//var session = require('web.session');
//var web_client = require('web.web_client');
//var _t = core._t;
//var QWeb = core.qweb;
//
//
//var ContentCalendar = AbstractAction.extend({
//    template: 'content_calendar',
//
//    hasControlPanel: true,
//    loadControlPanel: true, // default: false
//
//    init: function(parent, context) {
//    this.action_id = context['id'];
//    this._super(parent, context);
//    this.content_blocks = [1,2,3]
//    },
//
//});