from flask import Flask, request
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from time import sleep

### TEST ###
# BUCKET="neeraj"
# URL="http://localhost:8086"
# ORG="neeraj"
# TOKEN="CHaISdRHN-AMkRsoks5Kxzx8Dc3SPNFeO1gmpEnjK421ywFcXYf7-Rb2WdFVuogEVTJdiRYyg_Mf9GUPtjEDww=="

### Production ###
BUCKET="Weather"
URL="http://localhost:8086"
ORG="neeraj_room"
TOKEN="m6RE_uJLMEchIbAqQuZpAGQGNHD0_IOQWWYmAQevQjPNDM-dS2jHiMhgBL3DlGl2p7ww0WYBeWFPE_b3RMoCcA=="

TAG_LOC="location"
T_MEAS="temprature"
H_MEAS="humidity"
ROOM_MEAS="RoomCondition"


db_client=InfluxDBClient.from_config_file(config_file="config.json")  #(url=URL,org=ORG,token=TOKEN,debug=True)

db_writer=db_client.write_api(write_options=SYNCHRONOUS)
db_queryier=db_client.query_api()

def write_to_db(data):
    measurement=Point(ROOM_MEAS).tag(TAG_LOC,data[TAG_LOC])\
        .field(T_MEAS,data[T_MEAS])\
        .field(H_MEAS,data[H_MEAS])
    db_writer.write(BUCKET,record=measurement)

###### FLASK #######
app=Flask(__name__)

@app.route("/")
def default_page():
    return "Danger!!!"

@app.route("/write",methods=["POST"])
def write_handler():
    # print(request.data)
    print(request.get_json())
    write_to_db(request.get_json())
    # print(request.form)
    # print(request.remote_addr)
    return "OK",200

if __name__=="__main__":
    app.run(debug=True)