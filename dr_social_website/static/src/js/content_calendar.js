odoo.define('dr_social_website.content_calendar', function (require) {
"use strict";
console.log('lllllllllllllll')
const publicWidget = require('web.public.widget');



 $(document).ready(function (ev) {
// console.log('lllllllllllllllllllllllllllllllllllllllllllllllllll', ev)
    $(".revision").hide();
    $(".show_less").hide();
    var posts = $('.dashboard-table')
    var table_1 = $('.db-card')
    console.log(posts,'lllllllllllll',$('.red'))
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
//            $('.box-color')[i].style['background']='#bdbfb7';
//            $('.form-input').style['background-color']='#bdbfb7';
//            $('.form-input').css('background-color', '#bdbfb7');
//            $('.value_time').css('color', '#bdbfb7');

        }
        }
        for (let i = 0; i < table_1.length; i++) {
    console.log(table_1[i].attributes.value.value,'ppppppppppppppp')
        if (table_1[i].attributes.value.value === 'draft') {
            table_1[i].style.border = '2px solid #ffb914';

        }
//         if (posts[i].attributes.value.value === 'draft') {
////        console.log(posts[i].style.border = 'red','posts[i].style')
//            posts[i].style.border = '2px solid red';
////            posts[i].style.border = '2px solid red';
//
//        }
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
        'change .post_feedback_textarea': '_load_feedback',
        'change .post_message_textarea': '_load_message',
        'change .post_uploded_image': '_load_uploaded_image',
        'click .approve_button': '_approve_button',
        'click .feedback_revision': '_feedback_revision',
        'click .not_approved_button': '_not_approved_button',
        'click .show_more': '_show_more',
        'click .show_less': '_show_less',
        'change .date_input1': '_date_input',
        'blur .value_time': '_value_time',
    },
    _load_feedback:function(ev){
        ev.stopPropagation();
        var id = $(ev.target).data('id');
        var text = $(ev.target).val();
        var revision_button = $('.grey')
        var revision_text = $('.revision')
        var value = 'revision_'+ id;
        $('#'+ value).hide();
        revision_button.css('background-color', '#625454');
        console.log(text,this,revision_text);
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
        revision_button.css('background-color', '#625454');
//        console.log(text,this,revision_text);

    },
    _load_message:function(ev){
        var id = $(ev.target).data('id');
        var message = $(ev.target).val();
        this._rpc({
                model: 'social.post',
                method: 'write',
                args: [[parseInt(id)], {message:message}],

            }).then(function(result){
                console.log("result",result);
            });
    },
     _load_uploaded_image:function(ev){
        ev.stopPropagation();
        console.log("event: ", ev);
        var id = 'preview_' + String(ev.target.id);
        console.log("Preview: ", id);
        if(ev.target.files.length > 0){
        var src = URL.createObjectURL(ev.target.files[0]);
        var preview = document.getElementById(id);
        preview.src = src;
        preview.style.display = "block";
        }
       var self = this
       console.log('lkkkkk',ev)
        var id = $(ev.target).data('id');
        var image = ev.target.files;
        console.log(image.length,'kkkkkkkkkkkkkkkkkkkkkk')
        for (let i = 0; i < image.length; i++) {
          image = image[i]
          var name = image.name
           var reader = new FileReader();
           reader.readAsDataURL(image);
           reader.onload = function(ev) {
          console.log(image,name,'hhhhhhhhhhhhhhhh',ev.target.result)
           self._rpc({
                model: 'social.post',
                method: 'image_path',
                args: [ ,parseInt(id),name,ev.target.result],

            }).then(function(result){
                console.log("result",result);
            });
        }
        }
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
      _show_more:function(ev){
        var id = 'chartdiv_'+ String($(ev.target).data('id'));
        document.getElementById(id).style.height = '300px' ;
        $(".show_less").show();
        $(".show_more").hide();

    },
     _show_less:function(ev){
        var id = 'chartdiv_'+ String($(ev.target).data('id'));
        document.getElementById(id).style.height = '150px';
        $(".show_more").show();
        $(".show_less").hide();
    },
       _date_input:function(ev){
      console.log('jjjjjjjj',$(ev.target).val())
        var id = $(ev.target).data('id');
        var date = $(ev.target).val()
//        console.log(date);
        this._rpc({
                model: 'social.post',
                method: 'write',
//                 method: 'search_read',
                args: [[parseInt(id)], {post_method:'scheduled', scheduled_date:date, date:date}],

            }).then(function(result){
                console.log("result",result);
            });
    },
     _value_time:function(ev){
      console.log('jjjjjjjj',ev)
        var id = $(ev.target).data('id');
        var input_time = $(ev.target).val()
//        var space = input_time.split(':')
//        var time = space[1].split(' ')
        var date = ev.target.date
//        console.log(this,'thisssssssssss',time);
//        this._rpc({
//                model: 'social.post',
//                method: 'write',
//                args: [[parseInt(id)], {post_method:'scheduled', time:input_time}],
//
//            }).then(function(result){
//                console.log("result",result);
//            });
            this._rpc({
                model: 'social.post',
                method: 'time_change',
                args: [,parseInt(id),input_time],

            }).then(function(result){
                console.log("result",result);
            });
    },

    _approve_button: function (ev) {
    var id = $(ev.target).data('id')
//    console.log('iiiiiiiiiiiiiiiiiii')
     this._rpc({
        model: 'social.post',
        method: 'write',
        args: [[parseInt(id)], {state:'scheduled'}],

    }).then(function(result){
        console.log("result",result);
    });
    },
     _not_approved_button: function (ev) {
     var id = $(ev.target).data('id')
//          console.log('hhhhhhhhhhhhhh')

     this._rpc({
                model: 'social.post',
                method: 'write',
                args: [[parseInt(id)], {state:'not_approved'}],

            }).then(function(result){
                console.log("result",result);
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