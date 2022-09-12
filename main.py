import data, data_rep


def main():
    users_data = data.get()
    data_rep.start(users_data)


if __name__ == "__main__":
    try:
        main()
    except Exception as err:
        print('Exception:', err)
    else:
        print('Completed successfully!')
