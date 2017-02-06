// Generated by CoffeeScript 1.10.0
$(function() {
  var hits_id, url;
  hits_id = $('#hits_id').attr('data-value');
  PeriodLS = $('#PeriodLS').attr('data-value');
  console.log(hits_id, PeriodLS);
  //url = '/hits/' + hits_id + '/data';
  //$.getJSON(url, function(result) {
    
  //  return foldPlot(lcdata, periodLS);
  //});
  
  return $("#vote").click(function(e) {
    var label;
    e.preventDefault();
    label = $("#select-star").find(':selected').val();
    url = '/hits/' + hits_id + '/';
    return $.post(url, {
      'label': label
    }, function(result) {
      var new_url, next, point;
      next = result['next'];
      point = result['point'];
      if (point >= 1) {
        point = "+" + point;
        new_url = '/hits/' + next + '/';
        return $("#point").text(point).removeAttr('hidden').animate({
          bottom: '150px',
          opacity: '0.0'
        }, 750, function() {
          window.history.pushState({}, hits_id, url);
          return window.location.replace(new_url);
        });
      } else {
        new_url = '/hits/' + next + '/';
        window.history.pushState({}, hits_id, url);
        return window.location.replace(new_url);
      }
    });
  });
});
