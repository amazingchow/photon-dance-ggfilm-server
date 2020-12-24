# -*- coding: utf-8 -*-
from mako.template import Template
from mako.lookup import TemplateLookup


def render_nginx_custom_conf(root):
    conf_path = "{}/deploy/nginx".format(root)
    lookup = TemplateLookup(directories=[conf_path], output_encoding='utf-8', input_encoding='utf-8', default_filters=['decode.utf8'], encoding_errors='replace')
    
    nginx_http_server_template = lookup.get_template("/ggfilm-http-server.conf.example")
    values = {
        "project_path": root,
    }
    content = nginx_http_server_template.render(**values)
    content = str(content, encoding = "utf8")
    with open("{}/deploy/nginx/ggfilm-http-server.conf".format(root), "w") as fw:
        fw.write(content)

    nginx_https_server_template = lookup.get_template("/ggfilm-https-server.conf.example")
    values = {
        "project_path": root,
    }
    content = nginx_https_server_template.render(**values)
    content = str(content, encoding = "utf8")
    with open("{}/deploy/nginx/ggfilm-https-server.conf".format(root), "w") as fw:
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

    uwsgi_tencent_cloud_template = lookup.get_template("/uwsgi-tencent-cloud.ini.example")
    values = {
        "project_path": root,
    }
    content = uwsgi_tencent_cloud_template.render(**values)
    content = str(content, encoding = "utf8")
    with open("{}/ggfilm/uwsgi-tencent-cloud.ini".format(root), "w") as fw:
        fw.write(content)


def render_logrotate_custom_conf(root):
    conf_path = "{}/deploy/logrotate".format(root)
    lookup = TemplateLookup(directories=[conf_path], output_encoding='utf-8', input_encoding='utf-8', default_filters=['decode.utf8'], encoding_errors='replace')
    
    logrotate_template = lookup.get_template("/ggfilm.example")
    values = {
        "project_path": root,
    }
    content = logrotate_template.render(**values)
    content = str(content, encoding = "utf8")
    with open("{}/deploy/logrotate/ggfilm".format(root), "w") as fw:
        fw.write(content)


def render_cron_custom_conf(root):
    conf_path = "{}/deploy/cron".format(root)
    lookup = TemplateLookup(directories=[conf_path], output_encoding='utf-8', input_encoding='utf-8', default_filters=['decode.utf8'], encoding_errors='replace')
    
    cron_template = lookup.get_template("/ggfilm.example")
    values = {
        "project_path": root,
    }
    content = cron_template.render(**values)
    content = str(content, encoding = "utf8")
    with open("{}/deploy/cron/ggfilm".format(root), "w") as fw:
        fw.write(content)


if __name__ == "__main__":
    root = "/home/SENSETIME/zhoujian2/gomodule/github.com/amazingchow/photon-dance-ggfilm-server"
    render_nginx_custom_conf(root)
    render_uwsgi_custom_ini(root)
    render_logrotate_custom_conf(root)
    render_cron_custom_conf(root)
