

def get_breadcrumb(view_name):
    choices=view_name.split("_")
    path=''
    breadcrumb = dict()
    for i, option in enumerate(choices):
        path=path + option + '_'
        breadcrumb[path[:-1]] = option
    return breadcrumb