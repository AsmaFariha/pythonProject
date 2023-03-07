import justpy as jp
from pymongo import MongoClient
import smtplib , ssl

button_classes = 'bg-transparent hover:bg-blue-500 text-blue-700 font-semibold hover:text-white py-2 px-4 border border-blue-500 hover:border-transparent rounded m-2'
input_classes = 'border m-2 p-2'
session_data = {}

@jp.SetRoute('/login')
def user_login():
    wp = jp.WebPage()
    wp.display_url = '/User_Login'

    form1 = jp.Form(a=wp, classes='border m-8 p-8 w-128 l-256')

    user_label = jp.Label(text='User Name', classes='block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2', a=form1)
    in1 = jp.Input(placeholder='User Name', a=form1, classes='form-input')
    user_label.for_component = in1

    password_label = jp.Label(classes='block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2 mt-2', a=form1)
    jp.Div(text='Password', classes='block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2', a=password_label)
    jp.Input(placeholder='Password', a=password_label, classes='form-input', type='password')

    submit_button = jp.Input(value='Login', type='submit', a=form1, classes=button_classes)

    def submit_form(self, msg):
        print(msg)
        msg.page.redirect = '/form_submitted'
        session_data[msg.session_id] = msg.form_data

    form1.on('submit', submit_form)

    return wp

@jp.SetRoute('/form_submitted')
def form_submitted(request):
    wp = jp.WebPage()
    wp.display_url = '/verification'
    #form_verification = jp.Form(a=wp, classes='border m-8 p-8 w-128 l-256')
    for field in session_data[request.session_id]:
        if field.type in ['text']:
            username = field.value
            jp.Div(text=f'{field.placeholder}:  {field.value}', a=wp, classes='text-lg m-1 p-1')
        if field.type in ['password']:
            passwordvalue = field.value

    cluster = MongoClient("mongodb+srv://asmafariha:access123@cluster0.t1qqadg.mongodb.net/?retryWrites=true&w=majority")
    db = cluster["jobhuntbuddy"]
    collection = db["UserList"]
    collection_cache = db["cache"]

    def button_click_Home(self, msg):
        msg.page.redirect = "/home"

    def button_click_registration(self, msg):
        msg.page.redirect = "/registration"

    text="N"
    results = collection.find({"_id": username})
    for result in results:
        if result["password"] == passwordvalue:
            text = "Verified"
            collection_cache.insert_one({"_id":username})
            jp.Div(text='Thank you for login', a=wp, classes='text-xl m-2 p-2')
            button_div = jp.Div(classes='flex m-4 flex-wrap', a=wp)
            jp.Button(text='Home Page', a=button_div, classes=button_classes, click=button_click_Home)
    if text == "N":
        jp.Div(text='Authentication Failed!!!', a=wp, classes='text-lg m-1 p-1')
        button_div = jp.Div(classes='flex m-4 flex-wrap', a=wp)
        jp.Button(text='Register', a=button_div, classes=button_classes, click=button_click_registration)

    return wp


