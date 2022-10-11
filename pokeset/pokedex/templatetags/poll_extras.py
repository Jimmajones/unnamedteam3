from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def typecolor(type):
    if type == "NOR":
        text = '<span style="background-color:{color}" class="type_symbol">{text}</span>'.format(color="grey", text=type)
    elif type == "FIG":
        text = '<span style="background-color:{color}" class="type_symbol">{text}</span>'.format(color="darkorange", text=type)
    elif type == "FLY":
        text = '<span style="background-color:{color}" class="type_symbol">{text}</span>'.format(color="cyan", text=type)
    elif type == "POI":
        text = '<span style="background-color:{color}" class="type_symbol">{text}</span>'.format(color="mediumslateblue", text=type)
    elif type == "GRO":
        text = '<span style="background-color:{color}" class="type_symbol">{text}</span>'.format(color="gold", text=type)
    elif type == "ROC":
        text = '<span style="background-color:{color}" class="type_symbol">{text}</span>'.format(color="goldenrod", text=type)
    elif type == "BUG":
        text = '<span style="background-color:{color}" class="type_symbol">{text}</span>'.format(color="darkolivegreen", text=type)
    elif type == "GHO":
        text = '<span style="background-color:{color}" class="type_symbol">{text}</span>'.format(color="darkorchid", text=type)
    elif type == "STE":
        text = '<span style="background-color:{color}" class="type_symbol">{text}</span>'.format(color="darkgrey", text=type)
    elif type == "FIR":
        text = '<span style="background-color:{color}" class="type_symbol">{text}</span>'.format(color="orange", text=type)
    elif type == "WAT":
        text = '<span style="background-color:{color}" class="type_symbol">{text}</span>'.format(color="blue", text=type)
    elif type == "GRA":
        text = '<span style="background-color:{color}" class="type_symbol">{text}</span>'.format(color="green", text=type)
    elif type == "ELE":
        text = '<span style="background-color:{color}" class="type_symbol">{text}</span>'.format(color="gold", text=type)
    elif type == "PSY":
        text = '<span style="background-color:{color}" class="type_symbol">{text}</span>'.format(color="pink", text=type)
    elif type == "ICE":
        text = '<span style="background-color:{color}" class="type_symbol">{text}</span>'.format(color="lightskyblue", text=type)
    elif type == "DRA":
        text = '<span style="background-color:{color}" class="type_symbol">{text}</span>'.format(color="crimson", text=type)
    elif type == "DAR":
        text = '<span style="background-color:{color}" class="type_symbol">{text}</span>'.format(color="dimgrey", text=type)
    elif type == "FAI":
        text = '<span style="background-color:{color}" class="type_symbol">{text}</span>'.format(color="hotpink", text=type)
    else:
        text = '<span style="display:none" class="type_symbol">{text}</span>'
    return mark_safe(text)