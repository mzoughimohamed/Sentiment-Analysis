from django.shortcuts import render
from django.conf import settings
from .Code import load_page
import pandas as pd 
from django.http import HttpResponse, Http404
import os
import random
import string
import re
# Create your views here.
def homes (request):
    return render(request,"home.html")
def resultfile(request):
    listmaster = []
    listmaster1 = []
    error=False
    if request.method=="POST":
        file=request.FILES["document"]
        if( ".txt" in file.name):
            if(file.size>20):
                for line in file:
                    PAGE_URL=""+line.decode()
                    ScrapePost(PAGE_URL,listmaster)
                message="Scraping est Bien effectue"
        else :
            error=True
            message="Veuillez s'assurer que votre fichier est au format.txt avec chaque ligne contenant une seule URL"
            return render(request,"file.html",{
                "message":message,
                "error":error,
                })
        etat=False
        if (len(listmaster)==0):
             Message="0 Commentaire a été scrapée ..."
        else :
            for i in range(len(listmaster)):
                if listmaster[i]['text'] not in listmaster1:
                    listmaster1.append(listmaster[i]['text'])
            df = pd.DataFrame.from_dict({'Column1':listmaster1})
            df.to_excel('media/testfile.xlsx', header=True, index=False)
            append_df_to_excel(df,"media/Full_data.xlsx")
            Message=len(df.index)+"Commentaire Scrapées"
            etat=True
        dict={
            "fileurl":os.path.join(settings.BASE_DIR,'media/testfile.xlsx'),
            "etat":etat,
            "Message":Message,
        }
    return render(request,"Resultfile.html",dict)
def resulturl(request):
    listmaster = []
    listmaster1= []
    if request.method=="POST":
        PAGE_URL=request.POST.get('url')
        if((PAGE_URL!="")and("facebook.com" in PAGE_URL)):
            ScrapePost(PAGE_URL,listmaster)
            message="Scraping est Bien effectu.Vous Pouvez Télécharger votre fichier excel "
        if(request.POST.get('cb')=="on"):
            with open("media/Builtinurl.txt") as f:
                for line in f:
                    ScrapePost(line,listmaster)
    etat=False
    if (len(listmaster)==0):
        message="Nous n'avons pu Scrapper aucun commentaire ! Vérifiez votre localisateur de ressources uniforme s'il vous plaît "
    else :
        for i in range(len(listmaster)):
            if listmaster[i]['text'] not in listmaster1:
                listmaster1.append(listmaster[i]['text'])
        df = pd.DataFrame.from_dict({'Column1':listmaster1})
        df.to_excel("media/test.xlsx", header=True, index=False)
        Nombre=len(df.index)
        message=message+"<br/>"+Nombre+"Commentaire Scrapé"
        append_df_to_excel(df,"media/Full_data.xlsx")
        etat=True
    dict={
         "fileurl":os.path.join(settings.BASE_DIR,"/media/test.xlsx"),
         "etat":etat,
         "message":message, 
    }
    return render(request,"CrawlerResult.html",dict)

def filescraper(request):
    return render(request,"file.html")
def download(request):
    file_path = os.path.join(settings.BASE_DIR, "media/test.xlsx")
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404
def downloadjson(request):
    file_path = os.path.join(settings.BASE_DIR, "media/data.json")
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404
def telecharger(request):
    file_path = os.path.join(settings.BASE_DIR, "media/testfile.xlsx")
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404
def downloadfull(request):
    file_path = os.path.join(settings.BASE_DIR, "media/Full_data.xlsx")
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404
def randomSTR():
    letters = string.ascii_lowercase
    print ( ''.join(random.choice(letters) for i in range(10)) )






####section For Definition of necessary code for the scraping
def get_child_attribute(element, selector, attr):
	try:
		element = element.find_element_by_css_selector(selector)
		return str(element.get_attribute(attr))
	except: 
		return ''
	
