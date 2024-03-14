class Data:
    def get_data(data, file_name):
        try:
            get_file = open(f"./data_json/{file_name}.txt").read().splitlines()
            return get_file
        except FileNotFoundError:
            pass

    def write_data(data, file_name):
        f = open(f"./data_json/{file_name}.txt", "a")
        user_list = open(f"./data_json/{file_name}.txt").read()
        if str(data) not in user_list:
            f.write(str(data))
            f.write("\n")

    def del_data(del_data, file_name):
        f = open(f"./data_json/{file_name}.txt", "a")
        read_data = open(f"./data_json/{file_name}.txt").read().splitlines()
        open(f"./data_json/{file_name}.txt", "w")
        for data in read_data:
            if data != del_data:
                f.write(str(data))
                f.write("\n")
