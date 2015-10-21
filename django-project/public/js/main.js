( function( window, $ ) {
    $( function() {
        // var captcha = captchaEl.data( 'captcha' );

        var statusEl = $( '#status-message' ),
            queryString = window.location.search;
        // Show success/error messages
        if ( queryString.indexOf('status=failedSlider') !== -1 ) {
            statusEl.html('<div class="status"> <div class="icon-no"></div> <p>Image not placed in the right position</p> </div>');
        } else if ( queryString.indexOf('status=failedRobot') !== -1 ) {
            statusEl.html('<div class="status"> <div class="icon-no"></div> <p>Simulation data detected</p> </div>');
        } else if ( queryString.indexOf('status=validSlider') !== -1 ) {
            statusEl.html('<div class="status valid"> <div class="icon-yes"></div> <p>Slider test past</p> </div>');
        }  

        $(' .QapTcha').QapTcha();

    } );
}( window, jQuery ) );
