# encoding: utf-8
"""
- Public Tools
- Author@Wangjunxiong
"""


def get_table_name(ip):
    """
    :param ip: String 1.0.0.0 ~ 254.255.255.255
    :return: Table_name: String
    """
    ip = str(ip)
    try:
        head_number = ip[:ip.index('.')]
        return "IPsegment_" + str(head_number)
    except Exception as e:
        return e


def generate_sql_by_ip_domain(ip, domain):
    """
    :param ip: String
    :param domain: String
    :return: SQL
    """
    table_name = get_table_name(ip)
    insert_sql = """INSERT INTO {table_name} (origin_ip, domain) VALUES ('{origin_ip}', '{domain}')""".format(
                    table_name=table_name, origin_ip=ip, domain=domain)
    return insert_sql


if __name__ == '__main__':
    print generate_sql_by_ip_domain(ip="127.0.0.1", domain="wudly.cn")
