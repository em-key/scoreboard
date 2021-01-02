from django import template

register = template.Library()

@register.filter
def scorenumber(score):
    """
    Django template filter to convert regular numbers to two digit score numbers
    To have all LED of 7 segment font off '!' is required

    """

    score = int(score)
    if score < 10:
        return "!" + str(score)
    else:
        return score