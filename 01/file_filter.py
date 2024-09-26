def file_filter(file, find_list, stop_list):
    find_list = set(find_list)
    stop_list = set(stop_list)

    for line in file:
        words = set(line.strip().lower().split())

        if words & stop_list:
            continue

        if words & find_list:
            yield line.strip()
