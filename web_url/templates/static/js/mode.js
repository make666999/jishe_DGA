 document.getElementById('btn-plan-1').addEventListener('click', function() {
        showChart('chart_1');
    });
    document.getElementById('btn-plan-2').addEventListener('click', function() {
        showChart('chart_2');
    });
    document.getElementById('btn-plan-3').addEventListener('click', function() {
        showChart('chart_3');
    });

    // 显示对应的chart，隐藏其他的
    function showChart(chartId) {
        // 隐藏所有chart
        var charts = document.querySelectorAll('[id^="chart_"]');
        charts.forEach(function(chart) {
            chart.style.display = 'none';
        });

        // 显示指定的chart
        document.getElementById(chartId).style.display = 'block';
    }

    async function sendData() {
    const formData = {
        Local: document.getElementById('local').value,
        Device_Name: document.getElementById('deviceName').value,
        new_model_value: document.getElementById('modelValue').value
    };

    const response = await fetch('/api/send_data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    });

    const data = await response.json();
    alert(data.message);

