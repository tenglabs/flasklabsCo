from flask import redirect, render_template, url_for, flash, request, session, current_app
from ecommerce import db, app
from ecommerce.models import Product
from flask_login import current_user
from ecommerce.models import CustomerOrder

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


@app.route('/getorder')
def get_order():
    if current_user.is_authenticated:
        customer_id = current_user.id
        


        
        try:
            order = CustomerOrder(customer=current_user,orders=session['Shoppingcart'])
            db.session.add(order)
            db.session.commit()
            session.pop('Shoppingcart')
            flash('Your order has been sent successfully','success')
            return redirect('order-list')
        except Exception as e:
            print(e)
            flash('Some thing went wrong while get order', 'danger')
            return redirect(url_for('getcart'))

@app.route('/order-list')
def order_list():
    
    order_list = CustomerOrder.query.all()

    return render_template('cart/orders.html',order_list=order_list)
