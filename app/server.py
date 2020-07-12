from flask import make_response, jsonify,send_file
import requests
from app import api
import os
from flask_restplus import Api, Resource, fields
import tempfile
from app import plant_uml_decoder
from subprocess import Popen, PIPE

ns = api.namespace('', description='badges for gitlab')
@ns.route('/proxy/<encoded>')
@ns.param('encoded', 'The encoded script contents')
class OpenIssue(Resource):
    def get(self, encoded):
        """
        """
        url = 'http://' + os.environ['PLANTUML_HOST'] + ':' + os.environ['PLANTUML_PORT'] + '/' + os.environ[
            'PLANTUML_URL'] + '/' + str(encoded)
        decoded=plant_uml_decoder.plantuml_decode(encoded)
        attachment_filename = 'plantuml.png'
        mimetype = 'image/png'
        if(decoded.startswith('%TeX')):
            decoded=decoded[4:].strip()
            print('TeX')
            print(decoded)
            texdoc='\\def\\formula{' + decoded + '}\\input{/home/elbosso/formula.tex}'
            print (texdoc)
            process = Popen(['pdflatex', texdoc], stdout=PIPE, stderr=PIPE)
            stdout, stderr = process.communicate()
            print (stdout)
            print('----')
            print (stderr)
            file_out=tempfile.NamedTemporaryFile()
            print(file_out.name)
            process = Popen(['convert', '-density', '130', 'formula.pdf', file_out.name+'.png'], stdout=PIPE, stderr=PIPE)
            stdout, stderr = process.communicate()
            print (stdout)
            print('----')
            print (stderr)
            attachment_filename="formula.png"
            return send_file(file_out.name+'.png',
                             as_attachment=True,
                             attachment_filename=attachment_filename,
                             mimetype=mimetype)
        else:
            if(decoded.startswith('#wireviz')):
                url = 'http://' + os.environ['WIREVIZ_HOST'] + ':' + os.environ['WIREVIZ_PORT'] + '/' + os.environ[
                    'WIREVIZ_URL'] + '/' + str(encoded)
                attachment_filename = 'wireviz.png'
            else:
                url = 'http://' + os.environ['PLANTUML_HOST'] + ':' + os.environ['PLANTUML_PORT'] + '/' + os.environ['PLANTUML_URL'] + '/' + str(encoded)
                attachment_filename = 'plantuml.png'
            print(url)
    #        headers = {'Private-Token': os.environ['GITLAB_SECRET']}
            headers={}
            r = requests.get(url, headers=headers)
            #    print (r.headers)
            if r.status_code == 200:
                print(r.headers['Content-Type'])
                if 'Content-Disposition' in r.headers:
                   print(r.headers['Content-Disposition'])
                file_out=tempfile.NamedTemporaryFile()
                with open(file_out.name, 'wb') as out_file:
                    r.raw.decode_content = True
                    print('writing '+file_out.name)
                    out_file.write(r.content)
                file_out.seek(0)
                if 'Content-Type' in r.headers:
                    mimetype = r.headers['Content-Type']
                if 'Content-Disposition' in r.headers:
                    attachment_filename = r.headers['Content-Disposition']
                return send_file(file_out.name,
                                         as_attachment=True,
                                         attachment_filename=attachment_filename,
                                         mimetype=mimetype)
            else:
                dictionary=dict()
                dict['msg']='Error'
                response = jsonify(dictionary)
                response.status_code = r.status_code
                return response
