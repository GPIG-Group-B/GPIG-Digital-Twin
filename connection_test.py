from connections import TCPWorker

test_worker = TCPWorker()
test_worker.run()
test_worker.join()