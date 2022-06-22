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