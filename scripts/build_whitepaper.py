"""Generate the versioned, source-bound public whitepaper using ReportLab4.4.9."""
from pathlib import Path
import hashlib
import json
from xml.sax.saxutils import escape
import reportlab
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Image
from reportlab.platypus.tableofcontents import TableOfContents
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'site/whitepaper.json'
paper = json.loads(SOURCE.read_text(encoding='utf-8'))
source_hash = hashlib.sha256(json.dumps(paper, ensure_ascii=False, separators=(',', ':')).encode('utf-8')).hexdigest()
font_dir = Path(reportlab.__file__).parent / 'fonts'
pdfmetrics.registerFont(TTFont('OrioBody', str(font_dir / 'Vera.ttf')))
pdfmetrics.registerFont(TTFont('OrioBold', str(font_dir / 'VeraBd.ttf')))
pdfmetrics.registerFontFamily('OrioBody', normal='OrioBody', bold='OrioBold', italic='OrioBody', boldItalic='OrioBold')
blue, ink, muted = colors.HexColor('#1355e9'), colors.HexColor('#102a61'), colors.HexColor('#526783')
styles = getSampleStyleSheet()
body = ParagraphStyle('OrioBodyText', fontName='OrioBody', fontSize=9.5, leading=14.5,
                      textColor=ink, spaceAfter=10, allowWidows=0, allowOrphans=0)
chapter = ParagraphStyle('Chapter', parent=body, fontName='OrioBold', fontSize=16, leading=21,
                         textColor=blue, spaceBefore=18, spaceAfter=12, keepWithNext=True)
small = ParagraphStyle('OrioSmall', parent=body, fontSize=8, leading=12, textColor=muted)
cell = ParagraphStyle('OrioCell', parent=body, fontSize=8, leading=11, spaceAfter=0)
formula = ParagraphStyle('OrioFormula', parent=body, fontSize=8.2, leading=13,
                         backColor=colors.HexColor('#f2f7ff'), borderPadding=9, spaceBefore=6, spaceAfter=12)
title = ParagraphStyle('OrioTitle', parent=body, fontName='OrioBold', fontSize=31, leading=38,
                       textColor=ink, spaceAfter=22)
subtitle = ParagraphStyle('OrioSubtitle', parent=body, fontSize=15, leading=22, textColor=muted, spaceAfter=20)


class Whitepaper(SimpleDocTemplate):
    def afterFlowable(self, flowable):
        if isinstance(flowable, Paragraph) and flowable.style.name == 'Chapter':
            key = flowable._bookmark
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(flowable.getPlainText(), key, level=0, closed=False)
            self.notify('TOCEntry', (0, flowable.getPlainText(), self.page, key))


def furniture(canvas, doc):
    canvas.saveState()
    width, height = A4
    canvas.setStrokeColor(colors.HexColor('#dbe6fa'))
    canvas.line(52, height - 42, width - 52, height - 42)
    canvas.setFont('OrioBody', 7.5)
    canvas.setFillColor(muted)
    canvas.drawString(52, height - 31, 'ORIO.IO LAB  /  SPC 3.0')
    canvas.drawRightString(width - 52, height - 31, 'Technical whitepaper v' + paper['version'])
    canvas.line(52, 42, width - 52, 42)
    canvas.drawString(52, 29, 'November 14, 2026  |  Financial operations not enabled')
    canvas.drawRightString(width - 52, 29, str(doc.page))
    canvas.restoreState()


output = ROOT / 'site/assets/ORIO-SPC-3-Whitepaper.pdf'
output.parent.mkdir(parents=True, exist_ok=True)
doc = Whitepaper(str(output), pagesize=A4, rightMargin=52, leftMargin=52,
                topMargin=60, bottomMargin=58, pageCompression=1, invariant=1,
                title=paper['title'], author=paper['publisher'],
                subject='Version ' + paper['version'] + '; source-sha256:' + source_hash)
story = [Spacer(1, 26), Image(str(ROOT / 'site/assets/orio-original-blue.png'), width=125, height=65, kind='proportional'),
         Spacer(1, 40), Paragraph(escape(paper['title']), title), Paragraph(escape(paper['subtitle']), subtitle),
         Paragraph('Version ' + paper['version'] + ' | November 14, 2026 | ' + escape(paper['publisher']), body),
         Spacer(1, 20), Paragraph('ABSTRACT', chapter), Paragraph(escape(paper['abstract']), body),
         Spacer(1, 12), Paragraph('Founder-approved economics. Versioned engineering evidence. No guaranteed return, permanent dollar peg or financial launch is asserted.', small), PageBreak()]
# The cover label is not a numbered chapter or a TOC entry.
story[-5].style = ParagraphStyle('AbstractLabel', parent=chapter)
story.append(Paragraph('Contents', ParagraphStyle('Contents', parent=chapter)))
toc = TableOfContents()
toc.levelStyles = [ParagraphStyle('TOC', parent=body, fontSize=8.3, leading=10.5, spaceBefore=0, spaceAfter=0)]
story.extend([toc, PageBreak()])
for section in paper['sections']:
    heading = Paragraph(escape(section['title']), chapter)
    heading._bookmark = section['id']
    story.append(heading)
    for text in section['paragraphs']:
        story.append(Paragraph(escape(text), body))
    for text in section.get('equations', []):
        story.append(Paragraph(escape(text), formula))
    if 'table' in section:
        table = section['table']
        rows = [[Paragraph('<b>' + escape(value) + '</b>', cell) for value in table['columns']]]
        rows += [[Paragraph(escape(value), cell) for value in row] for row in table['rows']]
        widths = [90, doc.width - 90] if len(table['columns']) == 2 else [doc.width / len(table['columns'])] * len(table['columns'])
        rendered = Table(rows, colWidths=widths, repeatRows=1, hAlign='LEFT')
        rendered.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e6efff')),
            ('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8),
            ('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),
            ('LINEBELOW',(0,0),(-1,0),0.5,colors.HexColor('#b8cff6')),
            ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#f7faff')])]))
        story.extend([rendered, Spacer(1, 12)])
story.append(Spacer(1, 10))
for reference in paper['references']:
    story.append(Paragraph(escape(reference['id'] + '. ' + reference['title']) + '<br/><link color="#1355e9" href="' + escape(reference['url']) + '">' + escape(reference['url']) + '</link>', small))
story.append(Spacer(1, 10))
story.append(Paragraph('Canonical source SHA-256: ' + source_hash, small))
doc.multiBuild(story, onFirstPage=furniture, onLaterPages=furniture)
reader = PdfReader(output)
text = '\n'.join(page.extract_text() for page in reader.pages)
for section in paper['sections']:
    if section['title'] not in text:
        raise ValueError('Missing PDF chapter: ' + section['title'])
if len(text.split()) < 6000:
    raise ValueError('Whitepaper unexpectedly incomplete')
manifest = {'sourceSHA256': source_hash, 'pdfSHA256': hashlib.sha256(output.read_bytes()).hexdigest(),
            'version': paper['version'], 'pages': len(reader.pages), 'wordCount': len(text.split()),
            'financialExecutionEnabled': False}
(ROOT / 'site/whitepaper-pdf-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
print(json.dumps(manifest))
