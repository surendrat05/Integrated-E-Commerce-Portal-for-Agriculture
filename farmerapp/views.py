from django.shortcuts import render, redirect
from django.template import RequestContext
from django.contrib import messages
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
import os
from django.core.files.storage import FileSystemStorage
import pymysql
from django.http import HttpResponseServerError


global uname
global contact

def ViewUser(request):
    if request.method == 'GET':
        output = '<table border=1 align=center width=100%>'
        font = '<font size="" color="black">'
        arr = ['Username','Contact No','Gender','Email ID','Address','User Type']
        output += "<tr>"
        for i in range(len(arr)):
            output += "<th>"+font+arr[i]+"</th>"
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'farmerapp',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * FROM signup where usertype='User'")
            rows = cur.fetchall()
            for row in rows:
                username = row[0]
                
                contact = row[2]
                gender = row[3]
                email = row[4]
                address = row[5]
                utype = row[6]
                output += "<tr><td>"+font+str(username)+"</td>"
                
                output += "<td>"+font+contact+"</td>"
                output += "<td>"+font+str(gender)+"</td>"
                output += "<td>"+font+str(email)+"</td>"
                output += "<td>"+font+str(address)+"</td>"
                output += "<td>"+font+str(utype)+"</td>"              
        context= {'data':output}        
        return render(request, 'ViewDetails.html', context)

def ViewFarmer(request):
    if request.method == 'GET':
        output = '<table border=1 align=center width=100%>'
        font = '<font size="" color="black">'
        arr = ['Username','Contact No','Gender','Email ID','Address','User Type']
        output += "<tr>"
        for i in range(len(arr)):
            output += "<th>"+font+arr[i]+"</th>"
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'farmerapp',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * FROM signup where usertype='Farmer'")
            rows = cur.fetchall()
            for row in rows:
                username = row[0]
                
                contact = row[2]
                gender = row[3]
                email = row[4]
                address = row[5]
                utype = row[6]
                output += "<tr><td>"+font+str(username)+"</td>"
                
                output += "<td>"+font+contact+"</td>"
                output += "<td>"+font+str(gender)+"</td>"
                output += "<td>"+font+str(email)+"</td>"
                output += "<td>"+font+str(address)+"</td>"
                output += "<td>"+font+str(utype)+"</td>"              
        context= {'data':output}        
        return render(request, 'ViewDetails.html', context)

def ViewFruits(request):
    if request.method == 'GET':
        output = '<table border=1 align=center width=100%>'
        font = '<font size="" color="black">'
        arr = ['Product ID','Farmer Name','Product Name','crop Quantity (KG)','Price(Rs.) / KG','Product Location','Product Image']
        output += "<tr>"
        for i in range(len(arr)):
            output += "<th>"+font+arr[i]+"</th>"
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'farmerapp',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * FROM cropinfo")
            rows = cur.fetchall()
            for row in rows:
                crop_id = row[0]
                farmer_name = row[1]
                crop = row[3]
                quantity = row[4]
                price = row[5]
                location = row[6]
                image = row[7]
                output += "<tr><td>"+font+str(crop_id)+"</td>"
                output += "<td>"+font+farmer_name+"</td>"
                output += "<td>"+font+crop+"</td>"
                output += "<td>"+font+str(quantity)+"</td>"
                output += "<td>"+font+str(price)+"</td>"
                output += "<td>"+font+str(location)+"</td>"
                output += '<td><img src="/static/files/'+image+'" height="100" width="100"/></td>'                
        context= {'data':output}        
        return render(request, 'ViewDetails.html', context)

def ViewFruitDetails(request):
    if request.method == 'GET':
        output = '<table border=1 align=center width=100%>'
        font = '<font size="" color="black">'
        arr = ['Product ID','Farmer Name','Contact Number','Product Name','Crop Quantity (KG)','Price(Rs.) / KG','Product Location','Product Image','Cart']
        output += "<tr>"
        for i in range(len(arr)):
            output += "<th>"+font+arr[i]+"</th>"
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'farmerapp',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * FROM cropinfo")
            rows = cur.fetchall()
            for row in rows:
                crop_id = row[0]
                farmer_name = row[1]
                contact_no = row[2]
                crop = row[3]
                quantity = row[4]
                price = row[5]
                location = row[6]
                image = row[7]
                output += "<tr><td>"+font+str(crop_id)+"</td>"
                output += "<td>"+font+farmer_name+"</td>"
                output += "<td>"+font+contact_no+"</td>"
                output += "<td>"+font+crop+"</td>"
                output += "<td>"+font+str(quantity)+"</td>"
                output += "<td>"+font+str(price)+"</td>"
                output += "<td>"+font+str(location)+"</td>"
                output += '<td><img src="/static/files/'+image+'" height="100" width="100"/></td>'
                output += f'<td><a href="#" onclick="AddToCart({crop_id});">Add to Cart</a></td>'  # Modified here
        context = {'data': output}        
        return render(request, 'ViewFruitDetails.html', context)

