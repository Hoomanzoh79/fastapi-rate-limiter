def ip_key(request):
    client = request.client.host
    path = request.url.path

    return f"{client}:{path}"
