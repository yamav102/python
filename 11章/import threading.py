import threading

def worker(name):
    print(f"{name} 開始")
    # 重い処理やI/O処理を入れる

threads = []
for i in range(5):
    t = threading.Thread(target=worker, args=(f"スレッド{i}",))
    threads.append(t)
    t.start()

for t in threads:
    t.join() # 複数スレッドが終了するまで待機させている