def PriceUpdateAction(request):
    if request.method == 'POST':
        global uname
        cid = request.POST.get('t1', False)
        qty = request.POST.get('t2', False)
        price = request.POST.get('t3', False)
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'farmerapp',charset='utf8')
        db_cursor = db_connection.cursor()
        student_sql_query = "update cropinfo set crop_quantity="+str(float(qty))+", crop_price="+str(float(price))+" where crop_id='"+cid+"'" 
        db_cursor.execute(student_sql_query)
        db_connection.commit()
        print(db_cursor.rowcount, "Record Inserted")
        if db_cursor.rowcount == 1:
            output = "Product details updated"
        context= {'data':output}
        return render(request, 'FarmerScreen.html', context)
    

def PriceUpdateScreen(request):
    if request.method == 'GET':
        global uname
        cid = request.GET.get('t1', '')
        quantity = request.GET.get('t2', '')
        price = request.GET.get('t3', '')
        output = '<tr><td><font size="" color="black">Product&nbsp;Name</font></td><td><input type="text" name="t1" value="'+cid+'" size="30" readonly/></td></tr>'
        # Replace existing quantity value with the new one
        output += '<tr><td><font size="" color="black">New&nbsp;Quantity (KG)</font></td><td><input type="text" name="t2" value="' + quantity + '" size="30"/></td></tr>'
        output += '<tr><td><font size="" color="black">New&nbsp;Price (Rs.)</font></td><td><input type="text" name="t3" value="'+price+'" size="30"/></td></tr>'
        context= {'data':output}        
        return render(request, 'PriceUpdateScreen.html', context)




def UpdatePrice(request):
    if request.method == 'GET':
        global uname
        output = '<table border=1 align=center width=100%>'
        font = '<font size="" color="black">'
        arr = ['Product ID','Farmer Name','Product Name','crop Quantity (KG)','Price(Rs.) / KG','Product Location','Product Image','Update Details']
        output += "<tr>"
        for i in range(len(arr)):
            output += "<th>"+font+arr[i]+"</th>"
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'farmerapp',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * FROM cropinfo where farmer_name='"+uname+"'")
            rows = cur.fetchall()
            for row in rows:
                crop_id = row[0]
                farmer_name = row[1]
                crop = row[3]
                quantity = row[4]
                price = row[5]
                location = row[6]
                image = row[7]
                output += "<tr><td>"+font+str(crop_id)+"</td>"
                output += "<td>"+font+farmer_name+"</td>"
                output += "<td>"+font+crop+"</td>"
                output += "<td>"+font+str(quantity)+"</td>"
                output += "<td>"+font+str(price)+"</td>"
                output += "<td>"+font+str(location)+"</td>"
                output += '<td><img src="/static/files/'+image+'" height="100" width="100"/></td>'
                output += '<td><a href="PriceUpdateScreen?t1='+str(crop_id)+'&t2='+str(quantity)+'&t3='+str(price)+'">Click Here</a></td>'
        context= {'data':output}        
        return render(request, 'ViewPrices.html', context)


from django.http import HttpResponseBadRequest

def AddDetailsAction(request):
    if request.method == 'POST':
        global uname
        global contact
        cname = request.POST.get('t1', False)
        qty = request.POST.get('t2', False)
        price = request.POST.get('t3', False)
        desc = request.POST.get('t4', False)
        image = request.FILES.get('t5', False)  # Use get method to avoid KeyError if t5 is not present
        if not all([cname, qty, price, desc, image]):
            # If any required field is missing, return a bad request response
            return HttpResponseBadRequest("Missing required fields")
        
        if not image:
            return HttpResponseBadRequest("Please insert an image")
        
        imagename = image.name
        fs = FileSystemStorage()
        output = "Error in adding details"
        count = 0
        con = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='root', database='farmerapp', charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select count(*) from cropinfo")
            rows = cur.fetchall()
            for row in rows:
                count = row[0]
        count += 1
        db_connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='root', database='farmerapp', charset='utf8')
        db_cursor = db_connection.cursor()
        student_sql_query = "INSERT INTO cropinfo(crop_id, farmer_name, contact_no, crop_name, crop_quantity, crop_price, crop_location, crop_image) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        values = (str(count), uname, contact, cname, qty, price, desc, imagename)
        db_cursor.execute(student_sql_query, values)
        db_connection.commit()
        print(db_cursor.rowcount, "Record Inserted")
        if db_cursor.rowcount == 1:
            fs.save('farmerapp/static/files/' + imagename, image)
            output = cname + ' Product added successfully with ID ' + str(count)
        context = {'data': output}
        return render(request, 'AddDetails.html', context)

        

