$(function() {
  var onScroll;
  $('[data-toggle="tooltip"]').tooltip();
  if (typeof lcdata !== "undefined" && lcdata !== null) {
    curvePlot(lcdata);
  }
  onScroll = function() {
    if ($(window).scrollTop() > 90) {
      $('.macho-navbar').removeClass('navbar-transparent');
    } else {
      $('.macho-navbar').addClass('navbar-transparent');
    }
  };
  if (window.location.pathname === '/') {
    $('nav.macho-navbar').addClass('navbar-transparent');
    $(window).scroll(onScroll);
  }
});
