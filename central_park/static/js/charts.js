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
