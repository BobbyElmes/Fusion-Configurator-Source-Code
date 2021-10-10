from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.cache import never_cache
from django.views.decorators.cache import cache_control
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import  IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from datetime import datetime, timedelta
from django.http import JsonResponse
from ConfigWebApp.models import AccessLog, Users
from .forms import Register
from django.contrib.auth import authenticate, login
import csv
import math



# This all used to be part of the front end in js so it's messy

@cache_control(max_age=0, no_cache=True, no_store=True, must_revalidate=True)
def configurator(request):
    return render(request, 'build/index.html')

@cache_control(max_age=0, no_cache=True, no_store=True, must_revalidate=True)
def configuratorTest(request):
    return render(request, 'buildTest/index.html')

@cache_control(max_age=0, no_cache=True, no_store=True, must_revalidate=True)
def Statistics(request):
    return render(request, 'statistics/index.html')

@csrf_exempt
def LoginStats(request):
    if request.method == 'POST':


        form = Register(request.POST)
        context = {}
        if form.is_valid():
            passW = form.cleaned_data['password'].replace('"', '')
            userN = form.cleaned_data['username'].replace('"', '')
            print("USER: " + userN)
            print("PASSWORD: " + passW)
            user = authenticate(request,username=userN, password=passW)
            if user is not None:
                login(request,user)
                context['userMessage']  = "User: " + user.username + " signed in"
                t = Token.objects.get(user=Users.objects.get(username = userN))
                if(t is not None):
                    t.delete()

                t = Token.objects.create(user=Users.objects.get(username = userN))
                t.save()
                return HttpResponse(t.key)
            else:
                return HttpResponse("username or password incorrect")

            return HttpResponse("username or password incorrect")


@csrf_exempt
def LogAction(request):
    if request.method == 'POST':
        action = request.POST['action'].replace('"', '')
        queryId = request.POST['query'].replace('"', '')
        try:
            sessionId = request.POST['session_id'].replace('"', '')
        except:
            sessionId = "-1"

        print(action)
        print(queryId)

        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')


        if (action == "load"):
            mobile = request.POST['mobile'].replace('"', '')
            accessLog = AccessLog.objects.create(IpAddress=ip, QueryId=queryId, Mobile=(mobile == "True"))
            accessLog.save()
            sessionId = accessLog.SessionId
        else:
            try:
                accessLog = AccessLog.objects.get(SessionId = int(sessionId))
                accessLog.LastAccessed = datetime.now()

                if (action == "quote"):
                    accessLog.AddQuoteNum += 1
                if (action == "pdf"):
                    accessLog.PDFNum += 1
                if (action == "xlsx"):
                    accessLog.XLSXNum += 1
                accessLog.save()
            except:
                print("No Access Log for ip: " + ip + " and query: " + queryId)
        return HttpResponse(str(sessionId))