##########User Registration phase###############
@jp.SetRoute('/registration')
def form_registration():
    wp = jp.WebPage()
    wp.display_url = '/registration'  # Input form

    form1 = jp.Form(a=wp, classes='border m-8 p-8 w-128 l-256')

    user_label1 = jp.Label(text='User Name',
                           classes='block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2', a=form1)
    in1 = jp.Input(placeholder='User Name', a=form1, classes='form-input')
    user_label1.for_component = in1

    user_label2 = jp.Label(text='Email Address',
                           classes='block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2', a=form1)
    in2 = jp.Input(placeholder='Input valid Email', a=form1, classes='form-input')
    user_label2.for_component = in2

    password_label = jp.Label(classes='block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2 mt-2',
                              a=form1)
    jp.Div(text='Password', classes='block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2',
           a=password_label)
    passw = jp.Input(placeholder='Password', a=password_label, classes='form-input', type='password')

    submit_button = jp.Input(value='Register', type='submit', a=form1, classes=button_classes)

    # Submit button action
    def submit_form(self, msg):
        print(msg)
        print(in1.value)
        cluster = MongoClient(
            "mongodb+srv://asmafariha:access123@cluster0.t1qqadg.mongodb.net/?retryWrites=true&w=majority")
        db = cluster["jobhuntbuddy"]
        collection_auth = db["UserList"]
        collection_prof = db["UserProfile"]

        if collection_auth.count_documents({"_id": in1.value}) >= 1:
            jp.Div(text='UserName already in use. Try Another', classes=button_classes, a=wp)  # Check existing user
        else:
            post_user = {"_id": in1.value,
                         "password": passw.value}  # Add new user in authentication and user profile tables
            post_profile = {"_id": in1.value, "email": in2.value}
            collection_auth.insert_one(post_user)
            collection_prof.insert_one(post_profile)
            jp.Div(text='Registration Successful', classes=button_classes, a=wp)
            msg.page.redirect = "/login"
            # sending email
            sender = 'postmaster@sandboxc6cbdf39d9614ad6a792f43b19b7d6d6.mailgun.org'
            receivers = [in2.value]
            message = """From: From <JobHuntBuddy>

            Subject: Successful Registration

            Welcome to JobHuntBuddy portal! Wish you success!!!
            """
            smtpObj = smtplib.SMTP('smtp.mailgun.org', 587)
            smtpObj.starttls(context=ssl.create_default_context())
            smtpObj.login(sender, '653940aa7dddc84922ea87e7df43be32-15b35dee-a761ee1d')
            smtpObj.sendmail(sender, receivers, message)

    form1.on('submit', submit_form)
    return wp


#######HomePage
@jp.SetRoute('/home')
async def home(request):
    wp = jp.WebPage(data={'text': 'Initial text'})
    wp.display_url= '/Home-List of Application'

    cluster = MongoClient( "mongodb+srv://asmafariha:access123@cluster0.t1qqadg.mongodb.net/?retryWrites=true&w=majority")
    db = cluster["jobhuntbuddy"]
    collection = db["cache"]
    result = collection.find_one()
    jp.Div(text=result["_id"], a=wp, classes='text-lg m-1 p-1')


    def add_application(self, msg):
        msg.page.redirect = "/application"

    def logout_action(self, msg):
        msg.page.redirect = "/logout"

    button_div = jp.Div(classes='flex m-4 flex-wrap', a=wp)
    jp.Button(text='Add New Application', a=button_div, classes=button_classes, click=add_application)

    input_classes = "m-2 bg-gray-200 appearance-none border-2 border-gray-200 rounded xtw-64 py-2 px-4 text-gray-700 focus:outline-none focus:bg-white focus:border-purple-500"

    cluster = MongoClient( "mongodb+srv://asmafariha:access123@cluster0.t1qqadg.mongodb.net/?retryWrites=true&w=majority")
    db = cluster["jobhuntbuddy"]
    collection = db["UserActivityList"]
    results= collection.find({"username":result["_id"]})
    for result in results:
        jp.Div(text=result["companyname"], classes=input_classes, a=wp)
        jp.Div(text=result["companywebsite"], classes=input_classes, a=wp)
        jp.Div(text=result["jobtitle"], classes=input_classes, a=wp)
        jp.Div(text=result["date"], classes=input_classes, a=wp)
        jp.Div(text=result["coverletter"], classes=input_classes, a=wp)

    button_div = jp.Div(classes='flex m-4 flex-wrap', a=wp)
    jp.Button(text='Logout', a=button_div, classes=button_classes, click=logout_action)

    return wp


