from flask import render_template


def error_page_not_found(e):
    return render_template('404.html'),404

def error_server_internal(e):
    return render_template('500.html'),500