from excel_creator import generate_invoices2
import os
import subprocess


# 2 - trying to create the file in a temporary directory:
def test_generate_invoices_with_year_only(tmpdir):
    year = "2024"
    output_dir = tmpdir / "FACTURAS"
    year_folder = os.path.join(output_dir, str(year))
    # Create the directory structure
    if not os.path.exists(year_folder):
        os.makedirs(year_folder)
    generate_invoices2(year_filter=year, output_dir=output_dir)
    # Check if the folder was created:
    assert os.path.exists(year_folder), f"Folder {year_folder} was not created"
    # Check if any files exist in the year folder:
    files = os.listdir(year_folder)
    assert len(files) > 0, f"No files were created in {year_folder}"
    # Open the directory in Finder:
    subprocess.run(["open", output_dir])


# 1 - basic test to check if the function runs without errors (no file created):
# def test_generate_invoices():
# generate_invoices(year_filter="2024", month_filter="03")
# assert True


# 2 - check if file actually created and where:
# def test_generate_invoices_with_filters():
#    year = "2024"
#    month = "3"
#    year_folder = f"generated_excels/FACTURAS/{year}"
#    file_path = f"{year_folder}/{month}.xlsx"
#    generate_invoices(year_filter=year, month_filter=month)
# Check if the folder was created:
#    assert os.path.exists(year_folder), f"Folder {year_folder} was not created"
# Check if the file exists:
#    assert os.path.isfile(file_path), f"File {file_path} was not created"
# Clean up after the test (otherwise, files are generated):
#    if os.path.isfile(file_path):
#        os.remove(file_path)
#    if os.path.exists(year_folder):
#        os.rmdir(year_folder)
