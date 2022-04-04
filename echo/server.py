from http import HTTPStatus
import socket


with socket.socket() as s:

    s.bind(('', 5000))
    s.listen(1)
    while True:
        conn, addr = s.accept()

        while True:
            recv_bytes = conn.recv(1024)
            print(recv_bytes)
            request_str = recv_bytes.decode('utf-8')
            print(f'Message: \n"{recv_bytes}"')
            if request_str:
                # извлекаем статус запроса
                method = request_str[:request_str.find(" ")]
                status = request_str[request_str.find('status=') + 7:request_str.find(" ", request_str.find(' ') + 1)]
                # преобразуем полученное значение в http статус
                try:
                    http_status = HTTPStatus(int(status))
                    status_line = f'HTTP/1.1 {http_status.value} {http_status.name}'
                except ValueError:
                    http_status = HTTPStatus(200)
                    status_line = f'HTTP/1.1 {http_status.value} {http_status.name}'
                # извлекаем наименования заголовков
                headers_name = request_str.split('\n')
                headers_name_list = []
                for x in headers_name:
                    if x.find(":") == -1:
                        continue
                    else:
                        headers_name_list.append(x[:x.find(':')])

                # формируем тело ответа в html
                body = f'<p>Request Method: {method}</p>' \
                       f'<p>Request Source: {addr}</p>' \
                       f'<p>Response Status: {http_status.value} {http_status.name} </p>'

                for el in headers_name_list:
                    body += f'<p>header-name: {el}</p>'

                headers = '\r\n'.join([
                    status_line,
                    'Content-Type: text/html;',
                    f'Content-Length: {len(body)}'
                 ])

                # формируем и отправляем ответ
                resp = '\r\n\r\n'.join([
                    headers,
                    body
                ])
                sent_bytes = conn.send(resp.encode('utf-8'))
                print(f'{sent_bytes} bytes sent')
            else:
                break
        conn.close()
