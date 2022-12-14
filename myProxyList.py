import asyncio
from proxybroker import Broker


async def save(proxies, filename):
    """Save proxies to a file."""
    with open(filename, "w") as f:
        while True:
            proxy = await proxies.get()
            if proxy is None:
                break
            proto = "https" if "HTTPS" in proxy.types else "http"
            row = "%s://%s:%d\n" % (proto, proxy.host, proxy.port)
            row2 = "%s\n" % (proxy)
            f.write(row)


proxies = asyncio.Queue()
broker = Broker(proxies)
tasks = asyncio.gather(broker.find(types=["HTTPS"], countries=["GB"], limit=50),
                           save(proxies, filename="proxies.txt"))
loop = asyncio.get_event_loop()
loop.run_until_complete(tasks)
