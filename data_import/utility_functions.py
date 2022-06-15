from xml.etree.ElementTree import tostring


def list_to_pipe_del(list):
    out_str = ''
    for i in list:
        out_str+=str(i) + "|"
    return out_str