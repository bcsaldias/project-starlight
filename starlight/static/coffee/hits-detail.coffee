$ ->
  hits_id = $('#hits_id').attr('data-value')
  url = '/hits/'+hits_id + '/data'

  $.getJSON url, (result) ->
    $("#vote").removeAttr("hidden")
    profile = JSON.parse(result['profile'])[0]
    lightcurve = JSON.parse(result['lightcurve'])
    periodLS = profile['fields']['periodLS']

    mjd = Array()
    mag = Array()
    err = Array()
    for datapoint in lightcurve
        mjd.push datapoint['fields']['mjd']
        mag.push datapoint['fields']['mag']
        err.push datapoint['fields']['err']
    lcdata =
      mjd: mjd
      mag: mag
      err: err
    mainPlot lcdata

    foldPlot lcdata, periodLS



  $("#vote").click (e)->
      e.preventDefault()
      label = $("#select-star").find(':selected').val()

      url = '/hits/'+hits_id + '/'
      $.post(url,{'label': label}, (result)->
          next = result['next']
          point = result['point']

          if point >= 1
            point = "+" + point
            new_url = '/hits/'+next+'/'
            $("#point").text(point).removeAttr('hidden').animate({
              bottom: '150px'
              opacity: '0.0'
            }, 750, () ->
                window.history.pushState({}, hits_id, url)
                window.location.replace(new_url)
            )
          else
            new_url = '/hits/'+next+'/'
            window.history.pushState({}, hits_id, url)
            window.location.replace(new_url)
        )


  # # $("#save").click ()->
  # #   url = "/hits/" + hits_id + "/save"
  # #   $.get url, (result) ->
  # #
  # #     if $("#save").attr('value') == "true"
  # #       $("#save").attr("value", "false")
  # #       $("#save").html('<i class="fa fa-bookmark" aria-hidden="true"></i> Save')
  # #     else
  # #       $("#save").attr("value", "true")
  # #       $("#save").html('<i class="fa fa-check" aria-hidden="true"></i> Saved')
  #
  #
