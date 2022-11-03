# truncate log.txt --size 0
truncate summary.txt --size 0

# for i in {1..10}
# do
#   sudo docker exec consumer python3 /test-relay/consumer.py
#   python3 analyze_log.py
# done

sudo docker exec consumer python3 /test-relay/consumer.py
python3 analyze_log.py

python3 stt.py
