from bson import ObjectId
from flask import *
from flask import render_template
import hashlib
import pymongo
app = Flask("One-Stop-Shop")
app.secret_key = "1234"
CONNECTION_INFO="mongodb+srv://shrutiv:5FMQpAsTHubEo1AO@cluster0.use2f.mongodb.net/products?retryWrites=true&w=majority"
client = pymongo.MongoClient(CONNECTION_INFO)
db=client.get_database('OneStopShop')
card=0
total=0
cart_items = []
@app.route('/', methods=['POST', 'GET'])
def base():
    if request.method=='GET':
        db.cart_items.remove({})
        return render_template('index.html')
@app.route('/addProducts',methods=['GET','POST'])
def addProducts():
    if request.method=="GET":
        return render_template("addProducts.html")
    elif request.method=="POST":
        doc = dict(request.form)
        db.products.insert_one(doc)
        return redirect('/')

@app.route('/buyProducts',methods=['GET','POST'])
def buyProducts():
    if request.method=="GET":
        found_products=db.products.find()
        return render_template("buyProducts.html", products=found_products)
    elif request.method=="POST":
        #doc={}
        count = 0
        for item in request.form:
            if request.form[item]!='':
                found_product = db.products.find_one({'_id': ObjectId(item)})
                #ID=str(found_product['_id'])
                #items_stored=db.cart_items.find()
                #if items_stored.count()!=0:
                  #  for i in items_stored:
                        #if i['_id']==ID:
                            #count=int(i['bought'])+request.form[item]
                total_item_count=int(request.form[item])#+count
                itemtotal = int(found_product['price']) * total_item_count
                key={'_id':item}
                data={'title':found_product['title'],'price':found_product['price'],'bought':total_item_count,'item-total':itemtotal}
                db.cart_items.update(key,data,upsert=True)
        return redirect('/cart')
@app.route('/cart',methods=['GET'])
def cart():
    total=0
    cart_items_found=db.cart_items.find()
    for i in cart_items_found:
           print(i)
           total+=i['item-total']
    cart_items_found.rewind()
    return render_template('cart.html',cart_products=cart_items_found,totals=total)
@app.route('/emptyCart',methods=['GET','POST'])
def emptyCart():
    global total
    global cart_items
    if request.method=='GET':
        db.cart_items.remove({})
        cart_items=[]
        total=0
        return render_template('cart.html',product=cart_items,totals=total)
if __name__ == '__main__':
    app.run(debug=True)