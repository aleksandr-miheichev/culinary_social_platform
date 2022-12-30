from io import BytesIO

from django.http import FileResponse
from reportlab.lib.units import inch
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas


def pdf_creation(queryset):
    buffer = BytesIO()
    canvas = Canvas(buffer)
    registerFont(TTFont(
        name='DejaVuSerif',
        filename='DejaVuSerif.ttf',
        asciiReadable='UTF-8'
    ))
    canvas.setFont(psfontname="DejaVuSerif", size=28)
    canvas.drawString(x=2 * inch, y=11 * inch, text='Продуктовый помощник')
    canvas.setFont(psfontname="DejaVuSerif", size=16)
    canvas.drawString(x=1 * inch, y=10 * inch, text='Список покупок:')
    canvas.setFont(psfontname="DejaVuSerif", size=14)
    canvas.drawString(
        x=0.5 * inch,
        y=9 * inch,
        text='Наименование ингредиента:'
    )
    canvas.drawString(x=4 * inch, y=9 * inch, text='Количество:')
    canvas.drawString(x=6 * inch, y=9 * inch, text='Единица измерения:')
    height = 8 * inch
    for ingredient in queryset:
        canvas.drawString(
            x=1 * inch,
            y=height,
            text=f'{ingredient["ingredient__name"]}'
        )
        canvas.drawString(
            x=4.5 * inch,
            y=height,
            text=f'{ingredient["amount"]}'
        )
        canvas.drawString(
            x=7 * inch,
            y=height,
            text=f'{ingredient["ingredient__measurement_unit"]}'
        )
        height -= 0.5 * inch
    canvas.save()
    buffer.seek(0)
    return FileResponse(
        buffer,
        as_attachment=True,
        filename='ShoppingList.pdf'
    )
