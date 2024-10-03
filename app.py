from flask import Flask,render_template,request,url_for,redirect
from pymongo import MongoClient
from datetime import datetime

client=MongoClient('localhost',27017)

#Restaurant Database
rest_db=client.rest_db

#Collections
menu_collections=rest_db.menu

order_collection=rest_db.order_collection
app = Flask(__name__)


# Route for the home page
@app.route('/')
def home():
    return render_template('landing.html')


@app.route('/menu')
def menu():
    menu_items=menu_collections.find()
    return render_template('menu.html',items=menu_items)

@app.route('/order',methods=['POST'])
def order():
    order_details={}
    total_bill=0
    table_number=request.form.get('table_number')
    order_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    

    for item in menu_collections.find():
        dish_name = item['dish']
        quantity = request.form.get(f'quantity-{dish_name}', 0)
        
        if int(quantity) > 0:
            order_details[dish_name]=int(quantity)
            total_bill +=item['price'] * int(quantity)

    
 
            

    order_document ={
        'table_number':table_number,
        'order_time':order_time,
        'items':order_details,
        'total_bill':total_bill
    }

    menu_items = {item['dish']: item for item in menu_collections.find()}
    order_collection.insert_one(order_document)

    return render_template('order_summary.html',
                           order_details=order_details, 
                           total_bill=total_bill, 
                           table_number=table_number, 
                           order_time=order_time,
                           menu_items=menu_items
                           )

@app.route('/order-history')
def order_history():
    orders=order_collection.find()
    return render_template('order_history.html',orders=orders)




# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)