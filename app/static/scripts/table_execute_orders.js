function addDataInTable(table_id) {
    // Формат получаемых данных [id, client_name, warranty_period, repair_type, repair_cost, 
    // order_execution_date, message, date_of_receipt, order_receipt_date]
    get("/api/get_execution").then(data => {
        let table = document.getElementById(table_id);

        // Список ожидаемых прилетающих ключей
        let list_tag = ["order_id", "client_name", "repair_type",
            "repair_cost", "order_execution_date", "message", "date_of_receipt"];

        // Бежим по индексам даты и по ключам из list_tag, вставляем соответствующие значения в таблицу
        for (let item of data) {
            let new_row = table.insertRow(table.rows.length);

            let funny_data = {...item};
            funny_data.message = item.message === 1 ? "Работа успешно выполнена" : "Не удалось починить";

            for (let tag of list_tag) {
                new_row.insertCell().innerHTML = funny_data[tag];
            }

            let warranty_date = new Date((item["warranty_period"]));
            let order_receipt_date = new Date(item["order_receipt_date"]);

            // Проверка на наличие гарантии
            new_row.insertCell().innerHTML = warranty_date.getTime() < order_receipt_date.getTime() ? item["repair_cost"] : 0;

            // Вставляем данные в ячейки новой строки
            new_row.insertCell().innerHTML = `
                <div class="btn-group">
                    <button type="button" class="btn btn-outline-dark dropdown-toggle" data-bs-toggle="dropdown" aria-expanded="false">
                        Действие
                    </button>
                    <ul class="dropdown-menu">
                        <li><a class="dropdown-item" href="edit_execute_orders?id=${item["id"]}">Изменить</a></li>
                        <li><hr class="dropdown-divider"></li>
                        <li><a class="dropdown-item" onclick="del_row('/api/delete_execution', ${item["id"]}, ${"this.parentNode.parentNode.parentNode.parentNode.parentNode"})">Удалить</a></li>
                    </ul>
                </div>
            `;
        }
    }).catch(error => {
        console.log(error);
    })
}

addDataInTable("table_execute_orders");