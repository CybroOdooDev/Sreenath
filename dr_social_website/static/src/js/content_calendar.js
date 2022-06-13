odoo.define('dr_social_website.content_calendar', function (require) {
"use strict";
const publicWidget = require('web.public.widget');


 $(document).ready(function () {
    $(".revision").hide();
    })

publicWidget.registry.websiteEventSearchSponsor = publicWidget.Widget.extend({

 selector:'.dashboard-table',
 events: {
        'change .post_feedback_textarea': '_load_feedback',
        'change .post_message_textarea': '_load_message',
        'change .post_uploded_image': '_load_uploaded_image',
        'click .approve_button': '_approve_button',
        'click .not_approved_button': '_not_approved_button',
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
        this._rpc({
                model: 'social.post',
                method: 'write',
                args: [[parseInt(id)], {feedback:text}],

            }).then(function(result){
            });
    },
    _load_message:function(ev){
        var id = $(ev.target).data('id');
        var message = $(ev.target).val();
        this._rpc({
                model: 'social.post',
                method: 'write',
                args: [[parseInt(id)], {message:message}],

            }).then(function(result){
            });
    },
     _load_uploaded_image:function(ev){
        ev.stopPropagation();
        var id = 'preview_' + String(ev.target.id);
        if(ev.target.files.length > 0){
        var src = URL.createObjectURL(ev.target.files[0]);
        var preview = document.getElementById(id);
        preview.src = src;
        preview.style.display = "block";
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
      _date_input:function(ev){
        var id = $(ev.target).data('id');
        var date = $(ev.target).val()
        this._rpc({
                model: 'social.post',
                method: 'write',
//                 method: 'search_read',
                args: [[parseInt(id)], {post_method:'scheduled', scheduled_date:date, date:date}],

            }).then(function(result){
            });
    },
     _value_time:function(ev){
        var id = $(ev.target).data('id');
        var input_time = $(ev.target).val()
//        var space = input_time.split(':')
//        var time = space[1].split(' ')
        var date = ev.target.date
        this._rpc({
                model: 'social.post',
                method: 'write',
                args: [[parseInt(id)], {post_method:'scheduled', time:input_time}],

            }).then(function(result){
            });
    },

    _approve_button: function (ev) {
    var id = $(ev.target).data('id')
     this._rpc({
        model: 'social.post',
        method: 'write',
        args: [[parseInt(id)], {state:'scheduled'}],

    }).then(function(result){
    });
    },
     _not_approved_button: function (ev) {
     var id = $(ev.target).data('id')

     this._rpc({
                model: 'social.post',
                method: 'write',
                args: [[parseInt(id)], {state:'not_approved'}],

            }).then(function(result){
            });
    },




});


publicWidget.registry.websiteEventSearchSponsorss = publicWidget.Widget.extend({

 selector:'.form-groups',
 events: {
        'change .form-groups': '_load_feedback',

    },
    _load_feedback:function(ev){
        ev.stopPropagation();
        console.log('oppopopopopopoopoopopoopopopopo')
//        var id = $(ev.target).data('id');
//        var text = $(ev.target).val();
//        var revision_button = $('.grey')
//        var revision_text = $('.revision')
//        var value = 'revision_'+ id;
        $('#'+ value).hide();
        revision_button.css('background-color', '#625454');
//        this._rpc({
//                model: 'social.post',
//                method: 'write',
//                args: [[parseInt(id)], {feedback:text}],
//
//            }).then(function(result){
//            });
    },
});


});
