function addDataInTable(table_id) {
    // Формат получаемых данных [id, name, title(post)]
    get("/api/get_staff").then(data => {
        let table = document.getElementById(table_id);
        // let url_del = new URL("/api/delete_staff");

        // Бежим по индексам даты и по ключам, вставляем соответствующие значения в таблицу
        for (let item of data) {
            let new_row = table.insertRow(table.rows.length);

            for (let key in item) {
                new_row.insertCell().innerHTML = item[key];
            }

            new_row.insertCell().innerHTML = `
                <div class="btn-group">
                    <button type="button" class="btn btn-outline-dark dropdown-toggle" data-bs-toggle="dropdown" aria-expanded="false">
                        Действие
                    </button>
                    <ul class="dropdown-menu">
                        <li><a class="dropdown-item" href="edit_staff?id=${item["id"]}">Изменить</a></li>
                        <li><hr class="dropdown-divider"></li>
                        <li><a class="dropdown-item" onclick="del_row('/api/delete_staff', ${item["id"]}, ${"this.parentNode.parentNode.parentNode.parentNode.parentNode"})">Удалить</a></li>
                    </ul>
                </div>
            `;
        }
    }).catch(error => {
        console.log(error)
    })
}

addDataInTable("table_orders");