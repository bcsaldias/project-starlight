var computePeriod, curvePlot,
  slice = [].slice;

computePeriod = function(timeseries, period) {
  var epochs;
  epochs = timeseries.map(function(time) {
    return (time % period) / period;
  });
  return epochs;
};

curvePlot = function(lcdata) {
  var config, data, layout, magnitudes, time, timeperiods, timeperiods2;
  if (lcdata.periodicity) {
    timeperiods = computePeriod(lcdata.MJD, lcdata.period);
    timeperiods2 = (function() {
      var i, len, results;
      results = [];
      for (i = 0, len = timeperiods.length; i < len; i++) {
        time = timeperiods[i];
        results.push(time - 1);
      }
      return results;
    })();
    timeperiods = slice.call(timeperiods2).concat(slice.call(timeperiods));
    magnitudes = slice.call(lcdata.Mag).concat(slice.call(lcdata.Mag));
  } else {
    timeperiods = lcdata.MJD;
    magnitudes = lcdata.Mag;
  }
  data = {
    x: timeperiods,
    y: magnitudes,
    mode: 'markers',
    marker: {
      color: 'rgb(255, 217, 102)',
      size: 4,
      symbol: "star-dot"
    },
    fillcolor: 'rgb(255, 223, 89)',
    type: 'scatter'
  };
  layout = {
    margin: {
      b: 40,
      l: 40,
      r: 10,
      t: 10
    },
    paper_bgcolor: "#1f1f1f",
    plot_bgcolor: "#1f1f1f",
    yaxis: {
      autorange: 'reversed',
      gridcolor: "#808080",
      gridwidth: 1,
      tickfont: {
        color: "#fff"
      }
    },
    xaxis: {
      gridcolor: "#808080",
      gridwidth: 1,
      tickfont: {
        color: "#fff"
      }
    }
  };
  config = {
    staticPlot: true
  };
  Plotly.newPlot('plotly', [data], layout, config);
};
