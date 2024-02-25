async function set_data_in_form(choice_id, input_values, keys_from_db) {

    // считываем query параметр
    const urlSearchParams = new URLSearchParams(window.location.search);
    const params = Object.fromEntries(urlSearchParams.entries());

    let current_staff;

    // Формат получаемых данных [id, name, title]
    await get(`/api/get_staff?id=${params["id"]}`).then(res => {
        current_staff = res
    }).catch(error => {
        console.log(error)
    })

    addDataInSelect("/api/get_post", choice_id, true)

    let data_values = {};

    for (let key of keys_from_db) {
        data_values[key] = current_staff[key]
    }

    SetInputs(input_values["input"], true, data_values);

    // Формат получаемых данных [id, title]
    await get("/api/get_post").then(data => {
        data
        let index_counter = 0;

        // добавление в select
        for (let index_data in data) {

            // Айдишник нужного поста для селекта
            if (current_staff["title"] === data[index_data]["title"]) {
                index_counter = index_data;
            }
        }

        document.getElementById(`${input_values["select"]}`).selectedIndex = data["index"]

    }).catch(error => {
        console.log(error)
    })

}

// Выполнить функцию выше при загрузке страницы
set_data_in_form("choice_post", {"select": ["choice_post"], "input": ["staff_name"]}, ["name"]);

// Получаем данные из формы
function get_data_from_input() {
    let choice = $("#choice_post").val();
    let name = $("#staff_name").val();
    let post;

    // проверка на выбранное поле
    if (choice !== "choice_not_in_list") {
        post = $("#choice_post :selected").text();
    } else {
        post = $("#post_name").val();
    }

    //console.log(name, post)
    return {"name": name, "posts_name": post}
}

async function add_staff_in_db() {
    // получаем данные из формы
    let data = get_data_from_input();

    // флаг на наличие пустых полей в форме
    let flag_empty = false;

    // если есть пусты поля(в том числе не выбранные даты) flag_empty=true
    for (let key in data) {
        if (data[key] === "") {
            flag_empty = true;
            break;
        }
    }

    if (!flag_empty) {
        // clearInputs();
        let data_posts;

        await post("/api/add_post", {"title": data["posts_name"]}).then(res => {
            console.log(res)
        }).catch(error => {
            console.log(error)
        })

        let post_id;

        // Формат получаемых данных [id, name, title(post)]
        await get("/api/get_post").then(res => {
            data_posts = res.reverse();
        }).catch(error => {
            console.log(error)
        })

        // Поиск необходимой должности (для id)
        for (let post in data_posts) {
            if (data_posts[post]["title"] === data["posts_name"]) {
                post_id = data_posts[post]["id"]
                break;
            }
        }

        const urlSearchParams = new URLSearchParams(window.location.search);
        const params = Object.fromEntries(urlSearchParams.entries());

        console.log({"id": params["id"], "name": data["name"], "posts_id": post_id});

        // Формат отправляемых данных ['id', 'name', 'posts_id']
        await patch("/api/edit_staff", {
            "id": Number(params["id"]),
            "name": data["name"],
            "posts_id": post_id
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