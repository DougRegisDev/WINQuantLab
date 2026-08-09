from data.loader import load_data


def main():
    """
    Pono de entrada da aplicação.
    """
    dataframe = load_data("dados/winfut.csv")
    print(dataframe.head())


if __name__ == "__main__":
    main()
