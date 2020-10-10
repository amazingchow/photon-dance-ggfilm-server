# -*- coding: utf-8 -*-
from mako.template import Template
from mako.lookup import TemplateLookup


def render_nginx_custom_conf(root):
    conf_path = "{}/nginx".format(root)
    lookup = TemplateLookup(directories=[conf_path], output_encoding='utf-8', input_encoding='utf-8', default_filters=['decode.utf8'], encoding_errors='replace')
    
    nginx_http_server_template = lookup.get_template("/ggfilm-http-server.conf.example")
    values = {
        "project_path": root,
    }
    content = nginx_http_server_template.render(**values)
    content = str(content, encoding = "utf8")
    with open("{}/nginx/ggfilm-http-server.conf".format(root), "w") as fw:
        fw.write(content)

    nginx_https_server_template = lookup.get_template("/ggfilm-https-server.conf.example")
    values = {
        "project_path": root,
    }
    content = nginx_https_server_template.render(**values)
    content = str(content, encoding = "utf8")
    with open("{}/nginx/ggfilm-https-server.conf".format(root), "w") as fw:
        fw.write(content)


def render_uwsgi_custom_ini(root):
    ini_path = "{}/ggfilm".format(root)
    lookup = TemplateLookup(directories=[ini_path], output_encoding='utf-8', input_encoding='utf-8', default_filters=['decode.utf8'], encoding_errors='replace')
    
    uwsgi_template = lookup.get_template("/uwsgi.ini.example")
    values = {
        "project_path": root,
    }
    content = uwsgi_template.render(**values)
    content = str(content, encoding = "utf8")
    with open("{}/ggfilm/uwsgi.ini".format(root), "w") as fw:
        fw.write(content)

    uwsgi_local_template = lookup.get_template("/uwsgi-local.ini.example")
    values = {
        "project_path": root,
    }
    content = uwsgi_local_template.render(**values)
    content = str(content, encoding = "utf8")
    with open("{}/ggfilm/uwsgi-local.ini".format(root), "w") as fw:
        fw.write(content)


if __name__ == "__main__":
    root = "/home/ubuntu/py3-ggfilm"
    render_nginx_custom_conf(root)
    render_uwsgi_custom_ini(root)
