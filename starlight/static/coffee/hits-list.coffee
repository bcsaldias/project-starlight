$ ->

  context =
    'readOnly': true
    'angleOffset': -125
    'angleArc': 250
    'thickness': 0.4
    'width': "100%"
    'fgColor': "#8008BC"
    'bgColor': "#999999"
    'fontWeight': 'normal'
    'format': (v) ->
        v+"%"
  $('#progress').knob context
