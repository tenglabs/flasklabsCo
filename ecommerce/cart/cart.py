from flask import redirect, render_template, url_for, flash, request, session, current_app
from ecommerce import db, app
from ecommerce.models import Product
from flask_login import current_user

def MagerDicts(dict1, dict2):
    if isinstance(dict1, list) and isinstance(dict2,list):
        return  dict1+dict2
    elif isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))
    return False


@app.route('/addcart', methods=["POST"])
def AddCart():
    try:
        product_id = request.form.get('product_id')
        quantity = request.form.get('quantity')
        product = Product.query.filter_by(id=product_id).first()
        if product_id and quantity and request.method =='POST':
            DictItems = {product_id:{'title':product.title,'price':float(product.price),'quantity':quantity,
                                    'discount':product.discount, 'image':product.image}}

            if 'Shoppingcart' in session:
                print(session['Shoppingcart'])
                if product_id in session['Shoppingcart']:
                    print('Already in session')
                else:
                    session['Shoppingcart'] = MagerDicts(session['Shoppingcart'],DictItems)
                    return redirect(request.referrer)

            else:
                session['Shoppingcart'] = DictItems

                return redirect(request.referrer)

    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)

@app.route('/shopping-cart')
def getcart():
    if 'Shoppingcart' not in session:
        return redirect(request.referrer)
    subtotal = 0
    grandtotal = 0
    for key, product in session['Shoppingcart'].items():
        discount = (product['discount']/100) * float(product['price'])
        subtotal +=float(product['price']) * int(product['quantity'])
        subtotal -= discount
        subtotal = float("%.2f" % (subtotal))
        ploti_nologi = ("%.2f" % (.06 * float(subtotal)))
        
        grandtotal = float("%.2f" % (1.06 * subtotal))


    return render_template('cart/cart.html',tax=ploti_nologi, grandtotal=grandtotal,notax=subtotal)