def get_comment_info(comment):
	cmt_url = get_child_attribute(comment, '._3mf5', 'href')
	utime = get_child_attribute(comment, 'abbr', 'data-utime')
	text = get_child_attribute(comment, '._3l3x ', 'textContent')

	cmt_id = cmt_url.split('=')[-1]
	if cmt_id == None:
		cmt_id = comment.get_attribute('data-ft').split(':"')[-1][:-2]
		user_url = user_id = user_name = 'Acc clone'
	else:
		user_url = cmt_url.split('?')[0]
		user_id = user_url.split('https://www.facebook.com/')[-1].replace('/', '')
		user_name = get_child_attribute(comment, '._6qw4', 'innerText')

	return {
		'id': cmt_id,
		'utime': utime,
		'user_url': user_url,
		'user_id': user_id,
		'user_name': user_name,
		'text': text,
	}
def ScrapePost(PAGE_URL,listmaster):
    SCROLL_DOWN = 10
    FILTER_CMTS_BY = load_page.FILTER_CMTS.MOST_RELEVANT
    VIEW_MORE_CMTS = 4
    VIEW_MORE_REPLIES = 4
    load_page.start(
	PAGE_URL, 
	SCROLL_DOWN, 
	FILTER_CMTS_BY, 
	VIEW_MORE_CMTS, 
	VIEW_MORE_REPLIES
)
    driver = load_page.driver
    print('driver=',driver)
    total = 0

    listJsonPosts = [] 

    # list to contain the posts to be scrapped from the page
    listHtmlPosts = driver.find_elements_by_css_selector('[class="_427x"] .userContentWrapper')
    listHtmlPosts = driver.find_elements_by_css_selector('[class="_5pcr userContentWrapper"] .userContentWrapper')
    print('Start crawling', len(listHtmlPosts), 'posts...')


    for post in listHtmlPosts:
        post_url = get_child_attribute(post, '._5pcq', 'href').split('?')[0] # the post_url to be scrapped
        post_id = re.findall('\d+', post_url)[-1] # the post_id to be scrapped
        utime = get_child_attribute(post, 'abbr', 'data-utime')
        post_text = get_child_attribute(post, '.userContent', 'textContent') # the post_text to be scrapped
        total_shares = get_child_attribute(post, '[data-testid="UFI2SharesCount/root"]', 'innerText')
        total_cmts = get_child_attribute(post, '._3hg-', 'innerText')

        listJsonCmts = []
        listHtmlCmts = post.find_elements_by_css_selector('._7a9a>li') # list of the comments for each post

        num_of_cmts = len(listHtmlCmts) # number of comments for each post
        total += num_of_cmts # total number of comments for all posts

        if num_of_cmts > 0: # if the post has some comments
            print('Crawling', num_of_cmts, 'comments of post', post_id)
            for comment in listHtmlCmts: # for each comment of the post
                comment_owner = comment.find_elements_by_css_selector('._7a9b') 
                # the name of the person who posted the comment
                comment_info = get_comment_info(comment_owner[0])

                listJsonReplies = []
                # list of replies to the comment
                listHtmlReplies = comment.find_elements_by_css_selector('._7a9g')

                num_of_replies = len(listHtmlReplies)
                total += num_of_replies

                if num_of_replies > 0:
                    print('Crawling', num_of_replies, 'replies for', comment_info['user_name'] + "'s comment")
                    for reply in listHtmlReplies:
                        reply_info = get_comment_info(reply)
                        listJsonReplies.append(reply_info)
                        listmaster.append(reply_info)

                comment_info.update({ 'replies': listJsonReplies })
                listJsonCmts.append(comment_info)
                listmaster.append(comment_info)

        listJsonReacts = []
        listHtmlReacts = post.find_elements_by_css_selector('._1n9l')

        for react in listHtmlReacts:
            react_text = react.get_attribute('aria-label')
            listJsonReacts.append(react_text)

        listJsonPosts.append({
            'url': post_url,
            'id': post_id,
            'utime': utime,
            'text': post_text,
            'total_shares': total_shares,
            'total_cmts': total_cmts,
            'crawled_cmts': listJsonCmts,
            'reactions': listJsonReacts,
        })
    print('Total comments and replies crawled:', total)
    load_page.stop_and_save('media/data.json', listJsonPosts)
def append_df_to_excel(df, excel_path):
    df_excel = pd.read_excel(excel_path)
    result = pd.concat([df_excel, df], ignore_index=True)
    result.to_excel(excel_path,index=False)
