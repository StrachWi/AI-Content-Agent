from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', 'http://localhost:5173')
            self.end_headers()
            response = {"message": "AI 营销助手后端已启动！数据库连接正常。"}
            self.wfile.write(json.dumps(response).encode('utf-8'))
        elif self.path == '/api/templates':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', 'http://localhost:5173')
            self.end_headers()
            response = {
                "code": 200,
                "msg": "success",
                "data": [
                    {
                        "id": 1,
                        "name": "小红书种草模板",
                        "platform": "小红书",
                        "content": "大家好，我是{identity}，今天要给大家推荐一个超级好用的产品！{keyword}真的是太赞了，它能够{style}地解决{topic}问题，让你的生活变得更加美好。无论是在{platform}还是其他平台，这个产品都能为你带来意想不到的效果。",
                        "create_time": "2024-01-01T00:00:00"
                    },
                    {
                        "id": 2,
                        "name": "抖音推广模板",
                        "platform": "抖音",
                        "content": "家人们，谁懂啊！{keyword}真的绝了！作为一名{identity}，我必须要给大家安利这个宝藏产品。它不仅{style}，而且{emotion}，完全符合{platform}的风格。赶紧去试试吧，相信我，你一定会爱上它的！",
                        "create_time": "2024-01-02T00:00:00"
                    }
                ]
            }
            self.wfile.write(json.dumps(response).encode('utf-8'))
        elif self.path.startswith('/api/'):
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', 'http://localhost:5173')
            self.end_headers()
            response = {"code": 200, "msg": "success", "data": "模拟后端数据"}
            self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')
    
    def do_POST(self):
        if self.path == '/api/generate':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', 'http://localhost:5173')
            self.end_headers()
            # 模拟 AI 生成结果
            ai_result = f"这是为关键词 '{data.get('keyword', '')}' 生成的文案内容。使用了模板 ID {data.get('template_id', '')}，风格为 {data.get('style', '')}，情感基调为 {data.get('emotion', '')}。"
            response = {
                "code": 200,
                "msg": "生成成功",
                "data": {
                    "result": ai_result,
                    "history_id": 1
                }
            }
            self.wfile.write(json.dumps(response).encode('utf-8'))
        elif self.path.startswith('/api/'):
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', 'http://localhost:5173')
            self.end_headers()
            response = {"code": 200, "msg": "success", "data": data}
            self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')

def run_server():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, SimpleHandler)
    print('后端服务已启动，运行在 http://localhost:8000')
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()