pkill -f python

for i in `seq 0 3`; do
    python3 main.py --port=800$i --debug=False &
done

sudo nginx -c nginx.conf


