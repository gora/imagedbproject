jQuery.preloadImages = function()
{
  for(var i = 0; i<arguments.length; i++)
  {
    jQuery("<img>").attr("src", arguments[i]);
  }
}

function toggleImage(buttonElm, imgover, imgout) {
  buttonElm.mouseover(function(e) {
    $(this).attr("src", imgover); 
  }).mouseout(function(e) {
    $(this).attr("src", imgout);
  });
} 

$(document).ready(function(){

  $.preloadImages("/static/img/Search2.png",
                  "/static/img/clear2.png",
                  "/static/img/prev2.png",
                  "/static/img/next2.png",
/*                  "/static/img/Images2.png",
                  "/static/img/logos2.png",*/
                  "/static/img/Small2.png",
                  "/static/img/Medium2.png",
                  "/static/img/Large2.png",
                  "/static/img/original_size2.png");

  toggleImage($('#searchbutton'), "/static/img/Search2.png", "/static/img/Search.png"); 
  toggleImage($('#resetlink'), "/static/img/clear2.png", "/static/img/clear.png");
  toggleImage($('#previousbutton'), "/static/img/prev2.png", "/static/img/prev.png"); 
  toggleImage($('#nextbutton'), "/static/img/next2.png", "/static/img/next.png"); 
  toggleImage($('#download-small'), "/static/img/Small2.png", "/static/img/Small.png"); 
  toggleImage($('#download-medium'), "/static/img/Medium2.png", "/static/img/Medium.png"); 
  toggleImage($('#download-large'), "/static/img/Large2.png", "/static/img/Large.png"); 
  toggleImage($('#download-original'), "/static/img/original_size2.png", "/static/img/original_size.png"); 
//   toggleImage($('#images-section'), "/static/img/Images2.png", "/static/img/Images.png"); 
//   toggleImage($('#logos-section'), "/static/img/logos2.png", "/static/img/logos.png"); 


});