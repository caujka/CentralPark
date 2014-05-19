google.load('visualization', '1.0', {'packages':['corechart']});
      function drawChart(str) {
        
        var data = new google.visualization.DataTable();
        
        data.addColumn('string', 'car_numbers');
        data.addColumn('number', 'Price');
        data.addRows(str);

        var options = {};
        var chart = new google.visualization.PieChart(document.getElementById('chart_div'));
        chart.draw(data, options);
      }

      function drawDayStat(str) {
        var data = new google.visualization.DataTable();        
        data.addColumn('string', 'hours');
        data.addColumn('number', 'car count');
        data.addColumn('number', 'price');
        data.addRows(str);

        var options = {
          title: 'Parking place load during day',
          hAxis: {title: 'Hours', titleTextStyle: {color: 'black'}}
        };

        var bar_chart = new google.visualization.LineChart(document.getElementById('day_statistic_div'));
        bar_chart.draw(data, options);
      }

      function drawYearStat(str) {
        var data = new google.visualization.DataTable();        
        data.addColumn('string', 'days');
        data.addColumn('number', 'car count');
        data.addRows(str);

        var options = {
          title: 'Parking place load during year',
          hAxis: {title: 'Date', titleTextStyle: {color: 'black'}}
        };

        var polyline_chart = new google.visualization.LineChart(document.getElementById('year_statistic_div'));
        polyline_chart.draw(data, options);
      }

