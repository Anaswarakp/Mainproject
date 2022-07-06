import datetime
from django.contrib.auth.models import User
from django.shortcuts import render
from datetime import date
from django.views import View
from django.views.generic import TemplateView
import hashlib
import json
from django.http import JsonResponse
from cryptography.fernet import Fernet
from Crime.models import Blockchain_admin, Blockchain_ledger, Fir, Blockchain_ledger_encripted
from cryptography.fernet import Fernet

class Indexview(TemplateView):
    template_name = 'officer/officer_index.html'


class blockchain_profile(TemplateView):
    template_name = 'officer/blockchain_index.html'


class Blockchain_login(TemplateView):
    template_name = 'officer/admin_login.html'

    def post(self, request, *args, **kwargs):
        user = User.objects.get(id=self.request.user.id)
        key = request.POST['key']
        if (Blockchain_admin.objects.filter(user_id=user,key=key)):

            return render(request, 'officer/admin_index.html', {'message': " login Successfully"})

        else:
            return render(request, 'officer/officer_index.html', {'message': " invalid key"})

# class View_Fir(TemplateView):
#     template_name = 'officer/view_fir.html'
#     def get_context_data(self, **kwargs):
#         context = super(View_Fir,self).get_context_data(**kwargs)
#         key = Fernet.generate_key()
#         fernet = Fernet(key)
#         encMessage = fernet.encrypt(m.encode())
#         print("111111111111111111",encMessage)
#         fir = Blockchain_ledger.objects.filter(status1='inactive')
#         m="aaaaaaaaaaaaaaaaa"
#
#         context['fir'] = fir
#
#         return context

