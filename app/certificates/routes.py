from flask import render_template, request, make_response, jsonify
from app.certificates import bp
from app import db
from app.certificates.models import Certificate
# from app.forms import NewCertificateForm
from datetime import datetime


@bp.route('/', methods=['GET'])
def all_certificates():
    return render_template('certificates.html', certificates=Certificate.query.all())


@bp.route('/<certificate_id>', methods=['GET'])
def certificate(certificate_id):
    return render_template('certificate.html', certificate=Certificate.query.get(certificate_id))

@bp.route('/new_certificate', methods=['POST'])
def new_certificate():
    request_data = request.get_json()
    print('request_data: ', request_data)
    certificate = Certificate.create(user_id=request_data['user_id'], company_id=request_data['company_id'], points=request_data['points'])
    print('certificate: ', certificate)
    certificate_json = certificate.serialize()
    print('certificate_json: ', certificate_json)
    response_data = {
        "message": "Certificate created successfully",
        "certificate": certificate_json,
    }
    response = make_response(jsonify(response_data), 200)
    return response

@bp.route('/delete/<int:id>', methods=['GET','POST'])
def delete(id):
    certificate = Certificate.query.get(id)
    certificate.delete()
    return render_template('certificates.html', certificates=Certificate.query.all())