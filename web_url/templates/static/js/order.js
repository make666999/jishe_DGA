document.addEventListener('DOMContentLoaded', function () {
    var ws = new WebSocket(`ws://${serverIp}/websocket_user_list_management`); // 替换为您的WebSocket服务地址
    ws.onmessage = function (event) {
        var data = JSON.parse(event.data);
        var tbody = document.querySelector("#orders tbody");
        tbody.innerHTML = ''; // 清空现有的表格行

        data.collections_data.forEach(function (item, index) {
            var row = tbody.insertRow(); // 在表格末尾添加一行
            var cell0 = row.insertCell(0);
            cell0.innerHTML = '<input class="form-check-input" type="checkbox">';

            var cell1 = row.insertCell(1);
            cell1.innerHTML = `<a href="#">#${index + 1}</a>`; // 使用index作为ID

            var cell2 = row.insertCell(2);
            cell2.textContent = item.collection_name;


            var cell3 = row.insertCell(3);
            // 检查item.latest_timestamp是否有值
            if (item.latest_timestamp && item.latest_timestamp !== "") {
                cell3.textContent = item.latest_timestamp;
            } else {
                cell3.textContent = "该主机今日未上线"; // 没有时间戳时显示的消息
            }

            var cell4 = row.insertCell(4);

            var dailyCount = Number(item.daily_count); // 尝试将其转换为数字
            cell4.textContent = `${isNaN(dailyCount) ? '0' : dailyCount.toFixed(2)}`;


            var cell5 = row.insertCell(5);
              cell5.innerHTML = `<span class="badge bg-success">undefined</span>`; // "未知"或者您想显示的任何默认文本
            if (typeof item.latest_domain_type === "undefined" || item.latest_domain_type === null) {
                // 如果latest_domain_type是undefined或null，设置徽章为绿色
                cell5.innerHTML = `<span class="badge bg-success">undefined</span>`; // "未知"或者您想显示的任何默认文本
            }
            // else {
            //     // 如果latest_domain_type有其他值，设置徽章为红色
            //     cell5.innerHTML = `<span class="badge bg-danger">${item.latest_domain_type}</span>`;
            // }


            var cell6 = row.insertCell(6);
            cell6.className = 'text-end';
            cell6.innerHTML = `
                <div class="d-flex">
                    <div class="dropdown ms-auto">
                        <a href="#" data-bs-toggle="dropdown" class="btn btn-floating" aria-haspopup="true" aria-expanded="false">
                            <i class="bi bi-three-dots"></i>
                        </a>
                        <div class="dropdown-menu dropdown-menu-end">
                            <a href="#" class="dropdown-item">Show</a>
                            <a href="#" class="dropdown-item">Edit</a>
                            <a href="#" class="dropdown-item">Delete</a>
                        </div>
                    </div>
                </div>`;
        });
    };
});

