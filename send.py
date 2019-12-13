import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='120.24.170.233', port=5672,
                              credentials=pika.PlainCredentials("hitnslab", "hitnslab")))
channel = connection.channel()

channel.queue_declare(queue='hello')
domains = """0-007.com
0-1-0.com
0-130.com
0-17.cn
0-18baby.com
0-2-3.com
0-2-8.com
0-5.cc
0-5.com
0-71.com
0-9.cn
0-9999.com
0-9999.ru
0-a.cn
0-capital.com
0-chain.com
0-d.net
0-h.com
0-hr.cn
0-iq.com
0-w.com.cn
0.cc
0.vg
00-00gvb.com
00-11jbs.com
00-b.com
00-c.cc
00.cx
00.he.cn
00.tt
"""
for domain in domains.split('\n'):
    channel.basic_publish(exchange='', routing_key='hello', body=domain)
print(" [x] Sent %s" % domain)
connection.close()