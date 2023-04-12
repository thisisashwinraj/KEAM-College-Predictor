import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

class PredictionsReport:

    def college_predictions_report(df):
        # Create a PDF file and set its dimensions
        pdf_filename = 'data/statements/college_predictions.pdf'
        doc = SimpleDocTemplate(pdf_filename, pagesize=letter)

        # Convert the Pandas DataFrame to a list of lists
        data = [list(df.columns)] + df.values.tolist()

        # Create a table from the data and set its style
        table = Table(data)
        table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.blue),
                                   ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                   ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                   ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                   ('FONTSIZE', (0, 0), (-1, 0), 14),
                                   ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                   ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                   ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                                   ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                                   ('FONTSIZE', (0, 1), (-1, -1), 12),
                                   ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
                                   ('GRID', (0, 0), (-1, -1), 1, colors.black)]))

        # Add the table to the PDF and save it
        doc.build([table])

