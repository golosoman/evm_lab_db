function addDataInTable(table_id) {
    // Формат получаемых данных [id, client_name, product_name, brand, model, warranty_period, order_receipt_date]
    get("/api/get_order").then(data => {
        let table = document.getElementById(table_id);
        let list_tag = ["id", "client_name", "product_name",
            "brand", "model", "warranty_period", "order_receipt_date"];

        // Бежим по данным из даты, вставляем соответствующие значения в таблицу
        for (let item of data) {
            let new_row = table.insertRow(table.rows.length);

            for (let key of list_tag) {

                // Проверка на наличие гарнатийного периода
                if (key === "warranty_period") {

                    let warranty_date = new Date((item[key]));
                    let order_receipt_date = new Date(item["order_receipt_date"]);

                    // наличие гарантии
                    new_row.insertCell().innerHTML = warranty_date.getTime() < order_receipt_date.getTime() ? "Нет" : "Да";
                    continue;
                }

                // Вставляем данные в ячейки новой строки
                new_row.insertCell().innerHTML = item[key];
            }

            // Вставляем кнопки в ячейки
            new_row.insertCell().innerHTML = `
            <div class="btn-group">
                <button type="button" class="btn btn-outline-dark dropdown-toggle" data-bs-toggle="dropdown" aria-expanded="false">
                    Действие
                </button>
                <ul class="dropdown-menu">
                    <li><a class="dropdown-item" href="edit_data_order_table?id=${item["id"]}">Изменить</a></li>
                    <li><hr class="dropdown-divider"></li>
                    <li><a class="dropdown-item" onclick="del_row('/api/delete_order', ${item["id"]}, ${"this.parentNode.parentNode.parentNode.parentNode.parentNode"})">Удалить</a></li>
                </ul>
            </div>
        `;
        }
    }).catch(error => {
        console.log(error)
    })
}

// Отработка функции при загрузке окна
addDataInTable("table_orders");