#############Entry of Newly submitted Application info
@jp.SetRoute('/application')
def form_application(request):
    wp = jp.WebPage()
    wp.display_url = '/SaveApplication'  # Input form

    def logout_action(self, msg):
        msg.page.redirect = "/logout"

    button_div = jp.Div(classes='flex m-4 flex-wrap', a=wp)
    jp.Button(text='Logout', a=button_div, classes=button_classes, click=logout_action)

    cluster = MongoClient( "mongodb+srv://asmafariha:access123@cluster0.t1qqadg.mongodb.net/?retryWrites=true&w=majority")
    db = cluster["jobhuntbuddy"]
    collection = db["cache"]
    result = collection.find_one()
    jp.Div(text=result["_id"], a=wp, classes='text-lg m-1 p-1')

    form1 = jp.Form(a=wp, classes='border m-8 p-8 w-128 l-256')

    user_label1 = jp.Label(text='Company Name',
                           classes='block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2', a=form1)
    in1 = jp.Input(placeholder='Type company name here', a=form1, classes='form-input')
    user_label1.for_component = in1

    user_label3 = jp.Label(text='Address',
                           classes='block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2', a=form1)
    in3 = jp.Input(placeholder='Put Postal Code here', a=form1, classes='form-input')
    user_label3.for_component = in3

    user_label2 = jp.Label(text='Email Address',
                           classes='block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2', a=form1)
    in2 = jp.Input(placeholder='Input valid Email', a=form1, classes='form-input')
    user_label2.for_component = in2

    user_label4 = jp.Label(text='Job Title',
                           classes='block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2', a=form1)
    in4= jp.Input(placeholder='Input valid Email', a=form1, classes='form-input')
    user_label4.for_component = in4

    user_label5 = jp.Label(text='Job Description',
                           classes='block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2', a=form1)
    in5 =jp.Textarea(placeholder='Input the job responsibility and Requirement here', a=form1, classes='form-input')
    user_label5.for_component = in5

    user_label6 = jp.Label(text='Salary',
                           classes='block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2', a=form1)
    in6= jp.Input(placeholder='Salary Range (If posted)', a=form1, classes='form-input')
    user_label6.for_component=in6

    user_label7 = jp.Label(text='Website',
                           classes='block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2', a=form1)
    in7= jp.Input(placeholder='Company website', a=form1, classes='form-input')
    user_label7.for_component=in7


    user_label8 = jp.Label(text='Application Source',
                           classes='block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2', a=form1)
    in8= jp.Input(placeholder='Where did you find and applied for this job', a=form1, classes='form-input')
    user_label8.for_component =in8

    user_label10 = jp.Label(text='Application Date mm/DD/YYYY',
                           classes='block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2', a=form1)
    in10= jp.Input(placeholder='Date applied on', a=form1, classes='form-input')
    user_label10.for_component = in10

    user_label9 = jp.Label(text='Cover Letter',
                           classes='block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2', a=form1)
    in9=user_label9.for_component = jp.Textarea(placeholder='Put here if you want to store', a=form1,
                                         classes='form-input')
    user_label9.for_component = in9


    submit_button = jp.Input(value='Save', type='submit', a=form1, classes=button_classes)

    # Submit button action
    def submit_form(self, msg):
        print(msg)
        print(in1.value)
        cluster = MongoClient("mongodb+srv://asmafariha:access123@cluster0.t1qqadg.mongodb.net/?retryWrites=true&w=majority")
        db = cluster["jobhuntbuddy"]
        collection = db["UserActivityList"]
        collection_cache=db["cache"]

        username= collection_cache.find_one();

        post_apps = {"username":username["_id"] ,"companyname":in1.value , "companywebsite": in7.value , "email":in3.value  , "jobtitle": in4.value , "address": in2.value , "date":in10.value ,
                "description":in5.value ,"salary": in6.value ,"coverletter": in9.value ,"source":in8.value }
        collection.insert_one(post_apps)
        jp.Div(text='Your Application summary Successfully saved', classes=button_classes, a=wp)
        msg.page.redirect = "/home"

    form1.on('submit', submit_form)

    return wp

@jp.SetRoute('/logout')
async def logout(request):
    wp = jp.WebPage()
    wp.display_url= '/JobHuntBudy_Logout'


    input_classes = "m-2 bg-gray-200 appearance-none border-2 border-gray-200 rounded xtw-64 py-2 px-4 text-gray-700 focus:outline-none focus:bg-white focus:border-purple-500"

    cluster = MongoClient( "mongodb+srv://asmafariha:access123@cluster0.t1qqadg.mongodb.net/?retryWrites=true&w=majority")
    db = cluster["jobhuntbuddy"]
    collection = db["cache"]
    collection.drop()
    jp.Div(text="Thank you for Logout!!!!", classes=input_classes, a=wp)

    return wp

def main(argv=None):
    jp.justpy(user_login)


if __name__ == "__main__":
    main()
