const get = async (url) => (await axios.get(url)).data;
const post = async (url, dict_) => (await axios.post(url, dict_)).data;
const patch = async (url, dict_) => (await axios.patch(url, dict_)).data;

async function del_row(url, item_id, row_id) {
    // Формат отправляемых данных ['id']
    await post(url, {"id": item_id}).then(res => {
        row_id.parentNode.removeChild(row_id);
        console.log(res);
    }).catch(error => {
        console.log(error);
    })
}

function shower(divId) {
    $("#" + divId).show();
    //console.log("Я появился")
}

function hider(divId) {
    $("#" + divId).hide();
    //console.log("Я скрылся") 
}

function GFG_Fun(value) {
    if (value !== "choice_not_in_list") {
        hider('hide_div')
    } else {
        shower('hide_div')
    }
}

function SetInputs(data_keys, set_many_data = false, value = "") {
    if (set_many_data) {
        for (key of data_keys) {
            // Очистить поля ввода
            for (key_value in value) {
                // Очистить поля ввода
                document.getElementById(key).value = value[key_value];
            }
        }
    } else {
        for (key of data_keys) {
            // Очистить поля ввода
            document.getElementById(key).value = value;
        }
    }

}

async function addDataInSelect(get_url, choice_id, choose_not_in_list = true, add_data = false, add_data_with_param = false, data_in_select = []) {
    // Формат получаемых данных [id, title]
    await get(get_url).then(data => {
        let select = document.getElementById(choice_id);
        let keys;
        let opt;

        if (add_data) {
            // добавление в select
            if (add_data_with_param) {
                for (let item of data) {
                    keys = [...data_in_select];

                    opt = document.createElement('option');

                    opt.value = item[keys[0]];
                    opt.innerHTML = item[keys[1]];

                    select.appendChild(opt);
                }
            } else {
                for (let item of data) {
                    keys = [...data_in_select];

                    opt = document.createElement('option');

                    opt.value = item[keys[0]];
                    opt.innerHTML = item[keys[1]] + ": " + item[keys[2]];

                    select.appendChild(opt);
                }
            }
        } else {
            // добавление в select
            for (let item of data) {
                let keys = Object.keys(item);

                let opt = document.createElement('option');

                opt.value = item[keys[0]];
                opt.innerHTML = item[keys[1]];

                select.appendChild(opt);
            }


            if (choose_not_in_list) {
                // элемент, которого нету в списке
                let opt = document.createElement('option');

                opt.value = "choice_not_in_list";
                opt.innerHTML = "Отсутствует в списке";

                select.appendChild(opt);
            }
        }
    }).catch(error => {
        console.log(error)
    })
}

function get_data_from_input(dict_input) {
    let data_dict = {};
    let choice;

    for (input_fields_key in dict_input["field"]) {
        let id_input_field = `#${dict_input["field"][input_fields_key]}`;
        let object_input_field = $(id_input_field);

        data_dict[input_fields_key] = object_input_field.val();
    }

    for (elections_key in dict_input["select"]) {
        let id_choice_filed = `#${dict_input["select"][elections_key]}`;
        let object_choice_field = $(id_choice_filed);

        choice = object_choice_field.val();
        // console.log($(`${id_choice_filed} :selected`).text())
        // console.log($(`#${elections_key}`).val())
        data_dict[elections_key] = choice !== "choice_not_in_list" ? $(`${id_choice_filed} :selected`).text() : $(`#${elections_key}`).val();
    }

    return data_dict;
}

function check_fields(data) {
    // если есть пусты поля(в том числе не выбранные даты)
    for (let key in data) {
        if (data[key] === "") {
            return true
        }
    }
    return false;
}

function compare(data_from_input, data_from_db, input_keys, db_keys, keys_output) {
    let value_output = [];
    for (let one_data of data_from_db) {
        let compare_list = [];

        for (let index in input_keys) {
            compare_list.push(one_data[db_keys[index]] === data_from_input[input_keys[index]])
        }

        if (Number(compare_list.reduce((compare_list, rec) => compare_list * rec)) === 1) {
            for (let key of keys_output) {
                value_output.push(one_data[key])
            }
        } else {
            console.log("Совпадений нет")
        }
    }
    return value_output;
}
