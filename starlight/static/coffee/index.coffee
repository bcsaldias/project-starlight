$ ->
  onScroll = () ->
    if $(window).scrollTop() > 90
      $('.navbar-starlight').removeClass('navbar-transparent')
      return
    else
      $('.navbar-starlight').addClass('navbar-transparent')
      return

  $('nav.navbar-starlight').addClass('navbar-transparent')
  $(window).scroll(onScroll)
