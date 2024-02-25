async function add_order_in_db() {
    // Получаем данные из формы
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
        let brand_id;

        // Формат получаемых данных [id, name]
        await get("/api/get_brands").then(res => {
            let data_brands = res.reverse();
            brand_id = compare(data, data_brands, ["brand_name"], ["name"], ["id"])[0];

        }).catch(error => {
            console.log(error)
        })

        console.log({
            "name": data["product_name"], "brands_id": brand_id, "model": data["model_name"],
            "technical_specification": data["text_specification"], "warranty_period": data["warranty_date"]
        })

        // Формат отправляемых данных ['name', 'brands_id', 'model', 'technical_specification', 'warranty_period']
        await post("/api/add_product", {
                "name": data["product_name"], "brands_id": brand_id, "model": data["model_name"],
                "technical_specification": data["text_specification"], "warranty_period": data["warranty_date"]
            }
        ).then(res => {
            console.log(res)
        }).catch(error => {
            console.log(error)
        })

        // данные таблицы продукт из БД и id нужного
        let product_id;

        // Формат получаемых данных [id, name, brand_name, model, technical_specifications, warranty_period]
        await get("/api/get_product").then(res => {
            let products = res.reverse();
            product_id = compare(data, products, ["product_name", "brand_name", "model_name", "text_specification", "warranty_date"],
                ["name", "brand_name", "model", "technical_specifications", "warranty_period"], ["id"])[0];
        }).catch(error => {
            console.log(error)
        })

        // данные таблицы продукт из БД и id нужного
        let client_id;

        // Формат получаемых данных [id, name]
        await get("/api/get_client").then(res => {
            let clients = res.reverse();
            client_id = compare(data, clients, ["client_name"], ["name"], ["id"])[0];
        }).catch(error => {
            console.log(error)
        })

        console.log({
            "clients_id": client_id, "product_id": product_id,
            "order_receipt_date": data["date_order_acceptance"]
        })

        // Формат отправляемых данных ['clients_id', 'product_id', 'order_receipt_date']
        await post("/api/add_order", {
            "clients_id": client_id, "product_id": product_id,
            "order_receipt_date": data["date_order_acceptance"]
        }).then(res => {
            console.log(res)
        }).catch(error => {
            console.log(error)
        })

        SetInputs(["product_name", "brand_name", "model_name", "text_specification", "garantity_period",
            "client_name", "telephone_number", "date_order_acceptance"])
    } else {
        // info
        console.log("Не все поля заполнены!");
    }
}

// Выполнить функцию выше при загрузке страницы
addDataInSelect("/api/get_brands", "choice_brand");