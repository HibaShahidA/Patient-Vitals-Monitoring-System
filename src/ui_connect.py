from flask import Flask, request, redirect, session, send_from_directory
from auth_utils import authenticate_staff, is_authorized_for_patient

app = Flask(__name__, static_folder='../frontend', static_url_path='')
app.secret_key = 'secret' # for managing login 
