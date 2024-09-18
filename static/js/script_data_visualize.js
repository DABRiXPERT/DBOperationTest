// 參數名稱，與 data 對應
var parameterNames = ['Parameter A', 'Parameter B', 'Parameter C', 'Parameter D', 'Parameter E', 'Parameter F', 'Parameter G', 'Parameter H'];

// 動態生成圖表的容器
var container = document.getElementById('charts-container');
parameterNames.forEach(function(name, index) {
    // 為每個參數創建一個 div 來放置圖表
    var chartDiv = document.createElement('div');
    chartDiv.id = 'chart-' + index;
    container.appendChild(chartDiv);

    // 配置ApexCharts圖表
    var options = {
        chart: {
            type: 'line',
            height: 350
        },
        markers: {
            size: 5
        },
        stroke: {
            curve: 'smooth'
        },
        series: [{
            name: name,
            data: data[index]  // 對應的參數數據
        }],
        xaxis: {
            categories: labels  // X軸的 converted_date
        },
        title: {
            text: name + ' over Time',
            align: 'left'
        },
        yaxis: {
            title: {
                text: name + ' Value'
            }
        }
    };

    // 為每個參數生成一個圖表
    var chart = new ApexCharts(document.querySelector('#chart-' + index), options);
    chart.render();
});