class Blockchain:

    def __init__(self):
        self.chain = []
        self.create_block(nonce = 1, previous_hash = '0')

    def create_block(self, nonce, previous_hash):
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'nonce': nonce,
                 'previous_hash': previous_hash}
        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1]

    def proof_of_work(self, previous_nonce):
        new_nonce = 1
        check_nonce = False
        while check_nonce is False:
            hash_operation = hashlib.sha256(str(new_nonce**2 - previous_nonce**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_nonce = True
            else:
                new_nonce += 1
        return new_nonce

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_nonce = previous_block['nonce']
            nonce = block['nonce']
            hash_operation = hashlib.sha256(str(nonce**2 - previous_nonce**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True


# Creating our Blockchain
blockchain = Blockchain()

# Mining a new block
def mine_block(request):
    if request.method == 'GET':
        previous_block = blockchain.get_previous_block()
        previous_nonce = previous_block['nonce']
        nonce = blockchain.proof_of_work(previous_nonce)
        previous_hash = blockchain.hash(previous_block)
        block = blockchain.create_block(nonce, previous_hash)
        response = {'message': 'Congratulations, you just mined a block!',
                    'index': block['index'],
                    'timestamp': block['timestamp'],
                    'nonce': block['nonce'],
                    'previous_hash': block['previous_hash']}
    return JsonResponse(response)

# Getting the full Blockchain
def get_chain(request):
    if request.method == 'GET':
        response = {'chain': blockchain.chain,
                    'length': len(blockchain.chain)}
    return JsonResponse(response)

# Checking if the Blockchain is valid
def is_valid(request):
    if request.method == 'GET':
        is_valid = blockchain.is_chain_valid(blockchain.chain)
        if is_valid:
            response = {'message': 'All good. The Blockchain is valid.'}
        else:
            response = {'message': 'Houston, we have a problem. The Blockchain is not valid.'}
    return JsonResponse(response)





class View_Fir(TemplateView):
    template_name = 'officer/view_fir.html'
    def get_context_data(self, **kwargs):
        context = super(View_Fir,self).get_context_data(**kwargs)
        fir = Fir.objects.filter(status='null')
        context['fir'] = fir
        return context

    def post(self, request, *args, **kwargs):

        id=request.POST['id']
        type=request.POST['type']
        user = User.objects.get(id=self.request.user.id)
        f =Fir.objects.get(id=id)
        remark=request.POST['remark']
        if Blockchain_ledger.objects.filter(user_id =user.id,fir_id=f.id):
            return render(request,'officer/view_fir.html',{'message':'one time approval is only provided'})
        else:
            if Fir.objects.filter(id=id,status='null',blockchain_status='active',blockchain_count=3):
                print(2)
                Product = Fir.objects.filter(status='null')
                return render(request,'officer/view_fir.html',{'message':'Currently Active this product','pro':Product})
            else:
                  try:
                    print(3)
                    if Fir.objects.get(id=id,status='null',blockchain_status='not active',blockchain_count=2):
                        if type=="approve":
                            print(4)
                            Project = Fir.objects.get(id=id,status='null',blockchain_status='not active')





                            a=Project.blockchain_count
                            Project.blockchain_count=a+1
                            Project.blockchain_status='active'

                            b=Project.blockchain_entry_count
                            Project.blockchain_entry_count = b+1
                            Project.save()
                            ledger = Blockchain_ledger()
                            ledger.fir_id=Project.id
                            ledger.last_status = "active"

                            ledger.Remark=remark
                            ledger.status='approve'
                            ledger.blockchain_count=a+1
                            ledger.blockchain_entry_count=b+1
                            ledger.last_status='active'
                            ledger.user_id=user.id
                            ledger.save()



                            encript =Blockchain_ledger_encripted()
                            key = Fernet.generate_key()
                            fernet = Fernet(key)
                            message1="active"
                            meggage2 ='approve'
                            blockchain_count_enc ="a+1"

                            blockchain_entry_count_enc ="b+1"
                            last_status_enc = 'active'

                            enc_message1 = fernet.encrypt(message1.encode())

                            enc_remark = fernet.encrypt(remark.encode())
                            enc_meggage2 = fernet.encrypt(meggage2.encode())
                            enc_blockchain_count_enc = fernet.encrypt(blockchain_count_enc.encode())
                            enc_blockchain_entry_count_enc = fernet.encrypt(blockchain_entry_count_enc.encode())
                            enc_last_status_enc = fernet.encrypt(last_status_enc.encode())

                            username=user.first_name
                            enc_username = fernet.encrypt(username.encode())
                            encript.user_name =enc_username

                            encript.fir_id=Project.id
                            encript.last_status = enc_message1

                            encript.Remark=enc_remark

                            encript.status=enc_meggage2
                            encript.blockchain_count=enc_blockchain_count_enc
                            encript.blockchain_entry_count=enc_blockchain_entry_count_enc
                            encript.last_status=enc_last_status_enc
                            encript.user_id=user.id
                            encript.save()

                            previous_block = blockchain.get_previous_block()
                            previous_nonce = previous_block['nonce']
                            nonce = blockchain.proof_of_work(previous_nonce)
                            previous_hash = blockchain.hash(previous_block)
                            block = blockchain.create_block(nonce, previous_hash)
                            response = {'message': 'Congratulations, you just mined a block!',
                                            'index': block['index'],
                                            'timestamp': block['timestamp'],
                                            'nonce': block['nonce'],
                                            'previous_hash': block['previous_hash']}

                            s = {'chain': blockchain.chain,
                                        'length': len(blockchain.chain)}
                            json_string = json.dumps(s)
                            print("11111111111111111111",json_string)
                            with open('json_data.json', 'w') as outfile:
                                 json.dump(json_string, outfile)
                            file1 = open('media/datas.txt', 'w')
                            file1.writelines(s)
                            file1.close()




                            return render(request,'officer/officer_index.html',{'message':'Approved Successfully'})
                        else:
                            print(5)
                            Project = Fir.objects.get(id=id,status='null',blockchain_status='not active')
                            a=Project.blockchain_count
                            Project.blockchain_count=a-1
                            Project.blockchain_status='reject'
                            b=Project.blockchain_entry_count
                            Project.blockchain_entry_count = b+1
                            Project.save()
                            ledger = Blockchain_ledger()
                            ledger.fir_id=Project.id
                            ledger.last_status = "reject"

                            ledger.Remark=remark
                            ledger.status='reject'
                            ledger.last_status='reject'
                            ledger.blockchain_count=a-1
                            ledger.blockchain_entry_count=b+1
                            ledger.user_id=user.id
                            ledger.save()


                            encript =Blockchain_ledger_encripted()
                            key = Fernet.generate_key()
                            fernet = Fernet(key)
                            message1='reject'
                            meggage2 ='reject'
                            blockchain_count_enc ="a+1"

                            blockchain_entry_count_enc ="b+1"
                            last_status_enc = "reject"

                            enc_message1 = fernet.encrypt(message1.encode())

                            enc_remark = fernet.encrypt(remark.encode())
                            enc_meggage2 = fernet.encrypt(meggage2.encode())
                            enc_blockchain_count_enc = fernet.encrypt(blockchain_count_enc.encode())
                            enc_blockchain_entry_count_enc = fernet.encrypt(blockchain_entry_count_enc.encode())
                            enc_last_status_enc = fernet.encrypt(last_status_enc.encode())






                            username=user.first_name
                            enc_username = fernet.encrypt(username.encode())
                            encript.user_name =enc_username
                            encript.fir_id=Project.id
                            encript.last_status = enc_message1

                            encript.Remark=enc_remark
                            encript.status=enc_meggage2
                            encript.blockchain_count=enc_blockchain_count_enc
                            encript.blockchain_entry_count=enc_blockchain_entry_count_enc
                            encript.last_status=enc_last_status_enc
                            encript.user_id=user.id




                            encript.save()


                            return render(request,'officer/officer_index.html',{'message':'Reject Successfully'})
                  except:
                     if type=="approve":
                            print(6)
                            Project = Fir.objects.get(id=id,status='null',blockchain_status='not active')
                            a=Project.blockchain_count
                            Project.blockchain_count=a+1
                            b=Project.blockchain_entry_count
                            Project.blockchain_entry_count = b+1
                            Project.save()
                            ledger = Blockchain_ledger()
                            ledger.fir_id=Project.id

                            ledger.Remark=remark
                            ledger.status='approve'
                            ledger.blockchain_count=a+1
                            ledger.blockchain_entry_count=b+1
                            ledger.user_id=user.id
                            ledger.save()


                            encript =Blockchain_ledger_encripted()
                            key = Fernet.generate_key()
                            fernet = Fernet(key)

                            blockchain_count_enc ="a+1"

                            blockchain_entry_count_enc ="b+1"

                            status_enc='approve'
                            enc_remark = fernet.encrypt(remark.encode())
                            enc_status_enc = fernet.encrypt(status_enc.encode())
                            enc_blockchain_count_enc = fernet.encrypt(blockchain_count_enc.encode())
                            enc_blockchain_entry_count_enc = fernet.encrypt(blockchain_entry_count_enc.encode())
                            encript.fir_id=Project.id

                            username=user.first_name
                            enc_username = fernet.encrypt(username.encode())
                            encript.user_name =enc_username
                            encript.Remark=enc_remark
                            encript.status=enc_status_enc
                            encript.blockchain_count=enc_blockchain_count_enc
                            encript.blockchain_entry_count=enc_blockchain_entry_count_enc
                            encript.user_id=user.id
                            encript.save()



                            return render(request,'officer/officer_index.html',{'message':'Approved Successfully'})

                     else:
                            print(7)
                            Project = Fir.objects.get(id=id,status='null',blockchain_status='not active')
                            a=Project.blockchain_count
                            if a>0:
                                print('mmmmmm')
                                Project.blockchain_count=a-1
                                b=Project.blockchain_entry_count
                                Project.blockchain_entry_count = b+1
                                Project.save()
                                ledger = Blockchain_ledger()
                                ledger.fir_id=Project.id
                                ledger.Remark=remark
                                ledger.status='reject'
                                ledger.blockchain_count=a-1
                                ledger.blockchain_entry_count=b+1
                                ledger.user_id=user.id
                                ledger.save()

                                encript =Blockchain_ledger_encripted()
                                key = Fernet.generate_key()
                                fernet = Fernet(key)

                                blockchain_count_enc ="a-1"

                                blockchain_entry_count_enc ="b+1"
                                status_enc='reject'
                                enc_remark = fernet.encrypt(remark.encode())
                                enc_status_enc = fernet.encrypt(status_enc.encode())
                                enc_blockchain_count_enc = fernet.encrypt(blockchain_count_enc.encode())
                                enc_blockchain_entry_count_enc = fernet.encrypt(blockchain_entry_count_enc.encode())
                                encript.fir_id=Project.id
                                username=user.first_name
                                enc_username = fernet.encrypt(username.encode())
                                encript.user_name =enc_username
                                encript.Remark=enc_remark
                                encript.status=enc_status_enc
                                encript.blockchain_count=enc_blockchain_count_enc
                                encript.blockchain_entry_count=enc_blockchain_entry_count_enc
                                encript.user_id=user.id
                                encript.save()



                                return render(request,'officer/officer_index.html',{'message':'Reject Successfully'})
                            else:
                                Project.blockchain_count=0
                                b=Project.blockchain_entry_count
                                Project.blockchain_entry_count = b+1
                                Project.save()
                                ledger = Blockchain_ledger()
                                ledger.fir_id=Project.id

                                ledger.Remark=remark
                                ledger.status='reject'
                                ledger.blockchain_count=0
                                ledger.blockchain_entry_count=b+1
                                ledger.user_id=user.id
                                ledger.save()



                                encript =Blockchain_ledger_encripted()
                                key = Fernet.generate_key()
                                fernet = Fernet(key)

                                blockchain_count_enc ="0"

                                blockchain_entry_count_enc ="b+1"
                                status_enc='reject'
                                enc_remark = fernet.encrypt(remark.encode())
                                enc_status_enc = fernet.encrypt(status_enc.encode())
                                enc_blockchain_count_enc = fernet.encrypt(blockchain_count_enc.encode())
                                enc_blockchain_entry_count_enc = fernet.encrypt(blockchain_entry_count_enc.encode())
                                encript.fir_id=Project.id
                                username=user.first_name
                                enc_username = fernet.encrypt(username.encode())
                                encript.user_name =enc_username
                                encript.Remark=enc_remark
                                encript.status=enc_status_enc
                                encript.blockchain_count=enc_blockchain_count_enc
                                encript.blockchain_entry_count=enc_blockchain_entry_count_enc
                                encript.user_id=user.id
                                encript.save()
                                return render(request,'officer/officer_index.html',{'message':'Reject Successfully'})





class view_ledger_login(TemplateView):
    template_name = 'officer/view_ledger_login.html'
    def post(self, request, *args, **kwargs):
        user = User.objects.get(id=self.request.user.id)
        key = request.POST['key']
        fir_id = self.request.GET['c_id']
        count =len(key)
        range = key[0:count:4]
        print(range)
        ascii_values=[]
        for i in range:
            print(i)
            ascii_values.append(ord(i))
        values_sum =sum(ascii_values)
        print(values_sum)
        print(1111111)

        if (Blockchain_admin.objects.filter(user_id=user,key2=values_sum,)):
            encript =Blockchain_ledger.objects.filter(fir_id=fir_id)
            return render(request, 'officer/view_decripted_ledger.html', {'message': " login Successfully","encript":encript})

        else:

            encript =Blockchain_ledger_encripted.objects.filter(fir_id=fir_id)
            return render(request, 'officer/view_encripted_ledger.html', {'message': " invalid key","encript":encript})


class view_blockchain_login(TemplateView):
    template_name = 'officer/view_blockchain_login.html'
    def post(self, request, *args, **kwargs):
        user = User.objects.get(id=self.request.user.id)
        key = request.POST['key']
        if (Blockchain_admin.objects.filter(user_id=user,key=key)):
            with open('json_data.json') as json_file:
                data = json.load(json_file)
                print(data)
            return render(request, 'officer/view_block_chain.html', {'message': " login Successfully",'data':data})

        else:
            return render(request, 'officer/view_blockchain_login.html', {'message': " invalid key"})