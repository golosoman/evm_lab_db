async function addDataInSelect_2(choice_id) {
    // Формат получаемых данных [id, name, title]
    await get("/api/get_staff").then(res => {

        let data = res;
        let select = document.getElementById(choice_id);

        //console.log(data)

        console.log(choice_id)
        // добавление в select
        for (let index_data in data) {
            //console.log(data[index_data]["title"])
            let opt = document.createElement('option');
            // id - id в БД
            opt.value = data[index_data]["id"];
            opt.innerHTML = data[index_data]["title"] + ": " + data[index_data]["name"];
            select.appendChild(opt);
        }

        console.log(data)

    }).catch(error => {
        console.log(error)
    })

    const urlSearchParams = new URLSearchParams(window.location.search);
    const params = Object.fromEntries(urlSearchParams.entries());

    let execution;
    await get(`/api/get_execution?id=${params.id}`).then(res => {
            execution = res
        }
    ).catch(error => {
        console.log(error)
    })

    console.log(execution)
    elem = document.getElementById("order_id")
    elem.value = execution['order_id']
    elem = document.getElementById("type_repair")
    elem.value = execution['repair_type']
    elem = document.getElementById("repair_cost")
    elem.value = execution['repair_cost']
    elem = document.getElementById("date_execute")
    elem.value = execution['order_execution_date']
    elem = document.getElementById("receipt_date")
    elem.value = execution['order_receipt_date']

    elem = document.getElementById("choice_select")

    if (execution['message'] == 1) {
        elem.selectedIndex = 0
    } else {
        elem.selectedIndex = 1
    }

    let performer;
    await get(`/api/get_performer_by_execution?id=${params.id}`).then(res => {
        performer = res['staff_id']
    }).catch(error => {
        console.log(error)
    })

    await get(`/api/get_staff?id=${performer}`).then(res => {
        console.log(res)
        elem = document.getElementById("executer")
        elem.selectedIndex = res['id'] - 1
    }).catch(error => {
        console.log(error)
    })
}

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

        let type_id;
        await get(`/api/get_type_by_desc?description=${(document.getElementById("type_repair")).value}`).then(res => {
            type_id = res['id']
            console.log(res)
        }).catch(err => {
            console.log(err)
        })

        const urlSearchParams = new URLSearchParams(window.location.search);
        const params = Object.fromEntries(urlSearchParams.entries());
        let message;

        await patch("/api/edit_execution", {
            "id": params.id,
            "order_id": data["order_id"],
            "types_of_repairs_id": type_id,
            "repair_cost": data["repair_cost"],
            "order_execution_date": data["date_execute"],
            "message": data["message"],
            "date_of_receipt": data["receipt_date"]
        }).then(res => {
            console.log(res)
        }).catch(error => {
            console.log(error)
        })
    } else {
        console.log("Не все поля заполнены!");
    }
}

// Выполнить функцию выше при загрузке страницы
addDataInSelect("/api/get_order", "order_id", false, true, true, ["id", "id"]);

addDataInSelect_2("executer");
