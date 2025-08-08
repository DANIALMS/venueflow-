from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, SelectField, TextAreaField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Optional

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class LeadForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[Optional()])
    email = StringField('Email', validators=[Optional(), Email()])
    phone = StringField('Phone', validators=[Optional()])
    source = StringField('Lead Source', validators=[Optional()])
    event_type = StringField('Event Type', validators=[Optional()])
    event_date = StringField('Event Date', validators=[Optional()])
    guest_count = IntegerField('Guest Count', validators=[Optional()])
    budget_min = IntegerField('Budget Min', validators=[Optional()])
    budget_max = IntegerField('Budget Max', validators=[Optional()])
    stage = SelectField('Stage', choices=[(s,s) for s in ['New','Qualified','Toured','Proposal','Contract Sent','Booked','Won','Lost']])
    next_action = StringField('Next Action', validators=[Optional()])
    next_action_due = StringField('Next Action Due', validators=[Optional()])
    notes = TextAreaField('Notes', validators=[Optional()])
    submit = SubmitField('Save')

class EventForm(FlaskForm):
    name = StringField('Event Name', validators=[DataRequired()])
    event_type = StringField('Event Type', validators=[Optional()])
    venue_space = StringField('Venue Space', validators=[Optional()])
    event_date = StringField('Event Date', validators=[Optional()])
    start_time = StringField('Start', validators=[Optional()])
    end_time = StringField('End', validators=[Optional()])
    guest_count = IntegerField('Guests', validators=[Optional()])
    package = StringField('Package', validators=[Optional()])
    food_service = StringField('Food Service', validators=[Optional()])
    bar_service = StringField('Bar Service', validators=[Optional()])
    status = SelectField('Status', choices=[(s,s) for s in ['Tentative','Confirmed','Canceled']])
    contract_status = SelectField('Contract', choices=[(s,s) for s in ['Draft','Sent','Signed']])
    assigned_manager = StringField('Assigned Manager', validators=[Optional()])
    submit = SubmitField('Save')

class TaskForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    owner = StringField('Owner', validators=[Optional()])
    due_date = StringField('Due Date', validators=[Optional()])
    status = SelectField('Status', choices=[('Open','Open'),('Done','Done')])
    priority = SelectField('Priority', choices=[('Low','Low'),('Medium','Medium'),('High','High')])
    submit = SubmitField('Save')

class InvoiceForm(FlaskForm):
    issue_date = StringField('Issue Date', validators=[Optional()])
    due_date = StringField('Due Date', validators=[Optional()])
    tax_percent = FloatField('Tax %', validators=[Optional()])
    service_fee_percent = FloatField('Service Fee %', validators=[Optional()])
    gratuity_percent = FloatField('Gratuity %', validators=[Optional()])
    submit = SubmitField('Save')

class LineItemForm(FlaskForm):
    item = StringField('Item', validators=[DataRequired()])
    qty = IntegerField('Qty', validators=[Optional()])
    unit_price = FloatField('Unit Price', validators=[Optional()])
    submit = SubmitField('Add')
