from flask_cors import CORS
from flask import Flask, jsonify, request
from sqlalchemy import text
from os import environ
from .entities import entity
# from .entity import Session, engine, Base
# from .models import Tickets, TicketSchema, Contacts, ContactSchema, User, UserSchema
from passlib.hash import pbkdf2_sha256
from datetime import datetime, timedelta
from flask_jwt_extended import JWTManager,jwt_required, create_access_token
app = Flask(__name__)
CORS(app)
app.secret_key = "keeptherealtoyourselfeverytime"
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)

if __name__ == '__main__':
    app.run(debug = True)

jwt = JWTManager(app)

# @jwt.unauthorized_loader
# def unauthorized_response(callback):
#     return jsonify({
#         'ok': False,
#         'message': 'Missing Authorization Header'
#     }), 401
#######################################  REGISTER AND LOGIN #####################################
def authenticate(email, password):
    session = Session()
    user = session.query(User).filter_by(email=email).first()
    session.close()
    if user and pbkdf2_sha256.verify(password, user.password):
        return user
    else:
        return None

@app.route('/auth',methods=['POST'])
def auth_user():
    posted_data = request.get_json()
    user = authenticate(posted_data['email'],posted_data['password'])
    if not user:
         return jsonify({'ok':False, 'message': 'Invalid credentials!' }), 401
    access_token = create_access_token(identity=user.email)
    obj = {'email':user.email,'token':access_token,'fname':user.fname,'lname':user.lname}
    return jsonify({'ok': True, 'data': obj}), 200



@app.route('/register',methods=['POST'])
def add_user():

    # posted_data = UserSchema(only=('email','password','fname','lname')).load(json.loads(request.get_json()))
    # posted_data = request.get_json()
    # user = User(**posted_data)
    pd = request.get_json()
    user = User(pd['email'],pd['password'],pd['fname'],pd['lname'])
    session = Session()
    if session.query(User).filter_by(email = user.email).first():
        return jsonify({'message': 'User {} already exists'. format(user.email)}),401
    user.password = pbkdf2_sha256.hash(user.password)
    session.add(user)
    session.commit()
    session.close()
    return jsonify({'ok':True,'message': 'User created!'}),201


@app.route('/users',methods=['GET'])
def get_users():
    session = Session()
    user_objects = session.query(User).all()
    result = [{
        "id": user.id,
        "name": (user.fname+" "+user.lname)
    } for user in user_objects]
    # serializing as JSON
    session.close()
    return jsonify(result)


####################################### TICKET APIs #####################################
@app.route('/tickets',methods=['GET'])
def get_tickets():
    arg = request.args
    session = Session()
    # fetching from the database
    sort_arg = arg.get('sortedBy',default='created_at desc',type=str)
    builder = session.query(Tickets)
    ticket_objects = builder.order_by(Tickets.status,text(sort_arg)).all()
    schema = TicketSchema(many=True)
    tickets = schema.dump(ticket_objects)
    # serializing as JSON
    session.close()
    return jsonify(tickets)

@app.route('/tickets/<ticketId>',methods=['GET'])
def get_ticket_id(ticketId):
    session = Session()
    ticket_objects = session.query(Tickets).filter_by(id=ticketId).first()
    schema = TicketSchema()
    tickets = schema.dump(ticket_objects)
    # serializing as JSON
    session.close()
    return jsonify(tickets)

@app.route('/tickets/filter',methods=['GET'])
def ticket_filter():
    arg = request.args
    session = Session()
    # fetching from the database
    builder = session.query(Tickets)
    sort_arg=''
    for key in arg:
        if hasattr(Tickets,key):
            vals = request.args.getlist(key)
            print(getattr(Tickets,key))
            builder = builder.filter(getattr(Tickets,key).in_(vals))
        elif key=='sortedBy':
            sort_arg = arg.get('sortedBy',default='created_at desc',type=str)
    ticket_objects = builder.order_by(Tickets.status,text(sort_arg)).all()
    schema = TicketSchema(many=True)
    tickets = schema.dump(ticket_objects)
    # serializing as JSON
    session.close()
    return jsonify(tickets)

@app.route('/tickets/delete/<ticketId>',methods=['DELETE'])
def delete_ticket(ticketId):
    session = Session()
    ticket_obj = session.query(Tickets).filter_by(id=ticketId).first()
    session.delete(ticket_obj)
    session.commit()
    ticket_objects = session.query(Tickets).order_by(Tickets.status,Tickets.created_at.desc()).all()
    schema = TicketSchema(many=True)
    tickets = schema.dump(ticket_objects)
    session.close()
    return jsonify(tickets)


@app.route('/tickets', methods=['POST'])
def add_ticket():
    posted_ticket = TicketSchema(only=('subject', 'description','status','source','requester_id','responder_id','category')).load(request.get_json())
    ticket = Tickets(**posted_ticket)
    # persist exam
    session = Session()
    session.add(ticket)
    session.commit()
    # return created exam
    new_ticket = TicketSchema().dump(ticket)
    session.close()
    return jsonify(new_ticket), 201

@app.route('/tickets/update/<ticketId>', methods=['PUT'])
def update_ticket(ticketId):
    session = Session()
    posted_ticket = TicketSchema().load(request.get_json())
    session.query(Tickets).filter_by(id=ticketId).update(posted_ticket,synchronize_session=False)
    session.commit()
    session.close()
    return posted_ticket,201



####################################### CONTACT APIs #####################################


@app.route('/contacts', methods=['POST'])
def add_contact():
    pc = request.get_json()
    session = Session()
    contact = Contacts(pc['name'],pc['email'],pc['phone'],pc['company_name'])
    session.add(contact)
    session.commit()
    session.close()
    return jsonify({'ok':True,'message': 'Contact created!'}),201




@app.route('/contacts',methods=['GET'])
def get_contacts():
    # fetching from the database
    session = Session()
    contact_objects = session.query(Contacts).order_by(Contacts.created_at).all()
    results = [
            {
                "id":contact.id,
                "name": contact.name,
                "email": contact.email,
                "phone": contact.phone,
                "company_name": contact.company_name
            } for contact in contact_objects]
    # schema = ContactSchema(many=True)
    # contacts = schema.dump(contact_objects)
    session.close()
    # return jsonify(contacts)
    return jsonify(results)

@app.route('/contacts/<contactId>',methods=['GET'])
def get_contact_id(contactId):
    session = Session()
    contact_obj = session.query(Contacts).filter_by(id=contactId).first()
    result = {
                "id": contact_obj.id,
                "name": contact_obj.name,
                "email": contact_obj.email,
                "phone": contact_obj.phone,
                "company_name": contact_obj.company_name,
    }
    # serializing as JSON
    session.close()
    return jsonify(result)
    

@app.route('/contacts/delete/<contactId>', methods=['DELETE'])
def delete_contact(contactId):
    session = Session()
    contact_obj = session.query(Contacts).filter_by(id=contactId).first()
    session.delete(contact_obj)
    session.commit()
    session.close()
    return '', 201


@app.route('/contacts/update/<contactId>', methods=['PUT'])
def update_contact(contactId):
    session = Session()
    pc = request.get_json()
    # contact_obj = pc['name'],pc['email'],pc['phone'],pc['company_name'])
    session.query(Contacts).filter_by(id=contactId).update(pc,synchronize_session=False)
    session.commit()
    session.close()
    return jsonify(pc),201