@csrf_exempt
def GetAccessData(request):
    if request.method == 'POST':
        tokenVal = request.POST['authentication'].replace('"', '')
        print("TOKEN: " + tokenVal)
        user = Token.objects.get(key=tokenVal)
        if user is not None:
            concat = "0"
            fromDate = datetime.strptime(str(request.POST['from']).replace('"', ''), '%d/%m/%Y')
            toDate = datetime.strptime(str(request.POST['to']).replace('"', ''), '%d/%m/%Y')+ timedelta(days=1)
            summary = request.POST['summary'].replace('"', '')
            try:
                Logs = AccessLog.objects.filter(FirstAccessed__range=(fromDate,toDate))
            except:
                Logs = AccessLog.objects.none()

            if (summary == "1"):
                ips = set()

                Dictionary = {}
                for log in Logs.iterator():
                    mobile = 0
                    if (log.Mobile):
                        mobile = 1
                    if (log.QueryId in Dictionary):
                        if (log.IpAddress + log.QueryId) not in ips:
                            Dictionary[log.QueryId][0] += 1
                            ips.add(log.IpAddress + log.QueryId)


                        Dictionary[log.QueryId][1] += 1
                        Dictionary[log.QueryId][2] += log.AddQuoteNum
                        Dictionary[log.QueryId][3] += log.PDFNum
                        Dictionary[log.QueryId][4] += log.XLSXNum
                        Dictionary[log.QueryId][5] += (log.LastAccessed - log.FirstAccessed).total_seconds() / 3600
                        Dictionary[log.QueryId][6] += mobile

                    else:
                        Dictionary[log.QueryId] = [1,1,log.AddQuoteNum,log.PDFNum,log.XLSXNum, (log.LastAccessed - log.FirstAccessed).total_seconds() / 3600, mobile]
                        ips.add(log.IpAddress + log.QueryId)


                html = """
                    <table class="Table2">
                        <thead>
                            <tr>
                                <th>Query Id</th>
                                <th>Total Unique Users</th>
                                <th>Total Times Loaded</th>
                                <th>Total Quotes</th>
                                <th>Total PDF</th>
                                <th>Total XLSX</th>
                                <th>% Mobile</th>
                                <th>Total Time (hrs)</th>
                            </tr>
                        </thead>
                        <tbody>
                        """
                csv = "data:text/csv;charset=utf-8,Query Id,Total Unique Users,Total Times Loaded,Total Quotes,Total PDF,Total XLSX,% Mobile,Total Time (hrs)\r\n"
                for key in Dictionary:
                    values = [key,str(Dictionary[key][0]),str(Dictionary[key][1]),str(Dictionary[key][2]),str(Dictionary[key][3]),str(Dictionary[key][4]),str(round((Dictionary[key][6]/Dictionary[key][1])*100))+ "%",str(round(Dictionary[key][5]))]
                    html += "<tr>"
                    for value in values:
                        html += "<td>" + value + "</td>"
                        csv += value + ","
                    html += "</tr>"
                    csv = csv[:-1] + "\r\n"
                html += """
                        </tbody>
                    </table>"""
            else:
                html = """
                    <table>
                        <thead>
                            <tr>
                                <th>Query Id</th>
                                <th>Ip Address</th>
                                <th>Website Version</th>
                                <th>Date Accessed</th>
                                <th>Date Updated</th>
                                <th>Session Time</th>
                                <th>Quotes</th>
                                <th>PDF</th>
                                <th>XLSX</th>
                            </tr>
                        </thead>
                        <tbody>
                        """
                csv = "data:text/csv;charset=utf-8,Query Id,Ip Address,Website Version,Date Accessed,Date Updated,Session Time,Quotes,PDF,XLSX\r\n"
                iteratorNum = 0

                for log in reversed(Logs):
                    iteratorNum+=1;
                    mobile = "Desktop"
                    if (log.Mobile):
                        mobile = "Mobile"
                    logStringValues = [log.QueryId, log.IpAddress, mobile, log.FirstAccessed.strftime('%d/%m/%Y %H:%M:%S'), log.LastAccessed.strftime('%d/%m/%Y %H:%M:%S'), str(log.LastAccessed - log.FirstAccessed).split('.', 2)[0], str(log.AddQuoteNum), str(log.PDFNum), str(log.XLSXNum)]
                    html += "<tr>"
                    for value in logStringValues:
                        if (iteratorNum < 500):
                            html += "<td>" + value + "</td>"
                        csv += value + ","
                    html += "</tr>"

                    csv = csv[:-1] + "\r\n"

                if (iteratorNum >= 500):
                    concat = str(iteratorNum)

                html += """
                        </tbody>
                    </table>"""

            return JsonResponse({'html':html, 'csv':csv, 'concat':concat})
        else:
            return JsonResponse({'html':"", 'csv':"", 'concat':"0"})

