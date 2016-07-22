computePeriod = (timeseries, period) ->
  epochs = timeseries.map (time) -> (time % period) / period
  return epochs

mainPlot = (lcdata) ->
  data =
    x: lcdata.mjd
    y: lcdata.mag
    error_y:
      type: 'data'
      array: lcdata.err
      color: 'rgb(255, 217, 102)'
      width: 3
      opacity: 0.3
    mode: 'markers'
    marker:
      color: 'rgb(255, 217, 102)'
      size: 8
    type: 'scatter'

  layout =
    margin:
      b: 25
      l: 50
      r: 10
      t: 10
    paper_bgcolor: 'rgba(0,0,0,0)'
    plot_bgcolor: 'rgba(0,0,0,0)'
    yaxis:
      autorange: 'reversed'
      gridcolor: "#808080"
      gridwidth: 1
      tickfont:
        color: "#fff"
    xaxis:
      gridcolor: "#808080"
      gridwidth: 1
      tickfont:
        color: "#fff"
    height: 350

  config =
      staticPlot: true

  Plotly.newPlot 'plot-main', [data], layout, config
  return

foldPlot = (lcdata, period) ->
  times = computePeriod(lcdata.mjd, period)
  times2 = (time-1 for time in times)
  times = [times2..., times...]
  magnitudes = [lcdata.mag..., lcdata.mag...]

  data =
    x: times
    y: magnitudes
    mode: 'markers'
    marker:
      color: 'rgb(255, 217, 102)'
      size: 6
      opacity: 0.5
    type: 'scatter'

  layout =
    margin:
      b: 25
      l: 50
      r: 10
      t: 10
    paper_bgcolor: 'rgba(0,0,0,0)'
    plot_bgcolor: 'rgba(0,0,0,0)'
    yaxis:
      autorange: 'reversed'
      gridcolor: "#808080"
      gridwidth: 1
      tickfont:
        color: "#fff"
    xaxis:
      gridcolor: "#808080"
      gridwidth: 1
      tickfont:
        color: "#fff"
    height: 200

  config =
      staticPlot: true

  Plotly.newPlot 'plot-fold', [data], layout, config
  return
