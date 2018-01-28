import json
import speedtest
import sqlite3
import subprocess
import time

def fast():
    # Start chromium in headless mode
    ts = int(time.time())
    proc = subprocess.Popen(
        ['/usr/bin/chromium-browser', '--headless', '--repl', 'https://www.fast.com/'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)

    # Give time to the speed test to terminate
    time.sleep(60)

    try:
        outs, errs = proc.communicate(
            input='window.document.querySelector("#speed-value").textContent\nquit\n'.encode('utf-8'),
            timeout=5,
        )
    except subprocess.TimeoutExpired:
        proc.kill()
        outs, errs = proc.communicate()
    else:
        proc.terminate()

    return {
        'server': 'fast.com',
        'ts': ts,
        'ping': -1,
        'download': int(json.loads(outs.decode('utf-8')[4:-5])['result']['value']),
        'upload': -1,
    }

def speed():
    ts = int(time.time())

    servers = []
    s = speedtest.Speedtest()
    s.get_servers(servers)
    s.get_best_server()
    s.upload()
    s.download()

    results_dict = s.results.dict()
    return {
        'server': '{name} {sponsor}'.format(
            name=results_dict['server']['name'],
            sponsor=results_dict['server']['sponsor'],
        ),
        'ts': ts,
        'ping': int(results_dict['ping']),
        'download': int(results_dict['download']) // 1000000,
        'upload': int(results_dict['upload']) // 1000000,
    }

def main():
    with sqlite3.connect('speedtest.db') as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS RESULTS(
                server TEXT,
                ts INTEGER,
                ping INTEGER,
                download INTEGER,
                upload INTEGER,
                PRIMARY KEY (server, ts)
            )
        """)

        # Start by measuring speedtest
        speedtest_result = speed()
        # Wait a few seconds
        time.sleep(15)
        # Measure using fast.com
        fast_result = fast()

        # Persist results
        connection.executemany("""
            INSERT INTO RESULTS VALUES (
                :server,
                :ts,
                :ping,
                :download,
                :upload);
            """, (speedtest_result, fast_result))

if __name__ == '__main__':
    main()
