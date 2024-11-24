#author: Eli Davidson
#date: 2024-11-24

from flask import Flask,jsonify,request
import uuid
import math


app=Flask(__name__)

#global object to hold receipts data since program is ran in memory
receipts_data = {}

@app.route('/receipts/process',methods=['POST'])
def process_reciepts():
    
    #data is the post request payload
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data sent"}), 404
    
    #generate id string and get points
    receipt_id = str(uuid.uuid4())
    points = calculate_points(data)
    
    #set the points with the unique id
    receipts_data[receipt_id] = points
    return jsonify({"id":receipt_id})

@app.route('/receipts/<id>/points', methods=['GET'])
def get_points(id):

    # Check if the id exists in the receipts_data dictionary
    if id not in receipts_data:
        return jsonify({"error": "Receipt id not found"}), 404
    
    points = receipts_data[id]

    return jsonify({"points": points}), 200

def calculate_points(data):

    retailer_points = 0
    if data['retailer']:
        #alnum of each char in the retailer name
        retailer_points = sum(c.isalnum() for c in data['retailer'])
    
    #check if total is multiple of .25 and rounded
    sale_points = 0
    if data['total']:
        sale_points = 25 if float(data['total']) % 0.25 == 0 else 0
        sale_points += 50 if float(data['total']).is_integer() else 0
    
    #6 points if day of purchase is odd. yy-mm-dd format
    day_of_purchase_points = 6 if int(data['purchaseDate'].split('-')[-1]) % 2 != 0 else 0

    #int division of len of items and * 5 for every 2 items
    num_items_points = (len(data['items']) // 2) * 5

    #if len of descrip is multiple of 2 then round up price and mult by 0.2
    item_points = 0
    for item in data['items']:
        descrip = item['shortDescription'].strip()
        if len(descrip) % 3 == 0:
            item_points += math.ceil(float(item['price'])*0.2)

    #time is given in military time ==> 2pm = 14:00 ; 4pm = 16 :00
    hour, minute = map(int, data['purchaseTime'].split(':'))
    time_of_purchase_points = 10 if hour >= 14 and hour <= 16 else 0

    #return sum of all components
    return retailer_points+sale_points+day_of_purchase_points+num_items_points+item_points+time_of_purchase_points



if __name__ == '__main__':
    app.run(host='0.0.0',port=6000)