@csrf_exempt
def GetConifg(request):
    if request.method == 'POST':
        queryId = request.POST['id'].replace('"', '')
        config = CsvReader('static/Config/Config.csv')
        row = GetConfigSettings(config, queryId)

        return JsonResponse({'language':row[1], 'title':row[2], 'descriptions':row[3], 'price-list':row[4], 'currency':row[5], 'logo1': row[6], 'logo2': row[7], 'logo3':row[8], 'logo1-pdf':row[9], 'logo2-pdf':row[10], 'logo3-pdf':row[11], 'hide-languages-dropdown':row[12], 'hide-discount-box':row[13], 'hide-pdf': row[14], 'hide-xlsx': row[15], 'export-footer-text': row[16], 'tax-code': row[17]})


def CsvReader(path):
    matrix = []

    with open(path) as f:
        reader = csv.reader(f, delimiter=',')
        matrix.append(list(reader))
    matrix[0].pop(0)
    return matrix[0]

def GetConfigSettings(config, queryId):
    for row in config:
            if (row[0] == queryId):
                return row
    return config[0]

def CSVLoader(file, numItems):
    product = [[]]
    for i in range(0, numItems - 1):
        product.append([])
    csv = CsvReader(file)

    for i in range (len(csv)):
        index = 0
        space = True
        for c in range(len(csv[i])):
            if (csv[i][c] == ''):
                if(space == False):
                    space = True
                    index += 1

            else:
                if (space == True):
                    product[index].append([])
                    space = False
                product[index][len(product[index]) - 1].append(csv[i][c])

    return product

@csrf_exempt
def GetProductsAndDescriptions(request):
    #this array has the portrait, landscape and finally packer flashing
    #values & descriptions loaded into it


    language = int(request.POST['language'].replace('"', ''))
    pricelistFilename = request.POST['pricelist'].replace('"', '')
    descriptionFilename =  request.POST['description'].replace('"', '')

    fileCount = 0
    error = ""
    try:
        product = CSVLoader("static/Prices/" + pricelistFilename, 4)
        fileCount += 1
        descriptions = CSVLoader("static/Languages/" + descriptionFilename, 4)
        words = CSVLoader("static/Languages/Languages.csv", 1)
    except:
        if (fileCount == 0):
            error = "Invalid price list filename: '" + pricelistFilename + "' in the config."
        else:
            error = "Invalid description filename: '" + descriptionFilename + "' in the config"
        return JsonResponse({'error':error})

    productArr = [[], [], []]
    ids = []
    #first we sort our descriptions (character by character) by the ID column in order to allow for
    #binary search
    #sortedDesc.sort()
    sorted(descriptions,key=lambda l:l[0])
    for i in range(0, len(descriptions)):
        descriptions[i].sort()

    #now we create an array with only the sorted IDs
    #after this, we can binary search the sorted descriptions with the viridian IDs
    #present in the product file, in order to enable different panels and stuff to be
    #present in different versions of the configurator
    sortedColumn = []
    for i in range (0, len(descriptions)):
        currentCol = []
        for c in range (0, len(descriptions[i])):
            currentCol.append(descriptions[i][c][0])
        sortedColumn.append(currentCol)

    for c in range(0,3):
        ids.append([0 for i in range (len(product[c]))])
        for i in range(0, len(product[c])):
            if (len(product[c][i][0]) == 0):
                break;
            productArr[c].append([0,0,0,0])
            productArr[c][i][0] = product[c][i][2]
            ids[c][i] = product[c][i][0]
            productArr[c][i][1] = 0
            productArr[c][i][2] = float(product[c][i][1])
            productArr[c][i][3] = descriptions[c][BinarySearch(sortedColumn[c], product[c][i][2], 0, len(sortedColumn[c]) - 1)][language + 1]

    #now to load the panel values
    panelArr = []
    ids.append([0 for i in range (len(product[3]))])
    for i in range (0, len(product[3])):
        if (product[3][i][0] == ""):
            break;
        panelArr.append([0,0,0,0,0,0,0])
        panelArr[i][0] = product[3][i][5]
        ids[3][i] = product[3][i][0]
        panelArr[i][1] = 0
        panelArr[i][2] = float(product[3][i][2])
        panelArr[i][3] = float(product[3][i][1])
        panelArr[i][4] = descriptions[3][BinarySearch(sortedColumn[3], product[3][i][5], 0, len(sortedColumn[3])- 1)][language + 1]
        panelArr[i][5] = float(product[3][i][3])
        panelArr[i][6] = float(product[3][i][4])

    return JsonResponse({'ids':ids, 'products':productArr, 'panels':panelArr, 'product': product, 'description':descriptions, 'words':words, 'error':error})

