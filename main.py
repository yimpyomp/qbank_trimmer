from qbank_trimmer.pdf_tools import initial_config
from qbank_trimmer.catalog import generate_catalog, save_catalog, catalog_blank

def main():
    print("Starting trimmer")

    print("Checking for combined files")
    initial_config()

    print("Generating catalog")
    catalog = generate_catalog()
    catalog_blank(catalog)

    print("Saving catalog")
    save_catalog(catalog)

    print("Done")


if __name__ == "__main__":
    main()