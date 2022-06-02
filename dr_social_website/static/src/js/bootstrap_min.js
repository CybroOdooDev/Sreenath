   $('#calendar').datepicker({
                            inline: true,
                            firstDay: 1,
                            showOtherMonths: true,
                            dayNamesMin: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
                        });


    console.log('*****************', $('.ui-state-default'))

//    $('.ui-state-default').click(function(){
//    console.log('++++++++++++++++++++')
//    alert('++++++++++++++++++++++++++++++++++')
//    })

//    $( ".ui-state-default" ).each(function(ev) {
//    $(this).on("click", function(){
//        day = ev - 1;
//        month = $(this)[0].parentElement.dataset['month']
//        year = $(this)[0].parentElement.dataset['year']
//        year = $(this)[0].parentElement.dataset['year']
//        alert('++++++++++++++++++++++++++++++++++')
//        console.log('ssssssssssssssssssssssssssssssss', $(this)[0].parentElement.dataset.add)
//        console.log('day', day)
//        console.log('monthsssss', month)
//        console.log('yearsssssss', year)
//     let val = day
//$('#cash_narrat').val(val);
////$(this).reload();
//
//    });
//});
//
//
//$(document).ready(function(){
//    $(".ui-state-default").on('shown.bs.modal', function(){
//        $(this).find('input[type="text"]').focus();
//    });
//});