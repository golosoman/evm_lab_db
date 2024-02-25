async function set_data_in_form(choice_id, input_values, keys_from_db) {
    // считываем query параметр
    const urlSearchParams = new URLSearchParams(window.location.search);
    const params = Object.fromEntries(urlSearchParams.entries());

    let current_order;
    let data_values = {};

    // Формат получаемых данных [id, client_name, product_name, brand, model, warranty_period, order_receipt_date]
    await get(`/api/get_order?id=${params['id']}`).then(res => {
        current_order = res;
        data_values["product_name"] = current_order["product_name"];
        data_values["client_name"] = current_order["client_name"];
        data_values["warranty_period"] = current_order["warranty_period"];
        data_values["order_receipt_date"] = current_order["order_receipt_date"];
    }).catch(error => {
        console.log(error)
    })

    await get(`/api/get_product?id=${current_order["product_id"]}`).then(res => {
        let products = res;
        data_values["model"] = products["model"];
        data_values["technical_specifications"] = products["technical_specifications"];
    }).catch(error => {
        console.log(error)
    })

    // Формат получаемых данных [id, name, phoneNumber]
    await get("/api/get_client").then(res => {
        let clients = res.reverse();
        data_values["phoneNumber"] = compare(current_order, clients, ["client_name"], ["name"], ["id"])[0];
    }).catch(error => {
        console.log(error)
    })

    console.log(data_values["warranty_period"]);

    addDataInSelect("/api/get_brands", choice_id);

    SetInputs(input_values["input"], true, data_values);

    // Формат получаемых данных [id, name]
    await get("/api/get_brands").then(data => {
        data
        let index_counter = 0;

        // добавление в select
        for (let index_data in data) {

            // Айдишник нужного брэнда для селекта
            if (current_order["brand"] === data[index_data]["name"]) {
                index_counter = index_data;
            }
        }

        document.getElementById(`${input_values["select"]}`).selectedIndex = data[index_counter]

    }).catch(error => {
        console.log(error)
    })

}

// "choice_brand"

// Выполнить функцию выше при загрузке страницы
set_data_in_form("choice_brand", {
    "select": ["choice_brand"], "input": ["product_name", "model_name", "text_specification",
        "garantity_period", "client_name", "telephone_number", "date_order_acceptance"]
}, ["product_name", "model_name",
    "text_specification", "warranty_period", "client_name", "phoneNumber", "order_receipt_date"])

async function add_order_in_db() {

    let data = get_data_from_input({
        "select": {"brand_name": "choice_brand"},
        "field": {
            "product_name": "product_name",
            "model_name": "model_name",
            "text_specification": "text_specification",
            "warranty_date": "garantity_period",
            "client_name": "client_name",
            "telephone_number": "telephone_number",
            "date_order_acceptance": "date_order_acceptance"
        }
    });

    if (!check_fields(data)) {

        const urlSearchParams = new URLSearchParams(window.location.search);
        const params = Object.fromEntries(urlSearchParams.entries());

        // Формат отправляемых данных [name]
        await post("/api/add_client", {
            "name": data["client_name"],
            "phoneNumber": data["telephone_number"]
        }).then(res => {
            console.log(res)
        }).catch(error => {
            console.log(error)
        })

        // Формат отправляемых данных [brand_name]
        await post("/api/add_brand", {"brand_name": data["brand_name"]}).then(res => {
            console.log(res)
        }).catch(error => {
            console.log(error)
        })

        // данные таблицы брэнды из БД и id нужного
        let data_brands;
        let brand_id;

        // Формат получаемых данных [id, name]
        await get("/api/get_brands").then(res => {
            data_brands = res.reverse();
        }).catch(error => {
            console.log(error)
        })

        for (let brand_index in data_brands) {
            if (data_brands[brand_index]["name"] === data["brand_name"]) {
                brand_id = data_brands[brand_index]["id"];
                break;
            }
        }

        // данные таблицы продукт из БД и id нужного
        let products;
        let product_id;

        // Формат получаемых данных [id, name, brand_name, model, technical_specifications, warranty_period]
        await get("/api/get_product").then(res => {
            products = res.reverse();
        }).catch(error => {
            console.log(error)
        })


        function findIndex(products, data) {
            for (let product of products) {
                console.log(product, data)
                if (
                    product["name"] === data["product_name"] &&
                    product["brand_name"] === data["brand_name"] &&
                    product["model"] === data["model_name"] &&
                    product["technical_specifications"] === data["text_specification"] &&
                    product["warranty_period"] === data["warranty_date"]
                ) {
                    product_id = product["id"];
                    break;
                }
            }
        }

        // Поиск id добавленного продукта
        for (let product_index in products) {
            console.log(products[product_index], data)
            if (
                products[product_index]["name"] === data["product_name"] &&
                products[product_index]["brand_name"] === data["brand_name"] &&
                products[product_index]["model"] === data["model_name"] &&
                products[product_index]["technical_specifications"] === data["text_specification"] &&
                products[product_index]["warranty_period"] === data["warranty_date"]
            ) {
                product_id = products[product_index]["id"];
                break;
            }
        }
        // console.log(current_order);
        // Формат отправляемых данных ['id', 'name', 'brands_id', 'model', 'technical_specification', 'warranty_period']
        await patch("/api/edit_product", {
                "id": product_id, "name": data["product_name"], "brands_id": brand_id, "model": data["model_name"],
                "technical_specification": data["text_specification"], "warranty_period": data["warranty_date"]
            }
        ).then(res => {
            console.log(res)
        }).catch(error => {
            console.log(error)
        })

        // данные таблицы продукт из БД и id нужного
        let clients;
        let client_id;

        // Формат получаемых данных [id, name]
        await get("/api/get_client").then(res => {
            clients = res.reverse();
        }).catch(error => {
            console.log(error)
        })

        // Поиск id добавленного продукта
        for (let client_index in clients) {
            if (clients[client_index]["name"] === data["client_name"]) {
                client_id = clients[client_index]["id"];
                break;
            }
        }

        console.log({
            "clients_id": client_id, "product_id": product_id,
            "order_receipt_date": data["date_order_acceptance"]
        })

        // Формат отправляемых данных ['clients_id', 'product_id', 'order_receipt_date']
        await patch("/api/edit_order", {
            "clients_id": client_id, "product_id": product_id,
            "order_receipt_date": data["date_order_acceptance"]
        }).then(res => {
            console.log(res)
        }).catch(error => {
            console.log(error)
        })
    } else {
        // info
        console.log("Не все поля заполнены!");
    }
}