def BinarySearch(arr, x, start, end):
    # Base Condition
    if (start > end):
        return False

    # Find the middle index
    mid = math.floor((start + end) / 2.0)

    # Compare mid with given key x
    if (arr[mid] == x):
        return mid

    # If element at mid is greater than x,
    # search in the left half of mid
    if(arr[mid] > x):
        return BinarySearch(arr, x, start, mid-1);
    else:

        # If element at mid is smaller than x,
        # search in the right half of mid
        return BinarySearch(arr, x, mid+1, end);


@csrf_exempt
def GetProductsAndDescriptionsTest(request):
    #this array has the portrait, landscape and finally packer flashing
    #values & descriptions loaded into it


    language = int(request.POST['language'].replace('"', ''))
    pricelistFilename = request.POST['pricelist'].replace('"', '')
    descriptionFilename =  request.POST['description'].replace('"', '')

    fileCount = 0
    error = ""
    try:
        product = CSVLoader("static/Test/Prices/" + pricelistFilename, 4)
        fileCount += 1
        descriptions = CSVLoader("static/Test/Languages/" + descriptionFilename, 4)
        words = CSVLoader("static/Test/Languages/Languages.csv", 1)
    except:
        if (fileCount == 0):
            error = "Invalid price list filename: '" + pricelistFilename + "' in the config."
        else:
            error = "Invalid description filename: '" + descriptionFilename + "' in the config"
        return JsonResponse({'error':error})

    productArr = [[], [], []]
    ids = []
    #first we sort our descriptions (character by character) by the ID column in order to allow for
    #binary search
    #sortedDesc.sort()
    sorted(descriptions,key=lambda l:l[0])
    for i in range(0, len(descriptions)):
        descriptions[i].sort()

    #now we create an array with only the sorted IDs
    #after this, we can binary search the sorted descriptions with the viridian IDs
    #present in the product file, in order to enable different panels and stuff to be
    #present in different versions of the configurator
    sortedColumn = []
    for i in range (0, len(descriptions)):
        currentCol = []
        for c in range (0, len(descriptions[i])):
            currentCol.append(descriptions[i][c][0])
        sortedColumn.append(currentCol)

    for c in range(0,3):
        ids.append([0 for i in range (len(product[c]))])
        for i in range(0, len(product[c])):
            if (len(product[c][i][0]) == 0):
                break;
            productArr[c].append([0,0,0,0])
            productArr[c][i][0] = product[c][i][2]
            ids[c][i] = product[c][i][0]
            productArr[c][i][1] = 0
            productArr[c][i][2] = float(product[c][i][1])
            productArr[c][i][3] = descriptions[c][BinarySearch(sortedColumn[c], product[c][i][2], 0, len(sortedColumn[c]) - 1)][language + 1]

    #now to load the panel values
    panelArr = []
    ids.append([0 for i in range (len(product[3]))])
    for i in range (0, len(product[3])):
        if (product[3][i][0] == ""):
            break;
        panelArr.append([0,0,0,0,0,0,0])
        panelArr[i][0] = product[3][i][5]
        ids[3][i] = product[3][i][0]
        panelArr[i][1] = 0
        panelArr[i][2] = float(product[3][i][2])
        panelArr[i][3] = float(product[3][i][1])
        panelArr[i][4] = descriptions[3][BinarySearch(sortedColumn[3], product[3][i][5], 0, len(sortedColumn[3])- 1)][language + 1]
        panelArr[i][5] = float(product[3][i][3])
        panelArr[i][6] = float(product[3][i][4])

    return JsonResponse({'ids':ids, 'products':productArr, 'panels':panelArr, 'product': product, 'description':descriptions, 'words':words, 'error':error})

