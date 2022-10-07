import base64

def pic2py(pic_name):
    open_pic = open("%s" % pic_name,'rb')
    b64str = base64.b64encode(open_pic.read())
    open_pic.close()
    write_data = 'img = "%s"' % b64str.decode()
    f = open('%s.py' % pic_name.replace('.','_'),'w+')
    f.write(write_data)
    f.close()

if __name__ == '__main__':
    pic = 'output_not_selection_icon.png'
    pic2py(pic)