"""
__author__ = 'hitesh'
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, PageBreak
from PyPDF2 import PdfFileMerger
from pyPdf import PdfFileReader
import numpy as np
import matplotlib.pyplot as plt
from os.path import exists

plt.rcdefaults()


class ReportPdf(object):
    elements = []

    def addtable(self, column, row, table_data):
        col = column
        row = row
        colsize = 5.0 / col

        # Defininig table structure(nos of rows, nos of columns, size of rows, size of columns)
        tableobj = Table(table_data, col * [colsize * inch], row * [0.25 * inch])

        # Defining Table style
        tablestyle = [('VALIGN', (0, -1), (0, -1), 'MIDDLE'),
                      ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
                      ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.white),
                      ('BOX', (0, 0), (-1, -1), 0.25, colors.white)]

        for _ in xrange(0, row, 2):
            bgcolor = ('BACKGROUND', (0, _), (-1, _), colors.lightgrey)
            tablestyle.append(bgcolor)

        # noinspection PyArgumentList
        tableobj.setStyle(TableStyle(tablestyle))
        self.elements.append(tableobj)

    @staticmethod
    def gettotalpages(filename):
        pdffile = PdfFileReader(open(filename, 'rb'))
        return pdffile.getNumPages()

    @staticmethod
    def pdfmerger(resultpdf, *pdfs):
        merger = PdfFileMerger()
        all_pdf = pdfs
        for pdf in all_pdf:
            merger.append(open(pdf, 'rb'))

        with open(resultpdf, 'wb') as pdfout:
            merger.write(pdfout)
        return resultpdf

    def addimage(self, imgname):
        self.elements.append(Image(imgname, 5 * inch, 2.5 * inch))

    def addtwoimagesinrow(self, imgname1, imgname2):
        # table to get two images in single cell
        tableobj = Table([[Image(imgname1, 2.5 * inch, 2.2 * inch), Image(imgname2, 2.5 * inch, 2.2 * inch)]])
        # default style for table
        tableobj.setStyle(TableStyle())
        self.elements.append(tableobj)

    def pagebreak(self):
        self.elements.append(PageBreak())

    def builpdf(self, filename):
        doc = SimpleDocTemplate(filename, pagesize=A4)
        doc.build(self.elements)
        del self.elements[:]

    def delvalue(self):
        del self.elements


class Chart(object):
    def __init__(self, outdir='.', chartname='barchart', pagesize=(4, 4), bar_width=0.35):
        self.outdir = outdir
        self.chartname = chartname
        self.pagesize = pagesize
        self.bar_width = bar_width

    def createbarchart(self, xaxis, yaxis, xlabel, ylabel, title):
        x_axis_objects = xaxis
        y_axis_objects = yaxis
        x_axis_label = xlabel
        y_axis_label = ylabel
        bar_chart_title = title
        # len_x_objs = len(x_axis_objects)
        y_axis_pos = np.arange(len(x_axis_objects))
        # bar_width = 1.0 / len_x_objs

        if not exists(self.outdir):
            raise Exception("%s directory doesn't exists." % self.outdir)

        plt.figure(figsize=self.pagesize)
        plt.bar(y_axis_pos, y_axis_objects, self.bar_width, align='center', alpha=0.5)
        plt.xticks(y_axis_pos, x_axis_objects)
        plt.xlabel(x_axis_label)
        plt.ylabel(y_axis_label)
        plt.title(bar_chart_title)

        plt.savefig(self.outdir + "/" + self.chartname, dpi=100)
        plt.close()
        return self.outdir + "/" + self.chartname


if __name__ == "__main__":
    test = Chart(outdir='E:/Maple-labs/programs', chartname='barchart0.png')
    AA = test.createbarchart(('Shared Memory', 'Balloon Memory', 'Consumed memory'), (1, 5, 8), 'Parameters', 'Values',
                             'Memory Allocation')
    print AA
    data = [['Parameter', 'Value'],
            ['Shared Memory', '1 GB'],
            ['Balloon Memory', '5 GB'],
            ['Consumed memory', '8 GB']
            ]
    A = ReportPdf()
    A.addtable(2, 4, data)
    A.addimage('barchart0.png')
    A.addimage('barchart0.png')
    A.addimage('barchart0.png')
    A.pagebreak()
    A.addtwoimagesinrow('newgraph_u7.png', 'newgraph_u7.png')
    A.builpdf('E:/Maple-labs/programs/test2.pdf')

    ReportPdf.pdfmerger('result.pdf', 'report.pdf', 'test1.pdf', 'test2.pdf')
    value = ReportPdf.gettotalpages('E:/Maple-labs/programs/result.pdf')
    print "Total Pages in pdf are: ", value
