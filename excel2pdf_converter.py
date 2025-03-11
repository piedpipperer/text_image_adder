import os
import subprocess


def excel_to_pdf(excel_path, output_pdf_path):
    """
    Converts an Excel file to PDF using LibreOffice's command-line interface.

    :param excel_path: Path to the Excel file (.xlsx)
    :param output_pdf_path: Path where the PDF will be saved
    """
    if not os.path.exists(excel_path):
        raise FileNotFoundError(f"{excel_path} not found.")

    # Use LibreOffice to convert Excel to PDF
    try:
        command = [
            "libreoffice",
            "--headless",
            "--convert-to",
            "pdf",
            excel_path,
            "--outdir",
            os.path.dirname(output_pdf_path),
        ]
        print("executing_command", command)
        subprocess.run(command, check=True)

        # LibreOffice adds .pdf extension automatically,
        # so adjust the output path
        generated_pdf = os.path.splitext(excel_path)[0] + ".pdf"
        if os.path.exists(generated_pdf):
            os.rename(generated_pdf, output_pdf_path)
            print(f"PDF saved to {output_pdf_path}")
        else:
            print("PDF conversion failed.")

    except subprocess.CalledProcessError as e:
        print(f"Error occurred during conversion: {e}")


excel_folder = "generated_excels"
pdf_folder = "generated_pdfs"


# Ensure the generated_pdfs directory exists
if not os.path.exists(pdf_folder):
    os.makedirs(pdf_folder)

# Process each Excel file in the generated_excels folder
for filename in os.listdir(excel_folder):
    print(filename)
    if filename.endswith(".xlsx"):
        excel_path = os.path.join(excel_folder, filename)
        output_pdf_path = os.path.join(pdf_folder, filename.replace(".xlsx", ".pdf"))
        print(f"Converting {excel_path} to {output_pdf_path}...")
        excel_to_pdf(excel_path, output_pdf_path)
