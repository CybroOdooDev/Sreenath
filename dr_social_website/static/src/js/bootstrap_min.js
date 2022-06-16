

/**
* Schedule List
*/

/// Selectors
let inputEl = $('#scheduleListInput');
let scheduleBtn = $('#scheduleListButton');
let scheduleListEl = $('.db-schedule-input-container__list');
let errorEl = $('.db-error');

/// Add New Items

// Listen for submit button click.
scheduleBtn.on('click', function (e) {
// Clear Errors.
errorEl.html('');
// Get Selected Date.
let selectedDate = $('.datepicker-cell.selected');
let selectedDateDotContainer = $('.datepicker-cell.selected .db-schedule-dot-container');
// Get Input Value.
let enteredValue = inputEl.val();
// Check if the entered value is empty.
if ($.trim(enteredValue).length == 0) {
errorEl.html('Please enter a value.')
} else {
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
$(selectedDate).append("
<div class='db-schedule-dot-container'>
    <span class='db-schedule-dot'></span>
</div>
");
} else {
// Else add dot along with existing ones.
$(selectedDateDotContainer).append("<span class='db-schedule-dot'></span>");
}
}
});