def AddDetails(request):
    if request.method == 'GET':
       return render(request, 'AddDetails.html', {})

def UserLogin(request):
    if request.method == 'GET':
       return render(request, 'UserLogin.html', {})  

def index(request):
    if request.method == 'GET':
       return render(request, 'index.html', {})

def AdminLogin(request):
    if request.method == 'GET':
       return render(request, 'AdminLogin.html', {})

def FarmerLogin(request):
    if request.method == 'GET':
       return render(request, 'FarmerLogin.html', {})    

def Signup(request):
    if request.method == 'GET':
       return render(request, 'Signup.html', {})

def AdminLoginAction(request):
    global uname
    if request.method == 'POST':
        username = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        if username == 'admin' and password == 'admin':
            uname = username
            context= {'data':' '}
            return render(request, 'Adminscreen.html', context)
        else:
            context= {'data':'login failed'}
            return render(request, 'AdminLogin.html', context)
        
def FarmerLoginAction(request):
    global uname
    global contact
    if request.method == 'POST':
        username = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        index = 0
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'farmerapp',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select username,password,usertype,contact_no FROM signup")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == username and password == row[1] and row[2] == 'Farmer':
                    uname = username
                    index = 1
                    contact = row[3]
                    break		
        if index == 1:
            context= {'data':' '}
            return render(request, 'FarmerScreen.html', context)
        else:
            context= {'data':'login failed'}
            return render(request, 'FarmerLogin.html', context)

def UserLoginAction(request):
    global uname
    if request.method == 'POST':
        username = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        index = 0
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'farmerapp',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select username,password,usertype FROM signup")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == username and password == row[1] and row[2] == 'User':
                    uname = username
                    index = 1
                    break		
        if index == 1:
            context= {'data':' '}
            return render(request, 'UserScreen.html', context)
        else:
            context= {'data':'login failed'}
            return render(request, 'UserLogin.html', context)        

def SignupAction(request):
    if request.method == 'POST':
        username = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        contact = request.POST.get('t3', False)
        gender = request.POST.get('t4', False)
        email = request.POST.get('t5', False)
        address = request.POST.get('t6', False)
        utype = request.POST.get('t7', False)
        output = "none"
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'farmerapp',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select username FROM signup")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == username:
                    output = username+ " Username already exists"
                    break
        if output == 'none':
            db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'farmerapp',charset='utf8')
            db_cursor = db_connection.cursor()
            student_sql_query = "INSERT INTO signup(username,password,contact_no,gender,email,address,usertype) VALUES('"+username+"','"+password+"','"+contact+"','"+gender+"','"+email+"','"+address+"','"+utype+"')"
            db_cursor.execute(student_sql_query)
            db_connection.commit()
            print(db_cursor.rowcount, "Record Inserted")
            if db_cursor.rowcount == 1:
                output =  "Signup Process Completed"
        context= {'data':output}
        return render(request, 'Signup.html', context)

def AddToCart(request, product_id):
    con = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='root', database='farmerapp', charset='utf8')
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM cartitems WHERE crop_id = %s", (product_id,))
        cart_row = cur.fetchone()
        cur.execute("SELECT * FROM cropinfo WHERE crop_id = %s", (product_id,))
        row = cur.fetchone()
        if cart_row:
            cart_item = (cart_row[3]+1, cart_row[4]+row[5], product_id)
            cur.execute("UPDATE cartitems SET crop_quantity = %s, crop_price = %s WHERE crop_id = %s", cart_item)
            con.commit()
            messages.success(request, 'Product updated in cart successfully.')
        else:
            if row:
                cart_item = (None, row[0], row[3], "1", row[5])
                cur.execute("INSERT INTO cartitems VALUES (%s, %s, %s, %s, %s)", cart_item)
                con.commit()
                messages.success(request, 'Product added to cart successfully.')
            else:
                messages.error(request, 'Product not found.')
    return redirect('ViewFruitDetails')



