odoo.define('dr_social_website.content_tour', function (require) {
"use strict";
console.log('kkkkkkkkkkkkkkkkkkkkkkkkkkk')
const publicWidget = require('web.public.widget');

publicWidget.registry.websiteContentTour = publicWidget.Widget.extend({

 selector:'.content_tour',
 events: {
        'click .tour_start': '_tour_start',
        'click .next_1': '_next_1',
        'click .next_2': '_next_2',
        'click .next_3': '_next_3',
        'click .next_4': '_next_4',
        'click .next_5': '_next_5',
        'click .next_6': '_next_6',
        'click .next_7': '_next_7',
        'click .next_8': '_next_8',
        'click .menu_onboard': '_menu_onboard',
        'click .close_text': '_close_text',
        },
        _tour_start:function(e){
            console.log('fffffffffffffffffffffffffffffffff',e,$('.next1'))
            $('.row').addClass('d-none')
            $('.next1')[0].classList.remove('d-none')
        },
        _next_1:function(e){
            console.log('dddddddddddddd',e,$('.next2'))
            $('.next1').addClass('d-none')
            $('.next2')[0].classList.remove('d-none')
        },
        _next_2:function(e){
//            console.log('dddddddddddddd',e,$('.next2'))
            $('.arrow_2').addClass('d-none')
            $('.text_2').addClass('d-none')
            $('.next_2').addClass('d-none')
            $('.arrow_3')[0].classList.remove('d-none')
            $('.text_3')[0].classList.remove('d-none')
            $('.next_3')[0].classList.remove('d-none')
        },
        _next_3:function(e){
//            console.log('dddddddddddddd',e,$('.next2'))
            $('.arrow_3').addClass('d-none')
            $('.text_3').addClass('d-none')
            $('.next_3').addClass('d-none')
            $('.arrow_4')[0].classList.remove('d-none')
            $('.text_4')[0].classList.remove('d-none')
            $('.next_4')[0].classList.remove('d-none')
        },
        _next_4:function(e){
//            console.log('dddddddddddddd',e,$('.next2'))
            $('.arrow_4').addClass('d-none')
            $('.text_4').addClass('d-none')
            $('.next_4').addClass('d-none')
            $('.arrow_5')[0].classList.remove('d-none')
            $('.text_5')[0].classList.remove('d-none')
            $('.next_5')[0].classList.remove('d-none')
        },
        _next_5:function(e){
//            console.log('dddddddddddddd',e,$('.next2'))
            $('.arrow_5').addClass('d-none')
            $('.text_5').addClass('d-none')
            $('.next_5').addClass('d-none')
            $('.arrow_6')[0].classList.remove('d-none')
            $('.text_6')[0].classList.remove('d-none')
            $('.next_6')[0].classList.remove('d-none')
        },
         _next_6:function(e){
//            console.log('dddddddddddddd',e,$('.next2'))
            $('.arrow_6').addClass('d-none')
            $('.text_6').addClass('d-none')
            $('.next_6').addClass('d-none')
            $('.post_1').addClass('d-none')
            $('.post_2')[0].classList.remove('d-none')
            $('.arrow_7')[0].classList.remove('d-none')
            $('.text_7')[0].classList.remove('d-none')
            $('.next_7')[0].classList.remove('d-none')
        },
        _next_7:function(e){
//            console.log('dddddddddddddd',e,$('.next2'))
            $('.arrow_7').addClass('d-none')
            $('.text_7').addClass('d-none')
            $('.next_7').addClass('d-none')
            $('.post_2').addClass('d-none')
//            $('.post_2')[0].classList.remove('d-none')
            $('.arrow_8')[0].classList.remove('d-none')
            $('.text_8')[0].classList.remove('d-none')
//            $('.next_7')[0].classList.remove('d-none')
        },
        _next_8:function(e){
//            console.log('dddddddddddddd',e,$('.next2'))
            $('.arrow_8').addClass('d-none')
            $('.text_8').addClass('d-none')
            $('.next_8').addClass('d-none')
            $('.noclick').addClass('d-none')
            $('.finish_last')[0].classList.remove('d-none')
            $('.access_calendar')[0].classList.remove('d-none')
            $('.clickable')[0].classList.remove('d-none')
            $('.finish_page')[0].classList.remove('d-none')
            $('.finish_text')[0].classList.remove('d-none')
            $('.finish_text1')[0].classList.remove('d-none')
            $('.finish_text2')[0].classList.remove('d-none')
        },
        _menu_onboard:function(e){
        console.log('kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk')
            $('.text_menu')[0].classList.remove('d-none')

        },
        _close_text:function(e){
            $('.text_menu').addClass('d-none')

       },
});

});