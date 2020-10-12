# -*- coding: utf-8 -*-

def esc_replace_view2db(s):
    s = s.replace("/", "//") 
    s = s.replace("'", "''")
    s = s.replace('"', "''")  
    s = s.replace("[", "/[") 
    s = s.replace("]", "/]") 
    s = s.replace("%", "/%") 
    s = s.replace("&","/&")
    s = s.replace("_", "/_") 
    s = s.replace("(", "/(") 
    s = s.replace(")", "/)")
    return s


def esc_replace_db2view(s):
    s = s.replace("//", "/") 
    s = s.replace("''", '"')  
    s = s.replace("/[", "[") 
    s = s.replace("/]", "]") 
    s = s.replace("/%", "%") 
    s = s.replace("/&","&")
    s = s.replace("/_", "_") 
    s = s.replace("/(", "(") 
    s = s.replace("/)", ")")
    return s
