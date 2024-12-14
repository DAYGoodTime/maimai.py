import asyncio
from mitmproxy.http import HTTPFlow
import mitmproxy.proxy
import mitmproxy.proxy.layers

from examples.proxy_updater import updater

prompt = "Your scores are currently being updated. Please wait for a moment.\n 你的成绩正在更新中，请稍等片刻。"


class WechatWahlapAddon:
    wahlap_hosts = [
        "152.136.21.46",
        "tgk-wcaime.wahlap.com",
    ]

    async def request(self, flow: HTTPFlow):
        # modify the wahlap oauth requests
        # example: http://tgk-wcaime.wahlap.com/wc_auth/oauth/callback/maimai-dx?r=c9N1mMeLT&t=241114354&code=071EIC0003YUbTf5X31EIC0p&state=24F0976C60BD9796310AD933AFEF39FFCD7C0E64E9571E69A5AE5
        if flow.request.host in self.wahlap_hosts and flow.request.path.startswith("/wc_auth/oauth/callback/maimai-dx"):
            # prevent infinite loop if the server and client are both using the proxy (user is testing in the same machine)
            if not flow.request.headers.get("Flag", None):
                r, t, code, state = flow.request.query["r"], flow.request.query["t"], flow.request.query["code"], flow.request.query["state"]
                await updater.update_prober(r, t, code, state)
                flow.response.content = prompt.encode("utf-8")  # hint the user that the scores are being updated
                flow.response.status_code = 200  # replace the 302 redirect with a 200 OK