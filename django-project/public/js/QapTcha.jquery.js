/************************************************************************
*************************************************************************
@Name :       	QapTcha - jQuery Plugin
@Revison :    	4.2
@Date : 		06/09/2012  - dd/mm/YYYY
@Author:     	 ALPIXEL Agency - (www.myjqueryplugins.com - www.alpixel.fr)
@License :		 Open Source - MIT License : http://www.opensource.org/licenses/mit-license.php

**************************************************************************
 *************************************************************************/

/*****
Added image slider
Modder: stan
Date: 20/10/2015
 *****/

jQuery.QapTcha = {
    build : function(options)
    {
        // perform a xmlhttprequest
        _request = function( url, callback ) {
            var XMLHttpRequest = window.XMLHttpRequest;
            var ajaxRequest = new XMLHttpRequest();

            ajaxRequest.open( 'GET', url, true );
            ajaxRequest.onreadystatechange = function() {
                var response;

                if ( ajaxRequest.readyState !== 4 || ajaxRequest.status !== 200 ) {
                    return;
                }

                response = JSON.parse( ajaxRequest.responseText );
                callback( response );
            };

            ajaxRequest.send();
        };
        
        var defaults = {
            txtLock : 'Locked : form can\'t be submited',
	    txtUnlock : 'Unlocked : form can be submited',
	    disabledSubmit : true,
	    autoRevert : true,
	    verifyUrl : '/scroll',
            startUrl : '/startslider',
            imageUrl : '/getslider',
	    autoSubmit : false,
            request : _request
        };

        // currently just used to start the service
        _refresh = function ( config ) {
            config.request( config.startUrl, function( response ) {
                config.sliderPosition = response.sliderPosition;
            });
        };

        // sample the trace with equal separation if length is larger than count
        _sample = function (xs, count) {
            var xlen = xs.length;
            if ( xlen <= count ) {
                return xs;
            }
            else {
                var ys = [],
                    ylen = 0;
                for (var i=0; i < xlen; i++) {
                    if (i*count/xlen >= ylen) {
                        ys.push(xs[i]);
                        ylen += 1;
                    }
                }
                return ys;
            }
        };

	if(this.length>0)
	    return jQuery(this).each(function(i) {
		/** Vars **/
		var
		opts = $.extend(defaults, options),
		$this = $(this),
		form = $('form').has($this),
                Explanation = jQuery('<p>', {'class':'visualCaptcha-explanation',text:'slide to verify'}),
		Clr = jQuery('<div>',{'class':'clr'}),
		bgSlider = jQuery('<div>',{'class':'bgSlider'}),
		Slider = jQuery('<div>',{'class':'Slider'}),
		TxtStatus = jQuery('<div>',{'class':' TxtStatus dropError',text:opts.txtLock}),
		inputQapTcha = jQuery('<input>',{name:generatePass(32),value:generatePass(7),type:'hidden'}),
                dragging = [],
                moving = [],
                timestamp;
                
		/** Disabled submit button **/
		if(opts.disabledSubmit) form.find('input[type=\'submit\']').attr('disabled','disabled');

                /** request the image **/
                _refresh(opts);
                var imageSlider = jQuery('<div>', {'class':'ImageSlider'}),
                    fgSlider = jQuery('<div>', {'class':'fgSlider'}),
                    bgImage = jQuery('<img>', {'src':opts.imageUrl}),
                    fgImage = jQuery('<img>', {'src':opts.imageUrl+'/foreground'});
                
		/** Construct DOM **/
                Explanation.appendTo($this);
                imageSlider.insertAfter(Explanation);
                bgSlider.insertAfter(imageSlider);
		Clr.insertAfter(bgSlider);
		TxtStatus.insertAfter(Clr);
		inputQapTcha.appendTo($this);
		Slider.appendTo(bgSlider);
                bgImage.appendTo(imageSlider);
                fgSlider.insertAfter(bgImage);
                fgImage.appendTo(fgSlider);
		$this.show();

                // mouse movement
                if (!Date.now) {
                    Date.now = function() { return new Date().getTime(); };
                }

                $this.mouseenter( function () {
                    $this.mousemove( function (event) {
                        moving.push([event.pageX, event.pageY, Date.now() - timestamp]);
                    });
                    timestamp = Date.now();
                });

		Slider.draggable({
                    start: function() {
                        $this.off('mousemove');
                    },
                    drag: function(event,ui) {
                        dragging.push([event.pageX, event.pageY, Date.now() - timestamp]);
                        fgSlider.css({left:6 + ui.position.left});
                    },
		    revert: function(){
			if(opts.autoRevert)
			{
			    return true;
			}
		    },
		    containment: bgSlider,
		    axis:'x',
		    stop: function(event,ui){
			// subsample the data if needed
                        //movement = _sample(movement, 50);
                        var interactions = {
                            'dragging':dragging,
                            'moving': moving};
			$.post(opts.verifyUrl,
                               {
                                   'interactions':JSON.stringify(interactions),
                                   'position': (ui.position.left-44)*100.0/350
                               },
                               function(data) {
                                   window.location.replace('?status='+data.message)},
                               'json');
                        fgSlider.css({left:0});
		    }
		});

		function generatePass(nb) {
		    var chars = 'azertyupqsdfghjkmwxcvbn23456789AZERTYUPQSDFGHJKMWXCVBN_-#@';
		    var pass = '';
		    for(i=0;i<nb;i++){
		        var wpos = Math.round(Math.random()*chars.length);
		        pass += chars.substring(wpos,wpos+1);
		    }
		    return pass;
		}

	    });
    }
}; jQuery.fn.QapTcha = jQuery.QapTcha.build;
