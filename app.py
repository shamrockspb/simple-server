#!/usr/bin/env python
# encoding: utf-8
from flask import Flask, Response, send_file, request
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import os
import xml.etree.ElementTree as ET


app = Flask(__name__)
auth = HTTPBasicAuth()

users = {
    "s4user": generate_password_hash("E+[qE(-fjcS2kT.w")
}


@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username



@app.route('/sap/bc/srt/scs/sap/mmpur_purchaseorderrequest_in', methods=['POST'])
@auth.login_required
def purchase_order():
    #Parse and save data from request
    data_bin = request.data
    data = data_bin.decode("utf-8")

    root = ET.fromstring(data)
    for elem in root.findall(".//ID"):
        file = open("./data/" + elem.text, "w")
        file.write(data)
        file.close()

    #Prepare response
    xml = """
<?xml version="1.0"?>

<soap:Envelope
xmlns:soap="http://www.w3.org/2003/05/soap-envelope/"
soap:encodingStyle="http://www.w3.org/2003/05/soap-encoding"
xmlns:proc="http://sap.com/xi/Procurement">

<soap:Body>
  <proc:PurchaseOrderResponse>
    <Status>Success</Status>
  </proc:PurchaseOrderResponse>
</soap:Body>

</soap:Envelope>
    """
    return Response(xml, mimetype='application/xml')



@app.route('/sap/bc/srt/scs/sap/mmpur_purchaseorderrequest_in/<path:path>', methods=['GET'])
@auth.login_required
def purchase_order_read(path):
    return send_file(os.path.dirname(os.path.abspath(__file__)) + "/data/" +  path, mimetype='application/xml')

if __name__ == '__main__':
      app.run(host='0.0.0.0', port=8000)
