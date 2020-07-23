from flask import make_response, jsonify,send_file
import requests
from app import api
import os
from flask_restplus import Api, Resource, fields
import tempfile
from app import plant_uml_decoder
from subprocess import Popen, PIPE
import re
import uuid
import sys
import locale

ns = api.namespace('', description='badges for gitlab')
@ns.route('/proxy/png/<encoded>')
@ns.param('encoded', 'The encoded script contents')
class OpenIssue(Resource):
    def get(self, encoded):
        """
        """
        print(sys.stdout.encoding)
        print(locale.getdefaultlocale())
        print(locale.getpreferredencoding())
        print(encoded)
        url = 'http://' + os.environ['PLANTUML_HOST'] + ':' + os.environ['PLANTUML_PORT'] + '/' + os.environ[
            'PLANTUML_URL'] + '/' + str(encoded)
        attachment_filename = 'plantuml.png'
        mimetype = 'image/png'
        try:
            decoded=plant_uml_decoder.plantuml_decode(encoded)
        except:
            process = Popen(['plantuml','-charset','UTF-8','-decodeurl', encoded[2:]], stdout=PIPE, stderr=PIPE)
            stdout, stderr = process.communicate()
            #print (stdout)
            #print('-++-')
            #print (stderr)
            decoded=stdout.decode('utf-8')
        attachment_filename = 'plantuml.png'
        mimetype = 'image/png'
        #print('::')
        #print (decoded)
        while(decoded.startswith('@startuml')):
            decoded=decoded[9:-8].strip()
        #print('::')
        #print (decoded)
        matcher=re.search(r'^#gnuplot\s+?(\d+)x(\d+).*$' ,decoded,re.MULTILINE)
        #if(matcher):
            #print('found gnuplot')
        if(decoded.startswith('%TeX')):
            decoded=decoded[4:].strip()
            #print('TeX')
            #print(decoded)
            texdoc='\\def\\formula{' + decoded + '}\\input{/var/www/apache-flask/formula.tex}'
            #print (texdoc)
            theuuid=uuid.uuid4()
            process = Popen(['pdflatex','-jobname',str(theuuid),'-output-directory', '/tmp', texdoc], stdout=PIPE, stderr=PIPE)
            stdout, stderr = process.communicate()
            #print (stdout)
            #print('----')
            #print (stderr)
            file_out=tempfile.NamedTemporaryFile(suffix='.png')
            #print(file_out.name)
            process = Popen(['convert', '-density', os.environ['TEX_DPI'], '/tmp/'+str(theuuid)+'.pdf', file_out.name], stdout=PIPE, stderr=PIPE)
            stdout, stderr = process.communicate()
            #print (stdout)
            #print('----')
            #print (stderr)
            attachment_filename="formula.png"
            return send_file(file_out.name,
                             as_attachment=True,
                             attachment_filename=attachment_filename,
                             mimetype=mimetype)
        elif matcher: #(decoded.startswith('#gnuplot')):
            file_script=tempfile.NamedTemporaryFile(suffix='.gpt')
            file_output = tempfile.NamedTemporaryFile(suffix='.png')
            m = re.search(r'(^\s*?set\s+?output\s*?[\'"]).*?([\'"].*?$)', decoded, re.MULTILINE)
            if m:
                decoded=re.sub(r"(^\s*?set\s+?output\s*?['\"]).*?(['\"].*?$)", r'\1'+file_output.name+r'\2', decoded, flags=re.MULTILINE)
            else:
                decoded='set output \''+file_output.name+'\'\n'+decoded
            m = re.search(r'(^\s*?set\s+?terminal.*?$)', decoded, re.MULTILINE)
            if m:
                decoded=re.sub(r"(^\s*?set\s+?terminal.*?$)", r'set terminal pngcairo size '+matcher.group(1)+','+matcher.group(2)+' enhanced', decoded, flags=re.MULTILINE)
            else:
                decoded='set terminal pngcairo size '+matcher.group(1)+','+matcher.group(2)+' enhanced\n'+decoded
            #print(matcher.group(1)+','+matcher.group(2))
            #print(decoded)
            with open(file_script.name, 'w') as f:
                f.write(decoded)
            #print(file_script.name)
            #print(file_output.name)
            process = Popen(['gnuplot',file_script.name], stdout=PIPE, stderr=PIPE)
            stdout, stderr = process.communicate()
            #print (stdout)
            #print('----')
            #print (stderr)
            attachment_filename="gnuplot.png"
            return send_file(file_output.name,
                             as_attachment=True,
                             attachment_filename=attachment_filename,
                             mimetype=mimetype)
        else:
            if(decoded.startswith('#wireviz')):
                encoded=plant_uml_decoder.plantuml_encode(decoded)
                url = 'http://' + os.environ['WIREVIZ_HOST'] + ':' + os.environ['WIREVIZ_PORT'] + '/' + os.environ[
                    'WIREVIZ_URL'] + '/' + str(encoded)
                attachment_filename = 'wireviz.png'
            else:
                url = 'http://' + os.environ['PLANTUML_HOST'] + ':' + os.environ['PLANTUML_PORT'] + '/' + os.environ['PLANTUML_URL'] + '/' + str(encoded)
                attachment_filename = 'plantuml.png'
            #print(url)
    #        headers = {'Private-Token': os.environ['GITLAB_SECRET']}
            headers={}
            r = requests.get(url, headers=headers)
            #    print (r.headers)
            if r.status_code == 200:
                #print(r.headers['Content-Type'])
                #if 'Content-Disposition' in r.headers:
                   #print(r.headers['Content-Disposition'])
                file_out=tempfile.NamedTemporaryFile()
                with open(file_out.name, 'wb') as out_file:
                    r.raw.decode_content = True
                    #print('writing '+file_out.name)
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
                dictionary= {}
                dictionary['msg']='Error'
                response = jsonify(dictionary)
                response.status_code = r.status_code
                return response
