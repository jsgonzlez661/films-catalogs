function hideSpinner() {
    $(document).ready(function() {
        if ($('#spinner-load').css('visibility') != 'hidden') {
            $("#spinner-load").fadeToggle(1);
            // $('#spinner-load').css('visibility', 'hidden');
        } else {
            $('#spinner-load').css('visibility', 'visible');
            $('#movies-load').css('visibility', 'hidden');
        }
        $("#movies-load").fadeIn(1);
        $('#movies-load').css('visibility', 'visible');
    })
};