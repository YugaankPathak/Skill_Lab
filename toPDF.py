from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit

def toPDF():

    path = 'I:/Skill_Lab/Download/'

    pdf_path = path + 'summary.pdf'
    pdf = canvas.Canvas(pdf_path, pagesize=letter)
    pdf.setFont("Helvetica", 12)

    with open(path + 'summary.txt', "r", encoding='utf-8', errors='replace') as f:
        text = f.read()

    width,height = letter

    x = 50
    y = height - 50
    line_height = 20
    max_width = width - 2 * x

    
    for line in text.splitlines():

        wrapped_lines = simpleSplit(line, "Helvetica", 12, max_width)

        for wrapped_line in wrapped_lines:

            if y <= 20:  # If the line goes off the page, add a new page
                pdf.showPage()
                pdf.setFont("Helvetica", 12)
                y = height - 50

            pdf.drawString(x, y, wrapped_line)
            y -= line_height  # Move the cursor down

    pdf.save()  
    print(f"PDF saved at {pdf_path}")

#toPDF()