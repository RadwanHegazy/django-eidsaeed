from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from globals.generator import EidBuilder

def save_img (img) : 
    path = f'media/upload/{img.name}'
    with open(path, 'wb') as f:
        f.write(img.read())
        f.close()

    return path


class index_view (View) :

    def get(self, request, **kwargs) : 
        return render(request,'index.html')

    def post(self, request, **kwrags) : 
        templates = {
            'green' : 'eid_green.png',
            'blue' : 'eid_blue.png',
            'purple' : 'eid_purple.png',
        }
        usr_img = request.FILES.get('img', None)
        usr_name = request.POST.get('username')
        usr_template = request.POST.get('template', None)

        if usr_template not in templates.keys() or usr_template is None:
            messages.error(request, 'enter a vlid template')
            return redirect('index')


        usr_template = templates[usr_template]
        incoming_saved_path = save_img(usr_img)

        eid = EidBuilder(
            bg_img_path='globals/screens/' + usr_template,
            usr_img_path=incoming_saved_path,
            usr_name=usr_name
        )

        eid.run()

        return redirect(eid.output_path)