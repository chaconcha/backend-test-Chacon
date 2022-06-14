from django.shortcuts import render

"""
This file contains "frontend" endpoints that load HTML Vue pages,
each of these Vue pages uses the MenuViewset as
their "backend's" API for this project.
These views are meant to mock a Vue frontend
"""


def menuList(request):
    # View that shows the list of all menus and a form to create new ones
    return render(request, "menu-list.html")


def menuDetail(request, pk=None):
    # View that shows a specific menu, it's fields and the employee's responses
    # Allows to edit and delete the menu,
    # and to send a Slack reminder to the employees
    return render(request, "menu-detail.html", context={"pk": pk})


def menuResponse(request, pk=None):
    # Shows the menu and it's options
    # Allows employees to send their preferred meal choice
    return render(request, "menu-response.html", context={"pk": pk})
