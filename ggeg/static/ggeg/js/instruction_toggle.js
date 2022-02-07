$(function () {
    var $instruction_wrapper = $('div#instruction_wrapper');
    var $instruction_toggler = $('button#instruction_toggler');
    $instruction_wrapper.on('hide.bs.collapse', function () {
        $instruction_toggler.removeClass('btn-info').addClass('btn-primary');
        $instruction_toggler.html('Mostra istruzioni');
    });
    $instruction_wrapper.on('show.bs.collapse', function () {
        $instruction_toggler.addClass('btn-info').removeClass('btn-primary');
        $instruction_toggler.html('Nascondere istruzioni');
    })
})