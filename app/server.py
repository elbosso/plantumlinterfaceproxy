from flask import send_file
import requests
from app import api
import os
from flask_restplus import Api, Resource, fields
import tempfile
from app import plant_uml_decoder
from app import text2png
from subprocess import Popen, PIPE
import re
import uuid
import sys
import locale
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import tempfile
from shutil import copyfile
import cairosvg


ns = api.namespace('', description='badges for gitlab')
@ns.route('/proxy/png/<encoded>')
@ns.param('encoded', 'The encoded script contents')
class OpenIssue(Resource):
    @staticmethod
    def representsInt(s):
        try:
            int(s)
            return True
        except ValueError:
            return False
    def get(self, encoded):
        """
        """
        print(sys.stdout.encoding)
        print(locale.getdefaultlocale())
        print(locale.getpreferredencoding())
        print(encoded)
#        url = os.environ['PLANTUML_PROTOCOL']+'://' + os.environ['PLANTUML_HOST'] + ':' + os.environ['PLANTUML_PORT'] + '/' + os.environ[
#            'PLANTUML_URL'] + '/' + str(encoded)
        attachment_filename = 'plantuml.png'
        mimetype = 'image/png'
        try:
            decoded=plant_uml_decoder.plantuml_decode(encoded)
        except:
            todecode=encoded
            if encoded.startswith('~'):
                todecode=encoded[2:]
            process = Popen(['plantuml','-charset','UTF-8','-decodeurl', todecode], stdout=PIPE, stderr=PIPE)
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
        matchergnuplot=re.search(r'^#gnuplot\s+?(\d+)x(\d+).*$' ,decoded,re.MULTILINE)
        matchertex=re.search(r'^(%TeX\s+?(\d*)).*$' ,decoded,re.MULTILINE)
        #if(matchergnuplot):
            #print('found gnuplot')
        if matchertex:
        #if(decoded.startswith('%TeX')):
            decoded=decoded[len(matchertex.group(1)):].strip()
            #print('TeX')
            #print(decoded)
            #texdoc='\\def\\formula{' + decoded + '}\\input{/home/elbosso/formula.tex}'
            if self.representsInt(matchertex.group(2)):
                texdoc='\\def\\formulaCounter{'+matchertex.group(2)+'}\\def\\formula{' + decoded + '}\\input{/var/www/apache-flask/formula.tex}'
            else:
                texdoc='\\def\\formula{' + decoded + '}\\input{/var/www/apache-flask/formula.tex}'
            #print (texdoc)
            theuuid=uuid.uuid4()
            process = Popen(['pdflatex','-halt-on-error','-jobname',str(theuuid),'-output-directory', '/tmp', texdoc], stdout=PIPE, stderr=PIPE)
            stdout, stderr = process.communicate()
            if process.returncode==0:
                file_out=tempfile.NamedTemporaryFile(suffix='.png')
                dpi='95'
                if 'TEX_DPI' in os.environ:
                    dpi=os.environ['TEX_DPI']
                process = Popen(['convert', '-density', dpi, '/tmp/'+str(theuuid)+'.pdf', file_out.name], stdout=PIPE, stderr=PIPE)
                stdout, stderr = process.communicate()
                if process.returncode==0:
                    attachment_filename="formula.png"
                    return send_file(file_out.name,
                             as_attachment=True,
                             attachment_filename=attachment_filename,
                             mimetype=mimetype)
                else:
                    err = stderr.decode("UTF-8")
                    if len(stderr) < 1:
                        err = stdout.decode("UTF-8")
                    return self.errMgmt(err)
            else:
                err=stderr.decode("UTF-8")
                if len(stderr) <1:
                    err=stdout.decode("UTF-8")
                return self.errMgmt(err)
        elif matchergnuplot: #(decoded.startswith('#gnuplot')):
            file_script=tempfile.NamedTemporaryFile(suffix='.gpt')
            file_output = tempfile.NamedTemporaryFile(suffix='.png')
            m = re.search(r'(^\s*?set\s+?output\s*?[\'"]).*?([\'"].*?$)', decoded, re.MULTILINE)
            if m:
                decoded=re.sub(r"(^\s*?set\s+?output\s*?['\"]).*?(['\"].*?$)", r'\1'+file_output.name+r'\2', decoded, flags=re.MULTILINE)
            else:
                decoded='set output \''+file_output.name+'\'\n'+decoded
            m = re.search(r'(^\s*?set\s+?terminal.*?$)', decoded, re.MULTILINE)
            if m:
                decoded=re.sub(r"(^\s*?set\s+?terminal.*?$)", r'set terminal pngcairo size '+matchergnuplot.group(1)+','+matchergnuplot.group(2)+' enhanced', decoded, flags=re.MULTILINE)
            else:
                decoded='set terminal pngcairo size '+matchergnuplot.group(1)+','+matchergnuplot.group(2)+' enhanced\n'+decoded
            #print(matchergnuplot.group(1)+','+matchergnuplot.group(2))
            #print(decoded)
            with open(file_script.name, 'w') as f:
                f.write(decoded)
            #print(file_script.name)
            #print(file_output.name)
            process = Popen(['gnuplot',file_script.name], stdout=PIPE, stderr=PIPE)
            stdout, stderr = process.communicate()
            if process.returncode==0:
                attachment_filename="gnuplot.png"
                return send_file(file_output.name,
                             as_attachment=True,
                             attachment_filename=attachment_filename,
                             mimetype=mimetype)
            else:
                err=stderr.decode("UTF-8")
                if len(stderr) <1:
                    err=stdout.decode("UTF-8")
                return self.errMgmt(err)
        elif decoded.startswith('#regex'):
            try:
                dir_out = tempfile.TemporaryDirectory()

                print(dir_out.name)

                fxProfile = FirefoxProfile()

                fxProfile.set_preference("browser.download.folderList", 2)
                fxProfile.set_preference("browser.download.manager.showWhenStarting", False)
                fxProfile.set_preference("browser.download.dir", dir_out.name)
                fxProfile.set_preference("browser.helperApps.neverAsk.saveToDisk", "image/png,image/svg+xml")

                opts = Options()
                #opts.set_headless()
                opts.add_argument("--headless")
                #assert opts.headless  # Operating in headless mode
                geckoPath = './geckodriver'
                browser = Firefox(firefox_profile=fxProfile, executable_path=geckoPath, options=opts)
                browser.get('http://dockerhost.docker.lab:8077')
                search_form = browser.find_element_by_id('regexp-input')
                search_form.send_keys(decoded[6:].strip())
                search_form.submit()
                links = browser.find_elements_by_class_name('inline-icon')
                print(len(links))
                if(len(links)>0):
                    for link in links:
                        print(link.get_attribute("data-action"))
                        if (link.get_attribute("data-action") == 'download-png'):
                            print(link.get_attribute("href"))
                            WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, "//a[starts-with(@data-action, 'download-png')]"))).click()
                            link.click()
                            browser.close()
                            browser.quit()
                            attachment_filename = "re.png"
                            return send_file(dir_out.name + '/image.png',
                             as_attachment=True,
                             attachment_filename=attachment_filename,
                             mimetype=mimetype)
                else:
                    links = browser.find_elements_by_class_name('oi')
                    print('links: '+str(len(links)))
                    for link in links:
                        print(link.get_attribute("data-glyph"))
                        if (link.get_attribute("data-glyph") == 'data-transfer-download'):
                            print(link.get_attribute("href"))
                            WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, "//a[starts-with(@data-glyph, 'data-transfer-download')]"))).click()
                            link.click()
                            browser.close()
                            browser.quit()
                            print(os.listdir(dir_out.name))
                            cairosvg.svg2png(url=dir_out.name + '/image.svg', write_to=dir_out.name + '/image.png')                        
                            attachment_filename = "re.png"
                            return send_file(dir_out.name + '/image.png',
                             as_attachment=True,
                             attachment_filename=attachment_filename,
                             mimetype=mimetype)
            except Exception as exp:
                return self.errMgmt(exp.__str__())
        else:
            if(decoded.startswith('#wireviz')):
                encoded=plant_uml_decoder.plantuml_encode(decoded)
                url = os.environ['WIREVIZ_PROTOCOL'] +'://' + os.environ['WIREVIZ_HOST'] + ':' + os.environ['WIREVIZ_PORT'] + '/' + os.environ[
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
                if r.headers['Content-Type'] == 'image/png':
                    file_out = tempfile.NamedTemporaryFile()
                    with open(file_out.name, 'wb') as out_file:
                        r.raw.decode_content = True
                        # print('writing '+file_out.name)
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
                    err = r.content.decode("UTF-8")
                    return self.errMgmt(err)
    def errMgmt(self, err):
        """
        """
        file_out=tempfile.NamedTemporaryFile(suffix='.png')
        #resp = Response(err, mimetype='text/plain')
        #resp.status_code = 200
        #return resp
        text2png.text2png(err, file_out.name, fontfullpath="arial.ttf",width=600)
        return send_file(file_out.name,
                                as_attachment=True,
                                attachment_filename='error.png',
                                mimetype='image/png')