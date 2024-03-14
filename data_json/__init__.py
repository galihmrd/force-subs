class Data:
    def get_data(data, file_name):
        get_file = open(f"./data_json/{file_name}.txt").read().splitlines()
        return get_file

    def write_data(data, file_name):
        f = open(f"./data_json/{file_name}.txt", "a")
        user_list = open(f"./data_json/{file_name}.txt").read()
        if str(data) not in user_list:
            f.write(str(data))
            f.write("\n")
