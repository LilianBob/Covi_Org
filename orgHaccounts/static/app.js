function myHome() {
    var winH = $(window).height();
    var wrapperH = $('.wrapper').height();
    if(winH > wrapperH) {                            
        $('.wrapper').css({
            height: (winH) +'px'
        });
    }                                                                               
    $(window).resize(function(){
        var winH = $(window).height();
        var wrapperH = $('.wrapper').height();
        var diffH = wrapperH - winH;
        var newH = wrapperH - diffH;
        if(wrapperH > winH) {
            $('.wrapper').css({
                height: (newH) +'px'
            });
        }
    });  
}
$(document).ready(function() {
    myHome();
});