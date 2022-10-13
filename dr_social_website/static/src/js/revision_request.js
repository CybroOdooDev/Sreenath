odoo.define('dr_social_website.revision_requestss', function (require) {
"use strict";
const publicWidget = require('web.public.widget');
var rpc = require('web.rpc');

$(document).ready(function (ev) {
    var notifications = $('.db-revision-list__item')
//    var delete_notification = $('.delete_notification');
    console.log(notifications,'db-revision-list__item')
    for (let i = 0; i < notifications.length; i++) {
    console.log('notifications')
//        if (notifications[i].attributes.value){
//        console.log('--------------------------------------------------')
////            var delete_notify = 'notify_'+ String(delete_notification[i].id);
//                    console.log(notifications[i],'nnnnnnnnnnnnnn')
//                    notifications[i].style['background-color']= 'white';
////            $('#'+delete_notify).empty()
//            }
    }
})

console.log('pppppppppppppppppppp')
publicWidget.registry.websiteEventSearchSponsorss = publicWidget.Widget.extend({

 selector:'.db-revision-lists',
 events: {
        'click .feedack_view': '_feedack_view',
        'click .delete_notification': '_delete_notification',
        'click .db-revision-list__profile-update': '_load_client_names',
    },



    init: function(parent, context) {
        this.action_id = context['id'];
        this._super(parent, context);
        console.log('This is ittttttttttttttttttttttttttttttttttt')
        console.log('DAAATEEEEEEEEEEEEEEEEEEEE', JSON.parse(localStorage.getItem(`cal_1658341800000`)))
//        for (var i = 0; i < localStorage.length; i++){
//        var key=localStorage.key(i);
//        console.log('**************************', key+': '+localStorage.getItem(key));
//        }

            /// Selectors
    let inputEl = $('#scheduleListInput');
    let scheduleBtn = $('#scheduleListButton');
    let scheduleListEl = $('.db-schedule-input-container__list');
    let errorEl = $('.db-error');
    let selectedDateEl = $('.db-schedule-input-container__day');

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
     * Chage DOW Highlight on Date click
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
    * CONVERT ISO STRING TO DATE
    */
    function parseUnixString(unixStamp) {
      const options = { day: 'numeric', month: 'long' };
      const displayDate = new Date(Number(unixStamp)).toLocaleDateString('en-US', options).split(" ");
      return `${displayDate[1]}${getOrdinal(displayDate[1])} ${displayDate[0]}`;
    }

    /**
     * GET DATE ORDINALS
     */
    function getOrdinal(date) {
      switch (date % 10) {
        case 1:
          return "st";
          break;
        case 2:
          return "nd";
          break;
        case 3:
          return "rd";
          break;
        default:
          return "th";
          break;
      }
    }

    /**
    * LOAD VALUES TO SHCEDULE LIST
    * mode = 1: Execute on load only
    */
    function loadLocalData(selectedDate, mode) {
      let localData = JSON.parse(localStorage.getItem(`cal_${selectedDate}`));

      let selectedEl = $('.datepicker-cell.selected');

      // Reset Schedule List
      $(scheduleListEl).html(``);

      if (localData) {
        localData.items.forEach(function (item, i) {
          $(scheduleListEl).append(`
              <li class="db-schedule-input-container__item">
                <div class="db-schedule-input-container__badge">
                  <img class="db-schedule-input-contianer__image mr-1" src="/image/user_1.jpeg"></img>
                  ${item}
                </div>
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
      // Change date in the input container
      selectedDateEl.html(parseUnixString(selectedDate));
      loadLocalData(selectedDate, 0);
    });
    // On loading for the first time
    $(window).on('load', function (e) {
      let selectedDate = $('.datepicker-cell.selected').data('date');
      loadLocalData(selectedDate, 1);
      // Change date in the input container
      selectedDateEl.html(parseUnixString(selectedDate));
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
        // Save data to local storage
        localStorage.setItem(`cal_${selectedDate.data('date')}`, JSON.stringify(localData));


        // Clear input element.
        inputEl.val('');
        // Create a new schedule list element if entered value is not empty.
        $(scheduleListEl).append(`
              <li class="db-schedule-input-container__item">
                <div class="db-schedule-input-container__badge">
                  <img class="db-schedule-input-contianer__image mr-1" src="/image/user_1.jpeg"></img>
                ${enteredValue}
                </div>
              </li>
      `);
         rpc.query({
             model: 'revision.request.client',
                    method: 'client_name',
                    args: [localData,1,1],
        }).then(function(result){
            console.log("result!!!!!!!!!11",result);
            console.log("result!!!!!!!!!11",result[0]);


        });
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

    _load_client_names:function(ev){
            console.log('This is qwertyu')

    },

    _feedack_view:function(ev){
//        console.log(ev, 'ghfriusfdiufhdisua;foiuseoiufzs',$('.db-revision-list__item--active'))
////        var delete_notification = $('.delete_notification');
////        console.log('delete_notification', delete_notification[0].offsetParent.)
        var client_id = ev.target.id
//        var notification = 'notify_' + String(client_id)
//        console.log(notification,'lllllllllllllllllllllllllllllllllllllllllll')
////        $('#'+ notification)[0].style['background-color']= white;
         this._rpc({
            model: 'onyx.social.post',
            method: 'feedbacks_viewed',
            args: [ , parseInt(client_id)],

        }).then(function(result){})
//
    },
  _delete_notification:function(ev){
        console.log(ev, 'ghfriusfdiufhdisua;foiuseoiufzs',$('.db-revision-list__item--active'))
        var delete_notification = $('.delete_notification');
//        console.log('delete_notification', delete_notification[0].offsetParent.)
        var client_id = ev.target.id
        var notification = 'notify_' + String(client_id)
        console.log(notification,'lllllllllllllllllllllllllllllllllllllllllll', $('#'+ notification))
        $('#'+ notification).hide()
        this._rpc({
            model: 'onyx.social.post',
            method: 'delete_notification_revision',
            args: [ , parseInt(client_id)],

        }).then(function(result){})
//                console.log('This is lkjhgfdsa')


    },

});
});