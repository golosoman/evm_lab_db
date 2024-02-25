async function add_staff_in_db() {
    // получаем данные из формы
    let data = get_data_from_input({"select": {"posts_name": "choice_post"}, "field": {"name": "staff_name"}});
    // console.log(data)

    if (!check_fields(data)) {
        // Формат отправляемых данных ['title']
        await post("/api/add_post", {"title": data["posts_name"]}).then(res => {
            console.log(res)
        }).catch(error => {
            console.log(error)
        })


        // Формат получаемых данных [id, name, title(post)]
        let post_id;
        await get("/api/get_post").then(res => {
            let data_posts = res.reverse();

            post_id = compare(data, data_posts, ["posts_name"], ["title"], ["id"])[0];

            // // Поиск необходимой должности (ее id)
            // for (let post of data_posts) {
            //     if (post["title"] === data["posts_name"]) {
            //         post_id = post["id"]
            //         break;
            //     }
            // }
        }).catch(error => {
            console.log(error)
        })

        // Формат отправляемых данных ['name', 'posts_id']
        await post("/api/add_staff", {"name": data["name"], "posts_id": post_id}).then(res => {
            console.log(res)
        }).catch(error => {
            console.log(error)
        })

        SetInputs(["staff_name", "posts_name"])
    } else {
        // info
        console.log("Не все поля заполнены!");
    }
}

addDataInSelect("/api/get_post", "choice_post");
