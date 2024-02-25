async function add_execute_order_in_db() {
    // Получаем данные из формы
    let data = get_data_from_input({
        "select": {"staff": "executer", "message": "choice_select"},
        "field": {
            "order_id": "order_id", "type_repair": "type_repair", "repair_cost": "repair_cost",
            "date_execute": "date_execute", "receipt_date": "receipt_date"
        }
    });

    data["message"] = data["message"] === "Задача выполнена" ? 1 : 0;

    if (!check_fields(data)) {
        // формат отправляемых данных ['description']
        await post("/api/add_types_of_repairs", {"description": data["type_repair"]}).then(res => {
            console.log(res)
        }).catch(error => {
            console.log(error)
        })


        // текущий связанный заказ, необходим далее
        let current_order;

        // Формат получаемых данных [id, client_name, product_name, brand, model, warranty_period, order_receipt_date]
        await get(`/api/get_order?id=${Number(data["order_id"])}`).then(res => {
            current_order = res;
        }).catch(error => {
            console.log(error)
        })


        // вычисление стоимость исполнения услуг
        let date_order_receipt = new Date(current_order["order_receipt_date"]);
        let warranty_date = new Date(data["warranty_date"]);
        let payment = warranty_date.getTime() < date_order_receipt.getTime() ? data["repair_cost"] : 0;

        // данные таблицы заказов из БД и дата начала заказа нужного
        let id_types_of_repair;

        // Формат получаемых данных [id, desc]
        await get("/api/get_types_of_repairs").then(res => {
            let data_types_of_repairs = res.reverse();

            // Поиск необходимой починки (для id)
            for (let type_repair of data_types_of_repairs) {
                if (type_repair["desc"] === data["type_repair"]) {
                    id_types_of_repair = type_repair["id"]
                    break;
                }
            }
        }).catch(error => {
            console.log(error)
        })

        console.log({
            "order_id": data["order_id"],
            "types_of_repairs_id": id_types_of_repair,
            "repair_cost": data["repair_cost"],
            "order_execution_date": data["date_execute"],
            "message": data["message"],
            "date_of_receipt": data["receipt_date"],
            "amount_of_payment": payment
        })

        // формат отправляемых данных (['order_id', 'types_of_repairs_id', 'repair_cost',
        // 'order_execution_date' 'message', 'date_of_receipt', 'amount_of_payment']
        await post("/api/add_execution", {
            "order_id": data["order_id"],
            "types_of_repairs_id": id_types_of_repair,
            "repair_cost": data["repair_cost"],
            "order_execution_date": data["date_execute"],
            "message": Boolean(data["message"]),
            "date_of_receipt": data["receipt_date"],
            "amount_of_payment": payment
        }).then(res => {
            console.log(res)
        }).catch(error => {
            console.log(error)
        })

        let execute_order_id;

        // Формат получаемых данных [id, client_name, warranty_period, repair_type, repair_cost, 
        // order_execution_date, message, date_of_receipt, order_receipt_date]
        await get("/api/get_execution").then(res => {
            let execute_orders = res.reverse();

            let data_keys = {
                "id": current_order["id"],
                "type_repair": data["type_repair"],
                "repair_cost": data["repair_cost"],
                "date_execute": data["date_execute"],
                "message": Number(data["message"]),
                "receipt_date": data["receipt_date"],
                "payment": payment
            };

            execute_order_id = compare(data_keys, execute_orders, ["id", "repair_type", "repair_cost", "order_execution_date",
                "message", "date_of_receipt"], ["order_id", "type_repair", "repair_cost", "date_execute", "message", "receipt_date"], ["id"])[0]

        }).catch(error => {
            console.log(error)
        })

        // данные таблицы продукт из БД и id нужного
        let staff_id;
        let post_and_name = data["staff"].split(": ");
        // Формат получаемых данных [id, name, title]
        await get("/api/get_staff").then(res => {
            let staffs = res.reverse();

            // Поиск id добавленного исполненного заказа
            for (let staff_index in staffs) {
                if (
                    staffs[staff_index]["title"] === post_and_name[0] &&
                    staffs[staff_index]["name"] === post_and_name[1]
                ) {
                    staff_id = staffs[staff_index]["id"];
                    break;
                }
            }
        }).catch(error => {
            console.log(error)
        })

        console.log({"execution_of_orders_id": execute_order_id, "staff_id": staff_id});
        // Формат отправляемых данных ['execution_of_orders_id', 'staff_id']
        await post("/api/add_performer", {"execution_of_orders_id": execute_order_id, "staff_id": staff_id}
        ).then(res => {
            console.log(res)
        }).catch(error => {
            console.log(error)
        })

        SetInputs(["type_repair", "repair_cost", "date_execute", "receipt_date"])
    } else {
        console.log("Не все поля заполнены!");
    }
}

addDataInSelect("/api/get_staff", "executer", false, true, false, ["id", "title", "name"]);

addDataInSelect("/api/get_order", "order_id", false, true, true, ["id", "id"]);
