function myHome() {
    var winH = $(window).height();
    var wrapperH = $('.container-fluid').height();
    if(winH > wrapperH) {                            
        $('.container-fluid').css({
            height: (winH) +'px'
        });
    }                                                                               
    $(window).resize(function(){
        var winH = $(window).height();
        var wrapperH = $('.container-fluid').height();
        var diffH = wrapperH - winH;
        var newH = wrapperH - diffH;
        if(wrapperH > winH) {
            $('.container-fluid').css({
                height: (newH) +'px'
            });
        }
    });  
}
$(document).ready(function() {
    myHome();
});