function broken_line_chart(data) {
    let brokenEcharts = echarts.init(document.getElementById("broken_line"));

    window.addEventListener('resize', function () {
        myChart.resize();
    });


    let data1 = data['1室1厅']
    let data2 = data['2室1厅']
    let data3 = data['2室2厅']
    let data4 = data['3室2厅']

    echartsDate = [];
    for (var i = 0; i < data['date_li'].length; i++) {
        d = data['date_li'][i]
        echartsDate.push(d);
    }

    let option = {
        tooltip: {
            trigger: 'axis',
        },
        legend: {
            data: ['3室2厅', '2室2厅', '2室1厅', '1室1厅']
        },
        grid: {
            containLabel: true,
            left: '5%',
            right: '4%',
            bottom: '3%'
        },

        xAxis: {
            type: 'category',
            boundaryGap: false,
            data: echartsDate
        },
        yAxis: {
            type: 'value',
            name: '平均价格/元',
            nameLocation: 'center',
            nameGap: 30,
            axisLine: { show: true }
        },
        series: [

            {
                name: '3室2厅',
                type: 'line',
                data: data4
            },
            {
                name: '2室2厅',
                type: 'line',
                data: data3
            },
            {
                name: '2室1厅',
                type: 'line',
                data: data2
            },
            {
                name: '1室1厅',
                type: 'line',
                data: data1
            }
        ]
    }

    option && brokenEcharts.setOption(option, true);
}