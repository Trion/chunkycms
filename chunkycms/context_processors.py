

def live_edit(request):
    """ context processor to inject live editing header """

    return {"live_edit_mode": request.user.has_perm("chunkycms.change_page")}
