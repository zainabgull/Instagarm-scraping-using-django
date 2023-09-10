from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from .forms import InstagramScrapeForm
from .modules.scraper import scrape_instagram, save_image_to_database

class InstagramScrapeView(View):
    template_name = 'scrape_instagram.html'

    def get(self, request):
        form = InstagramScrapeForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = InstagramScrapeForm(request.POST)
        try:
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                hashtag = form.cleaned_data['hashtag']

                success, message = scrape_instagram(username, password, hashtag)

                if success:
                    return HttpResponse(message)
                else:
                    return HttpResponse(message, status=500)
        except Exception as e:
            # Handle exceptions here, you can log the error for debugging purposes
            error_message = f"An error occurred: {str(e)}"
            return HttpResponse(error_message, status=500)

        return render(request, self.template_name, {'form': form})
