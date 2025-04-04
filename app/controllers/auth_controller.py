from app.models.user import User, db
from app.models.product import Product
from app.services.openai_service import get_psychology_response
from werkzeug.security import generate_password_hash, check_password_hash
from app.utils.validation import validate_email, validate_phone

# Estados da conversa
USER_STATES = {}

def handle_incoming_message(message, sender):
    user = User.query.filter_by(phone=sender).first()
    
    if not user:
        return initiate_registration(sender, message)
    
    if user.phone in USER_STATES:
        return handle_registration_flow(user, message)
    
    if message.lower() == 'login':
        return handle_login(sender)
    
    if 'basic_psychology' in user.purchased_products:
        return handle_psychology_query(message)
    
    return "Por favor, adquira um produto primeiro."

def initiate_registration(sender, message):
    USER_STATES[sender] = {'step': 1}
    return "Bem-vindo! Vamos começar seu cadastro.\nPor favor, digite seu email:"

def handle_registration_flow(user, message):
    state = USER_STATES[user.phone]
    
    if state['step'] == 1:
        if not validate_email(message):
            return "Email inválido. Por favor, digite um email válido:"
        
        user.email = message
        state['step'] = 2
        return "Agora crie uma senha (mínimo 6 caracteres):"
    
    elif state['step'] == 2:
        if len(message) < 6:
            return "Senha muito curta. Mínimo 6 caracteres:"
        
        user.password = message
        user.purchased_products = ['basic_psychology']  # Produto padrão
        db.session.add(user)
        db.session.commit()
        
        del USER_STATES[user.phone]
        return ("Cadastro completo! Você tem acesso ao psicólogo virtual.\n"
                "Digite sua dúvida ou questão:")
    
    return "Ocorreu um erro no cadastro. Por favor, tente novamente."

def handle_psychology_query(message):
    return get_psychology_response(message)

def register_user(phone_number, password):
    if not validate_phone(phone_number):
        return 'Invalid phone number'
    
    if User.query.filter_by(phone_number=phone_number).first():
        return 'User already exists'
    
    user = User(phone_number=phone_number)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return 'User registered successfully'

def login_user(phone_number, password):
    if not validate_phone(phone_number):
        return 'Invalid phone number'
    
    user = User.query.filter_by(phone_number=phone_number).first()
    if user and user.check_password(password):
        return 'Login successful'
    return 'Invalid credentials'

def list_products():
    products = Product.query.all()
    return [product.name for product in products]