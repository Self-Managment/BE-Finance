API = "/api/"


class UserURLS:
    user = "user"
    base_url = f"{API}{user}"

    # POST
    register = "/register/"
    register_url = f"{base_url}{register}"

    # POST
    login = "/login/"
    login_url = f"{base_url}{login}"

    # GET
    user_data = "/user_data/"
    user_data_url = f"{base_url}{user_data}"


class DeskURLS:
    desk = "desk"
    base_url = f"{API}{desk}"

    # POST
    create_desk = "/create_desk/"
    create_desk_url = f"{base_url}{create_desk}"
    # GET
    get_desk_list = "/get_desk_list/"
    get_desk_list_url = f"{base_url}{get_desk_list}"
    # PATCH
    edit_desk = "/edit_desk/"
    edit_desk_url = f"{base_url}{edit_desk}"
    # DELETE
    delete_desk = "/delete_desk/"
    delete_desk_url = f"{base_url}{delete_desk}"

    # POST
    create_type = "/create_type/"
    create_type_url = f"{base_url}{create_type}"
    # GET
    get_task_type_list = "/get_task_type_list/"
    get_task_type_list_url = f"{base_url}{get_task_type_list}"

    # POST
    create_task = "/create_task/"
    create_task_url = f"{base_url}{create_task}"
    # GET
    get_task_list = "/get_task_list/"
    get_task_list_url = f"{base_url}{get_task_list}"
