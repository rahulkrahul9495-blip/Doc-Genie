import gradio as gr
import requests
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import tempfile


def generate_docstring(code, style):
    """
    Generate a simple docstring for the given Python code.
    """

    if not code.strip():
        return "Please paste Python code."

    if style == "Google":
        doc = '''"""
Summary of the function.

Args:
    param1: Description

Returns:
    Description
"""'''
    else:
        doc = '''"""
Summary
-------
Parameters
----------
param1 : type
    Description

Returns
-------
type
    Description
"""'''

    return code + "\n\n" + doc


def export_txt(content):
    file_path = "docstring_output.txt"
    with open(file_path, "w") as f:
        f.write(content)
    return file_path


def export_pdf(content):
    file_path = "docstring_output.pdf"
    c = canvas.Canvas(file_path, pagesize=letter)

    text = c.beginText(40, 750)
    text.setFont("Helvetica", 10)

    for line in content.split("\n"):
        text.textLine(line)

    c.drawText(text)
    c.save()

    return file_path


with gr.Blocks() as demo:

    gr.Markdown("# 📄 Doc-Genie Python Docstring Generator")

    file_upload = gr.File(label="Click to Upload Python File")
    code_input = gr.Textbox(lines=12, label="Paste Python Code")

    style = gr.Radio(["Google", "NumPy"], label="Docstring Style")

    generate_btn = gr.Button("Generate Docstring")

    output_code = gr.Textbox(lines=12, label="Generated Code")

    generate_btn.click(
        generate_docstring,
        inputs=[code_input, style],
        outputs=output_code
    )

    gr.Markdown("### Export Options")

    txt_btn = gr.Button("Download TXT")
    pdf_btn = gr.Button("Download PDF")

    txt_file = gr.File()
    pdf_file = gr.File()

    txt_btn.click(export_txt, inputs=output_code, outputs=txt_file)
    pdf_btn.click(export_pdf, inputs=output_code, outputs=pdf_file)


demo.launch(share=True)