from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import pickle
from django.views.decorators.csrf import csrf_exempt
import json


with open ('trained_model_lr.pkl', 'rb') as file:
    trained_model_lr = pickle.load(file)

with open ('trained_model_svm.pkl', 'rb') as file:
    trained_model_svm = pickle.load(file)

with open ('trained_model_nb.pkl', 'rb') as file:
    trained_model_nb = pickle.load(file)



def homePage(request):
    return HttpResponse("This is the home page.")


# i wanted to send news to backend, to give to ml model.
#for that, we have to use POST request, for that, we can use curl command.
#just like browser, curl command is taking the url, locating server, sending request to server and gettng response. 
#curl command is executed outside the server. yo backend code will run on server. we dont want to send news from server to server. so this curl command is not used here 
#yo curl command use garda :curl -X POST -H "Content-Type: application/json" -d '{"param1": "value1"}' http://127.0.0.1:8000/prediction/ , i got csrf token not set exception
# and we dont need csrf authentication. so we are ignoring csrf token 
@csrf_exempt                                      #this is for the below prediction function
def prediction(request):

    #print statement chai python code ho ani yo server ma run garxa. aile server laptop ho, so yo command promt ma dekhinxa, browser ma haina brcause cant return to browser.
    #http request always comtains body and this body has the data tha is sent with the request
    # this print gives the input data in http request in string form, in double quotes
    print(request.body)

    #we are sending data in json format to server, this data is sent in the form of a string, over the network. 
    #once server reads the string, we want to comvert it to a json object. 
    request_body = json.loads(request.body)
    print(request_body)
    input_news = []
    input_news.append(request_body['news'])      #request_body['news'] will get the value, which is the actual nepali news
    print(input_news)

    prediction_lr = trained_model_lr.predict(input_news)
    print(prediction_lr[0])


    prediction_svm = trained_model_svm.predict(input_news)
    print(prediction_svm[0])


    prediction_nb = trained_model_nb.predict(input_news)
    print(prediction_nb[0])


    true_prediction_count = 0
    fake_prediction_count = 0

    if(prediction_lr[0]==1):
        true_prediction_count += 1
    else:
        fake_prediction_count += 1

    if(prediction_svm[0]==1):
       true_prediction_count += 1
    else:
        fake_prediction_count += 1

    if(prediction_nb[0]==1):
        true_prediction_count += 1
    else:
        fake_prediction_count += 1


    response = "unknown"

    if(true_prediction_count > fake_prediction_count):
        response = "true"
    else:
        response = "fake"

    return JsonResponse({'prediction': response})

#when frontend is done, the js would take the news and create http post request and send it to server. for now, we are doing this using curl, because we dont have frontend
