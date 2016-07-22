$ ->
  context =
    'readOnly': true
    'angleOffset': -125
    'angleArc': 250
    'thickness': 0.2
    'fgColor': "#8008BC"
    'bgColor': "#999999"
  $('#points').knob context

  username = $('#username').attr('data-value')
  url = '/user/'+username+'/activities'
  $.getJSON url, (result) ->
    activities = result['activities']
    for activity in activities
      console.log activity
