# Local mock of the go-public pages API (POST/PUT/DELETE /api/pages, GET /p/<id>), for testing share.py without the network.
import http.server, json, secrets, re
PAGES = {}
CSP = "sandbox allow-scripts allow-popups allow-modals; default-src 'none'; script-src 'unsafe-inline' https://onetagai.com; style-src 'unsafe-inline'; img-src data: blob:; font-src data:; connect-src https://onetagai.com; form-action 'none'"
BADGE = '<div style="position:fixed;right:8px;bottom:8px;font:12px system-ui;background:#fff;border:1px solid #0b1020;padding:4px 8px">Made with OneTag · Report</div>'
class H(http.server.BaseHTTPRequestHandler):
    def _json(self, code, obj):
        b = json.dumps(obj).encode(); self.send_response(code); self.send_header("Content-Type","application/json"); self.end_headers(); self.wfile.write(b)
    def _body(self):
        return json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0)) or 0) or b"{}")
    def _auth(self, pid):
        return pid in PAGES and self.headers.get("Authorization") == "Bearer " + PAGES[pid]["token"]
    def do_POST(self):
        if self.path != "/api/pages": return self._json(404, {})
        b = self._body()
        if len(b.get("html","")) > 300_000 or 'type="password"' in b.get("html",""): return self._json(400, {"error": {"code": "rejected"}})
        pid, tok = secrets.token_hex(3), "pe_" + secrets.token_hex(12)
        PAGES[pid] = {"html": b["html"], "token": tok}
        self._json(200, {"id": pid, "url": f"http://127.0.0.1:8766/p/{pid}", "edit_token": tok, "claim_url": f"http://127.0.0.1:8766/claim/{pid}#{tok}",
                         "limits": {"page_tokens_per_day": 50000, "visitor_requests_per_min": 6, "max_output_tokens": 800}})
    def do_PUT(self):
        pid = self.path.rsplit("/", 1)[-1]
        if not self._auth(pid): return self._json(403, {"error": {"code": "bad_token"}})
        PAGES[pid]["html"] = self._body()["html"]; self._json(200, {"id": pid})
    def do_DELETE(self):
        pid = self.path.rsplit("/", 1)[-1]
        if not self._auth(pid): return self._json(403, {"error": {"code": "bad_token"}})
        del PAGES[pid]; self._json(200, {"deleted": pid})
    def do_GET(self):
        m = re.fullmatch(r"/p/(\w+)", self.path)
        if not m or m.group(1) not in PAGES: self.send_response(404); self.end_headers(); return
        html = PAGES[m.group(1)]["html"].replace("ONETAG_PAGE_KEY", "ot_demo000000000000000000000").replace("</body>", BADGE + "</body>")
        self.send_response(200); self.send_header("Content-Type", "text/html; charset=utf-8"); self.send_header("Content-Security-Policy", CSP); self.end_headers(); self.wfile.write(html.encode())
    def log_message(self, *a): pass
http.server.ThreadingHTTPServer(("127.0.0.1", 8766), H).serve_forever()
