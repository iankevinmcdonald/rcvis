from django.shortcuts import render, redirect, get_object_or_404
from .forms import UploadFileForm

from .models import JsonConfig
from .sankey.graphToD3 import D3Sankey
from .bargraph.graphToD3 import D3Bargraph
from .sankey.sankeyCreator import makeGraphWithFile

def index(request):
    form = UploadFileForm()
    return render(request, 'visualizer/uploadFile.html', {'form': form})

def upload(request):
    if request.method == 'POST' and request.FILES.get('rcvJson'):
        visualizerJson = request.FILES['rcvJson']

        config = JsonConfig(jsonFile=visualizerJson)
        config.hideDecimals = request.POST.get('hideDecimals', False) == "on"
        config.hideTransferlessRounds = request.POST.get('combineWinner', False) == "on"
        config.rotateNames = request.POST.get('rotateNames', False) == "on"
        graph = makeGraphWithFile(config)
        d3Sankey = D3Sankey(graph)

        # if it successfully created a graph, save it
        config.save()

        context = {
            'rcvresult': config.slug
        }
        return redirect('sankey', rcvresult=config.slug);
    else:
        return redirect('index')

def displaySankey(request, rcvresult):
    config = get_object_or_404(JsonConfig, slug=rcvresult)

    graph = makeGraphWithFile(config)
    d3Sankey = D3Sankey(graph)
    return render(request, 'sankey/sankey.html', {
        'title': graph.title,
        'date': graph.dateString,
        'config': config,
        'sankeyjs': d3Sankey.js
    })

def displayBargraph(request, rcvresult):
    config = get_object_or_404(JsonConfig, slug=rcvresult)

    graph = makeGraphWithFile(config)
    d3Bargraph = D3Bargraph(graph)
    return render(request, 'bargraph/bargraph.html', {
        'title': graph.title,
        'date': graph.dateString,
        'config': config,
        'bargraphjs': d3Bargraph.js
    })