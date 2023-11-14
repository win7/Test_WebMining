import requests
import lxml.html
from general.models import *
from general.serializers import *

def getRestaurantsTripadvisor(url):
    lista_restaurants = []
    try:
        # url = "https://www.tripadvisor.com.pe/Restaurants-g294314-Cusco_Cusco_Region.html"
        headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}
        session = requests.Session()
        response = session.get(url,headers=headers,stream=True)
        response.raw.decode_content = True
        tree = lxml.html.parse(response.raw)
        #check pagination
        pages=['#']
        pa_cont = tree.xpath('//*[@id="EATERY_LIST_CONTENTS"]/div[2]/div/div')
        if len(pa_cont) > 0 and pa_cont[0].attrib['class']=='pageNumbers':
            for pa in pa_cont[0]:
                if pa != None and pa.tag == 'a':
                    pages.append(pa.attrib['href'])
        count_page=0
        while count_page < len(pages):
            print('pages restaurant ',count_page)
            #if count_page == 5:#para en la tercer pagina de restaurantes
            #    break
            if count_page > 0:
                session = requests.Session()
                response = session.get('https://www.tripadvisor.com.pe'+pages[count_page],headers=headers,stream=True)
                response.raw.decode_content = True
                tree = lxml.html.parse(response.raw)

                pa_cont = tree.xpath('//*[@id="EATERY_LIST_CONTENTS"]/div[2]/div/div')
                if len(pa_cont) > 0 and pa_cont[0].attrib['class']=='pageNumbers':
                    for pa in pa_cont[0]:
                        if pa != None and pa.tag == 'a' and not pa.attrib['href'] in pages:
                            pages.append(pa.attrib['href'])
            #analizando
            select_card_res = tree.xpath('//*[@id="component_2"]/div')
            contador = 0
            for card in select_card_res[0]:
                link_res=card.find('.//div/span/div[1]/div[2]/div[1]/div/span/a')
                if link_res != None:
                    print('restaurant ',contador)
                    #if contador == 5: # para solo en 5 restaurantes por pagina
                    #   break
                    data_res = {} #DICCIONARIO RESTAURANT
                    #print(link_res.attrib['href'])#link
                    #print(link_res.text_content())#nombre rest
                    session_re = requests.Session()
                    rest_page_res = session_re.get( 'https://www.tripadvisor.com.pe'+link_res.attrib['href'],headers=headers,stream=True)
                    rest_page_res.raw.decode_content = True
                    restaurant_tree = lxml.html.parse(rest_page_res.raw)

                    txt_content_info =''
                    container_info = restaurant_tree.xpath('//*[@id="component_48"]')
                    if len(container_info) >0 and container_info[0].attrib['data-component']=='@ta/restaurants.detail-top-info':
                        txt_content_info ='component_48'
                    else:
                        container_info = restaurant_tree.xpath('//*[@id="component_49"]')
                        if len(container_info) >0 and container_info[0].attrib['data-component']=='@ta/restaurants.detail-top-info':
                            txt_content_info ='component_49'
                        else:
                            container_info = restaurant_tree.xpath('//*[@id="component_50"]')
                            if len(container_info) >0 and container_info[0].attrib['data-component']=='@ta/restaurants.detail-top-info':
                                txt_content_info ='component_50'

                    rest_nombre = restaurant_tree.xpath('///*[@id="'+txt_content_info+'"]/div/div[1]/h1/text()')
                    #print(rest_nombre)#--nombre rest
                    data_res['nombre'] = ' '
                    if len(rest_nombre) >0:
                        data_res['nombre'] = rest_nombre[0]
                    
                    rest_dir = restaurant_tree.xpath('//*[@id="'+txt_content_info+'"]/div/div[3]/span[1]/span/a/text()')
                    #print(rest_dir)#--direccion rest
                    data_res['direccion'] = ' '
                    if len(rest_dir)>0:
                        data_res['direccion'] = rest_dir[0]

                    rest_tel = restaurant_tree.xpath('//*[@id="'+txt_content_info+'"]/div/div[3]/span[2]/span/span[2]/a/text()')
                    #print(rest_tel)#--telefono rest
                    data_res['telefono'] = ' '
                    if len(rest_tel) >0:
                        data_res['telefono'] = rest_tel[0]

                    txt_content_detail =''
                    container_detail = restaurant_tree.xpath('//*[@id="component_49"]')
                    if len(container_detail) >0 and container_detail[0].attrib['data-component']=='@ta/restaurants.detail-overview-cards':
                        txt_content_detail ='component_49'
                    else:
                        container_detail = restaurant_tree.xpath('//*[@id="component_50"]')
                        if len(container_detail) >0 and container_detail[0].attrib['data-component']=='@ta/restaurants.detail-overview-cards':
                            txt_content_detail ='component_50'
                        else:
                            container_detail = restaurant_tree.xpath('//*[@id="component_51"]')
                            if len(container_detail) >0 and container_detail[0].attrib['data-component']=='@ta/restaurants.detail-overview-cards':
                                txt_content_detail ='component_51'

                    rest_rating = restaurant_tree.xpath('//*[@id="'+txt_content_detail+'"]/div[1]/div/div[1]/div/div[1]/div[1]/span[1]/text()')
                    #print(rest_rating)
                    data_res['calificacion'] = ' '
                    if len(rest_rating) >0:
                        data_res['calificacion'] = rest_rating[0]

                    data_res['tipo_comidas']=' '
                    if len(restaurant_tree.xpath('//*[@id="'+txt_content_detail+'"]/div[1]/div/div[2]/div/div/div[2]/div[1]/div[2]'))>0 and restaurant_tree.xpath('//*[@id="'+txt_content_detail+'"]/div[1]/div/div[2]/div/div/div[2]/div[1]/div[1]')[0].text_content()[:1]=='T':
                        rest_tipo_comidas = restaurant_tree.xpath('//*[@id="'+txt_content_detail+'"]/div[1]/div/div[2]/div/div/div[2]/div[1]/div[2]')
                        data_res['tipo_comidas'] = rest_tipo_comidas[0].text_content()
                        #print('tipos de comida')
                        #print(rest_tipo_comidas[0].text_content())

                    data_res['dietas_especiales'] =' '
                    if len(restaurant_tree.xpath('//*[@id="'+txt_content_detail+'"]/div[1]/div/div[2]/div/div/div[2]/div[2]/div[2]'))>0 and restaurant_tree.xpath('//*[@id="'+txt_content_detail+'"]/div[1]/div/div[2]/div/div/div[2]/div[2]/div[1]')[0].text_content()[:1]=='D':
                        rest_dietas = restaurant_tree.xpath('//*[@id="'+txt_content_detail+'"]/div[1]/div/div[2]/div/div/div[2]/div[2]/div[2]')
                        data_res['dietas_especiales'] = rest_dietas[0].text_content()
                        #print('dietas especiales')
                        #print(rest_dietas[0].text_content())

                    data_res['comidas'] =' '
                    if len(restaurant_tree.xpath('//*[@id="'+txt_content_detail+'"]/div[1]/div/div[2]/div/div/div[2]/div[3]/div[2]'))>0 and restaurant_tree.xpath('//*[@id="'+txt_content_detail+'"]/div[1]/div/div[2]/div/div/div[2]/div[3]/div[1]')[0].text_content()[:2]=='Co':
                        
                        rest_comida = restaurant_tree.xpath('//*[@id="'+txt_content_detail+'"]/div[1]/div/div[2]/div/div/div[2]/div[3]/div[2]')
                        
                        data_res['comidas'] = rest_comida[0].text_content()
                        #print('comidas')
                        #print(rest_comida[0].text_content())
                    #************************* en este punto se recomienda guardar en base de datos el hotel ******
                    serializer1 = RestauranteSerializer(data=data_res)
                    if serializer1.is_valid():
                        restaurante_ = serializer1.save()
                        #--------------------------------------------------------------
                        res_comentarios = []
                        #print('comentarios')
                        content_coment = restaurant_tree.xpath('//*[@id="taplc_location_reviews_list_resp_rr_resp_0"]/div')
                        pages_co=[]
                        #print(etree.tostring(content_coment[0], xml_declaration=True))
                        if len(content_coment)>0:
                            content_coment_page = content_coment[0].find('.//div[@class="pageNumbers"]')
                            if content_coment_page != None:
                                for pa_co in content_coment_page:
                                    if pa_co.tag == 'a' and 'data-page-number' in pa_co.attrib and 'href' in pa_co.attrib:
                                        pages_co.append(pa_co.attrib['href'])
                            count_page_co = 0
                            while count_page_co < len(pages_co):
                                print('comment page restaurant ',count_page_co)

                                if count_page_co > 0:
                                    session_co = requests.Session()
                                    rest_page_res = session_co.get( 'https://www.tripadvisor.com.pe'+pages_co[count_page_co],headers=headers,stream=True)
                                    rest_page_res.raw.decode_content = True
                                    co_restaurant_tree = lxml.html.parse(rest_page_res.raw)
                                    content_coment = co_restaurant_tree.xpath('//*[@id="taplc_location_reviews_list_resp_rr_resp_0"]/div')
                            
                                    if len(content_coment)>0:
                                        content_coment_page = content_coment[0].find('.//div[@class="pageNumbers"]')
                                        if content_coment_page != None:
                                            for pa_co in content_coment_page:
                                                if pa_co != None and pa_co.tag == 'a' and 'data-page-number' in pa_co.attrib and 'href' in pa_co.attrib and not pa_co.attrib['href'] in pages_co:
                                                    pages_co.append(pa_co.attrib['href'])

                                        hay_usuario=True
                                        count_com=0
                                        while hay_usuario and count_com < len(content_coment[0]):
                                            comment = content_coment[0][count_com].find('.//div[@class="review-container"]')
                                            #print(etree.tostring(comment, xml_declaration=True))
                                            if comment != None:
                                                re_comenta = {} #DICCIONARIO COMENTARIO DE RESTAURANT
                                                re_comenta['usuario'] = ' '
                                                co_usuario = comment.xpath('div/div/div/div[1]/div/div/div[1]/div[2]/div/text()')
                                                if len(co_usuario) > 0:
                                                    re_comenta['usuario'] = co_usuario[0]
                                                    #print(co_usuario)#--usuario
                                                co_rating = comment.xpath('div/div/div/div[2]/span[1]')
                                                re_comenta['calificacion'] = ' '
                                                if len(co_rating) > 0:
                                                    co_ra_aux = co_rating[0].attrib['class'].split(' ')
                                                    co_rating = co_ra_aux[-1][-2:]
                                                    re_comenta['calificacion'] = co_rating
                                                    #print(co_rating)#--calificacion /50
                                                re_comenta['fecha_comentario'] = ' '
                                                co_fecha = comment.find('.//span[@class="ratingDate"]')
                                                if co_fecha != None:
                                                    re_comenta['fecha_comentario'] = co_fecha.text
                                                co_comentario = comment.find('.//div[@class="prw_rup prw_reviews_text_summary_hsx"]')
                                                re_comenta['comentario'] =' '
                                                if co_comentario != None:
                                                    co_comentario_p = co_comentario.find('.//p')
                                                    if co_comentario_p != None:
                                                        re_comenta['comentario'] = co_comentario_p.text
                                                        #print(co_comentario_p.text)#-- comentario
                                                co_fecha_estadi = comment.find('.//div[@class="prw_rup prw_reviews_stay_date_hsx"]')
                                                re_comenta['fecha_estadia'] =' '
                                                if co_fecha_estadi != None:
                                                    re_comenta['fecha_estadia'] = co_fecha_estadi.text_content()
                                                    #print(co_fecha_estadi.text_content())#-- fecha estadia en rest
                                                #**************** en este punto se recomienda guardar en base de datos los comentarios respecto al restaurant
                                                re_comenta["id_restaurante"] = restaurante_.id_restaurante
                                                serializer2 = ComentariosSerializer(data=re_comenta)
                                                if serializer2.is_valid():
                                                    serializer2.save()
                                                else:
                                                    # return Resp(data=serializer2.errors, message="Error al Crear Restaurante.", flag=False, status=status.HTTP_400_BAD_REQUEST).send()
                                                    print(serializer2.errors)
                                                #------------------------------------------------------------------------
                                                #res_comentarios.append(re_comenta)
                                                #print('comentario ',count_com)
                                            count_com += 1
                                #print('comentario pagina ',count_page_co)
                                count_page_co +=1
                    else:
                        # return Resp(data=serializer.errors, message="Error al Crear Restaurante.", flag=False, status=status.HTTP_400_BAD_REQUEST).send()
                        print(serializer1.errors)
                    #data_res['comentarios'] = res_comentarios
                    #lista_restaurants.append(data_res)
                    contador +=1
                    
            count_page += 1
    except:
        print("error scrapeo")
    return True

# print(getRestaurantsTripadvisor())
