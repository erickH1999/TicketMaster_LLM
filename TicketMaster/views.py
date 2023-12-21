import requests, datetime
from django.http import JsonResponse
from django.shortcuts import render, redirect
# from .forms import Results  # importing the form class that was made (In forms.py) -NT from django.http import
# HttpResponse
from django.forms import Form
from django.contrib import messages

from TicketMaster.models import Events


# from .models import Events
# Create your views here.

def convert_to_12_hour_format(event_time):
    if event_time is None:
        return 'N/A'

    hours, minutes, seconds = map(int, event_time.split(':'))

    suffix = "PM" if hours >= 12 else "AM"

    hours_12 = ((hours + 11) % 12 + 1)

    return f'{hours_12}:{minutes:02d}:{seconds:02d} {suffix}'


def process_events(events):
    process_data = []

    for event in events:
        event_time = event['dates']['start'].get('localTime')

        if event_time != 'N/A':
            event_time = convert_to_12_hour_format(event_time)

        processed_event = {
            'name': event['name'],
            'venue': event['_embedded']['venues'][0]['name'],
            'venue_address': event['_embedded']['venues'][0]['address']['line1'],
            'city': event['_embedded']['venues'][0]['city']['name'],
            'state': event['_embedded']['venues'][0]['state']['name'],
            'event_date': datetime.datetime.strptime(event['dates']['start']['localDate'], "%Y-%m-%d").strftime(
                "%b %d %Y"
            ),
            'event_time': event_time,
            'picture': event['images'][0]['url'],
            'ticket_link': event['url'],
        }
        process_data.append(processed_event)

    return {'events': process_data}


def get_events(city, keyword):
    try:
        url = 'https://app.ticketmaster.com/discovery/v2/events.json'

        # ticketmaster API key
        api_key = 'SAkSR3t1pdGu6BCl6BCsIWJYNXTJvU14'

        # parameters for the API request
        params = {
            'apikey': api_key,
            'countryCode': 'US',
            'keyword': keyword,
            'city': city,
            'sort': 'date,asc'
        }

        # sending the GET request
        response = requests.get(url, params=params)
        data = response.json()
        return data
    except requests.RequestException as e:
        return JsonResponse({'error': f'Error making API request: {str(e)}'})


def results(request):
    if request.method == 'POST':
        # Getting the input of the search
        city = request.POST['city_name']
        keyword = request.POST['name_entered']
        # checking if the fields are filled
        if not city or not keyword:
            messages.info(request, 'Both a keyword and a city need to be provided!!')
            return redirect('results')
        # Calling the GET function to receive  the json data
        event_api_results = get_events(city, keyword)

        if '_embedded' not in event_api_results or 'events' not in event_api_results['_embedded']:
            messages.info(request, 'there was no results for the search you made!')
            return redirect('results')
        else:
            events = event_api_results['_embedded']['events']
            context = process_events(events)
            return render(request, 'SearchResults.html', context)

    return render(request, 'SearchResults.html')


def view_fav(request):
    events = Events.objects.all()
    favorites = {'events': events}
    return render(request, 'Favorites.html', favorites)


def create_fav(request):
    if request.method == 'POST':
        event_name = request.POST['event_name']
        event_venue = request.POST['event_venue']
        event_address = request.POST['event_address']
        event_city = request.POST['event_city']
        event_state = request.POST['event_state']
        event_date = request.POST['event_date']
        event_time = request.POST['event_time']
        event_img = request.POST['event_img']
        event_ticket_link = request.POST['event_ticket_link']

        if event_name is not None:
            Events.objects.create(event_name=event_name, event_hall_name=event_venue, event_address=event_address,
                                  event_city=event_city, event_state=event_state, event_date=event_date,
                                  event_time=event_time, event_img=event_img, event_ticket_link=event_ticket_link)

            return JsonResponse(
                {'favorited': True}
            )
    return JsonResponse({'error': 'something went wrong.'})


# update function to be updated later
def update_fav(request, event_id):
    return render(request, 'Favorites.html')


def delete_fav(request):
    if request.method == 'POST':
        event_id = request.POST['event_id']
        if event_id is not None:
            event = Events.objects.get(id=event_id)
            event.delete()
            return JsonResponse(
                {
                    'deleted': True,
                    'message': 'Event Deleted Successfully'
                }
            )
    return JsonResponse({'error': 'something went wrong.'})
