#!/usr/bin/python3
import connect as con
import time

N = 1000000
cli = con.connect()
if cli is not None:
  db = cli["ledger"]
  coll = db["transactions"]

  start = time.time()
  for i in range(N):
    myquery = {"id": i}
    mydoc = coll.find(myquery)
  end = time.time()-start
  print("Time Taken",end, " for Querying ", N)
    # for m in mydoc:
    #   print(m)
