# exponential increase of time after every fail and stop after 5 tries
import time

wait_time=1
attempt=1
max_tries=6

while attempt<max_tries:
    print("try:", attempt, "wait", wait_time)
    time.sleep(wait_time)
    wait_time*=2
    attempt+=1