def cartitems(request):
    con = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='root', database='farmerapp', charset='utf8')
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM cartitems")
        rows = cur.fetchall()

        output = '<table border=1 align=center width=100%>'
        font = '<font size="" color="black">'
        arr = ['Cart ID', 'Product Name', 'Quantity (KG)', 'Price(Rs.) / KG']
        output += "<tr>"
        for i in range(len(arr)):
            output += "<th>" + font + arr[i] + "</th>"

        total_price = 0  # Initialize total price 
        for row in rows:
            output += "<tr>"
            for i in range(len(row)):
                if i != 1:
                    output += "<td>" + font + str(row[i]) + "</td>"
            total_price += row[4]  # Calculate total price for each item and add to total_price
        output += "</tr></table>"

    context = {'data': output, 'total_price': total_price}  # Pass total_price to the template
    return render(request, 'cartitems.html', context)


def placeorder(request):
    try:
        con = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='root', database='farmerapp', charset='utf8')
    except pymysql.Error as e:
        return HttpResponseServerError("Error connecting to the database: {}".format(str(e)))

    if request.method == 'POST':
        try:
            with con:
                cur = con.cursor()

                cur.execute("SELECT * FROM cartitems")
                cart_items = cur.fetchall()

                for item in cart_items:
                    crop_id = item[1]
                    crop_quantity = item[3]
                    cur.execute("UPDATE cropinfo SET crop_quantity = crop_quantity - %s WHERE crop_id = %s", (crop_quantity, crop_id))
                    cur.execute("DELETE FROM cartitems WHERE cart_id = %s", (item[0],))

                con.commit()
        except pymysql.Error as e:
            return HttpResponseServerError("Error executing SQL query: {}".format(str(e)))
        finally:
            try:
                if con.open:
                    con.close()
            except pymysql.Error as e:
                pass  # Connection is already closed or encountered an error during closing

        return render(request, 'orderconfirmation.html')

    return redirect('cartitems')
def payment(request):
    if request.method == 'POST':
        address = request.POST.get('address')
        payment_method = request.POST.get('payment')
        total_price = request.POST.get('total_price')  # Assuming total_price is passed from the cart page

        # Save the address and payment method to the database
        try:
            con = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='root', database='farmerapp', charset='utf8')
            with con:
                cur = con.cursor()
                
                # Insert address and total price
                cur.execute("INSERT INTO address (cart_id, total_price) SELECT cart_id, %s FROM cartitems", (total_price,))
                con.commit()

                # Update crop quantities in cropinfo table
                cur.execute("SELECT crop_id, crop_quantity FROM cartitems")
                cart_items = cur.fetchall()

                for item in cart_items:
                    crop_id = item[0]
                    crop_quantity = item[1]
                    cur.execute("UPDATE cropinfo SET crop_quantity = crop_quantity - %s WHERE crop_id = %s", (crop_quantity, crop_id))

                # Delete corresponding entries from the address table
                cur.execute("DELETE FROM address WHERE cart_id IN (SELECT cart_id FROM cartitems)")

                # Delete cart items
                cur.execute("DELETE FROM cartitems")

                con.commit()
        except pymysql.Error as e:
            return HttpResponseServerError("Error processing payment: {}".format(str(e)))
        finally:
            try:
                if con.open:
                    con.close()
            except pymysql.Error as e:
                pass  # Connection is already closed or encountered an error during closing

        # Redirect to order confirmation page
        return render(request, 'orderconfirmation.html', {'total_price': total_price})
    else:
        return HttpResponseBadRequest("Invalid request method")

def payment_success(request):
    # You can pass any additional context variables you want to display in the success page
    total_price = request.POST.get('total_price')  # Assuming you're passing the total_price from the payment view
    return render(request, 'success.html', {'total_price': total_price})

from django.shortcuts import redirect

def clear_cart(request):
    try:
        con = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='root', database='farmerapp', charset='utf8')
    except pymysql.Error as e:
        return HttpResponseServerError("Error connecting to the database: {}".format(str(e)))

    try:
        with con:
            cur = con.cursor()
            
            # Delete all cart items
            cur.execute("DELETE FROM cartitems")
            con.commit()
    except pymysql.Error as e:
        return HttpResponseServerError("Error clearing cart: {}".format(str(e)))
    finally:
        try:
            if con.open:
                con.close()
        except pymysql.Error as e:
            pass  # Connection is already closed or encountered an error during closing
    
    # Redirect to ViewFruitDetails page
    return redirect('ViewFruitDetails')









    # Logic to retrieve items from the cart
    # For example, you can retrieve items stored in session or database
    # Then render them in the cart_items.html page


     
    

      


