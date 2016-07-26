$ ->
  $("[data-toggle]").click((e) ->
    e.preventDefault()
    target = $(this).find('img').attr('src')
    $("#image-modal").find("img").attr('src',target)
  )
