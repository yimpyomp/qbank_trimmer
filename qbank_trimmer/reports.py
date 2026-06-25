def save_catalog_blank_results(
        matched_ids,
        missing_from_catalog,
        missing_blank_pages,
        output_path="catalog_blank_results.txt"
):
    """
    Save a report showing how well blank-question pages were matched
    to the existing answer-key catalog.
    """

    with open(output_path, "w") as file:
        file.write("Catalog Blank Results\n")
        file.write("=====================\n\n")

        file.write("Summary\n")
        file.write("-------\n")
        file.write(f"Matched blank questions: {len(matched_ids)}\n")
        file.write(f"Blank IDs not found in answer catalog: {len(missing_from_catalog)}\n")
        file.write(f"Answer catalog IDs missing blank pages: {len(missing_blank_pages)}\n\n")

        file.write("Blank IDs not found in answer catalog\n")
        file.write("-------------------------------------\n")

        if missing_from_catalog:
            for question_id, page_index in missing_from_catalog:
                file.write(f"- {question_id} on blank PDF page {page_index + 1}\n")
        else:
            file.write("None\n")

        file.write("\nAnswer catalog IDs missing blank pages\n")
        file.write("-------------------------------------\n")

        if missing_blank_pages:
            for question_id in missing_blank_pages:
                file.write(f"- {question_id}\n")
        else:
            file.write("None\n")